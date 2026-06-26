#!/usr/bin/env python3
"""
daily_reflection.py
每天 23:00 自动运行
从 gbrain 读取今天的记忆，生成反思，写回 gbrain
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# 加载 gbrain_bridge
sys.path.insert(0, str(Path(__file__).parent.parent))
from gbrain_bridge import get_bridge

def run():
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"[daily_reflection] 开始每日反思: {date}")

    bridge = get_bridge()

    # 生成并写入每日反思
    slug = bridge.daily_reflection(date)

    print(f"[daily_reflection] 完成: {slug}")

    # 同时生成 self_narrative
    try:
        from self_narrative import generate_daily_narrative
        generate_daily_narrative(date)
        print(f"[daily_reflection] 自我叙事已更新")
    except Exception as e:
        print(f"[daily_reflection] 自我叙事跳过: {e}")

if __name__ == "__main__":
    run()
