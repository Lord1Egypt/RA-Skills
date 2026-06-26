#!/usr/bin/env python3
"""
批量创建会话脚本 - 同时发起多个生图/生视频任务
"""

import argparse
import json
import sys
import os
import concurrent.futures
import time

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_session, build_project_url, safe_run


def create_single_task(message: str, index: int) -> dict:
    """创建单个任务"""
    print(f"  [{index}] 创建任务: {message[:50]}...")
    try:
        result = create_session(message=message)
        result["task_index"] = index
        result["status"] = "success"
        result["projectUrl"] = build_project_url(result.get("projectUuid", ""))
        print(f"  [{index}] ✓ 成功 - Session: {result.get('sessionId', 'N/A')[:20]}...")
        return result
    except Exception as e:
        print(f"  [{index}] ✗ 失败: {e}")
        return {
            "task_index": index,
            "status": "error",
            "error": str(e),
            "message": message,
        }


def main():
    parser = argparse.ArgumentParser(
        description="批量创建会话任务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权

示例:
  # 从文件批量创建（每行一个任务描述）
  python3 batch_create.py --file tasks.txt

  # 直接指定多个任务
  python3 batch_create.py -m "生成猫的图片" -m "生成狗的图片" -m "生成鸟的图片"

  # 限制并发数
  python3 batch_create.py --file tasks.txt --workers 3

  # 保存结果
  python3 batch_create.py --file tasks.txt --output results.json
        """,
    )
    parser.add_argument(
        "-m", "--message",
        action="append",
        help="任务描述，可多次指定",
    )
    parser.add_argument(
        "--file",
        help="任务描述文件路径（每行一个任务）",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="并发数，默认 5",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="任务间隔延迟（秒），默认 0.5",
    )
    parser.add_argument(
        "--output",
        help="结果输出文件路径（JSON）",
    )
    args = parser.parse_args()

    # 收集任务
    messages = []
    if args.message:
        messages.extend(args.message)
    
    if args.file:
        if not os.path.exists(args.file):
            print(f"错误：文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            file_messages = [line.strip() for line in f if line.strip()]
            messages.extend(file_messages)
    
    if not messages:
        print("错误：未提供任何任务描述，使用 -m 或 --file 指定", file=sys.stderr)
        sys.exit(1)

    print(f"[*] 批量创建 {len(messages)} 个任务")
    print(f"[*] 并发数: {args.workers}, 间隔: {args.delay}s")
    print("-" * 60)

    # 执行批量创建
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for i, msg in enumerate(messages, 1):
            future = executor.submit(create_single_task, msg, i)
            futures.append(future)
            time.sleep(args.delay)
        
        # 收集结果
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # 统计
    success_count = sum(1 for r in results if r.get("status") == "success")
    error_count = len(results) - success_count

    print("-" * 60)
    print(f"[*] 完成: 成功 {success_count}, 失败 {error_count}, 总计 {len(results)}")

    # 输出结果
    output = {
        "total": len(results),
        "success": success_count,
        "error": error_count,
        "tasks": sorted(results, key=lambda x: x.get("task_index", 0)),
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"[*] 结果已保存: {args.output}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    safe_run(main)
