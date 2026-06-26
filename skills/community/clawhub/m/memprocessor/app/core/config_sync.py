"""配置同步器 - 通用版本

支持从配置文件读取人格配置，适用于各种部署场景。
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any

from app.core.persona import (
    PersonaProfile, ValueSystem, PersonalityDimension,
    GeneratePersonaRequest
)
from app.services.persona_service import PersonaService


class ConfigSync:
    """通用配置同步器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置同步器
        
        Args:
            config_path: 配置文件路径，可以是:
                - JSON 文件 (.json)
                - YAML 文件 (.yaml/.yml)
                - 包含配置文件的目录
        """
        self.config_path = Path(config_path) if config_path else None
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path or not self.config_path.exists():
            return self._default_config()
        
        # 根据文件类型加载
        if self.config_path.suffix == '.json':
            return json.loads(self.config_path.read_text())
        elif self.config_path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(self.config_path.read_text())
        else:
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """默认配置 - 通用人格模板"""
        return {
            "name": "AI Assistant",
            "base_seed": "好奇、友善、善于解决问题",
            "dimensions": {
                "openness": 70,
                "conscientiousness": 75,
                "extraversion": 60,
                "agreeableness": 80,
                "neuroticism": 40,
                "curiosity": 85,
                "empathy": 75,
                "assertiveness": 65,
                "humor": 60,
                "creativity": 70
            },
            "values": ["helpfulness", "honesty", "respect"],
            "consistency_rules": [
                "保持真诚和友善",
                "尊重用户隐私",
                "承认不确定性"
            ]
        }
    
    def generate_persona_request(self) -> GeneratePersonaRequest:
        """从配置生成人格创建请求"""
        config = self.load_config()
        
        return GeneratePersonaRequest(
            base_seed=config.get("base_seed", "好奇、友善、善于解决问题"),
            user_preferences={
                "name": config.get("name", "AI Assistant"),
                "traits": config.get("dimensions", {}),
                "values": config.get("values", [])
            },
            constraints=config.get("consistency_rules", [])
        )
    
    async def sync_to_persona_service(self, persona_service: PersonaService) -> Optional[PersonaProfile]:
        """同步配置到人格服务"""
        request = self.generate_persona_request()
        
        response = await persona_service.generate_persona(request)
        
        if response.success and response.persona:
            print(f"[ConfigSync] Persona '{response.persona.name}' created successfully")
            return response.persona
        else:
            print(f"[ConfigSync] Failed to create persona")
            return None


# 便捷函数
async def initialize_persona_from_config(
    persona_service: PersonaService,
    config_path: Optional[str] = None
) -> Optional[PersonaProfile]:
    """
    从配置文件初始化人格
    
    在 MemoryProcessor 启动时调用
    
    Args:
        persona_service: 人格服务实例
        config_path: 配置文件路径，如果不提供则使用默认配置
    
    Returns:
        创建的人格档案，或 None
    """
    sync = ConfigSync(config_path)
    return await sync.sync_to_persona_service(persona_service)
