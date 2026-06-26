#!/usr/bin/env python3
"""
会话状态管理器
维护历史人物伴游的会话状态，支持交互式会话模式
"""

import json
import re
from pathlib import Path
from typing import Optional, Dict
import sys
sys.path.insert(0, str(Path(__file__).parent))
from character_loader import CharacterLoader


class SessionManager:
    """历史人物伴游会话管理器"""
    
    def __init__(self):
        self.loader = CharacterLoader()
        self.current_character_id: Optional[str] = None
        self.current_persona: Optional[dict] = None
        self.conversation_history: list = []  # 对话历史
        self.current_relic: Optional[str] = None  # 当前讨论的文物（可选，用于上下文）
    
    def activate_character(self, character_id: str) -> bool:
        """激活历史人物
        
        Args:
            character_id: 人物 ID
        
        Returns:
            是否激活成功
        """
        persona = self.loader.load_character(character_id)
        if not persona:
            return False
        
        self.current_character_id = character_id
        self.current_persona = persona
        self.conversation_history = []  # 清空历史
        return True
    
    def switch_character(self, character_id: str) -> bool:
        """切换历史人物（自动调用生成器）"""
        # 先尝试从库中加载
        persona = self.loader.load_character(character_id)
        
        if not persona:
            # 尝试动态生成
            import subprocess
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "persona_generator.py"), character_id],
                capture_output=True
            )
            if result.returncode != 0:
                return False
            
            # 重新加载所有人物画像
            self.loader._load_all()
            
            # 尝试用原始输入加载
            persona = self.loader.load_character(character_id)
            
            # 如果失败，尝试通过姓名匹配加载
            if not persona:
                for pid, p in self.loader.get_all_personas().items():
                    if p['name'] == character_id:
                        persona = p
                        character_id = pid
                        break
            
            # 如果仍然失败，尝试遍历所有人物找到刚生成的
            if not persona:
                for pid, p in self.loader.get_all_personas().items():
                    # 检查是否包含输入的关键词
                    if character_id in p['name'] or character_id in p.get('title', ''):
                        persona = p
                        character_id = pid
                        break
            
            if not persona:
                return False
        
        self.current_character_id = character_id
        self.current_persona = persona
        self.conversation_history = []  # 清空历史
        return True
    
    def is_active(self) -> bool:
        """检查是否已激活人物"""
        return self.current_character_id is not None and self.current_persona is not None
    
    def update_relic(self, relic: str):
        """更新当前讨论的文物（可选，用于上下文提示）"""
        self.current_relic = relic
    
    def add_to_history(self, role: str, content: str):
        """添加到对话历史"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_persona_summary(self) -> str:
        """获取人物画像摘要（用于构建 prompt）"""
        if not self.is_active():
            return ""
        
        p = self.current_persona
        return f"""你是{p['name']}（{p['title']}），{p['era']}时期人物。
性格特点：{', '.join(p['personality']['traits'])}
核心价值观：{', '.join(p['personality']['values'])}
说话风格：{p['speaking_style']['tone']}
常用词汇：{', '.join(p['speaking_style']['vocabulary'])}
代表作品：{', '.join(p.get('famous_works', [])[:3])}"""
    
    def get_welcome_message(self) -> str:
        """获取激活人物后的欢迎消息"""
        if not self.is_active():
            return ""
        
        persona = self.current_persona
        greeting = persona.get('greeting', f'在下{persona["name"]}，幸会。')
        return f"🎭 召唤历史人物: {persona['name']} ({persona['title']})\n{greeting}"
    
    def clear(self):
        """清除会话状态"""
        self.current_character_id = None
        self.current_persona = None
        self.current_relic = None
        self.conversation_history = []


def create_session_manager() -> SessionManager:
    """工厂函数：创建会话管理器"""
    return SessionManager()