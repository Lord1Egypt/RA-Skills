"""
留言非语 — 异步命令行 Demo

与 main.py 的区别：
- 使用 AsyncConversationEngine，人格分析后台异步运行
- 用户不会因为第5/10/15轮的分析而多等一次 API 调用
- 输入 /quit 退出，/status 查看分析状态

运行方式：
    python main_async.py
"""

import asyncio
import json
import sys
import os

# 确保模块路径正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.conversation_async import AsyncConversationEngine


async def main():
    print("=" * 50)
    print("  留 言 非 语  [异步版]")
    print("  —— 不是治愈你，而是让你看见自己")
    print("=" * 50)
    print()
    print("命令：/quit 退出 | /status 查看分析状态")
    print("注：人格分析在后台进行，不影响对话响应速度")
    print("-" * 50)
    print()

    engine = AsyncConversationEngine()

    # 开场白
    opening = engine.get_opening()
    print(f"[{engine.current_counselor}]: {opening}")
    print()

    loop = asyncio.get_event_loop()

    while True:
        try:
            # asyncio 的 CLI 输入：用 run_in_executor 避免阻塞事件循环
            user_input = await loop.run_in_executor(None, lambda: input("你: ").strip())
        except (KeyboardInterrupt, EOFError):
            print("\n\n再见。希望你比来的时候更了解自己一点。")
            break

        if not user_input:
            continue

        if user_input == "/quit":
            print("\n再见。希望你比来的时候更了解自己一点。")

            # 等待后台分析任务完成（最多2秒），再展示人格画像
            status = engine.get_status()
            if status["analysis_running"]:
                print("(等待后台分析完成...)")
                try:
                    await asyncio.wait_for(engine._analysis_task, timeout=2.0)
                except (asyncio.TimeoutError, asyncio.CancelledError):
                    pass

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
            print(f"后台分析中: {'是' if status['analysis_running'] else '否'}")
            if status["personality_context"]:
                print(f"人格分析: {status['personality_context']}")
            if status["analysis_results"]:
                print(f"详细分析:\n{json.dumps(status['analysis_results'], ensure_ascii=False, indent=2)}")
            print(f"---\n")
            continue

        # 获取回复
        previous_counselor = engine.current_counselor
        response = await engine.chat(user_input)

        # 如果咨询师切换了，显示提示
        if engine.current_counselor != previous_counselor:
            print(f"\n  (切换至「{engine.current_counselor}」模式)\n")

        print(f"[{engine.current_counselor}]: {response}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
