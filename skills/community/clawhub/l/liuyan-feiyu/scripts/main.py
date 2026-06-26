"""
留言非语 — 命令行 Demo

让你在终端中体验完整的对话流程。
输入 /quit 退出，/status 查看当前分析状态。
"""

import sys
import os
import json

# 确保模块路径正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.conversation import ConversationEngine


def main():
    print("=" * 50)
    print("  留 言 非 语")
    print("  —— 不是治愈你，而是让你看见自己")
    print("=" * 50)
    print()
    print("命令：/quit 退出 | /status 查看分析状态")
    print("-" * 50)
    print()

    engine = ConversationEngine()

    # 开场白
    opening = engine.get_opening()
    print(f"[{engine.current_counselor}]: {opening}")
    print()

    while True:
        try:
            user_input = input("你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n再见。希望你比来的时候更了解自己一点。")
            break

        if not user_input:
            continue

        if user_input == "/quit":
            print("\n再见。希望你比来的时候更了解自己一点。")

            # 如果有分析结果，显示最终人格画像
            status = engine.get_status()
            if status["analysis_results"]:
                print("\n" + "=" * 50)
                print("  你的人格画像")
                print("=" * 50)
                results = status["analysis_results"]
                if "personality_summary" in results:
                    print(f"\n{results['personality_summary']}")
                print()
            break

        if user_input == "/status":
            status = engine.get_status()
            print(f"\n--- 当前状态 ---")
            print(f"对话轮数: {status['turn_count']}")
            print(f"当前咨询师: {status['current_counselor']}")
            if status["personality_context"]:
                print(f"人格分析: {status['personality_context']}")
            if status["analysis_results"]:
                print(f"详细分析: {json.dumps(status['analysis_results'], ensure_ascii=False, indent=2)}")
            print(f"---\n")
            continue

        # 获取回复
        previous_counselor = engine.current_counselor
        response = engine.chat(user_input)

        # 如果咨询师切换了，显示提示
        if engine.current_counselor != previous_counselor:
            print(f"\n  (切换至「{engine.current_counselor}」模式)\n")

        print(f"[{engine.current_counselor}]: {response}")
        print()


if __name__ == "__main__":
    main()
