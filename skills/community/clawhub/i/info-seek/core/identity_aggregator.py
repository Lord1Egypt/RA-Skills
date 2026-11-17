#!/usr/bin/env python3
"""
core/identity_aggregator.py — Maigret × Sherlock 双源聚合去重引擎（v2.1.0）

背景（2026-09-18 审计）：
  旧链路只用 capability_compensator 沿 degrade_to 取**首个成功源**即返回——
  Maigret 成功就永远不跑 Sherlock，两源从不融合，也无跨源交叉验证。
  本模块在不改代偿语义（能力族失效仍优雅降级）的前提下，提供**同层多源
  聚合**：当 Maigret/Sherlock 两个 identity_attribution 源都有效时，合并其
  发现，按 (平台, URL) 去重，双源命中做置信度增强并标记交叉确认。

零依赖 + 降级哲学：
  - 纯标准库；任何异常由调用方捕获，降级为"只用单源原始结果"。
  - 去重键归一化纯规则（域名 + 路径用户名），不依赖网络。

误报抑制（规则框架，阈值留待真实样本校准）：
  - 仅单源、低排名（site_rank 很大）、HTTP 非 2xx 的命中降档（weak），
    不删除（保守，避免漏报）；是否纳入最终锚点由 confidence 门控决定。
  - 已知高误报平台表（见 references 风险登记）可经 env/注册表扩展。
  - CN/IN/全局 分区：maigret tags 可能带国别（如 'in'），据此粗分区统计，
    供报告呈现；真正的国别误报率基线需真实样本，字段先就位。
"""
from __future__ import annotations

import re
import sys
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, unquote
from pathlib import Path as _eg_p

# G8-apply: 公共入口类型契约守卫（纯 stdlib，scripts/entry_guard.py）
_eg_dir = str(_eg_p(__file__).resolve().parent.parent / 'scripts')
if _eg_dir not in sys.path:
    sys.path.insert(0, _eg_dir)
from entry_guard import (require_text, require_mapping, require_sequence, coerce_mapping_list)

# 双源同时命中的置信增强幅度（封顶 1.0）
CROSS_SOURCE_BOOST = 0.10
# 仅单源命中时的低质量降档阈值
SINGLE_SOURCE_WEAK_RANK = 5_000_000     # maigret rank 大于此值视为长尾低权威
SINGLE_SOURCE_WEAK_CONF = 0.55          # 降档后的置信上限

# 平台名归一化（同一平台两源命名不一致）
_PLATFORM_ALIAS = {
    "github": "GitHub",
    "twitter": "X",
    "x": "X",
    "wordpressorg": "WordPress",
    "wordpress": "WordPress",
    "reddit": "Reddit",
    "instagram": "Instagram",
    "youtube": "YouTube",
    "telegram": "Telegram",
    "tiktok": "TikTok",
    "facebook": "Facebook",
    "linkedin": "LinkedIn",
}

# 已知高误报平台（小写匹配）。来源：2026-09-18 沙箱实测 + 公开 OSINT 经验，
# 真实全量基线待 P1 真实样本校准（见 ROADMAP P1#2）。
_HIGH_FALSE_POSITIVE_PLATFORMS = {
    "droners",      # 实测：必不存在用户名仍误报 Claimed
}


def _norm_platform(name: str) -> str:
    """平台名归一：去空格/大小写/常见别名映射。"""
    if not name:
        return ""
    key = re.sub(r"[\s_\-.]+", "", name.strip().lower())
    return _PLATFORM_ALIAS.get(key, name.strip())


def _url_key(url: str) -> str:
    """URL 去重键：小写主机 + 去尾部斜杠的路径（剥离 query/fragment）。

    例：https://GitHub.com/alice/ → (github.com, /alice)
    """
    if not url:
        return ""
    try:
        u = urlparse(url.strip())
        host = (u.netloc or "").lower().split(":")[0]
        host = re.sub(r"^www\.", "", host)
        path = re.sub(r"/+$", "", unquote(u.path or ""))
        return f"{host}|{path.lower()}"
    except Exception:
        return url.strip().lower().rstrip("/")


def _platform_key(name: str) -> str:
    """平台去重键（稳定规范形：小写、去分隔符、别名归一），与展示名分离。"""
    if not name:
        return ""
    norm = _norm_platform(name)
    return re.sub(r"[\s_\-.]+", "", norm.strip().lower())


def dedup_key(acc: Dict) -> Tuple[str, str]:
    """生成账号条目的去重键：优先 (规范平台键, URL键)；URL 缺失退平台+用户名。"""
    plat = _platform_key(acc.get("platform") or acc.get("source") or "")
    uk = _url_key(acc.get("url") or "")
    if uk:
        return (plat, uk)
    return (plat, (acc.get("username") or "").strip().lower())


def _region_of(acc: Dict) -> str:
    """粗国别分区：读 maigret tags 中的地区标记，缺省 global。

    maigret 实测 tags 可能含 'in'（India）等；CN 平台按域名后缀粗判。
    真实分区体系待真实样本校准。
    """
    tags = acc.get("tags") or []
    if isinstance(tags, list):
        low = {str(t).lower() for t in tags}
        if "cn" in low:
            return "CN"
        if "in" in low:
            return "IN"
    host = ""
    try:
        host = urlparse(acc.get("url") or "").netloc.lower()
    except Exception:
        pass
    if host.endswith(".cn") or host in ("weibo.com", "zhihu.com", "bilibili.com",
                                        "douyin.com", "xiaohongshu.com"):
        return "CN"
    if host.endswith(".in"):
        return "IN"
    return "global"


