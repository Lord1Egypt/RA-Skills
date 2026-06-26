"""
AI 服务配置
支持多种 AI 提供商
"""

import os
from enum import Enum

class AIProvider(Enum):
    MINIMAX = "minimax"
    OPENAI = "openai"
    ZHIPU = "zhipu"
    SILICONFLOW = "siliconflow"
    SILENCE = "silence"  # 仅规则响应，无AI

class AIConfig:
    def __init__(self):
        self.provider = os.getenv('AI_PROVIDER', 'silence')
        self.api_key = os.getenv('AI_API_KEY', '')
        self.model = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
        self.base_url = os.getenv('AI_BASE_URL', '')

    def get_provider(self) -> AIProvider:
        try:
            return AIProvider(self.provider.lower())
        except:
            return AIProvider.SILENCE

    def is_configured(self) -> bool:
        provider = self.get_provider()
        if provider == AIProvider.SILENCE:
            return True
        return bool(self.api_key)

    def get_system_prompt(self) -> str:
        return """你是 MyStock 的专业股票助手，专注于帮助用户管理持仓、分析股票。

能力：
1. 查询股票实时价格和涨跌情况
2. 分析持仓和观察列表
3. 提供投资参考建议（仅供参考，不构成投资建议）

注意事项：
- 回答要专业、准确
- 如果不确定，请明确说明
- 投资有风险，决策需谨慎"""

AI_CONFIG = AIConfig()
