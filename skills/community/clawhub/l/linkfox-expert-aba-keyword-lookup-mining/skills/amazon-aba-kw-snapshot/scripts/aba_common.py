#!/usr/bin/env python3
"""Shared ABA shell helpers: build analysisDescription + call L3 gateway."""
from __future__ import annotations

import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://tool-gateway.linkfox.com/aba/intelligentQuery"
VALID_REGIONS = {
    "US", "DE", "BR", "CA", "AU", "JP", "AE", "ES", "FR", "IT", "SA", "TR", "MX", "SE", "NL"
}
BOUNDARY_MSG = (
    "本壳仅覆盖 ABA 搜索词周维度数据（SFR/点击份额/转化份额/ASIN）。"
    "不提供：绝对搜索量、销量、价格、BSR、上架日、语义类目相关词。"
    "请改用 Keepa / Jungle Scout / 前台 SERP(linkfox-amazon-search-competition) 等。"
)


def get_api_key() -> str:
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key missing. export LINKFOXAGENT_API_KEY=... "
            "(https://skill.linkfox.com/linkfoxskills/guide.htm)",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def normalize_region(region: str | None) -> str:
    r = (region or "US").strip().upper()
    if r not in VALID_REGIONS:
        raise ValueError(f"invalid region {region!r}; allowed: {sorted(VALID_REGIONS)}")
    return r


def region_zh(region: str) -> str:
    # ABA NL parser prefers 中文站点表述
    m = {
        "US": "美国站",
        "DE": "德国站",
        "CA": "加拿大站",
        "UK": "英国站",
        "JP": "日本站",
        "FR": "法国站",
        "IT": "意大利站",
        "ES": "西班牙站",
        "AU": "澳大利亚站",
        "MX": "墨西哥站",
        "BR": "巴西站",
        "AE": "阿联酋站",
        "SA": "沙特站",
        "TR": "土耳其站",
        "SE": "瑞典站",
        "NL": "荷兰站",
    }
    return m.get(region, f"{region}站")


def reject_boundary(user_text: str | None) -> str | None:
    if not user_text:
        return None
    t = user_text.lower()
    bad = [
        ("绝对搜索量", ["绝对搜索量", "search volume exact", "exact volume", "sv绝对值"]),
        ("销量", ["月销", "日销", "units sold", "sales estimate"]),
        ("bsr", [" bsr", "best seller rank", "畅销排名"]),
        ("上架日", ["上架日", "launch date", "date first available"]),
    ]
    # keep simple
    checks = [
        ("绝对搜索量", any(x in t for x in ["绝对搜索量", "exact search volume"])),
        ("销量估算", any(x in t for x in ["月销", "销量估算", "units sold"])),
        ("BSR", "bsr" in t or "畅销排名" in t),
        ("上架日", "上架日" in t or "launch date" in t),
    ]
    hits = [name for name, hit in checks if hit]
    if hits:
        return BOUNDARY_MSG + f" 检测到越界意图: {', '.join(hits)}"
    return None


def call_aba(analysis_description: str, region: str = "US", create_download_url: bool = False) -> dict:
    region = normalize_region(region)
    payload = {
        "analysisDescription": analysis_description,
        "region": region,
        "createDownloadUrl": bool(create_download_url),
    }
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        API_URL,
        data=data,
        headers={
            "Authorization": get_api_key(),
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-ABA-Shell/1.0",
            "SESSION_ID": os.environ.get("SESSION_ID", ""),
            "MESSAGE_ID": os.environ.get("MESSAGE_ID", ""),
            "MODE_ID": os.environ.get("MODE_ID", ""),
            "APP_NAME": os.environ.get("APP_NAME", ""),
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body, "success": False}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}", "success": False}


def dedupe_clause(enabled: bool = True) -> str:
    if enabled:
        return "相同搜索词相同ASIN值保留最新的一个。"
    return "不去重不聚合，保留明细行。"


