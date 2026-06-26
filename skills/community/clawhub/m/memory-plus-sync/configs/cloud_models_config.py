"""
云端模型配置

配置 Kimi、Qwen、GLM 等云端模型的 API 连接
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class CloudModelConfig:
    """云端模型配置"""
    
    # Kimi (Moonshot AI)
    kimi_api_key: str = ""
    kimi_base_url: str = "https://api.moonshot.cn/v1"
    kimi_model: str = "moonshot-v1-8k"
    
    # Qwen (阿里云百炼)
    qwen_api_key: str = ""
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    qwen_model: str = "qwen-plus"
    
    # GLM (智谱 AI)
    glm_api_key: str = ""
    glm_base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    glm_model: str = "glm-4"
    
    # DeepSeek
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    
    # 通用配置
    timeout: int = 120
    max_retries: int = 3
    temperature: float = 0.7


def get_cloud_config() -> CloudModelConfig:
    """
    从环境变量加载云端模型配置
    
    环境变量:
    - KIMI_API_KEY
    - QWEN_API_KEY
    - GLM_API_KEY (或 ZHIPU_API_KEY)
    - DEEPSEEK_API_KEY
    """
    
    config = CloudModelConfig()
    
    # Kimi
    config.kimi_api_key = os.getenv("KIMI_API_KEY", "")
    
    # Qwen
    config.qwen_api_key = os.getenv("QWEN_API_KEY", "")
    
    # GLM (支持两种环境变量名)
    config.glm_api_key = os.getenv("GLM_API_KEY", "") or os.getenv("ZHIPUAI_API_KEY", "")
    
    # DeepSeek
    config.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
    
    return config


def get_available_cloud_models(config: Optional[CloudModelConfig] = None) -> list:
    """
    获取可用的云端模型列表
    
    Returns:
        list: 可用的模型配置列表
    """
    if config is None:
        config = get_cloud_config()
    
    available = []
    
    if config.kimi_api_key:
        available.append({
            "name": "Kimi",
            "model": config.kimi_model,
            "base_url": config.kimi_base_url,
            "api_key": config.kimi_api_key
        })
    
    if config.qwen_api_key:
        available.append({
            "name": "Qwen",
            "model": config.qwen_model,
            "base_url": config.qwen_base_url,
            "api_key": config.qwen_api_key
        })
    
    if config.glm_api_key:
        available.append({
            "name": "GLM",
            "model": config.glm_model,
            "base_url": config.glm_base_url,
            "api_key": config.glm_api_key
        })
    
    if config.deepseek_api_key:
        available.append({
            "name": "DeepSeek",
            "model": config.deepseek_model,
            "base_url": config.deepseek_base_url,
            "api_key": config.deepseek_api_key
        })
    
    return available


def create_cloud_client(model_name: str, config: Optional[CloudModelConfig] = None):
    """
    根据模型名称创建对应的客户端
    
    Args:
        model_name: 模型名称 (Kimi, Qwen, GLM, DeepSeek)
        config: 配置对象
    
    Returns:
        OpenAI 客户端实例
    """
    from openai import OpenAI
    
    if config is None:
        config = get_cloud_config()
    
    model_name = model_name.lower()
    
    if model_name == "kimi":
        return OpenAI(
            base_url=config.kimi_base_url,
            api_key=config.kimi_api_key,
            timeout=config.timeout
        ), config.kimi_model
    
    elif model_name == "qwen":
        return OpenAI(
            base_url=config.qwen_base_url,
            api_key=config.qwen_api_key,
            timeout=config.timeout
        ), config.qwen_model
    
    elif model_name == "glm":
        return OpenAI(
            base_url=config.glm_base_url,
            api_key=config.glm_api_key,
            timeout=config.timeout
        ), config.glm_model
    
    elif model_name == "deepseek":
        return OpenAI(
            base_url=config.deepseek_base_url,
            api_key=config.deepseek_api_key,
            timeout=config.timeout
        ), config.deepseek_model
    
    else:
        raise ValueError(f"不支持的云端模型：{model_name}")


if __name__ == "__main__":
    # 测试配置加载
    print("=== 云端模型配置检查 ===\n")
    
    config = get_cloud_config()
    available = get_available_cloud_models(config)
    
    if not available:
        print("⚠️  未配置任何云端模型 API Key")
        print("\n请设置以下环境变量:")
        print("  export KIMI_API_KEY=your_key")
        print("  export QWEN_API_KEY=your_key")
        print("  export GLM_API_KEY=your_key")
        print("  export DEEPSEEK_API_KEY=your_key")
    else:
        print(f"✅ 已配置 {len(available)} 个云端模型:\n")
        for model in available:
            print(f"  - {model['name']}: {model['model']}")
    
    print()
