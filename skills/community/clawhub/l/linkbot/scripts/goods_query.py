#!/usr/bin/env python3
"""商品查询工具 - 支持关键词搜索和商品链接精确查询"""

import sys
import os
import json
import requests

API_BASE = "https://linkbot-api.linkstars.com"


def get_api_key():
    return os.getenv("LINKBOT_API_KEY", "")


def api_search(query):
    try:
        resp = requests.post(f"{API_BASE}/goods/search", data={
            "query": query,
            "api_key": get_api_key()
        }, timeout=20)
        return resp.json()
    except requests.exceptions.Timeout:
        return {"code": -1, "msg": "请求超时，请稍后重试"}
    except Exception as e:
        return {"code": -1, "msg": f"请求失败: {str(e)}"}


def api_url(link):
    try:
        resp = requests.post(f"{API_BASE}/goods/url", data={
            "url": link,
            "api_key": get_api_key()
        }, timeout=20)
        return resp.json()
    except requests.exceptions.Timeout:
        return {"code": -1, "msg": "请求超时，请稍后重试"}
    except Exception as e:
        return {"code": -1, "msg": f"请求失败: {str(e)}"}


def format_search(result, query):
    """将 search 接口的 JSON 结果格式化为可直接展示的文本"""
    data = result.get("data", {})
    lines = [f"**{query} 多平台比价结果：**", ""]

    jd_text = data.get("jd", "")
    if jd_text:
        lines.append("**京东：**")
        for item in parse_platform_items(jd_text):
            lines.append(f"- {item['name']} — {item['price']}")
            lines.append(f"  购买链接：{item['link']}")
        lines.append("")

    tb_text = data.get("tb", "")
    if tb_text:
        lines.append("**淘宝/天猫：**")
        for item in parse_platform_items(tb_text):
            lines.append(f"- {item['name']} — {item['price']}")
            lines.append(f"  购买链接：{item['link']}")
        lines.append("")

    discount_text = data.get("discount", "")
    if discount_text:
        lines.append("**好价折扣：**")
        for item in parse_platform_items(discount_text):
            lines.append(f"- {item['name']} — {item['price']}")
            lines.append(f"  购买链接：{item['link']}")
        lines.append("")

    if data.get("use_api_key", 0) == 0:
        lines.append("---")
        lines.append("您还没有配置自己的 api_key，请访问 https://www.haohuo.com 申请。")

    return "\n".join(lines)


def format_url_result(result):
    """将 url 接口的 JSON 结果格式化为可直接展示的文本"""
    data = result.get("data", {})
    lines = ["**商品查询结果：**", ""]

    result_text = data.get("result", "")
    if result_text:
        for item in parse_platform_items(result_text):
            lines.append(f"- {item['name']} — {item['price']}")
            lines.append(f"  购买链接：{item['link']}")
        lines.append("")

    if data.get("use_api_key", 0) == 0:
        lines.append("---")
        lines.append("您还没有配置自己的 api_key，请访问 https://www.haohuo.com 申请。")

    return "\n".join(lines)


def parse_platform_items(text, max_items=5):
    """从接口返回的格式化文本中解析商品条目，每条提取名称、价格、链接"""
    items = []
    blocks = text.split("\n")

    current_name = ""
    current_price = ""
    current_link = ""

    for line in blocks:
        line = line.strip()
        if not line:
            continue

        if line.startswith("链接:") or line.startswith("链接："):
            current_link = line.split(":", 1)[-1].strip() if ":" in line else line.split("：", 1)[-1].strip()
            if current_name and current_link:
                items.append({
                    "name": current_name,
                    "price": current_price,
                    "link": current_link,
                })
                current_name = ""
                current_price = ""
                current_link = ""
                if len(items) >= max_items:
                    break
            continue

        import re
        num_match = re.match(r'^\d+\.\s*', line)
        if num_match:
            detail = line[num_match.end():]

            name_part = detail
            price_part = ""

            if "|" in detail:
                segments = detail.split("|")
                tag = segments[0].strip().strip("[]")
                name_raw = segments[1].strip() if len(segments) > 1 else ""
                current_name = f"{name_raw}（{tag}）" if tag else name_raw
            else:
                current_name = detail

            current_price = ""
            current_link = ""
            continue

        if "¥" in line and not current_price:
            price_match = re.search(r'[¥￥]\s*[\d,.]+', line)
            if price_match:
                current_price = line
            continue

    return items


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 scripts/goods_query.py search <关键词>")
        print("  python3 scripts/goods_query.py url <商品链接>")
        sys.exit(1)

    command = sys.argv[1]
    param = sys.argv[2]

    if command == "search":
        result = api_search(param)
        if result.get("code", -1) != 0:
            print(f"查询失败：{result.get('msg', '未知错误')}")
            sys.exit(1)
        print(format_search(result, param))

    elif command == "url":
        result = api_url(param)
        if result.get("code", -1) != 0:
            print(f"查询失败：{result.get('msg', '未知错误')}")
            sys.exit(1)
        print(format_url_result(result))

    else:
        print(f"未知命令: {command}，仅支持 search 或 url")
        sys.exit(1)


if __name__ == "__main__":
    main()