def build_A(p: dict) -> str:
    region = normalize_region(p.get("region"))
    kws = p.get("keywords") or p.get("keyword")
    if isinstance(kws, str):
        kws = [kws]
    if not kws:
        raise ValueError("keywords required")
    weeks = p.get("weeks") or 12
    top_k = int(p.get("top_k_asin") or 0)
    preset = (p.get("preset") or "").strip()
    zh = region_zh(region)
    kw_str = "、".join(f'"{k}"' for k in kws)
    parts = [f"筛选{zh}，"]
    if preset in ("季节节日趋势", "季节趋势") or p.get("seasonal"):
        parts.append(f"关键词{kw_str}在过去{weeks}周（含季节/节日窗口）的搜索热度排名趋势。")
    elif len(kws) > 1 or preset in ("多词/批量词表对比", "批量词表热度对比", "多词热度对比"):
        parts.append(f"批量对比关键词{kw_str}在过去{weeks}周的搜索热度排名。")
    else:
        parts.append(f"关键词{kw_str}在过去{weeks}周的搜索热度排名。")
    if top_k > 0 or preset in ("精确词热度+Top3", "品牌词热度追踪"):
        parts.append(f"并给出每个词点击份额Top{top_k or 3}的ASIN及点击占比、转化占比。")
    parts.append(dedupe_clause(p.get("dedupe", True)))
    return "".join(parts)


def build_B(p: dict) -> str:
    region = normalize_region(p.get("region"))
    kw = p.get("keyword") or (p.get("keywords") or [None])[0]
    if not kw:
        raise ValueError("keyword required")
    week = p.get("week") or "latest"
    top_k = int(p.get("top_k_asin") or 3)
    zh = region_zh(region)
    if week in ("latest", "newest", "最新"):
        time_s = "最新一周"
    else:
        time_s = f"报告周起始{week}"
    return (
        f'筛选{zh}，精确关键词"{kw}"在{time_s}的搜索热度排名，'
        f"以及点击份额Top{top_k}的ASIN、点击占比、转化占比。"
        f"{dedupe_clause(True)}"
    )


def build_C(p: dict) -> str:
    region = normalize_region(p.get("region"))
    seed = p.get("seed")
    if not seed:
        raise ValueError("seed required")
    zh = region_zh(region)
    sfr_min = p.get("sfr_min")
    sfr_max = p.get("sfr_max")
    top_n = int(p.get("top_n") or 50)
    include_asin = bool(p.get("include_asin") or p.get("top_k"))
    top_k = int(p.get("top_k") or 3)
    order_by = (p.get("order_by") or "sfr").lower()
    preset = (p.get("preset") or "").strip()
    filt = p.get("filter") or {}
    if isinstance(filt, str):
        preset = preset or filt
        filt = {}

    parts = [f'筛选{zh}，关键词包含"{seed}"']
    # SFR band
    if sfr_max is not None and sfr_min is not None:
        parts.append(f"，搜索排名在{sfr_min}到{sfr_max}之间")
    elif sfr_max is not None:
        parts.append(f"，当前搜索排名在{sfr_max}以内")
    elif sfr_min is not None:
        parts.append(f"，当前搜索排名在{sfr_min}以外")

    # preset filters
    pl = preset
    if pl in ("蓝海低垄断",) or filt.get("top1_click_max") is not None:
        cmax = filt.get("top1_click_max", 0.15)
        vmax = filt.get("top1_conv_max", 0.10)
        parts.append(
            f"，近三个月点击占比Top1 ASIN的点击占比低于{float(cmax)*100:.0f}%"
            f"且转化占比低于{float(vmax)*100:.0f}%"
        )
    if pl in ("点击垄断",) or filt.get("top1_click_min") is not None:
        cmin = filt.get("top1_click_min", 0.25)
        parts.append(f"，近三个月点击占比Top1 ASIN的点击占比高于{float(cmin)*100:.0f}%")
    if pl in ("高点低转",) or filt.get("click_gt_conv"):
        parts.append("，近3个月点击占比明显高于转化占比（高点击低转化）")
    if pl in ("高转化长尾",):
        if sfr_min is None and sfr_max is None:
            parts.append("，当前排名相对靠后的长尾")
        parts.append("，转化占比相对较高")
    if pl in ("热搜TopN",) and sfr_max is None:
        parts.append("，当前搜索排名靠前")

    parts.append(f"的搜索词，取约{top_n}条")
    if order_by in ("conversionshare", "conversion", "转化"):
        parts.append("，按转化占比排序")
    elif order_by in ("clickshare", "click", "点击"):
        parts.append("，按点击占比排序")
    else:
        parts.append("，按搜索热度排名排序")

    if include_asin or pl in ("扩词+Top ASIN", "扩词+TopASIN"):
        parts.append(f"，并给出每词Top{top_k} ASIN的点击占比与转化占比")
    parts.append("。" + dedupe_clause(True))
    return "".join(parts)


