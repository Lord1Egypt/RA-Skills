#!/usr/bin/env python3
"""
生成记忆摘要 - 将提取的内容生成可读性强的摘要
"""

from typing import Dict, List, Any
from datetime import datetime

class SummaryGenerator:
    """摘要生成器"""
    
    def __init__(self):
        self.date = datetime.now().strftime('%Y-%m-%d')
    
    def generate(self, memories: Dict[str, List[str]]) -> str:
        """
        生成摘要
        
        Args:
            memories: 提取的记忆字典
            
        Returns:
            摘要文本
        """
        sections = []
        
        # 标题
        sections.append(f"# {self.date} 记忆")
        sections.append("")
        sections.append("## 今日事项")
        sections.append("")
        
        # 决策
        if memories.get('decisions'):
            sections.append("### 重要决策")
            for decision in memories['decisions']:
                sections.append(f"- **决策：** {decision}")
            sections.append("")
        
        # 待办
        if memories.get('todos'):
            sections.append("### 待办事项")
            for todo in memories['todos']:
                if isinstance(todo, tuple) and len(todo) >= 2:
                    sections.append(f"- [ ] {todo[1]} - {todo[0]} - {todo[2] if len(todo) > 2 else ''}")
                else:
                    sections.append(f"- [ ] {todo}")
            sections.append("")
        
        # 约定
        if memories.get('appointments'):
            sections.append("### 约定/会议")
            for appointment in memories['appointments']:
                sections.append(f"- **约定：** {appointment}")
            sections.append("")
        
        # 事实
        if memories.get('facts'):
            sections.append("### 重要信息")
            for fact in memories['facts']:
                sections.append(f"- **事实：** {fact}")
            sections.append("")
        
        # 偏好
        if memories.get('preferences'):
            sections.append("### 用户偏好")
            for preference in memories['preferences']:
                sections.append(f"- **偏好：** {preference}")
            sections.append("")
        
        # 项目
        if memories.get('projects'):
            sections.append("### 项目进展")
            for project in memories['projects']:
                sections.append(f"- **项目：** {project}")
            sections.append("")
        
        # 如果没有内容，添加提示
        if len(sections) <= 4:
            sections.append("（今天没有提取到重要内容）")
            sections.append("")
        
        # 记录时间
        sections.append("---")
        sections.append(f"记录时间：{self.date}")
        
        return "\n".join(sections)
    
    def generate_quick_check(self, memories: Dict[str, List[str]]) -> str:
        """
        生成快速确认版本（用于让用户确认）
        
        Args:
            memories: 提取的记忆字典
            
        Returns:
            快速确认文本
        """
        total = sum(len(v) for v in memories.values() if v)
        
        if total == 0:
            return "今天没有提取到重要内容，需要我手动添加吗？"
        
        parts = []
        if memories.get('decisions'):
            parts.append(f"{len(memories['decisions'])}个决策")
        if memories.get('todos'):
            parts.append(f"{len(memories['todos'])}个待办")
        if memories.get('appointments'):
            parts.append(f"{len(memories['appointments'])}个约定")
        
        summary = "、".join(parts)
        return f"这是今天的重要内容：{summary}，对吗？"

if __name__ == "__main__":
    generator = SummaryGenerator()
    
    test_memories = {
        'decisions': ['用方案 A', '下周三开会'],
        'todos': [('小明', '完成报告', '周五')],
        'appointments': ['周三下午3点'],
        'facts': ['预算 10 万'],
        'preferences': ['喜欢用飞书'],
        'projects': ['新项目启动']
    }
    
    summary = generator.generate(test_memories)
    print("完整摘要：")
    print(summary)
    print("\n" + "="*50 + "\n")
    
    quick_check = generator.generate_quick_check(test_memories)
    print("快速确认：")
    print(quick_check)
