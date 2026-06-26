#!/usr/bin/env python3
"""
人物画像加载器
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict

PERSONAS_DIR = Path(__file__).parent.parent / "references"

# 别名映射
ALIASES = {
    "孔子": "kongzi",
    "孔丘": "kongzi",
    "仲尼": "kongzi",
    "至圣": "kongzi",
    "诗仙": "libai",
    "太白": "libai",
    "青莲": "libai",
    "李白": "libai",
    "东坡": "sushi",
    "苏轼": "sushi",
    "子瞻": "sushi",
    "东坡居士": "sushi",
    "卧龙": "zhugeliang",
    "诸葛亮": "zhugeliang",
    "孔明": "zhugeliang",
    "李清照": "liqingzhao",
    "易安": "liqingzhao",
    "清照": "liqingzhao",
    "千古第一才女": "liqingzhao",
    "张骞": "zhangqian",
    "博望侯": "zhangqian",
}


class CharacterLoader:
    
    def __init__(self):
        self.personas = {}
        self._load_all()
    
    def _load_all(self):
        """加载所有人物画像"""
        if not PERSONAS_DIR.exists():
            return
        
        for file_path in PERSONAS_DIR.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                persona = json.load(f)
                self.personas[persona['id']] = persona
    
    def load_character(self, identifier: str) -> Optional[dict]:
        """加载指定人物
        
        Args:
            identifier: 人物ID、姓名或别名
        
        Returns:
            人物画像字典，若未找到返回None
        """
        # 直接ID匹配
        if identifier in self.personas:
            return self.personas[identifier]
        
        # 别名匹配
        if identifier in ALIASES:
            alias_id = ALIASES[identifier]
            return self.personas.get(alias_id)
        
        # 姓名模糊匹配
        for pid, persona in self.personas.items():
            if persona['name'] == identifier:
                return persona
        
        return None
    
    def list_characters(self) -> list:
        """列出所有可用人物"""
        return list(self.personas.keys())
    
    def get_all_personas(self) -> dict:
        """获取所有人物画像"""
        return self.personas
    
    def save_persona(self, persona: Dict) -> bool:
        """保存人物画像到文件
        
        Args:
            persona: 人物画像字典
        
        Returns:
            是否保存成功
        """
        persona_id = persona['id']
        file_path = PERSONAS_DIR / f"{persona_id}.json"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(persona, f, ensure_ascii=False, indent=2)
            self.personas[persona_id] = persona
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    def _resolve_character_name(self, name: str) -> Optional[str]:
        """从姓名/别名解析出人物 ID
        
        Args:
            name: 人物姓名、别名或ID
        
        Returns:
            人物ID，若未找到返回None
        """
        if not name:
            return None
        
        # 清理输入
        name = name.strip()
        
        # 直接ID匹配
        if name in self.personas:
            return name
        
        # 别名匹配
        if name in ALIASES:
            return ALIASES[name]
        
        # 姓名模糊匹配
        for pid, persona in self.personas.items():
            if persona['name'] == name:
                return pid
        
        # 姓名包含匹配（处理别称）
        for pid, persona in self.personas.items():
            if name in persona['name'] or persona['name'] in name:
                return pid
        
        # 标题包含匹配
        for pid, persona in self.personas.items():
            if name in persona.get('title', ''):
                return pid
        
        return None