def _is_high_fp(acc: Dict) -> bool:
    plat = _norm_platform(acc.get("platform") or "").lower()
    return plat in _HIGH_FALSE_POSITIVE_PLATFORMS


def aggregate(results_by_source: Dict[str, List[Dict]],
              base_confidence: Optional[Dict[str, float]] = None) -> Dict:
    """聚合多个 identity_attribution 源的发现结果。

    参数：
      results_by_source: {"Maigret": [...], "Sherlock": [...]}
      base_confidence:   可选，源名 → 该源命中的默认置信（缺省用条目自带）
    返回：
      {
        "accounts": [合并去重后的账号条目],
        "stats": {sources, raw_total, deduped_total, cross_confirmed,
                  weak_single, dropped_fp, by_region: {...}},
        "duplicates": [(key, [sources...]), ...],   # 跨源命中的去重记录
      }
    """
    # G8-apply: 类型契约守卫（拒绝 None/非映射 → 受控 TypeError，替代 None.items 崩溃）
    require_mapping(results_by_source, "results_by_source")
    base_confidence = base_confidence or {}
    merged: Dict[Tuple[str, str], Dict] = {}
    order: List[Tuple[str, str]] = []
    duplicates: List[Tuple[str, List[str]]] = []
    raw_total = 0

    for source, accounts in results_by_source.items():
        for acc in (accounts or []):
            if not isinstance(acc, dict):
                continue
            # 缺口标记（manual_review 末端）不参与聚合
            if acc.get("_gap"):
                continue
            raw_total += 1
            key = dedup_key(acc)
            if not key or key == ("", ""):
                continue

            if key not in merged:
                entry = dict(acc)
                entry["platform"] = _norm_platform(acc.get("platform") or "") or source
                entry["sources"] = [source]
                entry["cross_source_confirmed"] = False
                entry["fp_flag"] = _is_high_fp(acc)   # 单源高误报标记，后续统一处置
                entry.setdefault("region", _region_of(acc))
                conf = acc.get("confidence")
                if conf is None:
                    conf = base_confidence.get(source, 0.8)
                entry["confidence"] = float(conf)
                merged[key] = entry
                order.append(key)
            else:
                entry = merged[key]
                if source not in entry["sources"]:
                    entry["sources"].append(source)
                    entry["cross_source_confirmed"] = True
                    # 双源交叉确认 → 置信增强（取两源较高者 + boost，封顶 0.99）
                    boost = CROSS_SOURCE_BOOST if len(entry["sources"]) == 2 else 0.0
                    entry["confidence"] = min(0.99,
                                              max(entry["confidence"],
                                                  float(acc.get("confidence") or 0.0)) + boost)
                    # 交叉确认 → 撤销单源高误报标记（复活）
                    entry["fp_flag"] = False
                    duplicates.append((f"{key[0]}|{key[1]}", list(entry["sources"])))
                # 字段补全：ids/tags/rank 取信息更丰富者
                if not entry.get("ids") and acc.get("ids"):
                    entry["ids"] = acc.get("ids")
                if not entry.get("tags") and acc.get("tags"):
                    entry["tags"] = acc.get("tags")
                    entry["region"] = _region_of(entry)
                if not entry.get("site_rank") and acc.get("site_rank"):
                    entry["site_rank"] = acc.get("site_rank")

    # 单源低质量降档（不删除）+ 单源高误报平台丢弃（跨源确认的已复活）
    weak_single = 0
    dropped_fp = 0
    accounts: List[Dict] = []
    by_region: Dict[str, int] = {}
    for key in order:
        e = merged[key]
        # 单源 + 高误报平台 → 丢弃（保守去除已知噪声）；统计入 dropped_fp
        if e.get("fp_flag") and not e.get("cross_source_confirmed"):
            dropped_fp += 1
            continue
        e.pop("fp_flag", None)
        region = e.get("region") or _region_of(e)
        e["region"] = region
        by_region[region] = by_region.get(region, 0) + 1
        if not e["cross_source_confirmed"]:
            try:
                hs = int(e.get("http_status") or 0)
                http_ok = hs == 0 or 200 <= hs < 300
            except (TypeError, ValueError):
                http_ok = True
            rank = int(e.get("site_rank") or 0)
            if (rank and rank > SINGLE_SOURCE_WEAK_RANK) or not http_ok:
                e["confidence"] = min(e["confidence"], SINGLE_SOURCE_WEAK_CONF)
                e["weak_single_source"] = True
                weak_single += 1
        accounts.append(e)

    cross_confirmed = sum(1 for a in accounts if a.get("cross_source_confirmed"))
    return {
        "accounts": accounts,
        "stats": {
            "sources": list(results_by_source.keys()),
            "raw_total": raw_total,
            "deduped_total": len(accounts),
            "cross_confirmed": cross_confirmed,
            "weak_single": weak_single,
            "dropped_fp": dropped_fp,
            "by_region": by_region,
        },
        "duplicates": duplicates,
    }
