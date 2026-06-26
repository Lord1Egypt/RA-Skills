#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Axiang Emoji Trigger
Automatically send emoji images based on emotion
"""

import os
import random
import re
from pathlib import Path

# Configuration
EMOJI_BASE_DIR = Path("C:/Users/Xiabi/.openclaw/workspace/axiang-emoji")

# Emotion mapping
EMOTION_MAP = {
    "happy": ["开心", "兴奋", "高兴", "开心"],
    "shy": ["害羞", "不好意思", "害羞"],
    "tsundere": ["傲娇", "生气", "傲娇"],
    "thinking": ["思考", "疑惑", "思考"],
    "touched": ["感动", "感谢", "感动"],
    "confident": ["自信", "得意", "自信"],
    "cheer": ["欢呼", "庆祝", "欢呼"],
    "sleepy": ["困倦", "累了", "困倦"],
}

# Emoji mapping
EMOJI_MAP = {
    "happy": "😆",
    "shy": "😳",
    "tsundere": "😤",
    "thinking": "🤔",
    "touched": "🥺",
    "confident": "😎",
    "cheer": "🎉",
    "sleepy": "😴",
    "default": "🦞",
}


def detect_emotion(text: str) -> str:
    """
    Detect emotion from text
    
    Args:
        text: Response text
    
    Returns:
        Emotion name (happy/shy/tsundere/etc.)
    """
    # Check for explicit emotion marker
    match = re.search(r'情绪：.*?→\s*(\w+)', text)
    if match:
        return match.group(1).lower()
    
    # Check for emoji at the end
    for emotion, emoji in EMOJI_MAP.items():
        if text.strip().endswith(emoji):
            return emotion
    
    # Keyword-based detection (simple)
    text_lower = text.lower()
    for emotion, keywords in EMOTION_MAP.items():
        if any(kw in text_lower for kw in keywords):
            return emotion
    
    return "default"


def get_emoji_file(emotion: str) -> Path:
    """
    Get random emoji file for emotion
    
    Args:
        emotion: Emotion name
    
    Returns:
        Path to emoji file
    """
    emoji_dir = EMOJI_BASE_DIR / emotion
    
    if not emoji_dir.exists():
        emoji_dir = EMOJI_BASE_DIR  # Fallback to default
    
    # Prefer thumbnail images
    emoji_files = list(emoji_dir.glob("*_thumb.png"))
    
    if not emoji_files:
        emoji_files = list(emoji_dir.glob("*.png"))
    
    if not emoji_files:
        return None
    
    return random.choice(emoji_files)


def send_emoji(emotion: str = None, text: str = None):
    """
    Send emoji image
    
    Args:
        emotion: Explicit emotion (optional)
        text: Response text (for auto-detection)
    """
    # Detect emotion
    if not emotion:
        if text:
            emotion = detect_emotion(text)
        else:
            emotion = "default"
    
    # Get emoji file
    emoji_file = get_emoji_file(emotion)
    
    if not emoji_file:
        print(f"[WARN] No emoji found for emotion: {emotion}")
        return None
    
    print(f"[INFO] Sending emoji: {emoji_file.name} (emotion: {emotion})")
    
    # Send via message tool (would be called by OpenClaw)
    # message --action send --channel feishu --filePath str(emoji_file)
    
    return str(emoji_file)


def parse_emotion_marker(text: str) -> dict:
    """
    Parse emotion marker from text
    
    Format:
    ---
    情绪：开心/兴奋 → happy 😆
    😆
    
    Args:
        text: Full response text
    
    Returns:
        Dict with emotion, folder, emoji
    """
    match = re.search(r'情绪：(.*?)\s*→\s*(\w+)\s*(\S+)', text)
    
    if match:
        return {
            "emotion_desc": match.group(1).strip(),
            "folder": match.group(2).strip(),
            "emoji": match.group(3).strip(),
        }
    
    return None


# CLI interface
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Axiang Emoji Trigger Test")
    print("=" * 60)
    
    # Test emotion detection
    test_texts = [
        ("好嘞！战斗开始！✨", "happy"),
        ("呜～对不起嘛...", "shy"),
        ("哼～才不是呢！", "tsundere"),
        ("让我想想...", "thinking"),
        ("太感谢你了！", "touched"),
        ("香香超厉害的！", "confident"),
        ("完成啦！🎉", "cheer"),
        ("好困哦...", "sleepy"),
    ]
    
    print("\n[Emotion Detection Test]")
    for text, expected in test_texts:
        detected = detect_emotion(text)
        status = "✓" if detected == expected else "✗"
        print(f"{status} '{text[:20]}...' -> {detected} (expected: {expected})")
    
    # Test emoji sending
    print("\n[Emoji File Test]")
    for emotion in ["happy", "shy", "tsundere", "thinking", "confident"]:
        emoji_file = get_emoji_file(emotion)
        if emoji_file:
            print(f"✓ {emotion}: {emoji_file.name}")
        else:
            print(f"✗ {emotion}: No emoji found")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
