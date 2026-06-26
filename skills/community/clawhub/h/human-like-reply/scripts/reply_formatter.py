#!/usr/bin/env python3
"""
Human-like Reply Formatter

This module processes AI-generated replies to make them sound more natural
and human-like, avoiding excessive greetings and mechanical expressions.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Default configuration
DEFAULT_CONFIG = {
    "greeting_threshold": 3,       # Rounds after which to reduce greetings
    "topic_change_threshold": 5,   # Rounds that constitute a topic change
    "silence_minutes": 30,         # Minutes of silence to consider it a new conversation
    "use_smileys": True,           # Whether to add smileys
    "formal_level": 0.3,           # 0=very casual, 1=very formal
    "greeting_patterns": [
        r"^(老板|老板，|老板！|老板\.)\s*",  # Common Chinese greetings
        r"^(您好|您好！|您好，)",           # Formal greetings
        r"^(好的，|好的！|好的\.)",        # Mechanical acknowledgments at start
    ],
    "avoid_patterns": [
        r"^(好的，|好的！|好的\.)",        # Remove mechanical "好的" at start
        r"^(明白了，|明白了！|明白了\.)",
        r"^(收到，|收到！|收到\.)",
        r"^(请稍等，|稍等，|稍等！)",
    ],
    "casual_replacements": {
        "好的": ["行", "OK", "没问题", "好嘞", "好滴", "妥了"],
        "明白了": ["懂了", "清楚啦", "了解", "收到", "明白", "了然"],
        "收到": ["收到", "get", "收到啦", "好嘞"],
        "请问": ["想问下", "问问", "问一下", "顺便问下"],
        "抱歉": ["不好意思", "对不起啊", "抱歉哈", "哎呀", "抱歉抱歉"],
        "非常感谢": ["太感谢了", "谢啦", "多谢", "谢谢老板", "感谢"],
        "正在处理": ["在弄了", "搞着呢", "正在办", "这就去弄", "马上处理"],
        "没有问题": ["没问题", "木有问题", "小意思", "easy"],
        "我知道了": ["我知道啦", "明白啦", "懂了懂了", "清楚"],
        "好的，我明白了": ["行，懂了", "OK了解", "收到明白"],
    },
    # filler words to occasionally insert (with probability)
    "filler_words": {
        "prefix": ["嗯，", "那个，", "话说，", "对了，", "哦，", "这样啊，", "emmm，", "我觉得吧，"],
        "mid_sentence": ["然后", "不过", "其实", "话说回来", "也就是说"],
    },
    "filler_probability": 0.15,      # How often to add filler words
    "sentence_variation": True,       # Vary sentence structure
    "use_reduplication": 0.2,         # Add reduplication like "看看", "弄弄" (casual only)
    "emotional_emojis": ["😄", "😊", "👍", "✌️", "🤔", "😅", "😭", "🔥", "💪", "🙏"],
}

class ReplyState:
    """Manages the state of conversation for human-like reply formatting."""

    def __init__(self, state_file: str = None):
        self.state_file = state_file or os.path.join(
            os.path.dirname(__file__),
            "..", "memory", "reply_state.json"
        )
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file or create default."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "conversations": {},
            "last_update": datetime.now().isoformat()
        }

    def _save_state(self):
        """Save state to file."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def get_conversation(self, session_key: str) -> Dict:
        """Get conversation state for a specific session."""
        if session_key not in self.state["conversations"]:
            self.state["conversations"][session_key] = {
                "rounds": 0,
                "last_message_time": None,
                "last_used_greeting": False,
                "current_topic": None,
                "greeting_count": 0
            }
        return self.state["conversations"][session_key]

    def update_conversation(self, session_key: str, used_greeting: bool,
                           topic: str = None):
        """Update conversation state after a reply."""
        conv = self.get_conversation(session_key)
        conv["rounds"] += 1
        conv["last_message_time"] = datetime.now().isoformat()
        conv["last_used_greeting"] = used_greeting
        if used_greeting:
            conv["greeting_count"] += 1
        if topic:
            conv["current_topic"] = topic
        self._save_state()

    @staticmethod
    def detect_topic_change(old_topic: str, new_message: str, history: List) -> bool:
        """
        Simple heuristic to detect if the topic has changed.
        """
        # If there's no old topic, it's a new topic
        if not old_topic:
            return True

        # Extract keywords from new message (simple approach)
        new_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', new_message))

        if not new_keywords:
            return False

        # Check overlap with recent history
        recent_messages = history[-3:] if len(history) >= 3 else history
        history_text = " ".join(recent_messages)
        history_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', history_text))

        # If low overlap, topic likely changed
        if len(new_keywords & history_keywords) < 2:
            return True

        return False

