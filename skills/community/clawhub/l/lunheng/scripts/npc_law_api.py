#!/usr/bin/env python3
"""
国家法律法规数据库 (flk.npc.gov.cn) API 客户端
最权威的中国法律法规数据来源（全国人大常委会维护）
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://flk.npc.gov.cn"
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://flk.npc.gov.cn/",
    "User-Agent": "Mozilla/5.0",
}

# 状态码映射
STATUS_MAP = {
    1: "已废止",
    2: "已修改",
    3: "有效",
    4: "尚未生效",
}


def search_law(keyword: str, page: int = 1, size: int = 10, search_type: int = 1) -> dict:
    """
    搜索法律法规。
    
    Args:
        keyword: 搜索关键词（法律名称）
        page: 页码
        size: 每页数量
        search_type: 1=标题搜索(精确), 2=全文搜索(模糊)
    
    Returns:
        {"total": int, "rows": [{"title", "sxx", "gbrq", "sxrq", "zdjgName", "flxz", "bbbs"}]}
    """
    body = json.dumps({
        "searchRange": 1,
        "sxrq": [],
        "gbrq": [],
        "searchType": search_type,
        "sxx": [],
        "gbrqYear": [],
        "flfgCodeId": [],
        "zdjgCodeId": [],
        "searchContent": keyword,
        "pageNum": page,
        "pageSize": size,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/law-search/search/list",
        data=body,
        headers=HEADERS,
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        return data
    except Exception as e:
        return {"total": 0, "rows": [], "error": str(e)}


def get_law_detail(bbbs: str) -> dict:
    """
    获取法律法规详情（含完整条文结构）。
    
    Args:
        bbbs: 法律唯一标识
    
    Returns:
        {"title", "sxx", "gbrq", "sxrq", "content": {"children": [...]}}
    """
    req = urllib.request.Request(
        f"{BASE_URL}/law-search/search/flfgDetails?bbbs={bbbs}",
        headers={"Referer": "https://flk.npc.gov.cn/"},
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        return data.get("data", {})
    except Exception as e:
        return {"error": str(e)}


def verify_law(name: str) -> dict:
    """
    验证法律是否存在及其状态。
    
    Args:
        name: 法律名称（全称或简称）
    
    Returns:
        {
            "found": bool,
            "official_name": str,      # 官方全称
            "status": str,             # 有效/已废止/已修改/尚未生效
            "status_code": int,        # 3/1/2/4
            "publish_date": str,       # 颁布日期
            "effective_date": str,     # 生效日期
            "authority": str,          # 制定机关
            "category": str,           # 法律/行政法规/司法解释等
            "bbbs": str,               # 唯一标识
        }
    """
    result = search_law(name, size=5)
    rows = result.get("rows", [])

    if not rows:
        return {"found": False, "query": name}

    # 找最匹配的结果（标题完全匹配或包含）
    best = None
    for row in rows:
        title = re.sub(r"<[^>]+>", "", row.get("title", ""))  # 去掉 HTML 高亮标签
        if title == name or name in title or title in name:
            best = row
            break

    if not best:
        best = rows[0]

    title = re.sub(r"<[^>]+>", "", best.get("title", ""))
    sxx = best.get("sxx", 0)

    return {
        "found": True,
        "official_name": title,
        "status": STATUS_MAP.get(sxx, f"未知({sxx})"),
        "status_code": sxx,
        "publish_date": best.get("gbrq", ""),
        "effective_date": best.get("sxrq", ""),
        "authority": best.get("zdjgName", ""),
        "category": best.get("flxz", ""),
        "bbbs": best.get("bbbs", ""),
    }


def get_article_count(bbbs: str) -> int:
    """获取法律的条文总数"""
    detail = get_law_detail(bbbs)
    content = detail.get("content", {})
    children = content.get("children", [])

    # 递归计算条文数
    def count_articles(items):
        count = 0
        for item in items:
            title = item.get("title", "")
            # 匹配 "第X条" 格式
            if re.match(r"第[零一二三四五六七八九十百千\d]+条", title):
                count += 1
            count += count_articles(item.get("children", []))
        return count

    return count_articles(children)


def verify_article_range(name: str, article_num: str) -> dict:
    """
    验证特定条款是否存在。
    
    Args:
        name: 法律名称
        article_num: 条款号（如 "667" 或 "第六百六十七条"）
    
    Returns:
        {"exists": bool, "total_articles": int, "law_info": dict}
    """
    law_info = verify_law(name)
    if not law_info.get("found"):
        return {"exists": False, "law_info": law_info}

    bbbs = law_info.get("bbbs", "")
    if not bbbs:
        return {"exists": None, "law_info": law_info, "note": "无法获取条文结构"}

    total = get_article_count(bbbs)
    return {
        "exists": None,  # 需要进一步解析条文结构才能确定
        "total_articles": total,
        "law_info": law_info,
    }


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="国家法律法规数据库 API 客户端")
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("search", help="搜索法律")
    s.add_argument("keyword")
    s.add_argument("--size", type=int, default=5)

    v = sub.add_parser("verify", help="验证法律状态")
    v.add_argument("name")

    d = sub.add_parser("detail", help="获取法律详情")
    d.add_argument("bbbs")

    args = parser.parse_args()

    if args.cmd == "search":
        result = search_law(args.keyword, size=args.size)
        print(f"共 {result.get('total', 0)} 条结果:")
        for row in result.get("rows", []):
            title = re.sub(r"<[^>]+>", "", row.get("title", ""))
            sxx = STATUS_MAP.get(row.get("sxx", 0), "?")
            print(f"  [{sxx}] {title} ({row.get('gbrq', '')})")

    elif args.cmd == "verify":
        result = verify_law(args.name)
        if result.get("found"):
            print(f"  官方名称: {result['official_name']}")
            print(f"  状态: {result['status']}")
            print(f"  颁布日期: {result['publish_date']}")
            print(f"  生效日期: {result['effective_date']}")
            print(f"  制定机关: {result['authority']}")
            print(f"  分类: {result['category']}")
        else:
            print(f"  未找到: {args.name}")

    elif args.cmd == "detail":
        result = get_law_detail(args.bbbs)
        print(json.dumps(result, ensure_ascii=False, indent=2)[:2000])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
