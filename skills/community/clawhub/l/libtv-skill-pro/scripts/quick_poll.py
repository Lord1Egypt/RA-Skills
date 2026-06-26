#!/usr/bin/env python3
"""
快速轮询脚本 - 简单快捷地轮询会话结果
"""

import argparse
import json
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))
from _common import query_session, safe_run


def poll_session(session_id: str, interval: int = 8, timeout: int = 600):
    """
    简单轮询会话直到有结果
    
    Returns:
        最后一条助手消息，或 None（超时）
    """
    print(f"[*] 开始轮询会话: {session_id}")
    print(f"[*] 间隔: {interval}s, 超时: {timeout}s")
    print("-" * 60)
    
    start_time = time.time()
    last_seq = 0
    check_count = 0
    
    try:
        while True:
            check_count += 1
            elapsed = int(time.time() - start_time)
            
            # 查询
            result = query_session(
                session_id=session_id,
                after_seq=last_seq
            )
            
            messages = result.get("messages", [])
            
            # 查找助手消息
            assistant_messages = [m for m in messages if m.get("role") == "assistant"]
            
            if assistant_messages:
                last_msg = assistant_messages[-1]
                content = last_msg.get("content", "")
                
                # 检查是否包含结果 URL
                if "http" in content or "完成" in content or "生成" in content:
                    print(f"\n✓ 第 {check_count} 次检查 (用时 {elapsed}s): 任务完成!")
                    print("-" * 60)
                    print(f"结果: {content[:500]}")
                    return last_msg
                else:
                    print(f"  第 {check_count} 次检查: 处理中...")
            else:
                print(f"  第 {check_count} 次检查: 等待中...")
            
            # 更新 last_seq
            if messages:
                last_seq = max(m.get("seq", 0) for m in messages)
            
            # 检查超时
            if time.time() - start_time > timeout:
                print(f"\n[!] 超时 ({timeout}s)")
                return None
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="快速轮询会话结果",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权

示例:
  # 基本轮询
  python3 quick_poll.py <session_id>

  # 自定义间隔和超时
  python3 quick_poll.py <session_id> --interval 5 --timeout 300

  # 安静模式（只输出最终结果）
  python3 quick_poll.py <session_id> --quiet

  # 保存结果
  python3 quick_poll.py <session_id> --output result.json
        """,
    )
    parser.add_argument("session_id", help="会话 ID")
    parser.add_argument(
        "--interval",
        type=int,
        default=8,
        help="轮询间隔（秒），默认 8",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="超时时间（秒），默认 600",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="安静模式",
    )
    parser.add_argument(
        "--output",
        help="结果输出文件",
    )
    
    args = parser.parse_args()
    
    # 如果安静模式，重定向输出
    if args.quiet:
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
    
    result = poll_session(args.session_id, args.interval, args.timeout)
    
    if args.quiet:
        sys.stdout = old_stdout
    
    if result:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"结果已保存: {args.output}")
        elif args.quiet:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print("-" * 60)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            print("轮询结束，未获取到结果")
        sys.exit(1)


if __name__ == "__main__":
    safe_run(main)
