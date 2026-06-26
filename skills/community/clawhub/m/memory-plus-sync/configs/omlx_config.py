"""
Qwen Coder Plus API 云端模型连接配置

直接从 openclaw.json 读取配置，保持与 OpenClaw 系统一致
使用通义千问 Coding Plan 专用模型
"""

import os
import json
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class QwenConfig:
    """Qwen Coder Plus API 云端模型配置（从 openclaw.json 读取）
    
    使用通义千问 Coding Plan 专用模型，针对代码生成和优化场景
    """

    # 服务地址
    base_url: str = "https://coding.dashscope.aliyuncs.com/v1"

    # API Key (从 openclaw.json 读取)
    api_key: str = ""

    # 默认模型 (qwen3-coder-plus)
    default_model: str = "qwen3-coder-plus"

    # 超时设置 (秒)
    timeout: int = 120

    # 最大重试次数
    max_retries: int = 3

    # 重试延迟 (秒)
    retry_delay: float = 1.0

    # 温度参数
    temperature: float = 0.3

    # 最大 tokens
    max_tokens: int = 8192

    # 上下文窗口
    context_window: int = 128000


def get_qwen_config() -> QwenConfig:
    """获取 Qwen Coder Plus API 配置，直接从 openclaw.json 读取"""

    config = QwenConfig()

    # 从 openclaw.json 读取配置
    openclaw_config_path = Path.home() / ".openclaw" / "openclaw.json"
    
    try:
        with open(openclaw_config_path, 'r', encoding='utf-8') as f:
            openclaw_config = json.load(f)
        
        # 从 bailian provider 读取 qwen3-coder-plus 配置
        providers = openclaw_config.get("models", {}).get("providers", {})
        bailian = providers.get("bailian", {})
        
        # 读取 base_url 和 api_key
        if bailian.get("baseUrl"):
            config.base_url = bailian["baseUrl"]
        
        if bailian.get("apiKey"):
            config.api_key = bailian["apiKey"]
        
        # 查找 qwen3-coder-plus 模型配置
        models = bailian.get("models", [])
        for model in models:
            if model.get("id") == "qwen3-coder-plus":
                if model.get("name"):
                    config.default_model = model["name"]
                if model.get("contextWindow"):
                    config.context_window = model["contextWindow"]
                if model.get("maxTokens"):
                    config.max_tokens = model["maxTokens"]
                break
        
        print(f"✅ 从 openclaw.json 加载 Qwen Coder Plus 配置:")
        print(f"   Base URL: {config.base_url}")
        print(f"   模型：{config.default_model}")
        print(f"   API Key: {'已配置' if config.api_key else '❌ 未配置'}")
        
    except FileNotFoundError:
        print(f"⚠️  警告：未找到 openclaw.json ({openclaw_config_path})")
        print("   使用默认配置")
    except json.JSONDecodeError as e:
        print(f"⚠️  警告：openclaw.json 解析失败：{e}")
        print("   使用默认配置")
    except Exception as e:
        print(f"⚠️  警告：读取 openclaw.json 失败：{e}")
        print("   使用默认配置")

    return config


# 别名保持向后兼容
get_omlx_config = get_qwen_config
OMLXConfig = QwenConfig


def check_qwen_connection(config: Optional[QwenConfig] = None) -> bool:
    """
    检查 Qwen Coder Plus API 连接状态
    通过实际调用聊天接口来验证连接

    Returns:
        bool: 连接是否成功
    """
    from openai import OpenAI

    if config is None:
        config = get_qwen_config()

    if not config.api_key:
        print("❌ Qwen API Key 未配置")
        return False

    try:
        client = OpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            timeout=10
        )
        
        # 通过实际调用测试连接
        response = client.chat.completions.create(
            model=config.default_model,
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=10
        )
        
        if response and response.choices:
            print(f"✅ Qwen API 连接成功")
            print(f"   模型：{response.model}")
            print(f"   用法：输入{response.usage.prompt_tokens} tokens, 输出{response.usage.completion_tokens} tokens")
            return True
        else:
            print("❌ Qwen API 返回空响应")
            return False

    except Exception as e:
        print(f"❌ Qwen API 连接检查失败:{e}")
        return False


# 别名保持向后兼容
check_omlx_connection = check_qwen_connection


def create_qwen_client(config: Optional[QwenConfig] = None):
    """
    创建 OpenAI 兼容的客户端

    Returns:
        OpenAI 客户端实例
    """
    from openai import OpenAI

    if config is None:
        config = get_qwen_config()

    client = OpenAI(
        base_url=config.base_url,
        api_key=config.api_key,
        timeout=config.timeout
    )

    return client


# 别名保持向后兼容
create_omlx_client = create_qwen_client


if __name__ == "__main__":
    # 测试连接
    print("=== Qwen Coder Plus API 连接测试 ===\n")

    config = get_qwen_config()
    print(f"配置:")
    print(f"  Base URL: {config.base_url}")
    print(f"  默认模型:{config.default_model}")
    print(f"  API Key:{'已配置' if config.api_key else '❌ 未配置'}")
    print(f"  超时:{config.timeout}s")
    print(f"  上下文窗口:{config.context_window}")
    print(f"  最大 tokens:{config.max_tokens}\n")

    if check_qwen_connection(config):
        print("\n✅ Qwen Coder Plus API 服务就绪")

        # 测试创建客户端
        client = create_qwen_client(config)
        print(f"✅ 客户端创建成功")
        
        # 测试 JSON 输出格式
        print("\n=== 测试 JSON 输出格式 ===")
        try:
            response = client.chat.completions.create(
                model=config.default_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                    {"role": "user", "content": 'Return a JSON object with keys: name, version, status. Example: {"name": "test", "version": "1.0", "status": "ok"}'}
                ],
                temperature=0.3,
                max_tokens=500
            )
            content = response.choices[0].message.content
            print(f"响应内容:\n{content}")
            
            # 尝试解析 JSON
            import json
            try:
                parsed = json.loads(content)
                print(f"\n✅ JSON 解析成功:")
                print(f"   name: {parsed.get('name')}")
                print(f"   version: {parsed.get('version')}")
                print(f"   status: {parsed.get('status')}")
            except json.JSONDecodeError as e:
                print(f"\n⚠️ JSON 解析失败：{e}")
                print("   但 API 连接正常")
                
        except Exception as e:
            print(f"\n❌ 测试调用失败：{e}")
    else:
        print("\n❌ Qwen API 服务不可用")
        print("\n请检查 openclaw.json 配置")
        exit(1)
