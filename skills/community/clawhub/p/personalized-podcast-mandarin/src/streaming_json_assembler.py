# -*- coding: utf-8 -*-
"""
流式JSON组装器
处理流式输出中的JSON分割和组装问题
"""
import json
from typing import Optional, Dict, Any


class StreamingJSONAssembler:
    """
    流式JSON组装器

    用于处理LLM流式输出中的JSON数据，能够：
    1. 累积接收到的文本片段
    2. 检测完整JSON对象的边界
    3. 提取并返回解析后的JSON
    """

    def __init__(self):
        self.buffer = ""
        self.json_start = -1
        self.depth = 0
        self.in_string = False
        self.escape = False

    def feed(self, chunk: str) -> Optional[Dict[str, Any]]:
        """
        接收一个文本片段，尝试提取完整的JSON对象

        Args:
            chunk: 新的文本片段

        Returns:
            如果提取到完整JSON对象，返回解析后的dict；否则返回None
        """
        self.buffer += chunk

        # 如果还没有找到JSON开始位置，先查找
        if self.json_start == -1:
            start_idx = self.buffer.find('{')
            if start_idx == -1:
                # 还没有JSON开始，继续累积
                # 保留最后100字符，防止 { 被分割
                if len(self.buffer) > 100:
                    self.buffer = self.buffer[-100:]
                return None
            self.json_start = start_idx
            self._reset_state()

        # 从JSON开始位置解析
        i = self.json_start
        while i < len(self.buffer):
            char = self.buffer[i]

            # 处理转义字符
            if self.escape:
                self.escape = False
                i += 1
                continue

            if char == '\\':
                self.escape = True
                i += 1
                continue

            # 处理字符串
            if char == '"' and not self.escape:
                self.in_string = not self.in_string
                i += 1
                continue

            # 只在非字符串状态下处理括号
            if not self.in_string:
                if char == '{':
                    if self.depth == 0:
                        self.json_start = i
                    self.depth += 1
                elif char == '}':
                    self.depth -= 1
                    if self.depth == 0:
                        # 找到完整的JSON对象
                        json_str = self.buffer[self.json_start:i+1]
                        try:
                            result = json.loads(json_str)
                            # 保留剩余部分作为新的buffer
                            self.buffer = self.buffer[i+1:]
                            self._reset_state()
                            return result
                        except json.JSONDecodeError:
                            # JSON解析失败，继续累积
                            pass

            i += 1

        return None

    def _reset_state(self):
        """重置解析状态"""
        self.json_start = -1
        self.depth = 0
        self.in_string = False
        self.escape = False

    def get_remaining(self) -> str:
        """获取当前buffer中的剩余内容"""
        return self.buffer

    def reset(self):
        """完全重置组装器状态"""
        self.buffer = ""
        self._reset_state()


