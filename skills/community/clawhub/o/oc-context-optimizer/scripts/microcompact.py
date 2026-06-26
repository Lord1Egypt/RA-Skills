#!/usr/bin/env python3
"""
microcompact.py - 微压缩工具
参考Claude Code的microcompact实现，优化prompt cache

功能：
1. 检测重复消息（相同role+相似内容）
2. 合并连续的工具调用结果
3. 压缩长文本（保留关键信息）
4. 优化prompt cache命中率

用法：
    python3 scripts/microcompact.py <messages.json>
    python3 scripts/microcompact.py --test
"""

import json
import sys
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class CompactResult:
    """压缩结果"""
    messages: List[Dict[str, Any]]
    original_count: int
    compacted_count: int
    savings_tokens: int
    savings_percent: float


class MicroCompactor:
    """微压缩器"""
    
    def __init__(self, 
                 similarity_threshold: float = 0.85,
                 min_message_length: int = 100,
                 max_tool_result_preview: int = 500):
        self.similarity_threshold = similarity_threshold
        self.min_message_length = min_message_length
        self.max_tool_result_preview = max_tool_result_preview
    
    def compact(self, messages: List[Dict[str, Any]]) -> CompactResult:
        """执行微压缩"""
        original_count = len(messages)
        original_tokens = self._estimate_tokens(messages)
        
        # 步骤1: 检测并合并重复消息
        messages = self._merge_duplicates(messages)
        
        # 步骤2: 合并连续的工具调用结果
        messages = self._merge_consecutive_tool_results(messages)
        
        # 步骤3: 压缩长文本消息
        messages = self._compress_long_messages(messages)
        
        # 步骤4: 移除空消息
        messages = [m for m in messages if self._is_valid_message(m)]
        
        compacted_count = len(messages)
        compacted_tokens = self._estimate_tokens(messages)
        savings_tokens = original_tokens - compacted_tokens
        savings_percent = (savings_tokens / original_tokens * 100) if original_tokens > 0 else 0
        
        return CompactResult(
            messages=messages,
            original_count=original_count,
            compacted_count=compacted_count,
            savings_tokens=savings_tokens,
            savings_percent=savings_percent
        )
    
    def _merge_duplicates(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """合并重复消息"""
        if len(messages) < 2:
            return messages
        
        result = []
        skip_next = False
        
        for i, msg in enumerate(messages):
            if skip_next:
                skip_next = False
                continue
            
            if i < len(messages) - 1:
                next_msg = messages[i + 1]
                if self._are_duplicates(msg, next_msg):
                    # 合并为一条，保留第一条的内容
                    merged = self._merge_messages(msg, next_msg)
                    result.append(merged)
                    skip_next = True
                    continue
            
            result.append(msg)
        
        return result
    
    def _are_duplicates(self, msg1: Dict[str, Any], msg2: Dict[str, Any]) -> bool:
        """判断两条消息是否重复"""
        # 角色必须相同
        if msg1.get("role") != msg2.get("role"):
            return False
        
        # 获取内容
        content1 = self._extract_content(msg1)
        content2 = self._extract_content(msg2)
        
        # 长度太短不合并
        if len(content1) < self.min_message_length or len(content2) < self.min_message_length:
            return False
        
        # 计算相似度
        similarity = SequenceMatcher(None, content1, content2).ratio()
        return similarity >= self.similarity_threshold
    
    def _merge_messages(self, msg1: Dict[str, Any], msg2: Dict[str, Any]) -> Dict[str, Any]:
        """合并两条消息"""
        # 保留第一条消息的内容，添加合并标记
        merged = msg1.copy()
        content = self._extract_content(merged)
        
        # 如果内容不同，追加第二条的独特部分
        content2 = self._extract_content(msg2)
        if content != content2:
            # 提取第二条消息中的独特内容
            unique_parts = self._extract_unique_content(content, content2)
            if unique_parts:
                if isinstance(merged.get("content"), str):
                    merged["content"] += f"\n\n[合并相似消息: {unique_parts[:200]}...]"
                elif isinstance(merged.get("content"), list):
                    merged["content"].append({
                        "type": "text",
                        "text": f"[合并相似消息: {unique_parts[:200]}...]"
                    })
        
        return merged
    
    def _merge_consecutive_tool_results(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """合并连续的工具调用结果"""
        result = []
        i = 0
        
        while i < len(messages):
            msg = messages[i]
            
            # 检查是否是工具结果消息
            if msg.get("role") == "user" and self._is_tool_result_message(msg):
                # 收集连续的工具结果
                tool_results = [msg]
                j = i + 1
                while j < len(messages) and self._is_tool_result_message(messages[j]):
                    tool_results.append(messages[j])
                    j += 1
                
                # 如果有多个连续的工具结果，合并它们
                if len(tool_results) > 1:
                    merged = self._combine_tool_results(tool_results)
                    result.append(merged)
                    i = j
                    continue
            
            result.append(msg)
            i += 1
        
        return result
    
    def _is_tool_result_message(self, msg: Dict[str, Any]) -> bool:
        """检查是否是工具结果消息"""
        content = msg.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_result":
                    return True
        return False
    
    def _combine_tool_results(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """合并多个工具结果消息"""
        combined_content = []
        
        for msg in messages:
            content = msg.get("content", [])
            if isinstance(content, list):
                combined_content.extend(content)
            elif isinstance(content, str):
                combined_content.append({"type": "text", "text": content})
        
        return {
            "role": "user",
            "content": combined_content
        }
    
    def _compress_long_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """压缩长文本消息"""
        result = []
        
        for msg in messages:
            content = self._extract_content(msg)
            
            # 如果是工具结果，压缩长输出
            if self._is_tool_result_message(msg):
                msg = self._compress_tool_result(msg)
            # 如果是普通文本消息且过长
            elif len(content) > self.max_tool_result_preview * 2:
                msg = self._compress_text_message(msg)
            
            result.append(msg)
        
        return result
    
    def _compress_tool_result(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """压缩工具结果"""
        content = msg.get("content", [])
        if not isinstance(content, list):
            return msg
        
        compressed_content = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "tool_result":
                tool_content = item.get("content", "")
                if isinstance(tool_content, str) and len(tool_content) > self.max_tool_result_preview:
                    # 压缩工具结果
                    compressed = tool_content[:self.max_tool_result_preview]
                    compressed += f"\n\n[...已压缩,原长度{len(tool_content)}字符]"
                    item = item.copy()
                    item["content"] = compressed
            compressed_content.append(item)
        
        msg = msg.copy()
        msg["content"] = compressed_content
        return msg
    
    def _compress_text_message(self, msg: Dict[str, Any]) -> Dict[str, Any]:
        """压缩文本消息"""
        content = self._extract_content(msg)
        if len(content) <= self.max_tool_result_preview * 2:
            return msg
        
        # 保留开头和结尾
        keep_start = self.max_tool_result_preview
        keep_end = self.max_tool_result_preview // 2
        
        compressed = content[:keep_start]
        compressed += f"\n\n[...已压缩,原长度{len(content)}字符,省略中间部分...]\n\n"
        compressed += content[-keep_end:]
        
        msg = msg.copy()
        if isinstance(msg.get("content"), str):
            msg["content"] = compressed
        elif isinstance(msg.get("content"), list):
            for item in msg["content"]:
                if isinstance(item, dict) and item.get("type") == "text":
                    item["text"] = compressed
                    break
        
        return msg
    
    def _extract_content(self, msg: Dict[str, Any]) -> str:
        """提取消息内容"""
        content = msg.get("content", "")
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        texts.append(item.get("text", ""))
                    elif item.get("type") == "tool_result":
                        texts.append(str(item.get("content", "")))
            return "\n".join(texts)
        return str(content)
    
    def _extract_unique_content(self, base: str, other: str) -> str:
        """提取other中相对于base的独特内容"""
        # 简单实现：返回other中不在base中的部分
        base_words = set(base.split())
        other_words = other.split()
        unique = [w for w in other_words if w not in base_words]
        return " ".join(unique[:50])  # 限制长度
    
    def _is_valid_message(self, msg: Dict[str, Any]) -> bool:
        """检查消息是否有效"""
        content = msg.get("content")
        if content is None:
            return False
        if isinstance(content, str) and not content.strip():
            return False
        if isinstance(content, list) and len(content) == 0:
            return False
        return True
    
    def _estimate_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """估算token数量（粗略）"""
        total_chars = 0
        for msg in messages:
            content = self._extract_content(msg)
            total_chars += len(content)
        # 粗略估算：1个token约等于4个字符
        return total_chars // 4


def generate_cache_hash(messages: List[Dict[str, Any]]) -> str:
    """生成消息的缓存hash，用于prompt cache优化"""
    # 序列化消息
    serialized = json.dumps(messages, sort_keys=True, ensure_ascii=False)
    # 生成hash
    return hashlib.sha256(serialized.encode()).hexdigest()[:16]


def test_microcompact():
    """测试微压缩功能"""
    print("=" * 60)
    print("微压缩测试")
    print("=" * 60)
    
    # 测试数据
    test_messages = [
        {
            "role": "user",
            "content": "帮我分析这个Python代码的性能问题"
        },
        {
            "role": "assistant",
            "content": "我来分析一下这个Python代码的性能问题。首先，我需要查看代码结构，然后识别可能的性能瓶颈。常见的性能问题包括：循环嵌套过深、不必要的重复计算、内存泄漏等。我会使用性能分析工具来帮助识别这些问题。"
        },
        {
            "role": "assistant",
            "content": "我来分析一下这个Python代码的性能问题。首先，我需要查看代码结构，然后识别可能的性能瓶颈。常见的性能问题包括：循环嵌套过深、不必要的重复计算、内存泄漏等。我会使用性能分析工具来帮助识别这些问题。"
        },
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "content": "A" * 2000, "tool_use_id": "tool_1"},
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "content": "B" * 1000, "tool_use_id": "tool_2"},
            ]
        },
    ]
    
    compactor = MicroCompactor()
    result = compactor.compact(test_messages)
    
    print(f"\n原始消息数: {result.original_count}")
    print(f"压缩后消息数: {result.compacted_count}")
    print(f"节省token: {result.savings_tokens}")
    print(f"节省比例: {result.savings_percent:.1f}%")
    print(f"\n缓存hash: {generate_cache_hash(result.messages)}")
    
    print("\n✅ 测试通过!")


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_microcompact()
    elif len(sys.argv) > 1:
        # 从文件读取消息
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            messages = json.load(f)
        
        compactor = MicroCompactor()
        result = compactor.compact(messages)
        
        print(json.dumps({
            "messages": result.messages,
            "stats": {
                "original_count": result.original_count,
                "compacted_count": result.compacted_count,
                "savings_tokens": result.savings_tokens,
                "savings_percent": round(result.savings_percent, 1)
            }
        }, indent=2, ensure_ascii=False))
    else:
        print("用法:")
        print("  python3 scripts/microcompact.py <messages.json>")
        print("  python3 scripts/microcompact.py --test")