def should_use_greeting(state: ReplyState, session_key: str, config: Dict,
                       is_new_topic: bool = False, user_greeting: bool = False) -> Tuple[bool, str]:
    """
    Determine whether to use a greeting in the next reply.

    Args:
        state: ReplyState instance
        session_key: Session identifier
        config: Configuration dictionary
        is_new_topic: Whether user just changed topic
        user_greeting: Whether user's message started with a greeting (like "老板")

    Returns:
        (should_greet, greeting_text)
    """
    conv = state.get_conversation(session_key)
    rounds = conv["rounds"]

    # Check if it's a new conversation (silence for too long)
    last_time = conv.get("last_message_time")
    if last_time:
        last_dt = datetime.fromisoformat(last_time)
        silence_seconds = (datetime.now() - last_dt).total_seconds()
        if silence_seconds > config["silence_minutes"] * 60:
            # It's been a while, greet again
            return True, get_greeting_text(config)

    # If user greeted, we should greet back (mirror behavior)
    if user_greeting and random.random() < 0.7:
        return True, get_greeting_text(config)

    # For first few rounds, greet with high probability
    if rounds < config["greeting_threshold"]:
        # Decay probability: round 1: 100%, round 2: 66%, round 3: 33%
        probability = (config["greeting_threshold"] - rounds + 1) / config["greeting_threshold"]
        if random.random() < probability:
            return True, get_greeting_text(config)
        return False, ""

    # After threshold, rarely greet unless topic changed
    if is_new_topic and random.random() < 0.2:
        return True, get_greeting_text(config)

    # Late rounds (5+), almost never greet unless special circumstances
    if rounds >= 5 and random.random() < 0.05:
        return True, get_greeting_text(config)

    return False, ""

