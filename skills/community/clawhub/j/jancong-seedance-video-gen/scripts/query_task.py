#!/usr/bin/env python3
"""
Seedance 2.0 视频生成 - 任务状态查询脚本
用法:
  python query_task.py <task_id> [--poll] [--interval <秒>]
"""

import argparse
import json
import os
import sys
import time
import urllib.request


def get_config():
    """获取 API 配置"""
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("ARK_API_URL", "https://ark.cn-beijing.volces.com")
    return api_key, base_url


def query_task(api_key, base_url, task_id):
    """查询任务状态"""
    url = f"{base_url}/api/v3/contents/generations/tasks/{task_id}"

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        method="GET",
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result


def format_status(result):
    """格式化状态输出"""
    status = result.get("status", "unknown")
    task_id = result.get("id", "N/A")
    model = result.get("model", "N/A")

    status_icons = {
        "pending": "⏳",
        "running": "🔄",
        "completed": "✅",
        "failed": "❌",
    }
    icon = status_icons.get(status, "❓")

    output = [f"{icon} 状态: {status.upper()}"]
    output.append(f"   Task ID: {task_id}")
    output.append(f"   模型: {model}")

    if "created_at" in result:
        from datetime import datetime
        created = datetime.fromtimestamp(result["created_at"])
        output.append(f"   创建时间: {created.strftime('%Y-%m-%d %H:%M:%S')}")

    if status == "completed":
        video_result = result.get("video_result", {})
        output.append(f"   🎥 视频: {video_result.get('video_url', 'N/A')}")
        output.append(f"   🖼️  封面: {video_result.get('cover_image_url', 'N/A')}")
    elif status == "failed":
        error = result.get("error", {})
        output.append(f"   错误码: {error.get('code', 'N/A')}")
        output.append(f"   错误信息: {error.get('message', 'N/A')}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Seedance 2.0 视频任务状态查询")
    parser.add_argument("task_id", help="任务 ID (如 cgt-20260410162021-xxxxx)")
    parser.add_argument("--poll", action="store_true", help="轮询模式，等待直到完成或失败")
    parser.add_argument("--interval", type=int, default=15, help="轮询间隔秒数 (默认: 15)")

    args = parser.parse_args()

    api_key, base_url = get_config()

    try:
        while True:
            result = query_task(api_key, base_url, args.task_id)
            print(format_status(result))
            print()

            status = result.get("status")

            if status in ("completed", "failed"):
                break

            if not args.poll:
                print(f"💡 使用 --poll 参数可持续轮询直到完成")
                break

            print(f"⏱️  {args.interval} 秒后再次查询...")
            time.sleep(args.interval)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"❌ API 错误 ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 查询已中断")


if __name__ == "__main__":
    main()
