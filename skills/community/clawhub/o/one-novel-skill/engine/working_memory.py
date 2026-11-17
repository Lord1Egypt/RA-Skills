#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
working_memory.py — 工作记忆

当前正在处理的上下文窗口（短期记忆）。
"""

import logging
from typing import List, Dict, Optional

_log = logging.getLogger("working_memory")


class WorkingMemory:
    """工作记忆 — 当前正在处理的上下文窗口"""

    def __init__(self):
        self.current_chapter = 0
        self.current_task = ""
        self.recent_context = ""

    def update(self, chapter: int, context: str):
        """更新当前章节的工作记忆"""
        self.current_chapter = chapter
        self.recent_context = context

    def get(self) -> str:
        """获取工作记忆文本"""
        return self.recent_context

    def set_task(self, task: str):
        """设置当前任务描述"""
        self.current_task = task

    def clear(self):
        """清空工作记忆"""
        self.current_chapter = 0
        self.current_task = ""
        self.recent_context = ""