def get_greeting_text(config: Dict) -> str:
    """Get a casual greeting text based on time of day and config."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        base = "早"
    elif 12 <= hour < 18:
        base = "哈喽"
    else:
        base = "哈喽"

    if config["use_smileys"] and random.random() < 0.5:
        smileys = [" 😄", " 😊", " 👍", " ✌️"]
        base += random.choice(smileys)

    return base

def add_filler_words(text: str, config: Dict) -> str:
    """Occasionally insert filler words to sound more natural."""
    if random.random() > config.get("filler_probability", 0.15):
        return text

    sentences = re.split(r'([。！？\n])', text)
    if len(sentences) < 2:
        return text

    # Choose a sentence to add filler to (prefer first or second, but not last)
    candidates = list(range(0, len(sentences)-2, 2))  # Even indices are sentences
    if not candidates:
        return text

    target_idx = random.choice(candidates)

    # Choose filler type
    filler_type = random.choice(["prefix", "mid_sentence"])
    fillers = config["filler_words"].get(filler_type, [])

    if not fillers:
        return text

    filler = random.choice(fillers)

    if filler_type == "prefix":
        # Add at the beginning of the sentence
        sentence = sentences[target_idx]
        if sentence.strip() and not re.match(r'^[嗯那对了哦]', sentence):
            sentences[target_idx] = filler + sentence
    elif filler_type == "mid_sentence" and len(sentence) > 10:
        # Insert in the middle of a longer sentence
        words = list(sentence)
        insert_pos = random.randint(2, len(words)-3)
        words.insert(insert_pos, filler)
        sentences[target_idx] = ''.join(words)

    return ''.join(sentences)

def vary_sentence_structure(text: str, config: Dict) -> str:
    """Add variation to sentence structure for more natural flow."""
    if not config.get("sentence_variation", True) or random.random() > 0.3:
        return text

    # occasionally change sentence endings
    replacements = {
        "吗？": ["是吧？", "对吗？", "呢？", ""],
        "呢？": ["是吧？", "对吗？", "吗？", ""],
        "吧。": ["啦。", "咯。", ""],
        "的。": ["滴。", "的呀。", ""],
    }

    for old, options in replacements.items():
        if old in text and random.random() < 0.4:
            new = random.choice([o for o in options if o])
            if new:
                text = text.replace(old, new, 1)
            break

    return text

def add_reduplication(text: str, config: Dict) -> str:
    """Add Chinese word reduplication for casual tone."""
    if config.get("formal_level", 0.5) > 0.4 or random.random() > config.get("use_reduplication", 0.2):
        return text

    # Words that can be reduplicated naturally
    reduplicable = ["看", "弄", "查", "问", "想", "试", "等", "研究"]

    for word in reduplicable:
        pattern = rf'({word})({word})'  # Already reduplicated, skip
        if re.search(pattern, text):
            return text

        # Replace single occurrence with reduplicated version
        if re.search(rf'\b{word}\b', text) and random.random() < 0.25:
            text = re.sub(rf'\b{word}\b', f"{word}{word}", text, count=1)
            break

    return text

def soft_punctuation(text: str) -> str:
    """Soften punctuation for more casual tone."""
    #  Replace some periods with "～" or "啦"
    if random.random() < 0.3:
        text = re.sub(r'([^。\n])。$', r'\1啦', text)  # End of text
        text = re.sub(r'([^。\n])。([^。])', r'\1～\2', text, count=1)  # Middle

    return text

def format_reply(text: str, config: Dict, use_greeting: bool = False,
                greeting_text: str = "") -> str:
    """
    Format a reply to be more human-like.

    Args:
        text: The original AI-generated reply
        config: Configuration dictionary
        use_greeting: Whether to prepend a greeting
        greeting_text: The greeting text to use

    Returns:
        Formatted reply string
    """
    # Remove leading greetings if we're not using one
    if not use_greeting:
        for pattern in config["greeting_patterns"]:
            text = re.sub(pattern, "", text, count=1, flags=re.UNICODE)

    # Remove avoid patterns at the start (like "好的，")
    for pattern in config["avoid_patterns"]:
        text = re.sub(pattern, "", text, count=1, flags=re.UNICODE)

    # Apply casual replacements (if formal_level is low)
    if config["formal_level"] < 0.5:
        for old, replacements in config["casual_replacements"].items():
            if old in text:
                # Replace with a random choice
                new = random.choice(replacements)
                # Only replace at start of sentence or after punctuation
                pattern = rf'(^|[。！？\n])\s*{re.escape(old)}'
                text = re.sub(pattern, rf'\1{new}', text)

    # Apply structural variations (only if casual)
    if config["formal_level"] < 0.6:
        text = add_filler_words(text, config)
        text = vary_sentence_structure(text, config)
        text = add_reduplication(text, config)

        if config.get("soften_punctuation", True):
            text = soft_punctuation(text)

    # Trim whitespace and any leading punctuation left over from removals
    text = text.strip()
    # Remove any leading comma or period that might be left
    text = re.sub(r'^[，,。\.]\s*', '', text)

    # Prepend greeting if needed
    if use_greeting and greeting_text:
        text = f"{greeting_text} {text}"

    return text

def detect_topic_change(old_topic: str, new_message: str, history: List) -> bool:
    """
    Simple heuristic to detect if the topic has changed.
    """
    # If there's no old topic, it's a new topic
    if not old_topic:
        return True

    # Extract keywords from new message (simple approach)
    new_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', new_message))

    if not new_keywords:
        return False

    # Check overlap with recent history
    recent_messages = history[-3:] if len(history) >= 3 else history
    history_text = " ".join(recent_messages)
    history_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', history_text))

    # If low overlap, topic likely changed
    if len(new_keywords & history_keywords) < 2:
        return True

    return False

# Random module is needed
import random

if __name__ == "__main__":
    # Test the formatter
    test_cases = [
        ("老板，明天天气怎么样？", True, "老板"),
        ("好的，我已经查到了。", False, ""),
        ("老板，那个事情处理好了吗？", True, "老板"),
    ]

    config = DEFAULT_CONFIG.copy()

    for original, greet, greeting in test_cases:
        result = format_reply(original, config, greet, greeting)
        print(f"Input: {original}")
        print(f"Output: {result}")
        print()