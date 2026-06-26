#!/usr/bin/env python3
"""
提取记忆内容 - 智能识别对话中的重要内容
"""

import re
from typing import List, Dict, Any

class MemoryExtractor:
    """记忆提取器"""
    
    def __init__(self):
        self.patterns = {
            'decision': [
                r'决定(?:用|选|是)?(.+)',
                r'我们决定(.+)',
                r'就这么定了[：:]\s*(.+)',
                r'最终方案[是：]\s*(.+)',
            ],
            'todo': [
                r'@(\w+)\s+(.+?)(?:截止|之前|前)?\s*(\S+)',
                r'(\w+)\s+要?\s*做(.+?)(?:截止|之前|前)?\s*(\S+)',
                r'任务[：:]\s*(.+)',
                r'待办[：:]\s*(.+)',
            ],
            'appointment': [
                r'(\S+)\s*(?:下午|上午|晚上)?\s*(\d+)[点时]\s*(\S+)',
                r'(\S+)\s*见面',
                r'(\S+)\s*开会',
                r'约定[：:]\s*(.+)',
            ],
            'fact': [
                r'预算[是：]\s*(\d+)\s*(\S+)',
                r'(\S+)\s*是\s*(\S+)',
                r'重要信息[：:]\s*(.+)',
            ],
            'preference': [
                r'我喜欢\s*(.+)',
                r'我偏好\s*(.+)',
                r'我习惯\s*(.+)',
                r'我不用\s*(.+)',
            ],
            'project': [
                r'新项目\s*(.+)',
                r'项目启动\s*(.+)',
                r'里程碑[：:]\s*(.+)',
            ]
        }
    
    def extract(self, conversation: str) -> Dict[str, List[str]]:
        """
        从对话中提取记忆内容
        
        Args:
            conversation: 对话文本
            
        Returns:
            提取的记忆字典
        """
        memories = {
            'decisions': [],
            'todos': [],
            'appointments': [],
            'facts': [],
            'preferences': [],
            'projects': []
        }
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, conversation)
                if matches:
                    key = category + 's' if not category.endswith('s') else category
                    if key in memories:
                        memories[key].extend(matches)
        
        return memories
    
    def extract_from_user_reminder(self, user_message: str) -> Dict[str, Any]:
        """
        从用户提醒中提取（"你忘了吗"等）
        
        Args:
            user_message: 用户消息
            
        Returns:
            提取结果
        """
        is_reminder = any(keyword in user_message 
                          for keyword in ['忘了', '不记得', '记性太差', '怎么不记得'])
        
        return {
            'is_reminder': is_reminder,
            'needs_update': is_reminder,
            'apology': "抱歉，让我检查一下..." if is_reminder else ""
        }

if __name__ == "__main__":
    extractor = MemoryExtractor()
    
    test_conversation = """
    用户：我们决定下周三下午3点开会！
    用户：预算是 10 万
    用户：@小明 周五前完成报告
    用户：我喜欢用飞书
    """
    
    memories = extractor.extract(test_conversation)
    print("提取的记忆：")
    print(memories)
