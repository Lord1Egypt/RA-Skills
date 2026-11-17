#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""
理财大V动态榜单查询脚本。

功能：
- 查询基金大V榜单
- 查询黄金大V榜单
- 根据问句自动判断查询资产类型和排行类型

用法：
    python3 query_blogger_trend.py 查看今日财经大V排行
    python3 query_blogger_trend.py 查看今日黄金大V排行
    python3 query_blogger_trend.py 查看今日买入最多的基金大V排行
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid
from typing import Dict, List

from jdjr_config import get_fund_api_base_url, get_fund_api_key, get_source_metadata, get_claw, set_claw


SKILL_CODE = "blogger-trend"
GOLD_RANK_TYPE_MAP = {
    "income": "1",
    "popularity": "2",
    "buy": "3",
    "position": "4",
}
FUND_RANK_TYPE_MAP = {
    "income": 401,
    "popularity": 402,
    "buy": 403,
    "position": 404,
}
RANK_TITLE_LABELS = {
    "income": "收益最多",
    "popularity": "人气最佳",
    "buy": "买入最多",
    "position": "持仓最多",
}


def post_json(path: str, payload: dict) -> dict:
    """向榜单网关发送 JSON POST 请求。"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "apikey": get_fund_api_key(),
        "x-skill-code": SKILL_CODE,
        "x-skill-run-id": str(uuid.uuid4()),
    }
    claw = get_claw()
    if claw:
        headers["x-claw"] = claw
    req = urllib.request.Request(
        f"{get_fund_api_base_url()}/{path.lstrip('/')}",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_text(text: str) -> str:
    """归一化文本，便于做简单匹配。"""
    return "".join(text.lower().split())


def infer_rank_mode(query: str) -> str:
    """根据问句推断排行类型。"""
    query_norm = normalize_text(query)
    if "人气" in query_norm:
        return "popularity"
    if "买入" in query_norm:
        return "buy"
    if "持仓" in query_norm:
        return "position"
    return "income"


def infer_asset_types(query: str) -> List[str]:
    """根据问句推断查询基金、黄金或两者。"""
    query_norm = normalize_text(query)
    has_gold = "黄金" in query_norm
    has_fund = "基金" in query_norm
    if has_gold and not has_fund:
        return ["gold"]
    if has_fund and not has_gold:
        return ["fund"]
    return ["gold", "fund"]


def build_gold_title(rank_mode: str) -> str:
    return f"今日{RANK_TITLE_LABELS[rank_mode]}的黄金大V排行"


def build_fund_title(rank_mode: str) -> str:
    return f"今日{RANK_TITLE_LABELS[rank_mode]}的基金大V排行"


def fetch_gold_ranking(rank_mode: str) -> Dict[str, object]:
    """查询黄金大V榜单并格式化。"""
    result = post_json("rank/gold-regular", {"rankType": GOLD_RANK_TYPE_MAP[rank_mode]})
    if not result.get("success"):
        raise ValueError("黄金大V榜单查询失败")

    rows = (result.get("data") or {}).get("rankInfoList") or []
    if rank_mode in {"income", "position"}:
        columns = [
            {"key": "rank", "label": "排名"},
            {"key": "userName", "label": "大V昵称"},
            {"key": "holdGram", "label": "持有克重"},
            {"key": "holdAmount", "label": "持有金额"},
            {"key": "holdIncome", "label": "持有收益"},
            {"key": "totalAccumulatedIncome", "label": "总收益额"},
            {"key": "rankValue", "label": "总持仓"},
            {"key": "totalFans", "label": "总粉丝数"},
            {"key": "latestTrade", "label": "最新交易记录"},
        ]
        items = [
            {
                "rank": item.get("rank", ""),
                "userName": item.get("userName", ""),
                "holdGram": (item.get("holdGram") or {}).get("text", ""),
                "holdAmount": (item.get("holdAmount") or {}).get("text", ""),
                "holdIncome": (item.get("holdIncome") or {}).get("text", ""),
                "totalAccumulatedIncome": (item.get("totalAccumulatedIncome") or {}).get("text", ""),
                "rankValue": (item.get("rankValue") or {}).get("text", ""),
                "totalFans": (item.get("totalFans") or {}).get("text", ""),
                "latestTrade": ((item.get("goldLatestTradeInfoVO") or {}).get("showText", "")),
            }
            for item in rows
        ]
    elif rank_mode == "popularity":
        columns = [
            {"key": "rank", "label": "排名"},
            {"key": "userName", "label": "大V昵称"},
            {"key": "holdGram", "label": "持有克重"},
            {"key": "publishContentCount", "label": "发布内容数量"},
            {"key": "competitionFans", "label": "本周持仓被订阅数"},
            {"key": "totalFans", "label": "总粉丝数"},
            {"key": "latestTrade", "label": "最新交易记录"},
            {"key": "rankValue", "label": "本周人气值"},
        ]
        items = [
            {
                "rank": item.get("rank", ""),
                "userName": item.get("userName", ""),
                "holdGram": (item.get("holdGram") or {}).get("text", ""),
                "publishContentCount": (item.get("publishContentCount") or {}).get("text", ""),
                "competitionFans": (item.get("competitionFans") or {}).get("text", ""),
                "totalFans": (item.get("totalFans") or {}).get("text", ""),
                "latestTrade": ((item.get("goldLatestTradeInfoVO") or {}).get("showText", "")),
                "rankValue": (item.get("rankValue") or {}).get("text", ""),
            }
            for item in rows
        ]
    else:
        columns = [
            {"key": "rank", "label": "排名"},
            {"key": "userName", "label": "大V昵称"},
            {"key": "holdGram", "label": "持有克重"},
            {"key": "holdAmount", "label": "持有金额"},
            {"key": "publishContentCount", "label": "发布内容数量"},
            {"key": "totalFans", "label": "总粉丝数"},
            {"key": "latestTrade", "label": "最新交易记录"},
            {"key": "rankValue", "label": "今日买入"},
        ]
        items = [
            {
                "rank": item.get("rank", ""),
                "userName": item.get("userName", ""),
                "holdGram": (item.get("holdGram") or {}).get("text", ""),
                "holdAmount": (item.get("holdAmount") or {}).get("text", ""),
                "publishContentCount": (item.get("publishContentCount") or {}).get("text", ""),
                "totalFans": (item.get("totalFans") or {}).get("text", ""),
                "latestTrade": ((item.get("goldLatestTradeInfoVO") or {}).get("showText", "")),
                "rankValue": (item.get("rankValue") or {}).get("text", ""),
            }
            for item in rows
        ]

    return {
        "assetType": "gold",
        "rankMode": rank_mode,
        "title": build_gold_title(rank_mode),
        "count": len(items),
        "columns": columns,
        "items": items,
    }


def fetch_fund_ranking(rank_mode: str) -> Dict[str, object]:
    """查询基金大V榜单并格式化。"""
    result = post_json(
        "rank/fund-multi",
        {
            "rankType": FUND_RANK_TYPE_MAP[rank_mode],
            "rankSortBy": 0,
            "pageSize": 10,
            "isNeedShowColumnName": True,
            "isNeedRecommendSku": True,
            "isNeedBestRank": False,
            "isNeedSingleSkuRankRadio": False,
            "isNeedFlowStatus": False,
        },
    )
    if not result.get("success"):
        raise ValueError("基金大V榜单查询失败")

    rows = ((result.get("data") or {}).get("fundRankList")) or []
    columns = [
        {"key": "rank", "label": "排名"},
        {"key": "userName", "label": "大V昵称"},
        {"key": "feature", "label": "大V特征"},
        {"key": "primaryMetric", "label": "主指标"},
        {"key": "secondaryMetric", "label": "补充指标"},
        {"key": "recommendFund", "label": "代表基金"},
    ]
    items = []
    for item in rows:
        user_info = item.get("userInfo") or {}
        recommend_sku = item.get("recommendSku") or {}
        show_column = (item.get("showColumn") or {}).get("text", "")
        show_column_value = (item.get("showColumnValue") or {}).get("text", "")
        feature = f"{show_column}{show_column_value}".strip() or "--"
        items.append(
            {
                "rank": user_info.get("rank", ""),
                "userName": user_info.get("userName", ""),
                "feature": feature,
                "primaryMetric": (item.get("rankColumnValue") or {}).get("text", ""),
                "secondaryMetric": (item.get("rankColumnName") or {}).get("text", ""),
                "recommendFund": recommend_sku.get("skuName", ""),
            }
        )

    return {
        "assetType": "fund",
        "rankMode": rank_mode,
        "title": build_fund_title(rank_mode),
        "count": len(items),
        "columns": columns,
        "items": items,
    }


def query_blogger_trend(query: str) -> Dict[str, object]:
    """根据问句查询大V榜单。"""
    rank_mode = infer_rank_mode(query)
    asset_types = infer_asset_types(query)
    source_scene = "OTHER"
    if asset_types == ["gold"]:
        source_scene = "GOLD"
    elif asset_types == ["fund"]:
        source_scene = "FUND"
    rankings = []
    for asset_type in asset_types:
        if asset_type == "gold":
            rankings.append(fetch_gold_ranking(rank_mode))
        else:
            rankings.append(fetch_fund_ranking(rank_mode))
    return {
        "success": True,
        "data": {
            "query": query,
            "rankMode": rank_mode,
            "assetTypes": asset_types,
            "rankings": rankings,
            "riskWarning": "投资有风险，跟单需谨慎，大V历史业绩不代表未来表现",
        },
        "source": get_source_metadata(source_scene),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="查询理财大V动态榜单")
    parser.add_argument("query", help="用户查询语句")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args()
    set_claw(args.claw)

    try:
        result = query_blogger_trend(args.query.strip())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print(json.dumps({"success": False, "error": "您的账户已被限制访问，如有疑问请联系京东黄金客服"}, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": f"HTTP {exc.code}"}, ensure_ascii=False))
        return 1
    except urllib.error.URLError as exc:
        print(json.dumps({"success": False, "error": f"网络请求失败: {exc.reason}"}, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
