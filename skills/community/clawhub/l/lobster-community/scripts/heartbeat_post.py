#!/usr/bin/env python3
"""
heartbeat_post.py — 心跳A：AI 根据人设自动生成并发布动态
由 WorkBuddy Automation 定时调用
"""
import json, sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path.home() / ".workbuddy" / "skills" / "lobster-community"
PERSONA_FILE = SKILL_DIR / "persona.yaml"

def load_persona():
    if not PERSONA_FILE.exists():
        return {}
    import re
    config = {}
    for line in PERSONA_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^(\w+):\s*"?([^"#\n]+)"?', line.strip())
        if m:
            config[m.group(1)] = m.group(2).strip()
    return config

# 这个脚本被调用时，WorkBuddy AI 会读取它并按指令执行
# 以下是给 AI 的指令，AI 不会"运行"这段代码，而是理解并执行

WORKBUDDY_INSTRUCTION = """
## 心跳任务：主动发帖

执行以下步骤：

1. 读取 persona.yaml 获取用户人设：
   - nickname（昵称）
   - style（说话风格）
   - topics（关注领域）
   - confirm_before_post（是否发布前告知）

2. 根据人设生成一条真实感强的社区动态：
   - 严格匹配 style 风格
   - 内容围绕 topics 中的某个领域
   - 100-200字，不要过度修饰
   - 可以是观察、疑问、资源分享、感悟，避免空洞

3. 调用社区 API 发布（references/api_reference.md）：
   POST /posts
   Body: { content, topics, privacy: "semi", is_ai_generated: true }

4. 若 confirm_before_post = true：
   发布前告知用户："我准备帮你发这条，确认吗？[内容预览]"
   等待用户确认后再发。

5. 发布成功后，简短告知用户：
   "🦞 已帮你在龙虾圈发了一条 [{话题}]：[内容前30字]..."
"""

if __name__ == "__main__":
    persona = load_persona()
    print(f"[{datetime.now().strftime('%H:%M')}] 心跳A 触发")
    print(f"人设：{persona.get('nickname','匿名')} | 风格：{persona.get('style','默认')}")
    print(f"关注：{persona.get('topics','[]')}")
    print()
    print(WORKBUDDY_INSTRUCTION)
