#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["aiohttp"]
# ///
"""
price-check v0.6.0 — search-only mode（break change vs v0.5.x）

变更：
- 砍掉 maishou 联盟转链（buy_url / copy_cmd），只保留原生平台搜索 URL
- 砍掉的原因：登录态用户点 u.jd.com / m.tb.cn 短链会被联盟反作弊判失效
  + 我们也不内嵌任何推广码（道德上更干净）
- 加 `human_report` JSON 字段：Python 直接渲染完整 markdown 报告，让 agent
  原样发给用户即可（避免 LLM 自由发挥砍数据）
- 加 `--report` CLI flag：直接输出 markdown 报告（不输出 JSON 噪音），
  纯命令行使用更友好

回滚：git checkout v0.5.4，或 clawhub install --version 0.5.4 price-check
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote

import aiohttp

# 模块加载路径（让相对 import 工作）
_BIN_DIR = Path(__file__).parent
sys.path.insert(0, str(_BIN_DIR))

import _data_layer as data_layer  # noqa: E402  内化的 maishou88.com API client
import db                          # noqa: E402
import feishu_sync                 # noqa: E402

HEADERS = data_layer.HEADERS
PLATFORM_MAP = data_layer.PLATFORM_MAP

# v0.5.2: 各平台原生搜索 URL 模板（用商品 title 兜底，防 maishou 转链不准）
SEARCH_URL_TEMPLATES: dict[str, str] = {
    "1": "https://s.taobao.com/search?q={kw}",                   # 淘宝/天猫
    "2": "https://search.jd.com/Search?keyword={kw}",            # 京东
    "3": "https://mobile.yangkeduo.com/search_result.html?search_key={kw}",  # 拼多多
    "10": "https://s.1688.com/selloffer/offer_search.htm?keywords={kw}",     # 1688
    # 抖音/快手/苏宁/唯品会/考拉 web 搜索体验差，留 None 让 agent 自行决定
}


def _normalize_query_for_search(query: str) -> str:
    """清理用户 query 用于电商原生搜索。

    去掉规格描述词（"内存"/"硬盘"/"存储"/"主存"/"固态硬盘" 等）—— 中文电商
    搜索引擎会按字面拉这些高权重词的相关结果，导致搜偏（搜"Mac Studio
    256G 内存 1T 硬盘"会拉来内存条 + 硬盘，而不是 Mac Studio）。
    """
    if not query:
        return query
    # 噪声词：用户描述商品规格时常用，但搜索引擎会按字面拉配件结果
    noise_terms = [
        "内存", "存储", "主存", "运行内存",
        "硬盘", "固态硬盘", "机械硬盘", "SSD", "ssd",
        "屏幕", "显示器",  # "Mac mini 24 寸 屏幕" 这种描述
    ]
    cleaned = query
    for term in noise_terms:
        cleaned = cleaned.replace(term, " ")
    # 折叠连续空格
    cleaned = " ".join(cleaned.split())
    return cleaned or query


def _make_search_url(source: Optional[str], query: Optional[str]) -> Optional[str]:
    """根据 source + 用户原始 query 生成原生平台搜索 URL。

    v0.6.1: 在生成 URL 前先用 _normalize_query_for_search 清理 query 里的
    规格描述词（内存 / 硬盘 等），避免电商原生搜索按字面分词搜偏。
    """
    if not source or not query:
        return None
    template = SEARCH_URL_TEMPLATES.get(str(source))
    if not template:
        return None
    cleaned = _normalize_query_for_search(query)
    return template.format(kw=quote(cleaned, safe=""))


# ---------- HistoryProvider plugin interface ----------
class HistoryProvider:
    name: str = "abstract"

    def get_history(
        self,
        product_query: str,
        best_deal: Optional[dict[str, Any]] = None,
    ) -> Optional[dict[str, Any]]:
        raise NotImplementedError


class NoOpHistoryProvider(HistoryProvider):
    name = "noop"

    def get_history(self, product_query, best_deal=None):
        return None


class LocalDBHistoryProvider(HistoryProvider):
    """v0.4: 用本地 SQLite price_snapshots 表当历史价数据源。

    返回结构：
        {
            "provider": "local_db",
            "market": { ... } | None,          # 该 query 的市场趋势
            "best_deal_history": { ... } | None,  # best_deal 商品历次价格
            "trap": None | "..."                # 检测到的"先涨后降"提示
        }
    """

    name = "local_db"
    MIN_QUERY_HISTORY = 3
    MIN_GOODS_HISTORY = 2
    LOOKBACK_DAYS = 90

    def get_history(self, product_query, best_deal=None):
        market = self._market_history(product_query)
        deal = None
        if best_deal:
            deal = self._goods_history(
                best_deal.get("goodsId"),
                best_deal.get("price"),
                best_deal.get("shopName"),
                best_deal.get("title"),
            )

        if market is None and deal is None:
            return None

        trap = self._detect_trap(deal) if deal else None

        return {
            "provider": "local_db",
            "market": market,
            "best_deal_history": deal,
            "trap": trap,
        }

    def _market_history(self, query: str) -> Optional[dict[str, Any]]:
        rows = db.query_history_by_query(query, days=self.LOOKBACK_DAYS)
        if len(rows) < self.MIN_QUERY_HISTORY:
            return None

        prices = [r["best_deal_price"] for r in rows if r.get("best_deal_price")]
        medians = [r["stats_median"] for r in rows if r.get("stats_median")]
        if not prices and not medians:
            return None

        latest = rows[-1]
        latest_price = latest.get("best_deal_price")
        median_30d = round(statistics.median(medians), 2) if medians else None

        return {
            "queries_count": len(rows),
            "earliest": rows[0].get("queried_at"),
            "latest": latest.get("queried_at"),
            "best_deal_price_min": round(min(prices), 2) if prices else None,
            "best_deal_price_median": round(statistics.median(prices), 2) if prices else None,
            "best_deal_price_max": round(max(prices), 2) if prices else None,
            "stats_median_30d": median_30d,
            "current_vs_30d_median": (
                round(latest_price / median_30d, 3)
                if (latest_price and median_30d) else None
            ),
        }

    def _goods_history(
        self,
        goods_id: str,
        current_price: Optional[float],
        shop: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        # 先尝试 goodsId 精确匹配
        rows = db.query_history_by_goodsid(goods_id, days=self.LOOKBACK_DAYS)
        # shopmind 的 goodsId 含 session token（中间一段会变），精确匹配往往失效；
        # fallback 按 (shop + title 前 30 字符) 模糊匹配作为商品稳定指纹
        if len(rows) < self.MIN_GOODS_HISTORY and shop and title:
            title_prefix = title[:30]
            rows = db.query_history_by_signature(shop, title_prefix, days=self.LOOKBACK_DAYS)
        if len(rows) < self.MIN_GOODS_HISTORY:
            return None

        prices = [r["price"] for r in rows if r.get("price")]
        if not prices:
            return None

        lo = min(prices)
        hi = max(prices)
        avg = round(statistics.mean(prices), 2)

        # 当前价位置（用 best_deal 实时价 vs 历史分布）
        rank = "mid"
        if current_price is not None and len(prices) >= 2:
            sorted_prices = sorted(prices)
            q1 = sorted_prices[len(sorted_prices) // 4]
            q3 = sorted_prices[len(sorted_prices) * 3 // 4]
            if current_price <= q1:
                rank = "low"
            elif current_price >= q3:
                rank = "high"

        # 找最低 / 最高对应的 snapshot
        low_row = min(rows, key=lambda r: r["price"])
        high_row = max(rows, key=lambda r: r["price"])

        return {
            "goodsId": goods_id,
            "snapshots_count": len(rows),
            "earliest": rows[0]["snapshot_at"],
            "latest": rows[-1]["snapshot_at"],
            "low": {"price": lo, "date": low_row["snapshot_at"]},
            "high": {"price": hi, "date": high_row["snapshot_at"]},
            "avg": avg,
            "current_price": current_price,
            "current_rank": rank,
            "_series": [{"date": r["snapshot_at"], "price": r["price"]} for r in rows],
        }

    def _detect_trap(self, deal: dict[str, Any]) -> Optional[str]:
        """先涨后降识别（v0.1 简版）：
        近 7 天内出现峰值，且峰值 > 历史均价 × 1.15，
        且当前价仍 > 历史均价 → 疑似"先涨没降回"。
        """
        series = deal.get("_series") or []
        if len(series) < 3:
            return None

        avg = deal.get("avg") or 0
        if avg <= 0:
            return None

        prices = [s["price"] for s in series]
        max_price = max(prices)
        max_idx = prices.index(max_price)
        max_date = series[max_idx]["date"]
        current_price = deal.get("current_price") or prices[-1]

        # 峰值远高于均价
        if max_price <= avg * 1.15:
            return None
        # 当前价仍接近或高于均价（没真降）
        if current_price < avg * 1.05:
            return None
        # 峰值必须在最近几个 snapshot 里（"近期"刚涨）
        if max_idx < len(series) - 3:
            return None

        return (
            f"近期峰值 ¥{max_price:.2f}（{max_date[:10]}）后未充分降回；"
            f"当前 ¥{current_price:.2f} 仍高于历史均价 ¥{avg:.2f}"
        )


# ---------- 配置常量 ----------
OUTLIER_RATIO = 0.3
MIN_CLEAN = 5
RELEVANCE_THRESHOLD = 0.75
AMBIGUOUS_MODEL_COUNT = 3


CONDITION_RULES: list[tuple[str, list[str]]] = [
    ("bundle",                  ["套装", "组合装", "礼盒装", "+iPhone", "+iPad",
                                 "+AirPods", "+MacBook", "+Apple",
                                 "+保护壳", "+钢化膜", "+保护套"]),
    ("accessory",               ["配件", "支架", "充电支架", "充电底座", "底座",
                                 "保护套", "保护壳", "保护膜", "屏幕膜", "钢化膜",
                                 "贴膜", "皮套", "替换头", "替换",
                                 "除螨仪", "除螨头", "电池组件",
                                 "Dok", "Dok免打孔",
                                 "适用于", "兼容"]),
    ("refurbished",             ["翻新", "认证翻新", "官翻", "renewed", "二手", "9成新",
                                 "样机", "展示机", "演示机", "展品", "模型机"]),
    ("activation_questionable", ["需签收激活", "需现场激活", "已激活", "已拆封", "拆封"]),
    ("parallel_import",         ["港版", "美版", "日版", "韩版", "欧版", "海外版",
                                 "海外", "全球版", "国际版"]),
    ("trusted_domestic",        ["国行", "大陆版", "国行正品", "国行原封"]),
]

SUSPICIOUS_CONDITIONS = ("refurbished", "bundle", "activation_questionable", "accessory")


TRUSTED_SHOP_LITERALS = [
    "Apple产品京东自营",
    "苹果京东自营",
    "Apple官方旗舰店",
    "苹果官方旗舰店",
]

TRUSTED_SHOP_PATTERNS = [
    re.compile(r"京东自营"),
    re.compile(r"^.*官方旗舰店$"),
    re.compile(r"^Apple.*旗舰店$"),
    re.compile(r"^.*天猫官方旗舰店$"),
]


MODEL_PATTERNS = [
    re.compile(r"V\d+", re.IGNORECASE),
    re.compile(r"iPhone\s*\d+(?:\s*Pro\s*Max|\s*Pro|\s*Plus|\s*Mini)?", re.IGNORECASE),
    re.compile(r"Switch\s*\d*", re.IGNORECASE),
    re.compile(r"\bOLED\b|\bLite\b", re.IGNORECASE),
    re.compile(r"Galaxy\s*S\d{1,2}(?:\s*Ultra|\s*Plus)?", re.IGNORECASE),
    re.compile(r"Pixel\s*\d+", re.IGNORECASE),
]


# ---------- shopmind 数据层适配 ----------
async def fetch_items(
    keyword: str, source: str = "0", page: int = 1
) -> list[dict[str, Any]]:
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        result = await data_layer.fetch_search_items(session, keyword, source=source, page=page)
    raw_items = result.get("items") or []
    return [_normalize_item(it, query=keyword) for it in raw_items]


# v0.6.0: _enrich_with_urls 已废弃（不再调 maishou detail API 拉转链）
# 历史可见 git checkout v0.5.4。当前只用 search_url（原生平台搜索）。


def _normalize_item(raw: dict[str, Any], query: str = "") -> dict[str, Any]:
    title = raw.get("title") or ""
    shop_name = raw.get("shopName") or ""
    source = str(raw.get("source"))
    cond_hits = _condition_hits(title)
    return {
        "goodsId": raw.get("goodsId"),
        "source": source,
        "platform": raw.get("sourceName") or PLATFORM_MAP.get(source, "未知"),
        "title": title,
        "shopName": shop_name,
        "originalPrice": float(raw.get("originalPrice") or 0),
        "rawPrice": float(raw.get("price") or 0),
        "price": float(raw.get("finalPrice") or 0),
        "couponAmount": raw.get("couponAmount", 0),
        "saved": raw.get("saved", 0),
        "discount": raw.get("discount", "无折扣"),
        "hasCoupon": raw.get("hasCoupon", False),
        "monthSales": raw.get("monthSales", 0),
        "condition": _classify_condition(cond_hits),
        "condition_hits": cond_hits,
        "is_trusted_shop": _is_trusted_shop(shop_name),
        "relevance": _title_relevance(query, title),
        "search_url": _make_search_url(source, query),  # v0.5.4+: 用户 query 生成原生搜索 URL
    }


# ---------- condition 识别 ----------
def _condition_hits(title: str) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for cond_name, keywords in CONDITION_RULES:
        matched = [kw for kw in keywords if kw in title]
        if matched:
            hits[cond_name] = matched
    return hits


def _classify_condition(hits: dict[str, list[str]]) -> str:
    for cond_name, _ in CONDITION_RULES:
        if cond_name in hits:
            return cond_name
    return "unknown"


def _is_trusted_shop(shop_name: str) -> bool:
    if not shop_name:
        return False
    for literal in TRUSTED_SHOP_LITERALS:
        if literal in shop_name:
            return True
    for pat in TRUSTED_SHOP_PATTERNS:
        if pat.search(shop_name):
            return True
    return False


# ---------- 标题相关性 ----------
def _tokenize(query: str) -> list[str]:
    return [t.strip() for t in query.split() if t.strip()]


def _title_relevance(query: str, title: str) -> dict[str, Any]:
    if not query or not title:
        return {"score": 0.0, "matched": [], "missing": [], "ambiguous": False}

    tokens = _tokenize(query)
    if not tokens:
        return {"score": 0.0, "matched": [], "missing": [], "ambiguous": False}

    title_lower = title.lower()
    matched: list[str] = []
    missing: list[str] = []
    for t in tokens:
        t_lower = t.lower()
        if t_lower in title_lower:
            matched.append(t)
        elif t_lower.endswith("g") and not t_lower.endswith("gb") and (t_lower + "b") in title_lower:
            matched.append(t)
        elif t_lower.endswith("gb") and t_lower[:-1] in title_lower:
            matched.append(t)
        else:
            missing.append(t)

    score = round(len(matched) / len(tokens), 2)

    all_models: list[str] = []
    for pat in MODEL_PATTERNS:
        all_models.extend(pat.findall(title))
    distinct_models = {m.lower().replace(" ", "") for m in all_models if m}
    ambiguous = len(distinct_models) >= AMBIGUOUS_MODEL_COUNT

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "ambiguous": ambiguous,
    }


# ---------- 价格分布、outlier 剔除 ----------
def _price_stats(items: list[dict[str, Any]]) -> dict[str, float]:
    prices = [i["price"] for i in items if i["price"] > 0]
    if not prices:
        return {"count": 0, "min": 0.0, "max": 0.0, "median": 0.0, "stdev": 0.0}
    return {
        "count": len(prices),
        "min": min(prices),
        "max": max(prices),
        "median": round(statistics.median(prices), 2),
        "stdev": round(statistics.stdev(prices), 2) if len(prices) > 1 else 0.0,
    }


def _filter_outliers(
    items: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], float]:
    valid = [i for i in items if i["price"] > 0]
    if len(valid) < 3:
        return list(items), [], 0.0
    prices = [i["price"] for i in valid]
    raw_med = statistics.median(prices)
    if raw_med <= 0:
        return list(items), [], 0.0
    threshold = raw_med * OUTLIER_RATIO
    clean = [i for i in items if i["price"] >= threshold]
    removed = [i for i in items if i["price"] < threshold]
    clean.sort(key=lambda x: x["price"])
    for idx, item in enumerate(clean):
        item["rank"] = idx + 1
    return clean, removed, round(threshold, 2)


# ---------- best_deal 选择 ----------
def _select_best_deal(
    clean_items: list[dict[str, Any]]
) -> tuple[Optional[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    flagged = [i for i in clean_items if i["condition"] in SUSPICIOUS_CONDITIONS]
    flagged_ids = {i["goodsId"] for i in flagged}

    low_relevance = [
        i for i in clean_items
        if i["goodsId"] not in flagged_ids
        and (i["relevance"]["score"] < RELEVANCE_THRESHOLD or i["relevance"]["ambiguous"])
    ]
    low_rel_ids = {i["goodsId"] for i in low_relevance}

    candidates = [
        i for i in clean_items
        if i["goodsId"] not in flagged_ids and i["goodsId"] not in low_rel_ids
    ]

    tier1 = [i for i in candidates if i["is_trusted_shop"] and i["condition"] in ("trusted_domestic", "unknown")]
    tier2 = [i for i in candidates if i["is_trusted_shop"] and i["condition"] == "parallel_import"]
    tier3 = [i for i in candidates if not i["is_trusted_shop"] and i["condition"] == "trusted_domestic"]

    for tier in (tier1, tier2, tier3):
        if tier:
            best = min(tier, key=lambda x: x["price"])
            return (
                {
                    "platform": best["platform"],
                    "shopName": best["shopName"],
                    "price": best["price"],
                    "title": best["title"],
                    "condition": best["condition"],
                    "is_trusted_shop": best["is_trusted_shop"],
                    "relevance": best["relevance"],
                    "goodsId": best["goodsId"],
                    "source": best["source"],
                    "search_url": best.get("search_url"),  # v0.6.0: search-only
                },
                flagged,
                low_relevance,
            )

    return None, flagged, low_relevance


# ---------- verdict ----------
def compute_verdict(
    best_deal: Optional[dict[str, Any]],
    stats: dict[str, float],
    history: Optional[dict[str, Any]],
) -> tuple[str, str]:
    n = int(stats["count"])
    med = stats["median"]

    if n == 0:
        return "无数据", "剔除后无可用价格记录"
    if med <= 0:
        return "无数据", f"中位数为 0（n={n}），无法判断"
    if best_deal is None:
        return (
            "数据质量不足，无法可信推荐",
            f"剔除噪音后 {n} 条中无满足相关性 + 信任层条件的候选",
        )

    price = best_deal["price"]
    rel = best_deal["relevance"]
    rel_str = f"匹配度 {int(rel['score'] * 100)}% ({len(rel['matched'])}/{len(rel['matched']) + len(rel['missing'])} token)"
    if rel["missing"]:
        rel_str += f"，缺 {'/'.join(rel['missing'])}"

    ratio = price / med
    locator = f"{best_deal['platform']}/{best_deal['shopName']}".rstrip("/")

    if history and history.get("trap"):
        return "别买", f"历史{history['trap']}"

    # 历史价附加信息（如有）
    hist_str = ""
    rank = None
    deal_hist = (history or {}).get("best_deal_history") or {}
    if deal_hist:
        rank = deal_hist.get("current_rank")
        avg = deal_hist.get("avg")
        lo_h = (deal_hist.get("low") or {}).get("price")
        hi_h = (deal_hist.get("high") or {}).get("price")
        if rank and avg is not None:
            rank_zh = {"low": "历史低位", "mid": "历史中位", "high": "历史高位"}.get(rank, rank)
            hist_str = f"；该商品历史 ¥{lo_h}–¥{hi_h}（均 ¥{avg}），当前处于 {rank_zh}"

    if ratio <= 0.85:
        pct = (1 - ratio) * 100
        verdict = "强烈推荐"
        return (verdict,
                f"可信最低价 ¥{price:.2f}（{locator}）比 {n} 平台中位数 ¥{med:.2f} 低 {pct:.1f}%；{rel_str}{hist_str}")
    if ratio <= 0.95:
        pct = (1 - ratio) * 100
        # 历史低位时升档为强烈推荐
        if rank == "low":
            return ("强烈推荐",
                    f"可信最低价 ¥{price:.2f}（{locator}）比 {n} 平台中位数 ¥{med:.2f} 低 {pct:.1f}%，且处于该商品历史低位；{rel_str}{hist_str}")
        return ("可以买",
                f"可信最低价 ¥{price:.2f}（{locator}）比 {n} 平台中位数 ¥{med:.2f} 低 {pct:.1f}%；{rel_str}{hist_str}")
    if ratio <= 1.0:
        pct = (1 - ratio) * 100
        # 历史高位时降档为再等等（已经是再等等，但加强 reason）
        return ("再等等",
                f"可信最低价 ¥{price:.2f}（{locator}）接近 {n} 平台中位数 ¥{med:.2f}（仅低 {pct:.1f}%）；{rel_str}{hist_str}")
    pct = (ratio - 1) * 100
    return ("再等等",
            f"可信最低价 ¥{price:.2f}（{locator}）高于 {n} 平台中位数 ¥{med:.2f} {pct:.1f}%；{rel_str}{hist_str}")


def compute_trap_warning(
    removed: list[dict[str, Any]],
    clean_count: int,
    threshold: float,
    flagged_count: int,
    low_relevance_count: int,
    best_deal: Optional[dict[str, Any]],
    clean_items: list[dict[str, Any]],
    flagged_items: list[dict[str, Any]],
    low_relevance_items: list[dict[str, Any]],
) -> Optional[str]:
    parts: list[str] = []

    if removed:
        n = len(removed)
        lo = min(i["price"] for i in removed)
        hi = max(i["price"] for i in removed)
        if clean_count < MIN_CLEAN:
            parts.append(
                f"⚠️ 剔除前 {n} 条价格远低于中位数（< ¥{threshold:.2f}，最低 ¥{lo:.2f}），"
                f"疑似配件/同关键词噪音；剔除后仅剩 {clean_count} 条，"
                f"不足 {MIN_CLEAN} 条最低样本，verdict 不可信。"
                f"建议加更精确关键词重跑。"
            )
        else:
            parts.append(f"⚠️ 已自动剔除 {n} 条配件/噪音商品（¥{lo:.2f}–¥{hi:.2f}，阈值 ¥{threshold:.2f}）")

    if flagged_count:
        parts.append(f"⚠️ 已过滤 {flagged_count} 条配件/翻新/套装/激活可疑商品")

    if low_relevance_count:
        ambiguous_n = sum(1 for i in low_relevance_items if i["relevance"]["ambiguous"])
        msg = f"⚠️ 已过滤 {low_relevance_count} 条标题不匹配的商品"
        if ambiguous_n:
            msg += f"，其中 {ambiguous_n} 条多型号堆砌"
        parts.append(msg)

    if best_deal:
        flagged_ids = {i["goodsId"] for i in flagged_items}
        low_rel_ids = {i["goodsId"] for i in low_relevance_items}
        safe = [
            i for i in clean_items
            if i["goodsId"] not in flagged_ids and i["goodsId"] not in low_rel_ids
        ]
        cheaper_untrusted = sorted(
            [i for i in safe if not i["is_trusted_shop"] and i["price"] < best_deal["price"]],
            key=lambda x: x["price"],
        )
        if cheaper_untrusted:
            cheapest = cheaper_untrusted[0]
            parts.append(
                f"💡 还有 {len(cheaper_untrusted)} 条更低价候选未进 best_deal："
                f"最低 ¥{cheapest['price']:.2f}（{cheapest['shopName'] or '店铺空'}），"
                f"因不是可信店铺被设计跳过。"
            )

    if not parts:
        return None
    return " ".join(parts)


# ---------- 主流程 ----------
def _safe_top_n(
    clean_items: list[dict[str, Any]],
    flagged: list[dict[str, Any]],
    low_relevance: list[dict[str, Any]],
    n: int = 3,
) -> list[dict[str, Any]]:
    """三层过滤后的安全候选 Top N（按 price 升序）。"""
    flagged_ids = {i["goodsId"] for i in flagged}
    low_rel_ids = {i["goodsId"] for i in low_relevance}
    safe = [
        i for i in clean_items
        if i["goodsId"] not in flagged_ids and i["goodsId"] not in low_rel_ids
    ]
    safe.sort(key=lambda x: x["price"])
    return safe[:n]


def _render_human_report(result: dict[str, Any]) -> str:
    """v0.6.0: Python 直接渲染完整 markdown 报告，作为 JSON 的 human_report 字段。

    LLM agent 拿到 JSON 后只需把这个字符串原样发给用户即可，可以在尾部追加
    "我的建议" 段（基于其产品判断）。这样关键信息（链接、verdict、历史价、
    透明度）一定显示，不会被 LLM 自由发挥砍掉。
    """
    product = result.get("product", "")
    verdict = result.get("verdict", "")
    verdict_reason = result.get("verdict_reason", "")
    best_deal = result.get("best_deal") or {}
    stats = result.get("stats") or {}
    stats_raw = result.get("stats_raw") or {}
    history = result.get("history_summary") or {}
    trap = result.get("trap_warning") or ""
    removed = result.get("removed_outliers") or []
    flagged = result.get("flagged_items") or []
    low_rel = result.get("low_relevance_items") or []

    excluded_ids = {x.get("goodsId") for x in (removed + flagged + low_rel)}
    safe = sorted(
        [x for x in (result.get("all_platforms") or []) if x.get("goodsId") not in excluded_ids],
        key=lambda x: x.get("price", 0),
    )

    lines: list[str] = [f"🛒 比价 · {product}", ""]

    # 顶部警告区
    rel = best_deal.get("relevance") or {}
    if best_deal and rel.get("missing"):
        lines.extend([
            "⚠️ **重要提醒：SKU 不完全匹配**",
            f"   你查的是「{product}」，最划算可信价对应的实际 SKU 是「{best_deal.get('title','')[:60]}」，"
            f"缺关键词 [{'/'.join(rel.get('missing') or [])}]。",
            "   下方数据**仅供参考**，不能直接作为目标 SKU 的购买推荐。",
            "   想要精准 SKU，请加更严格关键词（如 \"国行\"/\"全新\"/容量）重查。",
            "",
        ])
    elif not best_deal:
        lines.extend([
            "⚠️ **重要提醒：本次召回不足以可信推荐**",
            f"   {verdict_reason}",
            "",
        ])

    # 最划算可信价
    lines.append("🏆 最划算可信价（已过滤翻新/套装/配件/激活可疑/标题不匹配）")
    if best_deal:
        trusted_mark = " ✓ 可信店铺" if best_deal.get("is_trusted_shop") else ""
        match_pct = int(rel.get("score", 0) * 100)
        matched = "+".join(rel.get("matched") or [])
        missing = rel.get("missing") or []
        miss_str = f"，缺 {'/'.join(missing)}" if missing else ""
        search_url = best_deal.get("search_url")

        lines.append(
            f"   ¥{best_deal.get('price','?')} | {best_deal.get('platform','')} / "
            f"{best_deal.get('shopName','')}{trusted_mark}"
        )
        lines.append(f"   {best_deal.get('title','')}")
        lines.append(f"   匹配度 {match_pct}% ({matched}){miss_str}")
        if search_url:
            lines.append(f"   🔍 在 {best_deal.get('platform','')} 搜索：{search_url}")
        lines.append("")
        lines.extend([
            "> 💡 **使用方式**：复制上面的搜索链接到浏览器 / 直接在购物 App 里搜商品标题，"
            "找到对应商品下单。本 skill 不内嵌任何推广追踪，链接登录后照样能用。",
            "",
        ])
    else:
        lines.extend(["   （信任层 + 相关性层全过滤后无可信候选）", ""])

    # Top 3 候选 — v0.6.1: 改用纯文本列表（飞书 markdown table 渲染长 URL 会串行）
    lines.append("📊 全网前 3 名候选（已三层过滤）")
    if safe:
        lines.append("")
        for i, item in enumerate(safe[:3], 1):
            shop = item.get("shopName") or "-"
            trusted = " ✓" if item.get("is_trusted_shop") else ""
            title_short = (item.get("title") or "")[:50]
            search_url = item.get("search_url") or ""
            lines.append(f"  [{i}] ¥{item.get('price','?')} | {item.get('platform','')} / {shop}{trusted}")
            lines.append(f"      {title_short}")
            if search_url:
                lines.append(f"      🔍 {search_url}")
            lines.append("")
    else:
        lines.extend(["   无安全候选", ""])

    # 历史价
    deal_hist = history.get("best_deal_history") or {}
    market_hist = history.get("market") or {}
    lines.append(f"📈 历史价（{(history or {}).get('provider', 'noop')}）")
    if deal_hist:
        lines.append(
            f"   该商品 {deal_hist.get('snapshots_count','?')} 次快照 · "
            f"历史最低 ¥{(deal_hist.get('low') or {}).get('price','?')} | 最高 ¥{(deal_hist.get('high') or {}).get('price','?')} | 均 ¥{deal_hist.get('avg','?')}"
        )
        lines.append(f"   **当前处于 {deal_hist.get('current_rank','?')}**")
    if market_hist:
        lines.append(
            f"   该 query 已查询 {market_hist.get('queries_count','?')} 次 · "
            f"市场 30 日中位 ¥{market_hist.get('stats_median_30d','?')} · "
            f"当前/中位 {market_hist.get('current_vs_30d_median','?')}"
        )
    if history.get("trap"):
        lines.append(f"   ⚠️ {history['trap']}")
    if not deal_hist and not market_hist:
        lines.append("   本地数据不足（同 query 查 ≥3 次或同商品出现 ≥2 次后会有）")
    lines.append("")

    # 工具结论（verdict）
    lines.append(f"🤖 工具 verdict: 「{verdict}」")
    lines.append(f"   {verdict_reason}")
    lines.append("")

    # 透明度
    lines.append("⚠️ 透明度")
    if trap:
        lines.append(f"   {trap}")
    raw_count = stats_raw.get("count", "?")
    filter_summary = (
        f"剔除 {len(removed)} 条噪音 / 过滤 {len(flagged)} 条状态可疑 / "
        f"过滤 {len(low_rel)} 条标题不匹配"
    )
    relevant_count = int(stats.get("count", 0) or 0)
    if relevant_count > 0:
        relevant_median = float(stats.get("median", 0) or 0)
        relevant_min = float(stats.get("min", 0) or 0)
        relevant_max = float(stats.get("max", 0) or 0)
        lines.append(f"   数据来源：{raw_count} 平台原始召回 → {filter_summary}")
        lines.append(
            f"   → 相关候选 {relevant_count} 条 · 中位 ¥{relevant_median:.0f} · "
            f"区间 ¥{relevant_min:.0f}–¥{relevant_max:.0f}（verdict 比较基准）"
        )
    else:
        lines.append(
            f"   数据来源：{raw_count} 平台原始召回 → {filter_summary} → 相关候选 0 条"
        )

    return "\n".join(lines)


def _make_history_provider() -> HistoryProvider:
    """根据 config.json 选择 history provider；默认 local_db。"""
    try:
        config = feishu_sync.load_config()
        hp = config.get("history_provider") or {}
        ptype = hp.get("type", "local_db")
        if ptype == "noop":
            return NoOpHistoryProvider()
        return LocalDBHistoryProvider()
    except Exception:
        return LocalDBHistoryProvider()


async def run(query: str, source: str = "0", page: int = 1, no_cache: bool = False) -> dict[str, Any]:
    t0 = time.time()

    # 30min 缓存命中
    if not no_cache:
        cached = db.cache_get(query, source, page)
        if cached:
            cached["_meta"]["from_cache"] = True
            return cached

    items = await fetch_items(query, source=source, page=page)
    stats_raw = _price_stats(items)

    clean_items, removed, threshold = _filter_outliers(items)

    history_provider: HistoryProvider = _make_history_provider()

    best_deal: Optional[dict[str, Any]] = None
    flagged: list[dict[str, Any]] = []
    low_relevance: list[dict[str, Any]] = []

    if not items:
        verdict, verdict_reason = "无数据", "shopmind 未返回任何商品记录"
        history = None
        stats = _price_stats(clean_items)  # 空 stats
    elif removed and len(clean_items) < MIN_CLEAN:
        verdict = "数据噪音过多，无法判断"
        verdict_reason = (
            f"原始 {stats_raw['count']} 条中 {len(removed)} 条疑似噪音（< ¥{threshold:.2f}），"
            f"剔除后仅 {len(clean_items)} 条，低于 {MIN_CLEAN} 条最低样本"
        )
        flagged = [i for i in clean_items if i["condition"] in SUSPICIOUS_CONDITIONS]
        low_relevance = [
            i for i in clean_items
            if i["relevance"]["score"] < RELEVANCE_THRESHOLD or i["relevance"]["ambiguous"]
        ]
        history = None
        stats = _price_stats(clean_items)
    else:
        best_deal, flagged, low_relevance = _select_best_deal(clean_items)
        # v0.6.2: stats 改成"真正相关的候选"分布（去 outlier + 去 flagged + 去 low_relevance）
        # 之前 stats = clean_items 含大量 low_relevance 噪音商品（query "Mac Studio 256G 内存
        # 1T 硬盘" 召回的内存条 / 硬盘等），导致 verdict_reason 出现 "高于中位数 3962%" 这种
        # 离谱数字。现在 stats.median 真实反映目标 SKU 的市场分布。
        flagged_ids = {i["goodsId"] for i in flagged}
        low_rel_ids = {i["goodsId"] for i in low_relevance}
        relevant_items = [
            i for i in clean_items
            if i["goodsId"] not in flagged_ids and i["goodsId"] not in low_rel_ids
        ]
        stats = _price_stats(relevant_items)
        # v0.4: 在 best_deal 已知后才查 history（含 best_deal 自己的历史）
        history = history_provider.get_history(query, best_deal=best_deal)
        verdict, verdict_reason = compute_verdict(best_deal, stats, history)

    # v0.6.0: 不再调 detail API 拉转链（联盟反作弊登录态会失效）
    # 直接用 search_url（在 _normalize_item 已生成）

    trap = compute_trap_warning(
        removed, len(clean_items), threshold,
        len(flagged), len(low_relevance),
        best_deal, clean_items, flagged, low_relevance,
    )

    duration_ms = int((time.time() - t0) * 1000)

    result = {
        "product": query,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "best_deal": best_deal,
        "history_summary": history,
        "all_platforms": items,
        "removed_outliers": removed,
        "flagged_items": flagged,
        "low_relevance_items": low_relevance,
        "stats": stats,
        "stats_raw": stats_raw,
        "trap_warning": trap,
        "_meta": {
            "skill": "price-check",
            "version": "0.6.4",
            "history_provider": history_provider.name,
            "data_source": "internalized maishou88.com client (derived from shopmind-price-compare by xiaohaook)",
            "outlier_filter": f"price < raw_median × {OUTLIER_RATIO}",
            "min_clean_samples": MIN_CLEAN,
            "relevance_threshold": RELEVANCE_THRESHOLD,
            "ambiguous_model_count": AMBIGUOUS_MODEL_COUNT,
            "condition_classifier": "title-keyword (v0.6)",
            "trusted_shop_classifier": "shopName-pattern (v0.6)",
            "suspicious_conditions": list(SUSPICIOUS_CONDITIONS),
            "duration_ms": duration_ms,
            "from_cache": False,
            "agent_must_render": (
                "RENDER RULE: 拿到本 JSON 后，**第一步永远是把 `human_report` 字段原样发给用户**。"
                "不要省略 / 重新组织 / 翻译 / 简化 human_report。"
                "你只能在 human_report 完整发完之后追加一段「我的建议」（≤200 字）。"
            ),
        },
    }

    # v0.6.0: Python 直接渲染完整 markdown，避免 LLM 自由发挥砍数据
    result["human_report"] = _render_human_report(result)

    # 持久化（写库失败不影响输出）
    db.persist_query(query, source, page, result, duration_ms)
    db.cache_set(query, source, page, result)

    # 飞书同步（opt-in）—— fire-and-forget
    try:
        feishu_sync.sync_query_to_feishu(query, result)
    except Exception as e:
        print(f"[price-check] feishu sync error: {e}", file=sys.stderr)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="price-check v0.6.0 — search-only 比价 + verdict + 历史价"
    )
    parser.add_argument("query", help="商品搜索词（中英文用空格分隔，例：'iPhone 16 Pro 256G'）")
    parser.add_argument("--source", default="0", help="平台编号（0=全部）")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--no-cache", action="store_true",
                        help="忽略 30min 缓存，强制重打 maishou API")
    parser.add_argument("--report", action="store_true",
                        help="只输出人类可读 markdown 报告（不输出 JSON）")
    args = parser.parse_args()

    result = asyncio.run(run(args.query, source=args.source, page=args.page, no_cache=args.no_cache))
    if args.report:
        print(result.get("human_report", ""))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
