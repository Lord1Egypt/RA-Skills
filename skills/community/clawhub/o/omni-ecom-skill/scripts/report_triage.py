#!/usr/bin/env python3
"""Stage 0 step 1: traverse every uploaded report and identify type, metrics, period and granularity.

Design: rule-first with a model fallback. The script itself never calls a model.
Anything the keyword rules cannot classify is written into
`identification.model_review_pending`; the team lead lets the model decide and
feeds the verdicts back through `--model-verdicts`, which keeps the whole
pipeline reproducible and regression-testable.

Usage:
    python report_triage.py --input-root <dir> --output report-inventory.json \
        --run-id <run_id> --client-scope <client>
    python report_triage.py --input-root <dir> --output out.json --run-id r --client-scope c \
        --model-verdicts model-verdicts.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from artifact_contract import native_stage_identity

SCHEMA_VERSION = "2.0"
TYPE_TAXONOMY_VERSION = "t15-1.0"
DOMAIN_TAXONOMY_VERSION = "d10-1.0"

SUPPORTED_EXT = {".xls", ".xlsx", ".csv", ".tsv", ".xlsm"}

# report_type -> (domain, label, file keywords, header keywords)
TYPE_RULES = {
    "trade_sales": ("transaction", "交易销售报表",
                    ["交易", "销售", "成交", "订单", "支付", "生意参谋", "概况"],
                    ["支付金额", "支付子订单数", "成交金额", "下单金额", "客单价", "支付买家数", "订单数"]),
    "refund_aftersales": ("transaction", "退款售后报表",
                          ["退款", "售后", "退货"],
                          ["退款金额", "退款笔数", "退款率", "退款原因", "成功退款"]),
    "traffic": ("traffic", "流量报表",
                ["流量", "访客", "来源", "入店"],
                ["访客数", "浏览量", "曝光", "点击率", "跳失率", "人均浏览量", "uv", "pv"]),
    "product": ("product", "商品报表",
                ["商品", "宝贝", "spu", "sku", "库存", "货品"],
                ["商品访客数", "加购人数", "收藏人数", "商品标题", "商品id", "库存"]),
    "content": ("content_live", "内容报表",
                ["内容", "短视频", "光合", "素材", "笔记"],
                ["播放量", "完播率", "点赞", "评论", "分享", "发布数", "互动"]),
    "livestream": ("content_live", "直播报表",
                   ["直播", "场次"],
                   ["直播间", "场观", "开播", "观看人次", "停留时长", "gpm", "直播时长"]),
    "creator": ("content_live", "达人报表",
                ["达人", "kol", "主播", "分销", "合作"],
                ["达人昵称", "达人id", "带货", "佣金比例", "合作"]),
    "advertising": ("advertising", "投放报表",
                    ["投放", "推广", "广告", "万相台", "直通车", "引力魔方", "京准通", "千川", "计划", "消耗"],
                    ["花费", "消耗", "展现", "点击", "cpc", "roi", "roas", "成交笔数", "点击率", "平均点击花费"]),
    "customer_service": ("service", "客服报表",
                         ["客服", "接待", "咨询", "旺旺", "服务"],
                         ["接待人数", "响应时长", "首次响应", "满意度", "会话", "询单", "未回复"]),
    "market_benchmark": ("market", "市场大盘报表",
                         ["大盘", "市场", "行业", "竞品", "类目", "排行"],
                         ["行业", "类目", "大盘", "市场份额", "排名", "竞店"]),
    "member_fans": ("asset", "会员粉丝报表",
                    ["会员", "粉丝", "人群", "私域", "复购", "老客"],
                    ["会员数", "粉丝数", "复购率", "新老客", "入会", "人群"]),
    "finance_profit": ("finance", "财务利润报表",
                       ["财务", "利润", "成本", "结算", "对账", "费用"],
                       ["成本", "毛利率", "毛利", "净利", "费用", "结算金额"]),
    "review_sentiment": ("service", "评价舆情报表",
                         ["评价", "评论", "舆情", "差评", "dsr"],
                         ["评价", "评分", "差评", "dsr", "好评"]),
    "inventory_supply": ("product", "库存供应链报表",
                         ["库存", "供应链", "发货", "仓储", "备货"],
                         ["库存", "可用库存", "在途", "发货时效", "缺货"]),
}

PLATFORM_RULES = [
    ("tmall", ["天猫", "淘宝", "tmall", "taobao", "生意参谋"]),
    ("jd", ["京东", "jd", "京准通", "商智"]),
    ("douyin", ["抖音", "douyin", "千川", "巨量"]),
    ("wxvideo", ["视频号", "微信"]),
    ("xhs", ["小红书", "xhs", "red", "薯条"]),
    ("pdd", ["拼多多", "pdd"]),
    ("kuaishou", ["快手", "kuaishou"]),
    ("amazon", ["亚马逊", "amazon"]),
    ("tiktok", ["tiktok"]),
    ("youzan", ["有赞", "youzan"]),
]

# standard metric name -> (unit, aggregation, is_core, match keywords)
METRIC_ALIASES = [
    ("gmv", "元", "sum", True, ["支付金额", "成交金额", "销售额", "gmv", "下单金额"]),
    ("paid_orders", "单", "sum", True, ["支付子订单数", "支付订单数", "成交笔数", "订单数"]),
    ("paid_buyers", "人", "distinct_count", True, ["支付买家数", "成交客户数", "买家数", "客户数"]),
    ("aov", "元", "avg", True, ["客单价"]),
    ("item_price", "元", "avg", False, ["件单价", "单价"]),
    ("refund_amount", "元", "sum", True, ["退款金额", "退款额", "成功退款金额"]),
    ("refund_rate", "%", "ratio", True, ["退款率", "退款占比"]),
    ("uv", "人", "distinct_count", True, ["访客数", "uv", "商品访客数", "独立访客"]),
    ("pv", "次", "sum", False, ["浏览量", "pv"]),
    ("conversion_rate", "%", "ratio", True, ["转化率", "支付转化率", "成交转化率"]),
    ("ctr", "%", "ratio", False, ["点击率", "ctr"]),
    ("impressions", "次", "sum", False, ["展现", "曝光", "展示"]),
    ("clicks", "次", "sum", False, ["点击次数", "点击量", "clicks"]),
    ("ad_spend", "元", "sum", True, ["花费", "消耗", "广告费"]),
    ("cpc", "元", "avg", True, ["cpc", "平均点击花费", "点击成本"]),
    ("roi", "倍", "ratio", True, ["roi", "roas", "投产比"]),
    ("add_cart", "次", "sum", False, ["加购人数", "加购次数", "收藏加购"]),
    ("favorites", "次", "sum", False, ["收藏人数", "收藏量"]),
    ("service_sessions", "次", "sum", True, ["接待人数", "会话数", "咨询量"]),
    ("first_response_sec", "秒", "avg", True, ["首次响应时长", "首响", "响应时长"]),
    ("satisfaction", "%", "ratio", True, ["满意度", "评分"]),
    ("new_members", "人", "sum", False, ["新增会员", "入会", "新增粉丝"]),
    ("repurchase_rate", "%", "ratio", True, ["复购率"]),
    ("gross_margin", "元", "sum", True, ["毛利", "毛利额"]),
    ("gross_margin_rate", "%", "ratio", True, ["毛利率"]),
    ("inventory_qty", "件", "last", False, ["库存", "可用库存", "库存数量"]),
    ("play_count", "次", "sum", True, ["播放量", "播放次数", "vv"]),
    ("finish_rate", "%", "ratio", False, ["完播率"]),
    ("live_viewers", "人", "sum", True, ["场观", "观看人次", "观看人数"]),
    ("gpm", "元", "ratio", False, ["gpm"]),
]

DIMENSION_ALIASES = [
    ("spu", ["商品id", "商品名称", "宝贝", "商品标题", "spu"]),
    ("sku", ["sku", "规格", "尺码", "颜色"]),
    ("channel", ["渠道", "来源", "流量来源", "一级来源", "二级来源"]),
    ("keyword", ["关键词", "搜索词", "词"]),
    ("crowd", ["人群", "客群", "年龄", "性别", "地域"]),
    ("campaign", ["计划", "单元", "推广计划", "活动"]),
    ("creator", ["达人", "主播", "kol", "账号"]),
    ("room", ["直播间", "场次", "开播"]),
    ("agent", ["客服", "接待", "旺旺", "员工"]),
    ("category", ["类目", "品类", "行业"]),
    ("shop", ["店铺", "门店"]),
    ("date", ["日期", "时间", "统计日期", "月份", "周"]),
    ("region", ["省份", "城市", "地区", "区域"]),
]

TIME_COL_HINTS = ["日期", "时间", "统计日期", "统计周期", "月份", "周", "date", "day", "period"]
GRANULARITY_FROM_NAME = [
    ("daily", ["日报", "日报表", "每日", "日维度", "_日"]),
    ("weekly", ["周报", "周维度", "每周", "周度"]),
    ("monthly", ["月报", "月维度", "每月", "月度"]),
    ("quarterly", ["季报", "季度"]),
    ("session", ["场次", "直播"]),
    ("campaign", ["计划", "活动"]),
    ("transaction", ["明细", "订单明细", "流水"]),
]
DATE_PATTERNS = [
    re.compile(r"(20\d{2})[-/年.](\d{1,2})[-/月.](\d{1,2})"),
    re.compile(r"(20\d{2})[-/年.](\d{1,2})$"),
    re.compile(r"(20\d{2})(\d{2})(\d{2})"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_table(path: Path, max_rows: int = 5000):
    """Return (header_list, sample_rows, total_row_count, header_row_index, preamble_text).

    The preamble is everything above the real header row. Exported marketplace
    reports carry the shop and platform name there, so it is the most reliable
    place to detect the platform.
    """
    ext = path.suffix.lower()
    try:
        import pandas as pd
    except Exception:
        return _read_csv_stdlib(path, max_rows)

    if ext in {".xls", ".xlsx", ".xlsm"}:
        try:
            head = pd.read_excel(path, header=None, nrows=15)
        except Exception:
            return [], [], 0, 0, ""
        header_row = _detect_header_row(head)
        preamble = _preamble_text(head, header_row)
        try:
            df = pd.read_excel(path, header=header_row, nrows=max_rows)
        except Exception:
            return [], [], 0, header_row, preamble
        cols = [str(c).strip() for c in df.columns if str(c).strip() and not str(c).startswith("Unnamed")]
        rows = df.head(200).astype(object).where(df.head(200).notna(), None).values.tolist()
        try:
            total = len(pd.read_excel(path, header=header_row, usecols=[0]))
        except Exception:
            total = len(df)
        return cols, rows, total, header_row, preamble

    # csv / tsv
    for enc in ("utf-8-sig", "gbk", "utf-8", "latin-1"):
        try:
            sep = "\t" if ext == ".tsv" else ","
            head = pd.read_csv(path, header=None, nrows=15, encoding=enc, sep=sep)
            header_row = _detect_header_row(head)
            df = pd.read_csv(path, header=header_row, encoding=enc, sep=sep, nrows=max_rows)
            cols = [str(c).strip() for c in df.columns if str(c).strip() and not str(c).startswith("Unnamed")]
            rows = df.head(200).astype(object).where(df.head(200).notna(), None).values.tolist()
            total = sum(1 for _ in path.open("r", encoding=enc, errors="ignore")) - header_row - 1
            return cols, rows, max(total, 0), header_row, _preamble_text(head, header_row)
        except Exception:
            continue
    return [], [], 0, 0, ""


def _read_csv_stdlib(path: Path, max_rows: int):
    try:
        with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as fh:
            rows = list(csv.reader(fh))
    except Exception:
        return [], [], 0, 0
    if not rows:
        return [], [], 0, 0, ""
    header = [c.strip() for c in rows[0] if c.strip()]
    body = rows[1:max_rows + 1]
    sample = [r[:len(header)] for r in body[:200]]
    return header, sample, len(body), 0, ""


def _detect_header_row(head) -> int:
    """Exported reports often carry 1-3 title rows above the real header."""
    best_idx, best_score = 0, -1
    try:
        frame = head.fillna("")
    except Exception:
        return 0
    for idx in range(min(len(frame), 10)):
        values = [str(v).strip() for v in frame.iloc[idx].tolist()]
        non_empty = [v for v in values if v and v.lower() != "nan"]
        if not non_empty:
            continue
        score = len(non_empty) + len(set(non_empty))
        if score > best_score:
            best_idx, best_score = idx, score
    return best_idx


def _preamble_text(head, header_row: int) -> str:
    if header_row <= 0:
        return ""
    try:
        frame = head.fillna("")
    except Exception:
        return ""
    parts = []
    for idx in range(min(header_row, len(frame))):
        for v in frame.iloc[idx].tolist():
            s = str(v).strip()
            if s and s.lower() != "nan":
                parts.append(s)
    return " ".join(parts)


def classify(file_name: str, columns: list[str]) -> tuple[str, str, str, int, list[str]]:
    name_l = file_name.lower()
    header_text = " ".join(columns).lower()
    # A livestream funnel also contains sales columns. Two independent live
    # markers resolve that overlap; a filename alone cannot reclassify a trade table.
    session_marker=any(word in header_text for word in ('场次','开播','直播间','场观'))
    audience_marker=any(word in header_text for word in ('观看','直播间','场观','直播时长'))
    if session_marker and audience_marker and ('直播' in name_l or '直播' in header_text):
        return 'livestream','content_live','high',6,['直播场次与观看/直播字段共同命中；成交字段不改变业务域']
    best_type, best_score, evidence = "unidentified", 0, []
    for rtype, (_domain, _label, fkw, hkw) in TYPE_RULES.items():
        score = 0
        hits = []
        for kw in fkw:
            if kw.lower() in name_l:
                score += 3
                hits.append(f"文件名含「{kw}」")
        for kw in hkw:
            if kw.lower() in header_text:
                score += 2
                hits.append(f"表头含「{kw}」")
        if score > best_score:
            best_type, best_score, evidence = rtype, score, hits
    if best_score == 0:
        return "unidentified", "unclassified", "low", 0, ["规则库无命中"]
    confidence = "high" if best_score >= 5 else ("medium" if best_score >= 3 else "low")
    domain, label = TYPE_RULES[best_type][0], TYPE_RULES[best_type][1]
    return best_type, domain, confidence, best_score, evidence


def detect_platform(file_name: str, columns: list[str],
                    preamble: str = "", root_name: str = "") -> str:
    """Platform clues live in the file name first, then the header, then the
    title rows above the header, then the containing folder name."""
    for source in (file_name, " ".join(columns), preamble, root_name):
        text = (source or "").lower()
        if not text:
            continue
        for key, kws in PLATFORM_RULES:
            if any(kw in text for kw in kws):
                return key
    return "unknown"


def normalize_metrics(columns: list[str]) -> list[dict]:
    metrics = []
    for col in columns:
        c = col.lower().replace(" ", "")
        matched = None
        for std, unit, agg, core, kws in METRIC_ALIASES:
            if any(kw in c for kw in kws):
                matched = (std, unit, agg, core)
                break
        if matched:
            metrics.append({"raw_name": col, "standard_name": matched[0], "unit": matched[1],
                            "aggregation": matched[2], "is_core": matched[3]})
        else:
            metrics.append({"raw_name": col, "standard_name": col, "unit": "",
                            "aggregation": "unknown", "is_core": False})
    return metrics


def detect_dimensions(columns: list[str]) -> list[str]:
    dims = []
    for col in columns:
        c = col.lower().replace(" ", "")
        for std, kws in DIMENSION_ALIASES:
            if any(kw in c for kw in kws) and std not in dims:
                dims.append(std)
    return dims


def _norm_date(m) -> str:
    if m.lastindex == 3:
        y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
    else:
        y, mo, d = m.group(1), int(m.group(2)), 1
    mo = min(max(mo, 1), 12)
    return f"{y}-{mo:02d}-{d:02d}"


def detect_time(columns: list[str], rows: list[list], file_name: str):
    """Return (start, end, time_column, granularity, note)."""
    time_col = None
    for col in columns:
        c = col.lower().replace(" ", "")
        if any(h in c for h in TIME_COL_HINTS):
            time_col = col
            break
    dates: list[str] = []
    if time_col and rows:
        idx = columns.index(time_col)
        for r in rows:
            if idx < len(r) and r[idx] not in (None, ""):
                for pat in DATE_PATTERNS:
                    m = pat.search(str(r[idx]))
                    if m:
                        dates.append(_norm_date(m))
                        break
    if not dates:
        for pat in DATE_PATTERNS:
            m = pat.search(file_name)
            if m:
                dates.append(_norm_date(m))
                break
    note = ""
    if dates:
        start, end = min(dates), max(dates)
        unique_months = {d[:7] for d in dates}
        gran = granularity_from_name(file_name)
        if gran == "unknown":
            if len(unique_months) <= 1 and len(set(dates)) <= 1:
                gran = "snapshot"
            elif len(unique_months) > 6:
                gran = "monthly"
            else:
                gran = "daily"
    else:
        start = end = None
        gran = granularity_from_name(file_name)
        note = "未识别到时间列或时间关键词，需人工确认期间"
    return start, end, time_col, gran, note


def granularity_from_name(file_name: str) -> str:
    name_l = file_name.lower()
    for gran, kws in GRANULARITY_FROM_NAME:
        if any(kw in name_l for kw in kws):
            return gran
    return "unknown"


def detect_completeness(columns: list[str], rows: list[list]) -> tuple[dict, float]:
    if not rows or not columns:
        return {"missing_rate": 1.0, "empty_columns": len(columns), "has_total_row": False,
                "notes": "无有效数据行"}, 1.0
    total_cells = 0
    missing = 0
    empty_cols = 0
    width = len(columns)
    for ci in range(width):
        col_missing = 0
        for r in rows:
            total_cells += 1
            v = r[ci] if ci < len(r) else None
            if v is None or str(v).strip() in ("", "nan", "None", "-"):
                missing += 1
                col_missing += 1
        if col_missing >= max(1, len(rows)):
            empty_cols += 1
    rate = round(missing / total_cells, 4) if total_cells else 1.0
    has_total = any(
        str(r[0]).strip() in ("合计", "总计", "汇总", "全部", "小计") for r in rows if r
    )
    return {"missing_rate": rate, "empty_columns": empty_cols, "has_total_row": has_total,
            "notes": ""}, rate


def decide_verdict(row_count: int, missing_rate: float, metrics: list[dict],
                   columns: list[str]) -> tuple[str, str]:
    if row_count == 0:
        return "insufficient", "无有效数据行，无法支撑任何分析"
    if not columns:
        return "insufficient", "未能解析表头，需人工确认文件结构"
    if missing_rate > 0.5:
        return "insufficient", f"数据缺失率 {missing_rate:.0%}，超过 50% 可用阈值"
    if not any(m["aggregation"] != "unknown" for m in metrics):
        return "partial", "未识别到标准指标列，只能做清单与结构层面描述"
    if missing_rate > 0.2:
        return "partial", f"数据缺失率 {missing_rate:.0%}，可分析但结论需标注置信度"
    return "analyzable", ""


def potential(rtype: str, metrics: list[dict]) -> list[str]:
    names = {m["standard_name"] for m in metrics}
    out = []
    if rtype == "trade_sales":
        out = ["GMV 与订单趋势", "客单价结构", "退款前销售口径核对"]
    elif rtype == "refund_aftersales":
        out = ["退款金额与退款率", "退款原因分布", "净销售口径还原"]
    elif rtype == "traffic":
        out = ["访客与流量来源结构", "渠道效率", "UV 价值"]
    elif rtype == "advertising":
        out = ["花费与 ROI", "可承受 CPC 测算", "渠道投产对比"]
    elif rtype == "customer_service":
        out = ["接待量与响应时长", "询单转化", "服务质量与退款关联"]
    elif rtype == "market_benchmark":
        out = ["行业大盘对比", "竞品位置", "份额变化"]
    elif rtype in ("content", "livestream", "creator"):
        out = ["内容/直播产出", "转化贡献", "达人效率"]
    elif rtype == "member_fans":
        out = ["会员与粉丝增长", "复购结构", "老客贡献"]
    elif rtype == "finance_profit":
        out = ["毛利与费用结构", "净利还原", "投放盈亏边界"]
    elif rtype == "product":
        out = ["SPU 结构", "加购收藏", "库存与动销"]
    if "conversion_rate" in names:
        out.append("转化率拆解")
    if "refund_amount" in names:
        out.append("扣退款后净口径")
    return out


def build_entry(idx: int, path: Path, root_name: str = "") -> dict:
    columns, rows, total, header_row, preamble = read_table(path)
    rtype, domain, confidence, score, evidence = classify(path.name, columns)
    metrics = normalize_metrics(columns) if columns else []
    dims = detect_dimensions(columns) if columns else []
    start, end, time_col, gran, note = detect_time(columns, rows, path.name)
    completeness, missing_rate = detect_completeness(columns, rows)
    verdict, reason = decide_verdict(total, missing_rate, metrics, columns)
    entry = {
        "report_id": f"R{idx:03d}",
        "file_name": path.name,
        "file_path": str(path.resolve()),
        "file_ext": path.suffix.lower(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "sha256": sha256_file(path) if path.exists() else "",
        "platform": detect_platform(path.name, columns, preamble, root_name),
        "report_type": rtype,
        "report_type_label": TYPE_RULES.get(rtype, ("", "未识别报表"))[1],
        "domain": domain,
        "confidence": confidence,
        "identified_by": "rule" if rtype != "unidentified" else "manual",
        "identify_evidence": evidence,
        "time_scope": {"start": start, "end": end, "time_column": time_col,
                       "has_explicit_time": start is not None, "note": note},
        "granularity": gran,
        "row_count": total,
        "column_count": len(columns),
        "header_row_index": header_row,
        "metrics": metrics,
        "dimensions": dims,
        "completeness": completeness,
        "verdict": verdict,
        "analysis_potential": potential(rtype, metrics) if verdict != "insufficient" else [],
    }
    if reason:
        entry["verdict_reason"] = reason
    return entry


def apply_model_verdicts(reports: list[dict], verdicts: dict) -> None:
    for rep in reports:
        v = verdicts.get(rep["report_id"])
        if not v:
            continue
        rtype = v.get("report_type")
        if rtype not in TYPE_RULES:
            continue
        rep["report_type"] = rtype
        rep["report_type_label"] = TYPE_RULES[rtype][1]
        rep["domain"] = v.get("domain") or TYPE_RULES[rtype][0]
        rep["identified_by"] = "model"
        rep["confidence"] = v.get("confidence", "medium")
        rep["identify_evidence"] = v.get("identify_evidence") or ["模型判定"]
        if v.get("metrics"):
            rep["metrics"] = v["metrics"]
        if v.get("granularity"):
            rep["granularity"] = v["granularity"]
        if v.get("time_scope"):
            rep["time_scope"].update(v["time_scope"])
        if v.get("verdict"):
            rep["verdict"] = v["verdict"]
            if v.get("verdict_reason"):
                rep["verdict_reason"] = v["verdict_reason"]


def scan(input_root: Path, exts: set[str]) -> list[Path]:
    found = []
    for p in sorted(input_root.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts and not p.name.startswith("~$"):
            found.append(p)
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage 0 step 1: report inventory and identification")
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--client-scope", required=True)
    ap.add_argument("--team-version", required=True)
    ap.add_argument("--model-verdicts", default=None, help="JSON with model decisions for pending items")
    ap.add_argument("--ext", default=",".join(sorted(SUPPORTED_EXT)))
    ap.add_argument("--max-rows", type=int, default=5000)
    args = ap.parse_args(argv)

    root = Path(args.input_root)
    if not root.exists():
        print(json.dumps({"status": "input_root_missing", "path": str(root)}, ensure_ascii=False))
        return 2
    exts = {e if e.startswith(".") else "." + e for e in args.ext.split(",") if e.strip()}
    files = scan(root, exts or SUPPORTED_EXT)
    reports = [build_entry(i + 1, p, root.name) for i, p in enumerate(files)]

    pending = []
    rule_hits = 0
    for rep in reports:
        if rep["report_type"] == "unidentified":
            pending.append({
                "report_id": rep["report_id"],
                "file_name": rep["file_name"],
                "candidate_types": ["trade_sales", "traffic", "advertising", "customer_service"],
                "header_sample": [m["raw_name"] for m in rep["metrics"][:20]],
            })
        else:
            rule_hits += 1

    model_hits = 0
    if args.model_verdicts:
        vpath = Path(args.model_verdicts)
        if vpath.exists():
            verdicts = json.loads(vpath.read_text(encoding="utf-8"))
            apply_model_verdicts(reports, verdicts)
            model_hits = sum(1 for r in reports if r["identified_by"] == "model")
            pending = [p for p in pending
                       if reports[[r["report_id"] for r in reports].index(p["report_id"])]["identified_by"] == "rule"
                       and reports[[r["report_id"] for r in reports].index(p["report_id"])]["report_type"] == "unidentified"]

    unidentified = sum(1 for r in reports if r["report_type"] == "unidentified")
    inventory = {
        **native_stage_identity("report_inventory", args.team_version),
        "run_id": args.run_id,
        "client_scope": args.client_scope,
        "team_version": args.team_version,
        "issued_at": now_iso(),
        "scanned_root": str(root.resolve()),
        "report_count": len(reports),
        "identification": {
            "mode": "rule_first_model_fallback",
            "type_taxonomy_version": TYPE_TAXONOMY_VERSION,
            "domain_taxonomy_version": DOMAIN_TAXONOMY_VERSION,
            "rule_hits": rule_hits,
            "model_hits": model_hits,
            "unidentified": unidentified,
            "low_confidence_ids": [r["report_id"] for r in reports if r["confidence"] == "low"],
            "model_review_pending": pending,
        },
        "reports": reports,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": "inventory_ready" if unidentified == 0 else "inventory_pending_model_review",
        "report_count": len(reports),
        "rule_hits": rule_hits,
        "model_hits": model_hits,
        "unidentified": unidentified,
        "output": str(out.resolve()),
    }, ensure_ascii=False))
    return 0 if unidentified == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
