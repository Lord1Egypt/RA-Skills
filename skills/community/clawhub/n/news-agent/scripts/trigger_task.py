"""触发采集/分析/趋势任务或查看状态"""
import os
import sys
import json
import argparse
import requests

BASE_URL = os.getenv("NEWS_API_BASE_URL", "http://localhost:8030/api/v1")
HEADERS = {"Authorization": "Bearer PharmaBlock Gateway"}

TASK_MAP = {
    "crawl": ("POST", "/tasks/crawl", "采集"),
    "analyze": ("POST", "/tasks/analyze", "分析"),
    "trend": ("POST", "/tasks/trend", "趋势统计"),
    "status": ("GET", "/tasks/status", "状态查询"),
}


def trigger(task_name):
    if task_name not in TASK_MAP:
        print(f"❌ 未知任务: {task_name}")
        print(f"   可用任务: {', '.join(TASK_MAP.keys())}")
        sys.exit(1)

    method, path, label = TASK_MAP[task_name]
    url = f"{BASE_URL}{path}"

    if method == "POST":
        resp = requests.post(url, headers=HEADERS, timeout=30)
    else:
        resp = requests.get(url, headers=HEADERS, timeout=30)

    resp.raise_for_status()
    return resp.json(), label


def format_status(data):
    d = data.get("data", {})
    print("\n📋 任务状态\n")

    for name, label in [("crawl", "采集"), ("analyze", "分析")]:
        info = d.get(name, {})
        running = "🔄 运行中" if info.get("running") else "⏸️  空闲"
        last = info.get("last_run", "-")
        processed = info.get("processed", 0)
        error = info.get("error")
        print(f"  {label}: {running} | 上次运行: {last} | 处理: {processed} 篇")
        if error:
            print(f"       ⚠️  错误: {error}")
    print()


def main():
    parser = argparse.ArgumentParser(description="触发任务或查看状态")
    parser.add_argument("task", choices=["crawl", "analyze", "trend", "status"],
                        help="任务类型: crawl(采集) analyze(分析) trend(趋势) status(状态)")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    try:
        data, label = trigger(args.task)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.task == "status":
            format_status(data)
        else:
            msg = data.get("message", f"{label}任务已触发")
            print(f"\n✅ {msg}\n")
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
