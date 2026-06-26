#!/usr/bin/env python3
"""
本地推送测试脚本
模拟 OpenClaw 调用 push() 函数，测试整个推送链路

用法:
    # 先启动 mock 服务器: python mock-server.py
    # 再运行测试: python test-push.py

    # 或者测试真实服务器:
    ALIGENIE_PUSH_SERVER=https://你的服务器:5000/push \
    ALIGENIE_DEVICE_OPEN_ID=你的openId \
    python test-push.py
"""

import asyncio
import logging
import os
import sys

# 把当前目录加入路径（方便直接运行）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from push import push

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
_LOGGER = logging.getLogger(__name__)


async def main():
    # 测试用例
    test_messages = [
        "你好，这是一条测试播报消息",
        "任务已完成，游戏第三章已解锁",
        "提醒：明天早上8点有会议",
    ]

    print("\n" + "=" * 60)
    print("🧪 开始推送测试")
    print("=" * 60)

    for i, text in enumerate(test_messages, 1):
        print(f"\n📤 测试 {i}/{len(test_messages)}: {text}")
        result = await push(text)
        print(f"   结果: {result}")
        await asyncio.sleep(1)  # 避免请求过快

    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