def build_D(p: dict) -> str:
    region = normalize_region(p.get("region"))
    seed = p.get("seed") or ""
    zh = region_zh(region)
    window = int(p.get("window_weeks") or 8)
    sfr_max = p.get("sfr_max")
    mode = (p.get("compare_mode") or p.get("preset") or "wow").strip()
    # map preset cn
    cmap = {
        "周环比上升": "wow",
        "多周连续上升": "consecutive_up",
        "新词上榜爆发": "first_seen_within",
        "需求稳定词": "stable",
        "热度恶化掉词": "consecutive_down",
    }
    mode = cmap.get(mode, mode)
    th = p.get("thresholds") or {}
    if isinstance(th, (int, float, str)):
        th = {"pct": th}
    pct = th.get("pct") or th.get("improve_pct") or 30
    stable_pct = th.get("stable_pct") or 10
    first_months = th.get("months") or 1

    parts = [f"筛选{zh}，"]
    if seed:
        parts.append(f'关键词包含"{seed}"，')
    if sfr_max is not None:
        parts.append(f"最新排名在{sfr_max}以内，")

    if mode in ("wow", "wow_up"):
        parts.append(
            f"过去{window}周内，本周搜索排名相对上周提升（排名数值下降）约{pct}%及以上的搜索词。"
        )
    elif mode in ("consecutive_up",):
        parts.append(
            f"近{window}周搜索排名呈多周连续上升（排名数值持续变好/变小），"
            f"阶段提升约{pct}%的搜索词。"
        )
    elif mode in ("consecutive_down", "掉词", "恶化"):
        parts.append(
            f"近{window}周搜索热度恶化（排名数值变大）或连续掉出核心名次的搜索词，"
            f"恶化约{pct}%及以上。"
        )
    elif mode in ("first_seen_within", "new"):
        parts.append(
            f"近{first_months}个月才进入排名榜单，且当前排名较好的新词/爆发词。"
        )
    elif mode in ("stable",):
        parts.append(
            f"近{window}周搜索排名波动不超过{stable_pct}%的需求稳定词。"
        )
    else:
        raise ValueError(f"unknown compare_mode: {mode}")
    parts.append(dedupe_clause(True))
    return "".join(parts)


