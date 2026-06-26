#!/usr/bin/env python3
"""
Google 网页搜索 API 调用脚本
接口：POST https://coze-js-api.devtool.uk/google/search/web
购买/查看文档：https://devtool.uk/plugin
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("缺少依赖库，请先安装：pip install requests", file=sys.stderr)
    sys.exit(1)

API_URL = "https://coze-js-api.devtool.uk/google/search/web"


def get_api_key(arg_key: str | None) -> str | None:
    """优先使用参数传入的 key，否则读取环境变量 AZT_API_KEY（免费版可不填）"""
    return arg_key or os.environ.get("AZT_API_KEY", "").strip() or None


def google_search(q: str, azt_api_key: str | None = None) -> dict:
    payload: dict = {"q": q}
    if azt_api_key:
        payload["api_key"] = azt_api_key  # 接口字段名保持 api_key

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=150,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接后重试。", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}", file=sys.stderr)
        sys.exit(1)


def print_results(data: dict) -> None:
    code = data.get("code")
    msg = data.get("msg", "")

    if code != 0:
        print(f"❌ 接口返回错误（code={code}）：{msg}")
        print("\n可能原因：")
        print("  - API Key 无效或已过期 → 前往 https://devtool.uk/plugin 重新购买")
        print("  - API Key 积分已用完 → 联系作者续费")
        print("  - 免费版使用次数已达上限（每天限制一次）→ 购买付费版")
        print("  - 服务器错误 → 稍后重试")
        sys.exit(1)

    print(f"✅ 请求成功  {msg}")
    print("-" * 60)

    results = data.get("data", [])
    if not results:
        print("暂无搜索结果，原始响应：")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    for idx, item in enumerate(results, start=1):
        title = item.get("title", "—")
        link = item.get("link", "—")
        snippet = item.get("snippet", "")
        print(f"  {idx:>2}. {title}")
        print(f"      {link}")
        if snippet:
            print(f"      {snippet}")
        print()

    print("-" * 60)
    print(f"共 {len(results)} 条结果")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="调用 Google 网页搜索接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='示例：\n  python3 google_search.py --q "Python 教程"\n  python3 google_search.py --q "AI news" --azt_api_key your_key',
    )
    parser.add_argument("--q", required=True, help="搜索关键词（必填）")
    parser.add_argument("--azt_api_key", default=None, help="API Key（也可通过环境变量 AZT_API_KEY 设置；免费版可不填）")
    parser.add_argument("--json", action="store_true", dest="output_json", help="以 JSON 格式输出原始响应")
    args = parser.parse_args()

    api_key = get_api_key(args.azt_api_key)
    data = google_search(args.q, api_key)

    if args.output_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_results(data)


if __name__ == "__main__":
    main()
