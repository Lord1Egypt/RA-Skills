#!/usr/bin/env python3
"""
会话监控脚本 - 实时监控会话消息进展，支持多种输出格式
"""

import argparse
import json
import sys
import os
import time
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from _common import query_session, safe_run


def format_message(msg: dict, format_type: str = "simple") -> str:
    """格式化消息输出"""
    role = msg.get("role", "unknown")
    content = msg.get("content", "")
    seq = msg.get("seq", 0)
    msg_type = msg.get("type", "")
    
    if format_type == "simple":
        prefix = "🤖" if role == "assistant" else "👤"
        content_preview = content[:100] + "..." if len(content) > 100 else content
        return f"{prefix} [{seq}] {content_preview}"
    
    elif format_type == "json":
        return json.dumps(msg, ensure_ascii=False)
    
    elif format_type == "detailed":
        timestamp = msg.get("timestamp", "")
        return f"[{seq}] {role:10} {msg_type:10} {timestamp}\n    {content[:200]}"
    
    return str(content)


def extract_urls(content: str) -> list:
    """从内容中提取 URL"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, content)


def main():
    parser = argparse.ArgumentParser(
        description="实时监控会话消息进展",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权

示例:
  # 基本监控
  python3 monitor_session.py <session_id>

  # 轮询模式（每 10 秒查询一次）
  python3 monitor_session.py <session_id> --poll --interval 10

  # 只显示助手消息
  python3 monitor_session.py <session_id> --role assistant

  # 提取所有 URL
  python3 monitor_session.py <session_id> --extract-urls

  # JSON 格式输出
  python3 monitor_session.py <session_id> --format json

  # 监控并保存到文件
  python3 monitor_session.py <session_id> --poll --output log.json
        """,
    )
    parser.add_argument("session_id", help="会话 ID")
    parser.add_argument(
        "--after-seq",
        type=int,
        default=0,
        help="从指定 seq 开始查询",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        help="轮询模式",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=8,
        help="轮询间隔（秒），默认 8",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="轮询超时时间（秒），默认 3600",
    )
    parser.add_argument(
        "--role",
        choices=["user", "assistant", "all"],
        default="all",
        help="过滤角色",
    )
    parser.add_argument(
        "--format",
        choices=["simple", "json", "detailed"],
        default="simple",
        help="输出格式",
    )
    parser.add_argument(
        "--extract-urls",
        action="store_true",
        help="提取并显示所有 URL",
    )
    parser.add_argument(
        "--output",
        help="输出文件路径",
    )
    args = parser.parse_args()

    print(f"[*] 监控会话: {args.session_id}")
    print(f"[*] 模式: {'轮询' if args.poll else '单次查询'}")
    if args.poll:
        print(f"[*] 轮询间隔: {args.interval}s, 超时: {args.timeout}s")
    print("-" * 60)

    all_messages = []
    last_seq = args.after_seq
    start_time = time.time()
    poll_count = 0

    try:
        while True:
            poll_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if args.poll:
                print(f"\n[{current_time}] 第 {poll_count} 次轮询 (after_seq={last_seq})")
            
            # 查询会话
            result = query_session(
                session_id=args.session_id,
                after_seq=last_seq
            )
            
            messages = result.get("messages", [])
            
            if not messages:
                if args.poll:
                    print("  无新消息")
                else:
                    print("  无消息")
            else:
                print(f"  收到 {len(messages)} 条消息:")
                
                for msg in messages:
                    all_messages.append(msg)
                    
                    # 更新 last_seq
                    msg_seq = msg.get("seq", 0)
                    if msg_seq > last_seq:
                        last_seq = msg_seq
                    
                    # 角色过滤
                    if args.role != "all" and msg.get("role") != args.role:
                        continue
                    
                    # 输出消息
                    formatted = format_message(msg, args.format)
                    print(f"    {formatted}")
                    
                    # 提取 URL
                    if args.extract_urls:
                        urls = extract_urls(msg.get("content", ""))
                        if urls:
                            print(f"    🔗 发现的 URL:")
                            for url in urls:
                                print(f"      - {url}")
            
            # 非轮询模式直接退出
            if not args.poll:
                break
            
            # 检查超时
            if time.time() - start_time > args.timeout:
                print(f"\n[!] 轮询超时 ({args.timeout}s)")
                break
            
            # 等待下一轮
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n[!] 用户中断")

    # 输出统计
    print("-" * 60)
    print(f"[*] 监控结束，共 {len(all_messages)} 条消息")

    # 保存结果
    if args.output:
        output_data = {
            "session_id": args.session_id,
            "total_messages": len(all_messages),
            "poll_count": poll_count,
            "messages": all_messages,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"[*] 结果已保存: {args.output}")


if __name__ == "__main__":
    safe_run(main)
