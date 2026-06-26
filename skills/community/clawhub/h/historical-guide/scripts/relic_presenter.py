#!/usr/bin/env python3
"""
文物讲解生成器
结合历史人物性格，生成符合角色风格的文物讲解
"""

import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from api_config import load_api_config
from utils import build_system_prompt


class RelicPresenter:
    """文物讲解呈现器"""
    
    def __init__(self, persona: dict):
        self.persona = persona
        self.name = persona['name']
        self.style = persona['speaking_style']
    
    def get_greeting(self) -> str:
        """获取人物问候语"""
        return self.persona.get('greeting', f'在下{self.name}，幸会。')
    
    def get_self_introduction(self) -> str:
        """获取人物自我介绍"""
        return self.persona.get('self_intro', f'吾乃{self.name}。')
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return build_system_prompt(self.persona, mode="explanation")
    
    def _build_user_prompt(self, relic_name: str) -> str:
        """构建用户提示词"""
        return f"""请以{self.name}的身份，为我讲解这件文物：

文物名称：{relic_name}

请用{self.name}的口吻进行讲解。"""
    
    def explain_relic(self, relic_name: str) -> str:
        """生成文物讲解"""
        config = load_api_config()
        try:
            return self._generate_with_api(relic_name, config)
        except Exception as e:
            return f"抱歉，当前API调用失败，请稍后再试。"
    
    def _generate_with_api(self, relic_name: str, config: dict) -> str:
        """使用API生成讲解"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['api_key']}"
        }
        
        payload = {
            "model": config['model'],
            "messages": [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": self._build_user_prompt(relic_name)}
            ],
            "temperature": 0.8,
            "max_tokens": 1000
        }
        
        response = requests.post(
            config['api_base'],
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