def build_E(p: dict) -> str:
    region = normalize_region(p.get("region"))
    zh = region_zh(region)
    match = (p.get("match") or "contains").lower()
    seed = p.get("seed")
    kws = p.get("keywords")
    if isinstance(kws, str):
        kws = [kws]
    if not seed and not kws:
        raise ValueError("seed or keywords required")
    aggregate = p.get("aggregate")
    if aggregate is None:
        aggregate = False
    report_week = p.get("report_week")
    date_from = p.get("date_from")
    date_to = p.get("date_to")
    weeks = p.get("weeks")

    parts = [f"筛选{zh}，"]
    if kws:
        kw_str = "、".join(f'"{k}"' for k in kws)
        parts.append(f"精确关键词{kw_str}")
    else:
        if match == "exact":
            parts.append(f'精确关键词"{seed}"')
        else:
            parts.append(f'关键词包含"{seed}"')

    if report_week:
        parts.append(f"在报告周{report_week}的明细数据")
    elif date_from and date_to:
        parts.append(f"在{date_from}至{date_to}的明细数据")
    elif weeks:
        parts.append(f"在过去{weeks}周的明细数据")
    else:
        parts.append("在最近可用周的明细数据")
    parts.append("，输出搜索词、报告周、SFR、点击ASIN、点击占比、转化占比等字段。")
    parts.append(dedupe_clause(bool(aggregate)))
    return "".join(parts)


def build_F(p: dict) -> str:
    region = normalize_region(p.get("region"))
    zh = region_zh(region)
    asins = p.get("asins") or p.get("asin")
    if isinstance(asins, str):
        asins = [a.strip() for a in asins.replace(";", ",").split(",") if a.strip()]
    if not asins:
        raise ValueError("asins required")
    weeks = p.get("weeks") or 4
    min_share = p.get("min_share")
    order_by = (p.get("order_by") or "sfr").lower()
    top_n = p.get("top_n")
    asin_str = "、".join(asins)
    parts = [
        f"筛选{zh}，查找ASIN为{asin_str}在过去{weeks}周作为被点击ASIN所对应的搜索词，"
        f"给出搜索词、搜索热度排名、点击占比、转化占比"
    ]
    if min_share is not None:
        parts.append(f"，点击占比或转化占比不低于{min_share}")
    if top_n:
        parts.append(f"，每个ASIN约{top_n}条词")
    if order_by in ("clickshare", "click"):
        parts.append("，按点击占比排序")
    elif order_by in ("conversionshare", "conversion"):
        parts.append("，按转化占比排序")
    else:
        parts.append("，按搜索热度排名排序")
    parts.append("。" + dedupe_clause(True))
    return "".join(parts)


BUILDERS = {
    "A": build_A,
    "B": build_B,
    "C": build_C,
    "D": build_D,
    "E": build_E,
    "F": build_F,
}


def run_shell(shell_id: str, params: dict) -> dict:
    shell_id = shell_id.upper()
    if shell_id not in BUILDERS:
        raise ValueError(f"unknown shell {shell_id}")
    # boundary optional check on free text
    br = reject_boundary(params.get("user_text") or params.get("raw_query"))
    if br:
        return {"success": False, "boundary": True, "msg": br, "errcode": 400}

    desc = BUILDERS[shell_id](params)
    region = normalize_region(params.get("region"))
    # download defaults
    if "createDownloadUrl" in params:
        dl = bool(params.get("createDownloadUrl"))
    elif "download" in params:
        dl = bool(params.get("download"))
    else:
        dl = shell_id == "E"  # detail export default download true-ish; still opt
        if shell_id == "E":
            dl = bool(params.get("download", True))
        else:
            dl = False

    result = call_aba(desc, region=region, create_download_url=dl)
    result = dict(result) if isinstance(result, dict) else {"raw": result}
    result["_meta"] = {
        "shell": shell_id,
        "analysisDescription": desc,
        "region": region,
        "createDownloadUrl": dl,
    }
    return result


def main_cli(shell_id: str):
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            f"Usage: shell_{shell_id.lower()}.py '<JSON params>'\n"
            f"Shell {shell_id} — builds analysisDescription and calls ABA L3.\n"
            f"Requires LINKFOXAGENT_API_KEY.",
            file=sys.stderr,
        )
        sys.exit(0 if sys.argv[1:] and sys.argv[1] in ("-h", "--help") else 1)
    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    try:
        out = run_shell(shell_id, params)
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # default demo
    print("import aba_common and call run_shell(shell_id, params)", file=sys.stderr)
    sys.exit(1)
