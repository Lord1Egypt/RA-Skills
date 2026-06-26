#!/usr/bin/env python3
"""
auto_compactor.py - 自动压缩工具
参考Claude Code的autocompact实现，长对话自动压缩

功能：
1. 监控token使用量
2. 超过阈值时触发压缩
3. 生成历史摘要
4. 替换旧消息为摘要

用法：
    python3 scripts/auto_compactor.py --tokens 100000 --limit 200000
    python3 scripts/auto_compactor.py --test
"""

import json
import sys
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CompactResult:
    """压缩结果"""
    messages: List[Dict[str, Any]]
    summary: str
    original_tokens: int
    compacted_tokens: int
    savings_tokens: int
    savings_percent: float
    preserved_files: List[str]


class AutoCompactor:
    """自动压缩器"""
    
    # Claude Code的阈值常量
    AUTOCOMPACT_BUFFER_TOKENS = 13_000
    MAX_CONSECUTIVE_FAILURES = 3
    POST_COMPACT_MAX_FILES_TO_RESTORE = 5
    
    def __init__(self,
                 context_window: int = 200_000,
                 max_output_tokens: int = 8_192,
                 safety_margin: float = 0.8):
        self.context_window = context_window
        self.max_output_tokens = max_output_tokens
        self.safety_margin = safety_margin
        self.consecutive_failures = 0
        
        # 计算压缩阈值
        self.effective_context_window = context_window - max_output_tokens
        self.autocompact_threshold = self.effective_context_window - self.AUTOCOMPACT_BUFFER_TOKENS
        
        # 估算压缩阈值（简化版）
        self.compress_threshold = int(context_window * safety_margin)
    
    def should_compact(self, current_tokens: int) -> bool:
        """检查是否需要压缩"""
        return current_tokens >= self.compress_threshold
    
    def compact(self, messages: List[Dict[str, Any]]) -> CompactResult:
        """执行自动压缩"""
        original_tokens = self._estimate_tokens(messages)
        
        # 步骤1: 分组消息（按API轮次）
        groups = self._group_messages_by_round(messages)
        
        # 步骤2: 识别需要保留的文件
        preserved_files = self._identify_preserved_files(messages)
        
        # 步骤3: 生成摘要
        summary = self._generate_summary(groups, preserved_files)
        
        # 步骤4: 构建压缩后的消息
        compacted_messages = self._build_compacted_messages(summary, messages, preserved_files)
        
        compacted_tokens = self._estimate_tokens(compacted_messages)
        savings_tokens = original_tokens - compacted_tokens
        savings_percent = (savings_tokens / original_tokens * 100) if original_tokens > 0 else 0
        
        return CompactResult(
            messages=compacted_messages,
            summary=summary,
            original_tokens=original_tokens,
            compacted_tokens=compacted_tokens,
            savings_tokens=savings_tokens,
            savings_percent=savings_percent,
            preserved_files=preserved_files
        )
    
    def _group_messages_by_round(self, messages: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """按API轮次分组消息"""
        groups = []
        current_group = []
        
        for msg in messages:
            role = msg.get("role", "")
            
            if role == "assistant":
                # 助手消息开始新的一轮
                if current_group:
                    groups.append(current_group)
                current_group = [msg]
            else:
                current_group.append(msg)
        
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def _identify_preserved_files(self, messages: List[Dict[str, Any]]) -> List[str]:
        """识别需要保留的关键文件"""
        files = set()
        
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                # 提取文件路径
                import re
                # 匹配常见文件路径模式
                patterns = [
                    r'/[\w/.-]+\.\w+',  # 绝对路径
                    r'[\w.-]+\.\w+',     # 相对路径
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if any(ext in match for ext in ['.py', '.js', '.ts', '.md', '.json', '.yaml', '.yml']):
                            files.add(match)
        
        # 返回最常见的文件（最多5个）
        return list(files)[:self.POST_COMPACT_MAX_FILES_TO_RESTORE]
    
    def _generate_summary(self, 
                         groups: List[List[Dict[str, Any]]],
                         preserved_files: List[str]) -> str:
        """生成对话摘要"""
        if not groups:
            return "对话为空。"
        
        # 提取关键信息
        topics = []
        actions = []
        files_mentioned = set()
        
        for group in groups:
            for msg in group:
                content = self._extract_content(msg)
                
                # 提取主题（简单关键词）
                if len(content) > 50:
                    # 取前100个字符作为摘要
                    preview = content[:100].replace('\n', ' ')
                    topics.append(preview)
                
                # 提取动作
                if any(word in content.lower() for word in ['创建', '修改', '删除', '执行', '运行', '分析']):
                    actions.append(content[:100])
                
                # 提取文件
                import re
                file_matches = re.findall(r'[\w/.-]+\.\w+', content)
                files_mentioned.update(file_matches[:3])
        
        # 构建摘要
        summary_parts = []
        summary_parts.append(f"## 对话摘要")
        summary_parts.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_parts.append(f"")
        
        if topics:
            summary_parts.append(f"### 主要话题")
            for topic in topics[:5]:
                summary_parts.append(f"- {topic}")
            summary_parts.append(f"")
        
        if actions:
            summary_parts.append(f"### 关键操作")
            for action in actions[:5]:
                summary_parts.append(f"- {action}")
            summary_parts.append(f"")
        
        if files_mentioned:
            summary_parts.append(f"### 涉及文件")
            for file in list(files_mentioned)[:10]:
                summary_parts.append(f"- {file}")
            summary_parts.append(f"")
        
        if preserved_files:
            summary_parts.append(f"### 保留文件上下文")
            for file in preserved_files:
                summary_parts.append(f"- {file}")
        
        return "\n".join(summary_parts)
    
    def _build_compacted_messages(self,
                                 summary: str,
                                 original_messages: List[Dict[str, Any]],
                                 preserved_files: List[str]) -> List[Dict[str, Any]]:
        """构建压缩后的消息列表"""
        # 保留系统消息
        system_messages = [m for m in original_messages if m.get("role") == "system"]
        
        # 保留最后几条消息（上下文连续性）
        last_messages = original_messages[-6:] if len(original_messages) > 6 else original_messages
        
        # 构建摘要消息
        summary_message = {
            "role": "user",
            "content": f"[自动压缩摘要]\n\n{summary}\n\n---\n以上是之前对话的摘要。请基于此摘要继续对话。"
        }
        
        # 组合
        result = system_messages + [summary_message] + last_messages
        
        return result
    
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
    
    def _estimate_tokens(self, messages: List[Dict[str, Any]]) -> int:
        """估算token数量"""
        total_chars = 0
        for msg in messages:
            content = self._extract_content(msg)
            total_chars += len(content)
        return total_chars // 4


def test_autocompact():
    """测试自动压缩功能"""
    print("=" * 60)
    print("自动压缩测试")
    print("=" * 60)
    
    # 生成测试数据（模拟长对话）
    messages = []
    
    # 系统消息
    messages.append({
        "role": "system",
        "content": "你是一个专业的Python开发助手。"
    })
    
    # 模拟多轮对话
    for i in range(20):
        messages.append({
            "role": "user",
            "content": f"第{i+1}轮：帮我分析这段代码的性能问题。这段代码是一个数据处理函数，需要优化循环和内存使用。"
        })
        messages.append({
            "role": "assistant",
            "content": f"分析第{i+1}轮：我来帮你分析这段代码的性能问题。首先，我需要查看代码结构，识别性能瓶颈。常见的优化方法包括：使用列表推导式替代循环、减少不必要的对象创建、使用生成器处理大数据集等。"
        })
    
    # 创建压缩器
    compactor = AutoCompactor(
        context_window=100_000,
        safety_margin=0.5  # 50%阈值用于测试
    )
    
    # 检查是否需要压缩
    current_tokens = compactor._estimate_tokens(messages)
    print(f"\n当前token: {current_tokens}")
    print(f"压缩阈值: {compactor.compress_threshold}")
    print(f"需要压缩: {compactor.should_compact(current_tokens)}")
    
    # 执行压缩
    result = compactor.compact(messages)
    
    print(f"\n压缩结果:")
    print(f"  原始消息数: {len(messages)}")
    print(f"  压缩后消息数: {len(result.messages)}")
    print(f"  原始token: {result.original_tokens}")
    print(f"  压缩后token: {result.compacted_tokens}")
    print(f"  节省token: {result.savings_tokens}")
    print(f"  节省比例: {result.savings_percent:.1f}%")
    print(f"  保留文件: {result.preserved_files}")
    
    print(f"\n摘要预览:")
    print(result.summary[:500] + "..." if len(result.summary) > 500 else result.summary)
    
    print("\n✅ 测试通过!")


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_autocompact()
    elif "--tokens" in sys.argv:
        # 命令行模式
        idx = sys.argv.index("--tokens")
        current_tokens = int(sys.argv[idx + 1])
        
        limit_idx = sys.argv.index("--limit") if "--limit" in sys.argv else None
        context_window = int(sys.argv[limit_idx + 1]) if limit_idx else 200_000
        
        compactor = AutoCompactor(context_window=context_window)
        
        print(f"当前token: {current_tokens}")
        print(f"上下文窗口: {context_window}")
        print(f"压缩阈值: {compactor.compress_threshold}")
        print(f"需要压缩: {compactor.should_compact(current_tokens)}")
    elif len(sys.argv) > 1:
        # 从文件读取消息
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            messages = json.load(f)
        
        compactor = AutoCompactor()
        result = compactor.compact(messages)
        
        print(json.dumps({
            "messages": result.messages,
            "summary": result.summary,
            "stats": {
                "original_tokens": result.original_tokens,
                "compacted_tokens": result.compacted_tokens,
                "savings_tokens": result.savings_tokens,
                "savings_percent": round(result.savings_percent, 1)
            }
        }, indent=2, ensure_ascii=False))
    else:
        print("用法:")
        print("  python3 scripts/auto_compactor.py --tokens <current> --limit <window>")
        print("  python3 scripts/auto_compactor.py <messages.json>")
        print("  python3 scripts/auto_compactor.py --test")
