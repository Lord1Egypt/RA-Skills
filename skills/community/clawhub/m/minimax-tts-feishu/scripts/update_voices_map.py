#!/usr/bin/env python3
import os
"""
更新 voices-map.md
从 MiniMax API 获取最新音色列表，筛选中文音色后更新本地 voices-map.md
"""

import requests
import re
from datetime import datetime

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
VOICES_MAP_PATH = os.environ.get("TTS_VOICES_MAP_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "voices-map.md"))


def get_all_voices():
    """从 API 获取所有音色"""
    url = "https://api.minimaxi.com/v1/get_voice"
    payload = {"voice_type": "all"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    result = response.json()
    voices = result.get("system_voice", [])
    return voices


def is_chinese_voice(voice: dict) -> bool:
    """判断是否为中文音色"""
    voice_name = voice.get("voice_name", "")
    voice_id = voice.get("voice_id", "")
    description = voice.get("description", [])

    chinese_keywords = ["中文", "普通话", "粤语", "Mandarin", "Chinese"]

    text = voice_name + " " + voice_id + " " + " ".join(description if isinstance(description, list) else [])

    for kw in chinese_keywords:
        if kw.lower() in text.lower():
            return True
    return False


def format_description(desc) -> str:
    """格式化描述字段"""
    if isinstance(desc, list):
        return " ".join(str(d) for d in desc if d)
    return str(desc) if desc else ""


def format_voices_table(voices: list) -> str:
    """格式化音色列表为 markdown 表格"""
    lines = [
        "| voice_id | 名称 | 描述 |",
        "|----------|------|------|"
    ]
    for v in voices:
        voice_id = v.get("voice_id", "")
        voice_name = v.get("voice_name", "")
        desc = format_description(v.get("description", ""))
        lines.append(f"| **{voice_id}** | {voice_name} | {desc[:40]} |")
    return "\n".join(lines)


def build_voices_map(voices: list, custom_voices: list = None) -> str:
    """构建完整的 voices-map.md 内容"""
    chinese_voices = [v for v in voices if is_chinese_voice(v)]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    voice_table = format_voices_table(chinese_voices)

    custom_section = ""
    if custom_voices:
        custom_lines = [
            "",
            "## 自定义音色",
            "",
            "| voice_id | 创建时间 | 描述 | 状态 |",
            "|----------|----------|------|------|"
        ]
        for cv in custom_voices:
            custom_lines.append(
                f"| {cv.get('voice_id', '')} | {cv.get('created', '')} | "
                f"{cv.get('description', '')} | {cv.get('status', '')} |"
            )
        custom_section = "\n".join(custom_lines)

    content = f"""# 声音音色映射

更新时间：{now}

## 默认音色

**Chinese (Mandarin)_Gentle_Senior（温柔学姐）**

## 内置音色（中文，共 {len(chinese_voices)} 个）

| voice_id | 名称 | 描述 |
|----------|------|------|
{chr(10).join(f"| **{v.get('voice_id', '')}** | {v.get('voice_name', '')} | {format_description(v.get('description', ''))[:40]} |" for v in chinese_voices)}

{custom_section}

---
*本文件由 update_voices_map.py 自动更新*
"""
    return content


def main():
    print("正在获取最新音色列表...")
    voices = get_all_voices()
    print(f"获取到 {len(voices)} 个系统音色")

    chinese_voices = [v for v in voices if is_chinese_voice(v)]
    print(f"其中中文音色 {len(chinese_voices)} 个")

    # 读取现有的自定义音色
    existing_custom = []
    try:
        with open(VOICES_MAP_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        custom_matches = re.findall(r"\| (ttv-voice-\S+) \| (\S+) \| (.+?) \| (.+?) \|", content)
        for match in custom_matches:
            existing_custom.append({
                "voice_id": match[0],
                "created": match[1],
                "description": match[2],
                "status": match[3]
            })
    except Exception:
        pass

    # 构建新内容（不使用 f-string 列表推导）
    table_lines = [
        "| voice_id | 名称 | 描述 |",
        "|----------|------|------|"
    ]
    for v in chinese_voices:
        voice_id = v.get("voice_id", "")
        voice_name = v.get("voice_name", "")
        desc = format_description(v.get("description", ""))[:40]
        table_lines.append(f"| **{voice_id}** | {voice_name} | {desc} |")

    custom_section = ""
    if existing_custom:
        custom_lines = [
            "",
            "## 自定义音色",
            "",
            "| voice_id | 创建时间 | 描述 | 状态 |",
            "|----------|----------|------|------|"
        ]
        for cv in existing_custom:
            custom_lines.append(
                f"| {cv.get('voice_id', '')} | {cv.get('created', '')} | "
                f"{cv.get('description', '')} | {cv.get('status', '')} |"
            )
        custom_section = "\n".join(custom_lines)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# 声音音色映射

更新时间：{now_str}

## 默认音色

**Chinese (Mandarin)_Gentle_Senior（温柔学姐）**

## 内置音色（中文，共 {len(chinese_voices)} 个）

"""
    content += "\n".join(table_lines)
    content += f"""

{custom_section}

---
*本文件由 update_voices_map.py 自动更新*
"""

    with open(VOICES_MAP_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 已更新 {VOICES_MAP_PATH}")
    print(f"   中文音色: {len(chinese_voices)} 个")
    if existing_custom:
        print(f"   自定义音色: {len(existing_custom)} 个")


if __name__ == "__main__":
    main()
