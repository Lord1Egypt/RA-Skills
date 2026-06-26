"""
API配置适配器 - 支持多平台LLM服务
"""

import os
from typing import Optional, Dict, Any


class APIAdapter:
    """多平台API适配器"""

    SUPPORTED_PROVIDERS = {
        "dashscope": {
            "name": "DashScope (阿里云)",
            "env_key": "DASHSCOPE_API_KEY",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "models": ["qwen-turbo", "qwen-plus", "qwen-max"]
        },
        "openai": {
            "name": "OpenAI",
            "env_key": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "models": ["gpt-3.5-turbo", "gpt-4"]
        },
        "deepseek": {
            "name": "DeepSeek",
            "env_key": "DEEPSEEK_API_KEY",
            "base_url": "https://api.deepseek.com/v1",
            "models": ["deepseek-chat", "deepseek-coder"]
        },
        "zhipu": {
            "name": "智谱AI",
            "env_key": "ZHIPU_API_KEY",
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "models": ["glm-4", "glm-4-flash"]
        },
        "moonshot": {
            "name": "Moonshot (月之暗面)",
            "env_key": "MOONSHOT_API_KEY",
            "base_url": "https://api.moonshot.cn/v1",
            "models": ["moonshot-v1-8k", "moonshot-v1-32k"]
        },
        "local": {
            "name": "本地模型 (Ollama)",
            "env_key": None,
            "base_url": "http://localhost:11434",
            "models": ["qwen2.5:0.5b", "llama3"]
        }
    }

    def __init__(self, provider: str = "dashscope", api_key: Optional[str] = None):
        """
        初始化API适配器

        Args:
            provider: 服务提供商名称
            api_key: API密钥（可选，默认从环境变量读取）
        """
        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"不支持的提供商: {provider}。支持: {list(self.SUPPORTED_PROVIDERS.keys())}")

        self.provider = provider
        self.config = self.SUPPORTED_PROVIDERS[provider]

        # API密钥优先级：参数 > 环境变量
        self.api_key = api_key
        if not self.api_key and self.config["env_key"]:
            self.api_key = os.environ.get(self.config["env_key"])

    @property
    def base_url(self) -> str:
        """获取API基础URL"""
        return self.config["base_url"]

    @property
    def available_models(self) -> list:
        """获取可用模型列表"""
        return self.config["models"]

    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def __repr__(self) -> str:
        return f"APIAdapter(provider='{self.provider}', name='{self.config['name']}')"


# 使用示例
if __name__ == "__main__":
    # 使用 DashScope
    adapter = APIAdapter("dashscope")
    print(adapter)

    # 使用本地模型（无需API Key）
    local = APIAdapter("local")
    print(local)

    # 自定义API Key
    custom = APIAdapter("openai", api_key="your-key-here")
    print(custom)