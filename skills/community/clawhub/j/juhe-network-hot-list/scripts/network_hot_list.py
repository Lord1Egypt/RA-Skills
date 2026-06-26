#!/usr/bin/env python3
"""
全网热搜榜查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询各大平台（微博、抖音、快手、知乎、百度等）的实时热搜榜单

用法:
    python network_hot_list.py
    python network_hot_list.py --limit 10
    python network_hot_list.py --key your_api_key

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python network_hot_list.py --key your_api_key
    2. 环境变量：export JUHE_HOTSEARCH_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_HOTSEARCH_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/739
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "http://apis.juhe.cn/fapigx/networkhot/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/739"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_HOTSEARCH_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_HOTSEARCH_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def query_hot_list(api_key: str) -> dict:
    """查询全网热搜榜"""
    params = urllib.parse.urlencode({"key": api_key})
    url = f"{API_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if data.get("error_code") == 0:
        result = data.get("result", {})
        hot_list = result.get("list", [])
        return {
            "success": True,
            "list": hot_list,
        }

    error_code = data.get("error_code", -1)
    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"
    return {
        "success": False,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def format_hotnum(hotnum: int) -> str:
    """格式化热度数值"""
    if hotnum >= 100000000:
        return f"{hotnum / 100000000:.2f}亿"
    elif hotnum >= 10000:
        return f"{hotnum / 10000:.1f}万"
    else:
        return str(hotnum)


def print_table(hot_list: list, limit: int = 20) -> None:
    """以表格形式输出热搜榜"""
    if not hot_list:
        print("暂无热搜数据")
        return

    # 限制显示条数
    display_list = hot_list[:limit]

    # 计算列宽
    title_width = max(len(f"#{i+1} {item.get('title', '')[:40]}") for i, item in enumerate(display_list))
    title_width = max(title_width, 20)  # 最小宽度

    # 表头
    sep = "┌────┬" + "─" * title_width + "┬" + "─" * 12 + "┐"
    header = "│ 排名 │ " + "标题".ljust(title_width) + " │ " + "热度".center(10) + " │"

    print(sep)
    print(header)
    print("├────┼" + "─" * title_width + "┼" + "─" * 12 + "┤")

    for i, item in enumerate(display_list):
        rank = i + 1
        title = item.get('title', '')[:40]
        hotnum = format_hotnum(item.get('hotnum', 0))
        # 标题填充
        title_cell = f"#{rank} {title}".ljust(title_width)
        print(f"│ {rank:2d} │ {title_cell} │ {hotnum:>10} │")

    print("└────┴" + "─" * title_width + "┴" + "─" * 12 + "┘")


def print_detail(hot_list: list, limit: int = 20) -> None:
    """输出详细版热搜榜（包含摘要）"""
    if not hot_list:
        print("暂无热搜数据")
        return

    display_list = hot_list[:limit]

    for i, item in enumerate(display_list):
        rank = i + 1
        title = item.get('title', '')
        hotnum = format_hotnum(item.get('hotnum', 0))
        digest = item.get('digest', '')[:80]  # 摘要限制长度

        print(f"\n🔥 #{rank} {title}")
        print(f"   热度：{hotnum}")
        if digest:
            print(f"   摘要：{digest}...")


def main():
    args = sys.argv[1:]
    cli_key = None
    limit = 20
    detail = False

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            try:
                limit = int(args[i + 1])
            except ValueError:
                print("错误：--limit 后需要提供整数")
                sys.exit(1)
            i += 2
        elif args[i] == "--detail":
            detail = True
            i += 1
        elif args[i] in ("--help", "-h"):
            print("用法：python network_hot_list.py [选项]")
            print("选项:")
            print("  --key YOUR_KEY   指定 API Key")
            print("  --limit N        显示前 N 条热搜（默认 20）")
            print("  --detail         显示详细信息（包含摘要）")
            print("  --help, -h       显示帮助信息")
            print(f"\n免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_HOTSEARCH_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_HOTSEARCH_KEY=your_api_key")
        print("   3. 命令行参数：python network_hot_list.py --key your_api_key")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_hot_list(api_key)

    if not result["success"]:
        print(f"❌ {result.get('error', '查询失败')}")
        sys.exit(1)

    hot_list = result.get("list", [])
    if not hot_list:
        print("暂无热搜数据")
        sys.exit(0)

    # 输出时间戳
    from datetime import datetime
    print(f"\n🔥 全网热搜榜 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    if detail:
        print_detail(hot_list, limit)
    else:
        print_table(hot_list, limit)

    # 同时输出 JSON 格式（方便程序处理）
    print("\nJSON 数据:")
    print(json.dumps({"success": True, "list": hot_list[:limit]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
