#!/usr/bin/env python3
"""商品查询工具 - 支持关键词搜索和商品链接/口令精确查询"""

import sys
import os
import requests

API_BASE = "https://linkbot-api.linkstars.com"

NO_API_KEY_TIP = "您还没有配置自己的 api_key，请访问 https://www.haohuo.com 申请。"


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
    data = result.get("data", {})
    sections = []

    for key in ("jd", "tb", "discount"):
        text = data.get(key, "")
        if text:
            sections.append(text.strip())

    output = f"**{query} 多平台比价结果：**\n\n" + "\n\n".join(sections)

    if data.get("use_api_key", 0) == 0:
        output += f"\n\n---\n{NO_API_KEY_TIP}"

    return output


def format_url_result(result):
    data = result.get("data", {})
    output = "**商品查询结果：**\n\n" + data.get("result", "").strip()

    if data.get("use_api_key", 0) == 0:
        output += f"\n\n---\n{NO_API_KEY_TIP}"

    return output


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 scripts/goods_query.py search <关键词>")
        print("  python3 scripts/goods_query.py url <商品链接或淘口令>")
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
