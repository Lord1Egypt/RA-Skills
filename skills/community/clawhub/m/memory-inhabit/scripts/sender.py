#!/usr/bin/env python3
"""
Memory-Inhabit Sender — 伴侣模式消息发送器

用法：
  python3 sender.py              检查并生成一条待发送消息（供 cron 调用）
  python3 sender.py --dry-run    预览不实际发送
"""

import json
import re
import sys
import os
import random
import subprocess
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).parent
SKILL_DIR = SCRIPTS_DIR.parent
STATE_FILE = SKILL_DIR / ".mi_state.json"


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def run_checker():
    """运行本技能内的 checker.py 检查是否该发消息"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "checker.py"), "check"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return {"should_send": False, "reason": "checker_error"}
    try:
        return json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        return {"should_send": False, "reason": "parse_error"}


def mark_sent():
    """标记已发送"""
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "checker.py"), "mark"],
        capture_output=True, timeout=10
    )


def save_to_history(persona_name, message, role="persona"):
    """保存到对话历史"""
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "memory.py"), "save", persona_name, message, role],
        capture_output=True, timeout=10
    )


def generate_voice(text, voice_name="xiaoxiao"):
    """调用本技能内的 tts.py 生成语音文件"""
    output_path = f"/tmp/mi_voice_{datetime.now().strftime('%H%M%S')}.mp3"
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "tts.py"), text, "-o", output_path, "-v", voice_name],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode == 0 and Path(output_path).exists():
        return output_path
    return None


def sanitize_message(text):
    """过滤模板消息中的特殊标签，防止注入攻击"""
    if not text:
        return ""
    # 移除 <qqmedia> 等标签，只保留纯文字
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def pick_message(templates):
    """根据时间段选择消息"""
    hour = datetime.now().hour
    if 6 <= hour < 11:
        pool = templates.get("morning", [])
    elif 11 <= hour < 14:
        pool = templates.get("afternoon", [])
    elif 14 <= hour < 18:
        pool = templates.get("afternoon", []) + templates.get("random", [])
    elif 18 <= hour < 23:
        pool = templates.get("evening", [])
    else:
        pool = templates.get("random", [])

    all_templates = pool + templates.get("random", [])
    if not all_templates:
        all_templates = ["在想什么呢？"]
    
    raw = random.choice(all_templates)
    return sanitize_message(raw)


def main():
    dry_run = "--dry-run" in sys.argv
    
    # 1. 检查是否该发
    check = run_checker()
    
    if not check.get("should_send"):
        reason = check.get("reason", "unknown")
        print(f"NO_REPLY (reason: {reason})")
        sys.exit(0)
    
    # 2. 选消息
    templates = check.get("templates", {})
    message = pick_message(templates)
    
    # 3. 判断是否发语音
    voice_enabled = check.get("voice_enabled", False)
    voice_prob = check.get("voice_probability", 0.3)
    voice_name = check.get("voice_name", "xiaoxiao")
    use_voice = voice_enabled and random.random() < voice_prob
    
    voice_path = None
    if use_voice:
        voice_path = generate_voice(message, voice_name)
        if not voice_path:
            print(f"⚠️ 语音生成失败，降级为文字")
            use_voice = False
    
    # 4. 构造输出
    if use_voice and voice_path:
        # 语音消息：不重复文字，直接发语音
        output = f"<qqmedia>{voice_path}</qqmedia>"
        medium = "voice"
    else:
        output = message
        medium = "text"
    
    # 5. 标记已发送 + 记录历史
    if not dry_run:
        mark_sent()
        state = load_state()
        if state:
            persona_name = state.get("active_persona")
            if persona_name:
                save_to_history(persona_name, message, "persona")
    
    # 6. 输出结果
    print(f"✅ [{medium}] {message}")
    if voice_path:
        print(f"   语音文件: {voice_path}")
    print("---")
    print(output)


if __name__ == "__main__":
    main()
