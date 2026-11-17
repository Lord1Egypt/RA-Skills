#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spec_validator.py — 章节规格验证合约

功能: 自动校验章节正文与spec规格的一致性
  1. must_happen 事件是否在正文中出现
  2. before_state/after_state 角色状态是否变化合理
  3. 字数是否符合预期
"""

import re, json
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class SpecValidationError:
    """规格校验问题"""
    def __init__(self, field: str, expected: str, actual: str, severity: str = "warning"):
        self.field = field
        self.expected = expected[:120]
        self.actual = actual[:120]
        self.severity = severity  # "error" / "warning"

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.field}: 期望={self.expected} 实际={self.actual}"


class SpecValidator:
    """规格验证器"""

    def __init__(self, book_dir: Optional[str] = None):
        self.book_dir = Path(book_dir) if book_dir else None

    def validate(self, spec: dict, text: str, chapter: int) -> List[SpecValidationError]:
        """验证单章规格与正文的一致性"""
        errors = []

        # 1. 字数校验
        expected_wc = spec.get("suggested_word_count", spec.get("word_count", 2500))
        actual_wc = len(text)
        dev = abs(actual_wc - expected_wc) / max(expected_wc, 1)
        if dev > 0.4:
            errors.append(SpecValidationError(
                "字数", f"~{expected_wc}字", f"{actual_wc}字 (偏差{dev*100:.0f}%)",
                "error" if dev > 0.6 else "warning",
            ))

        # 2. must_happen 事件校验
        must_happen = spec.get("must_happen", [])
        if isinstance(must_happen, list):
            for event in must_happen:
                if isinstance(event, str):
                    keywords = event[:20]
                    if not self._text_contains(text, keywords):
                        errors.append(SpecValidationError(
                            f"must_happen事件", event[:60], "未在正文中找到",
                            "error",
                        ))
                elif isinstance(event, dict):
                    kw = event.get("event", str(event))[:20]
                    if not self._text_contains(text, kw):
                        errors.append(SpecValidationError(
                            f"must_happen事件", kw, "未在正文中找到", "error",
                        ))
            # 如果 must_happen 为空，不做校验（可能没写）

        # 3. 开场检查（前500字必须有钩子或冲突）
        opening = text[:500]
        hook_signals = ["?", "！", "突然", "但是", "然而", "没想到",
                        "不对劲", "奇怪", "发现", "看到了", "来了",
                        "什么", "谁", "为什么"]
        has_hook = any(s in opening for s in hook_signals)
        if not has_hook and len(opening) > 100:
            errors.append(SpecValidationError(
                "开篇钩子", "前500字有悬念或冲突信号", "未检测到钩子信号",
                "warning",
            ))

        # 4. 章末检查（最后200字不能是总结式结尾）
        ending = text[-200:]
        bad_endings = ["终于明白", "终会明白", "总算", "结束了", "告一段落",
                       "于是", "从此", "就这样", "因此", "一切都"]
        for be in bad_endings:
            if be in ending:
                errors.append(SpecValidationError(
                    "章末类型", "动作/对话/悬念收尾", f"含'{be}'疑似总结式结尾",
                    "warning",
                ))
                break

        # 5. 角色出场检查（spec中的新出场角色是否在正文中出现了）
        after_state = spec.get("after_state", {})
        if isinstance(after_state, dict):
            new_chars = after_state.get("new_characters", [])
            if isinstance(new_chars, list):
                for char in new_chars:
                    name = char if isinstance(char, str) else (
                        char.get("name", "") if isinstance(char, dict) else "")
                    if name and len(name) <= 6:
                        if name not in text:
                            errors.append(SpecValidationError(
                                f"新角色'{name}'", "在正文中出场", "正文未找到名字", "warning",
                            ))

        return errors

    def validate_chapter_file(self, chapter: int) -> List[SpecValidationError]:
        """从项目目录加载章节规格和正文进行校验"""
        if not self.book_dir:
            return []

        spec_path = self.book_dir / "规格" / f"第{chapter:03d}.json"
        text_path = self.book_dir / "正文" / f"第{chapter:03d}.txt"

        if not spec_path.exists():
            return [SpecValidationError("规格文件", "存在", "不存在", "error")]
        if not text_path.exists():
            return [SpecValidationError("正文文件", "存在", "不存在", "error")]

        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return [SpecValidationError("规格文件", "有效JSON", "解析失败", "error")]

        text = text_path.read_text(encoding="utf-8", errors="replace")
        return self.validate(spec, text, chapter)

    def validate_batch(self, start: int, end: int) -> Dict[int, List[SpecValidationError]]:
        """批量校验章节"""
        results = {}
        for ch in range(start, end + 1):
            errs = self.validate_chapter_file(ch)
            if errs:
                results[ch] = errs
        return results

    def _text_contains(self, text: str, keywords: str) -> bool:
        """检查文本是否包含关键词（模糊匹配）"""
        clean_kw = keywords.strip()
        if not clean_kw:
            return True
        return clean_kw[:15] in text
