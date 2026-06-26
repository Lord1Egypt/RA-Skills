#!/usr/bin/env python3
import os
"""
MiniMax TTS - 查询可用音色列表
"""

import requests
import json

API_KEY = os.environ.get("MINIMAX_API_KEY", "")


def list_voices(category: str = "system_voice", limit: int = 50) -> list:
    """
    查询 MiniMax 可用音色列表
    
    Args:
        category: 音色类型
            - system_voice: 系统音色（默认）
            - voice_cloning: 克隆音色
            - voice_generation: 生成音色
        limit: 返回数量限制
    
    Returns:
        音色列表
    """
    url = "https://api.minimaxi.com/v1/get_voice"
    payload = {"voice_type": "all"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    result = response.json()
    
    voices = result.get(category, [])
    return voices[:limit]


def format_voice_list(voices: list) -> str:
    """格式化音色列表为可读文本"""
    lines = []
    for v in voices:
        voice_id = v.get("voice_id", "")
        voice_name = v.get("voice_name", "")
        language = v.get("language", "")
        gender = v.get("gender", "")
        if voice_id and voice_name:
            lines.append(f"- **{voice_id}** — {voice_name} ({gender}, {language})")
    return "\n".join(lines) if lines else "未找到音色"


def main():
    print("正在获取 MiniMax 可用音色列表...\n")
    
    categories = {
        "system_voice": "系统音色",
        "voice_cloning": "克隆音色",
        "voice_generation": "生成音色",
    }
    
    for cat_key, cat_name in categories.items():
        voices = list_voices(category=cat_key, limit=20)
        if voices:
            print(f"=== {cat_name} ({len(voices)}个) ===")
            for v in voices[:20]:
                print(f"  {v.get('voice_id')}: {v.get('voice_name', '')}")
            if len(voices) > 20:
                print(f"  ... 还有 {len(voices)-20} 个")
            print()


if __name__ == "__main__":
    main()
