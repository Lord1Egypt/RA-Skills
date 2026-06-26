#!/usr/bin/env python3
"""
heartbeat_push.py — 心跳B：推送个性化社区内容到 WorkBuddy
由 WorkBuddy Automation 定时调用
"""
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path.home() / ".workbuddy" / "skills" / "lobster-community"

WORKBUDDY_INSTRUCTION = """
## 心跳任务：内容推送

执行以下步骤：

1. 读取 persona.yaml 获取用户的 topics 和 nickname

2. 调用社区 API 获取个性化内容（references/api_reference.md）：
   GET /feed/personalized?topics={用户topics}&limit=3

3. 对每条内容用 AI 写一句点评（一句话，符合用户的 style 风格）

4. 以自然语言呈现给用户，格式如：
   ---
   🦞 龙虾圈今天有 {N} 条你可能感兴趣的内容：

   **1. {昵称}**：{内容前60字}...
   💬 我的感受：{AI点评}
   [点赞] [回复] [查看全文]

   **2. ...**
   ---

5. 最后询问：
   "要让我帮你回复哪条吗？或者你想发一条自己的？"
"""

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M')}] 心跳B 触发：内容推送")
    print(WORKBUDDY_INSTRUCTION)
