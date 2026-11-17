#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""
京东金融资讯查询脚本（资讯 + 快讯合流）

功能：
- 查询任意关键字相关的资讯新闻（京东金融公开数据 queryInformation，免鉴权）
- 同时合并黄金快讯流（BFF queryNewsFlash），去重后统一输出
- 无论用户说「查快讯 / 新闻 / 资讯」都走本脚本，不再区分两个数据源

用法：
    python3 jdjr_query_news.py 黄金
    python3 jdjr_query_news.py 特朗普 10
    python3 jdjr_query_news.py A股 5
    python3 jdjr_query_news.py 黄金 --no-flash   # 仅资讯，不合并快讯
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime

from jdjr_config import get_source_metadata, get_claw_headers, set_claw


# 京东金融 API 基础地址
BASE_URL = "https://ms.jr.jd.com/gw2/generic/ugActs/h5/m"

# 黄金资讯流场景ID（快讯）
GOLD_FEED_TAG_ID = 20225


def _normalize_for_dedup(text: str) -> str:
    """归一化文本用于去重：去除【】标签、空白、标点，取核心正文前段。"""
    if not text:
        return ""
    # 去掉开头的【xxx】标签
    t = re.sub(r"^【[^】]*】", "", text)
    # 去除所有空白与常见标点
    t = re.sub(r"[\s，,。.、：:；;！!？?（）()\"'“”‘’\-—…]", "", t)
    return t[:40]


def query_news(keyword: str, size: int = 5) -> list:
    """查询资讯（jdjr 公开数据），返回标准化 news 列表。"""
    payload = {"query": keyword, "size": size}
    req = urllib.request.Request(
        f"{BASE_URL}/queryInformation",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **get_claw_headers()},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if not result.get("success"):
        raise RuntimeError(result.get("resultMsg", "查询失败"))

    data = result.get("resultData", {}).get("data", {})
    information_list = data.get("informationList", [])

    news_items = []
    for item in information_list:
        timestamp = int(item.get("timeStamp", 0))
        dt = datetime.fromtimestamp(timestamp / 1000) if timestamp else None
        news_items.append({
            "time": dt.strftime("%Y-%m-%d %H:%M") if dt else "",
            "timestamp": timestamp,
            "title": item.get("title", "").strip(),
            "content": item.get("content", "").strip(),
            "url": item.get("subUrl", ""),
        })
    return news_items


def query_news_flash(tag_id: int = GOLD_FEED_TAG_ID, page_size: int = 10) -> list:
    """查询黄金快讯流（BFF），返回标准化 news 列表；失败时返回空列表（静默降级）。"""
    try:
        import bff_client
        import jos
    except ImportError:
        return []

    try:
        access_token = jos._valid_access_token()
    except Exception:
        access_token = None

    try:
        data = bff_client.get(
            bff_client.PATH_NEWS_FLASH,
            {"tagId": tag_id, "pageSize": page_size, "lastId": "", "accessToken": access_token or ""},
        ) or {}
    except Exception:
        # 快讯接口异常不影响资讯主流程，静默降级
        return []

    result_list = data.get("resultList", []) if isinstance(data, dict) else []
    news_items = []
    for item in result_list:
        content = (item.get("content") or "").strip()
        if not content:
            continue
        pt = item.get("publishTime")
        timestamp = 0
        time_str = ""
        if isinstance(pt, (int, float)):
            timestamp = int(pt)
            try:
                time_str = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M")
            except (OSError, ValueError):
                time_str = ""
        # 快讯 content 常形如【标题】正文，标题作为 title 提取
        m = re.match(r"^【([^】]*)】(.*)$", content)
        title = m.group(1).strip() if m else ""
        news_items.append({
            "time": time_str,
            "timestamp": timestamp,
            "title": title,
            "content": content,
            "url": "",
        })
    return news_items


def merge_news(jdjr_items: list, flash_items: list) -> list:
    """合并资讯与快讯并去重。

    去重策略：归一化后的正文核心前段为 key；
    若重合，保留信息更完整的一条（优先带 url 的 jdjr 资讯）。
    """
    merged = {}
    order = []

    def _key(item):
        base = item.get("content") or item.get("title") or ""
        return _normalize_for_dedup(base)

    # 先放 jdjr 资讯（信息更全：有 url），再放快讯
    for item in jdjr_items + flash_items:
        k = _key(item)
        if not k:
            continue
        if k not in merged:
            merged[k] = item
            order.append(k)
        else:
            # 已存在：若原条目无 url 而新条目有 url，则用新条目替换
            existing = merged[k]
            if not existing.get("url") and item.get("url"):
                merged[k] = item

    items = [merged[k] for k in order]
    # 按时间倒序（有 timestamp 的排前，最新在前）
    items.sort(key=lambda x: x.get("timestamp") or 0, reverse=True)
    return items


def build_result(keyword: str, size: int, with_flash: bool = True) -> dict:
    """构建统一的资讯查询结果（资讯 + 快讯合流去重）。"""
    jdjr_items = query_news(keyword, size)
    flash_items = query_news_flash() if with_flash else []
    news = merge_news(jdjr_items, flash_items)
    # 清理内部字段 timestamp
    for n in news:
        n.pop("timestamp", None)
    return {
        "success": True,
        "data": {
            "keyword": keyword,
            "count": len(news),
            "news": news,
        },
        "source": get_source_metadata("NEWS"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="查询京东金融资讯（资讯+快讯合流）")
    parser.add_argument("keyword", nargs="?", default="黄金", help="查询关键字（默认：黄金）")
    parser.add_argument("size", nargs="?", type=int, default=10, help="查询条数（默认10条）")
    parser.add_argument("--no-flash", action="store_true", help="不合并快讯，仅查资讯")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args()
    set_claw(args.claw)

    try:
        result = build_result(args.keyword, args.size, with_flash=not args.no_flash)
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