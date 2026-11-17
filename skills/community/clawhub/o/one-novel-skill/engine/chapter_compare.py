#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chapter_compare.py — 章节对比引擎

自动检测连续章节之间：
  1. 人设漂移 — 角色性格/说话方式/行为逻辑突变
  2. 时间线断裂 — 事件顺序/时间跨度矛盾
  3. 伏笔遗漏 — 前文伏笔未在后续章节推进或回收
  4. 场景连续性 — 上章结尾和下章开头的衔接问题
"""

import re, json, logging
from pathlib import Path
from collections import Counter
from typing import List, Dict, Optional, Any

_log = logging.getLogger("chapter_compare")

# ── 角色声线特征检测 ──

class CharacterVoiceFingerprint:
    """提取角色的说话方式和行为模式特征"""

    def __init__(self, name: str):
        self.name = name
        self.dialogue_samples: List[str] = []
        self.action_patterns: List[str] = []
        self.avg_sentence_len = 0
        self.emotion_words: List[str] = []

    def extract(self, text: str):
        """从文本中提取角色的声线特征"""
        # 提取对话（中文引号内的内容）
        dialogues = re.findall(r'["\u201c]([^"\u201d]+)["\u201d]', text)
        dialogues += re.findall(r"'([^']+)'", text)
        dialogues += re.findall(r"\u300c([^\u300d]+)\u300d", text)

        # 过滤短对话
        dialogues = [d for d in dialogues if len(d) > 3]
        self.dialogue_samples = dialogues[:10]  # 最多保留10句

        if self.dialogue_samples:
            lens = [len(d) for d in self.dialogue_samples]
            self.avg_sentence_len = sum(lens) / len(lens)

        # 提取情绪词
        emotion_patterns = [
            "冷静", "暴躁", "温柔", "冷漠", "热情", "愤怒", "悲伤", "喜悦",
            "不耐烦", "耐心", "嘲讽", "鼓励", "威胁", "恳求",
        ]
        for word in emotion_patterns:
            if word in text:
                self.emotion_words.append(word)

    def compare(self, other: "CharacterVoiceFingerprint") -> List[str]:
        """比较两个声线特征，返回差异列表"""
        issues = []
        name = self.name

        # 对话长度变化 > 50%
        if self.avg_sentence_len > 0 and other.avg_sentence_len > 0:
            ratio = max(self.avg_sentence_len, other.avg_sentence_len) / \
                    max(1, min(self.avg_sentence_len, other.avg_sentence_len))
            if ratio > 1.5:
                issues.append(
                    f"[声线漂移] {name}: 对话长度变化 {ratio:.1f}x "
                    f"({self.avg_sentence_len:.0f}字 → {other.avg_sentence_len:.0f}字)"
                )

        # 情绪词突变（新增/消失的情绪词 > 3个）
        old_emotions = set(self.emotion_words)
        new_emotions = set(other.emotion_words)
        if old_emotions and new_emotions:
            added = new_emotions - old_emotions
            removed = old_emotions - new_emotions
            if len(added) >= 3:
                issues.append(f"[情绪突变] {name}: 新增情绪特征: {', '.join(sorted(added))}")
            if len(removed) >= 3:
                issues.append(f"[情绪突变] {name}: 消失情绪特征: {', '.join(sorted(removed))}")

        return issues

# ── 时间线检测 ──

def detect_timeline_break(prev_text: str, curr_text: str) -> List[str]:
    """检测两章之间的时间线断裂"""
    issues = []

    # 检测时间标记
    time_patterns = [
        (r"(\d+)天后", "天"),
        (r"(\d+)天后", "天"),
        (r"(\d+)个月后", "月"),
        (r"(\d+)年后", "年"),
        (r"第(\d+)天", "天"),
        (r"(\d+)小时", "小时"),
        (r"次日", "天"),
        (r"第二天", "天"),
        (r"当晚", "晚"),
        (r"第二天一早", "早"),
    ]

    prev_times = []
    curr_times = []
    for pattern, unit in time_patterns:
        for m in re.finditer(pattern, prev_text):
            prev_times.append((m.group(0), m.start()))
        for m in re.finditer(pattern, curr_text):
            curr_times.append((m.group(0), m.start()))

    # 检测明显的时间跳跃
    jump_markers = ["三个月后", "半年后", "一年后", "三年后", "五年后", "十年后"]
    has_jump = any(marker in curr_text for marker in jump_markers)
    has_transition = any(
        phrase in curr_text[:200]
        for phrase in ["转眼", "时光飞逝", "岁月如梭", "不知不觉", "一晃"]
    )

    if has_jump and not has_transition:
        issues.append("[时间线] 存在大跨度时间跳跃但缺少过渡描写")

    # 检测事件时间矛盾
    # 如果上章结尾是夜晚，下章开头是清晨但没有时间过渡标记
    night_markers = ["夜", "晚上", "深夜", "半夜", "凌晨"]
    morning_markers = ["早上", "早晨", "清晨", "天亮", "日出"]

    prev_is_night = any(m in prev_text[-200:] for m in night_markers)
    curr_is_morning = any(m in curr_text[:200] for m in morning_markers)

    if prev_is_night and curr_is_morning:
        has_sleep_transition = any(
            m in curr_text[:300] for m in ["醒来", "睡", "起床", "睁眼"]
        )
        if not has_sleep_transition:
            issues.append("[时间线] 上章结尾夜晚 → 本章开头清晨，缺少睡眠/时间过渡")

    return issues

# ── 伏笔检测 ──

def detect_foreshadow_gap(
    prev_text: str, curr_text: str,
    foreshadows: List[dict], chapter: int
) -> List[str]:
    """检测前文伏笔是否在后续章节推进"""
    issues = []

    for fs in foreshadows:
        planted = fs.get("chapter_planted", 0)
        content = fs.get("content", "")
        status = fs.get("status", "open")

        # 跳过已回收的伏笔
        if status == "resolved":
            continue

        # 伏笔已超过 10 章未推进
        if chapter - planted >= 10:
            issues.append(
                f"[伏笔遗漏] 第{planted}章伏笔已超过{chapter - planted}章未推进: {content[:50]}"
            )
        # 伏笔已超过 5 章，检查当前章是否有推进
        elif chapter - planted >= 5:
            keywords = re.findall(r"[\u4e00-\u9fff]{2,6}", content)
            mentioned = any(kw in curr_text for kw in keywords if len(kw) >= 2)
            if not mentioned:
                issues.append(
                    f"[伏笔停滞] 第{planted}章伏笔已{chapter - planted}章未推进: {content[:50]}"
                )

    return issues

# ── 场景连续性检测 ──

def detect_scene_continuity(prev_text: str, curr_text: str) -> List[str]:
    """检测上章结尾和下章开头的场景衔接"""
    issues = []

    prev_end = prev_text[-300:]
    curr_start = curr_text[:300]

    # 检测位置一致性
    prev_locations = re.findall(r"(?:在|到|去|来)([\u4e00-\u9fff]{2,6}(?:房间|大厅|广场|门口|楼上|楼下|外面|里面|办公室|家里|医院|学校))", prev_end)
    curr_locations = re.findall(r"(?:在|到|去|来)([\u4e00-\u9fff]{2,6}(?:房间|大厅|广场|门口|楼上|楼下|外面|里面|办公室|家里|医院|学校))", curr_start)

    # 检测角色位置连续性
    prev_chars_here = re.findall(r"([\u4e00-\u9fff]{2,4})(?:站|坐|躺|走|跑|回|进|出)", prev_end)
    curr_chars_here = re.findall(r"([\u4e00-\u9fff]{2,4})(?:站|坐|躺|走|跑|回|进|出)", curr_start)

    # 如果角色集合相同但位置变了，检查是否有移动描写
    prev_set = set(prev_chars_here)
    curr_set = set(curr_chars_here)
    common = prev_set & curr_set
    if common and prev_locations and curr_locations:
        if prev_locations != curr_locations:
            # 检查是否有位置转换描写
            move_markers = ["离开", "走到", "来到", "赶到", "回到", "进入", "穿过", "下了"]
            has_move = any(m in curr_start for m in move_markers)
            if not has_move:
                char_names = "、".join(common)
                issues.append(
                    f"[场景跳跃] 角色{char_names}从{prev_locations[0]}跳到{curr_locations[0]}，缺少移动描写"
                )

    return issues

# ── 主角人设一致性检测 ──

def detect_character_drift(prev_text: str, curr_text: str) -> List[str]:
    """检测主角人设是否在两章间漂移"""
    issues = []

    # 行为模式变化
    # 如果上章主角被动/退缩，本章突然主动/激进
    passive_patterns = ["不敢", "害怕", "退缩", "犹豫", "沉默", "忍"]
    active_patterns = ["主动", "果断", "毫不", "直接", "立刻", "马上"]

    prev_passive = sum(1 for p in passive_patterns if p in prev_text)
    prev_active = sum(1 for a in active_patterns if a in prev_text)
    curr_passive = sum(1 for p in passive_patterns if p in curr_text)
    curr_active = sum(1 for a in active_patterns if a in curr_text)

    if prev_passive > 0 and curr_passive == 0 and curr_active >= 5:
        if prev_active <= 2:
            issues.append("[人设漂移] 主角从被动/退缩型突然变为主动型，缺少性格转变的触发事件")

    if prev_active >= 5 and curr_active == 0 and curr_passive >= 3:
        issues.append("[人设漂移] 主角从主动型突然变为被动型，缺少合理解释")

    return issues

# ── 统一入口 ──

def compare_chapters(
    prev_text: str,
    curr_text: str,
    chapter: int,
    foreshadows: Optional[List[dict]] = None,
    book_dir: str = "",
) -> Dict[str, Any]:
    """比较两个连续章节，返回所有检测到的问题

    Args:
        prev_text: 上一章正文
        curr_text: 当前章正文
        chapter: 当前章节号
        foreshadows: 伏笔列表
        book_dir: 书籍目录（用于读取角色状态）

    Returns:
        {"issues": [...], "summary": "...", "score": 0-100}
    """
    all_issues = []

    # 1. 场景连续性
    all_issues.extend(detect_scene_continuity(prev_text, curr_text))

    # 2. 时间线断裂
    all_issues.extend(detect_timeline_break(prev_text, curr_text))

    # 3. 人设漂移
    all_issues.extend(detect_character_drift(prev_text, curr_text))

    # 4. 伏笔遗漏
    if foreshadows:
        all_issues.extend(
            detect_foreshadow_gap(prev_text, curr_text, foreshadows, chapter)
        )

    # 5. 角色声线（如果 state.json 中有角色列表）
    if book_dir:
        try:
            state_path = Path(book_dir) / "state.json"
            if state_path.exists():
                state = json.loads(state_path.read_text(encoding="utf-8"))
                chars = state.get("characters", {})
                # 简单检测：如果主角出现在两章中，比较声线
                for name in chars:
                    prev_voice = CharacterVoiceFingerprint(name)
                    curr_voice = CharacterVoiceFingerprint(name)
                    prev_voice.extract(prev_text)
                    curr_voice.extract(curr_text)
                    all_issues.extend(prev_voice.compare(curr_voice))
        except Exception:
            pass

    # 计算评分
    total_checks = 5
    failed_checks = len(set(
        issue.split("]")[0] if "]" in issue else issue
        for issue in all_issues
    ))
    score = max(0, 100 - failed_checks * 15)

    # 生成摘要
    categories = Counter()
    for issue in all_issues:
        cat = issue.split("]")[0].replace("[", "") if "]" in issue else "其他"
        categories[cat] += 1

    summary_parts = []
    for cat, count in categories.most_common():
        summary_parts.append(f"{cat}: {count}处")
    summary = "；".join(summary_parts) if summary_parts else "未发现问题"

    return {
        "issues": all_issues,
        "summary": summary,
        "score": score,
        "chapter": chapter,
    }
