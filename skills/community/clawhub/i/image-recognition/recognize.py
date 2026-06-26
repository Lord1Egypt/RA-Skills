#!/usr/bin/env python3
"""
图片识别脚本 - Image Recognition
通用图片识别，支持多种视觉模型提供商

使用方法：
    python3 recognize.py <图片路径> [问题]

环境变量（可选，默认从 OpenClaw 配置读取）：
    IMAGE_MODEL_PROVIDER: 模型提供商 (bailian, openrouter, openai)
    IMAGE_MODEL_API_KEY: API Key
    IMAGE_MODEL_NAME: 模型名称
    IMAGE_MODEL_ENDPOINT: API 端点
"""

import sys
import os
import base64
import requests
import json


def get_model_config():
    """
    获取模型配置
    优先级：环境变量 > OpenClaw 配置文件 > 默认配置
    """
    config = {
        "provider": "bailian",
        "api_key": None,
        "model": "qwen3.5-plus",
        "endpoint": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
        "headers": {
            "Content-Type": "application/json"
        }
    }
    
    # 1. 尝试从环境变量读取
    if os.environ.get("IMAGE_MODEL_PROVIDER"):
        config["provider"] = os.environ.get("IMAGE_MODEL_PROVIDER")
    
    if os.environ.get("IMAGE_MODEL_API_KEY"):
        config["api_key"] = os.environ.get("IMAGE_MODEL_API_KEY")
    
    if os.environ.get("IMAGE_MODEL_NAME"):
        config["model"] = os.environ.get("IMAGE_MODEL_NAME")
    
    if os.environ.get("IMAGE_MODEL_ENDPOINT"):
        config["endpoint"] = os.environ.get("IMAGE_MODEL_ENDPOINT")
    
    # 2. 如果环境变量没有，尝试从 OpenClaw 配置读取
    if not config["api_key"]:
        try:
            openclaw_config_path = os.path.expanduser("~/.openclaw/openclaw.json")
            if os.path.exists(openclaw_config_path):
                with open(openclaw_config_path, 'r') as f:
                    openclaw_config = json.load(f)
                
                # 查找第一个支持视觉的模型（优先 bailian）
                models = openclaw_config.get("models", {}).get("providers", {})
                
                # 优先检查 bailian
                for preferred_provider in ["bailian", "openrouter"]:
                    if preferred_provider in models:
                        provider_config = models[preferred_provider]
                        api_key = provider_config.get("apiKey")
                        provider_models = provider_config.get("models", [])
                        
                        for model_info in provider_models:
                            model_input = model_info.get("input", [])
                            model_id = model_info.get("id", "")
                            
                            # 跳过已下线的模型
                            if "hunter-alpha" in model_id.lower():
                                continue
                            
                            if "image" in model_input and api_key:
                                config["provider"] = preferred_provider
                                config["api_key"] = api_key
                                config["model"] = model_id
                                
                                # 设置端点和 headers
                                if "bailian" in preferred_provider.lower() or "dashscope" in provider_config.get("baseUrl", "").lower():
                                    config["endpoint"] = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
                                    config["headers"]["Authorization"] = f"Bearer {api_key}"
                                elif "openrouter" in preferred_provider.lower():
                                    config["endpoint"] = "https://openrouter.ai/api/v1/chat/completions"
                                    config["headers"]["Authorization"] = f"Bearer {api_key}"
                                    config["headers"]["HTTP-Referer"] = "https://openclaw.ai"
                                    config["headers"]["X-Title"] = "OpenClaw"
                                else:
                                    # 默认 OpenAI 兼容格式
                                    config["endpoint"] = provider_config.get("baseUrl", config["endpoint"]) + "/chat/completions"
                                    config["headers"]["Authorization"] = f"Bearer {api_key}"
                                
                                break
                        if config["api_key"]:
                            break
        except Exception as e:
            pass  # 如果读取失败，继续使用默认配置
    
    # 3. 如果还是没有 API Key，使用默认 Bailian Key（仅作为后备）
    if not config["api_key"]:
        config["api_key"] = "sk-sp-e20dc070c4724e909f4b0be4d1d386e0"
        config["headers"]["Authorization"] = f"Bearer {config['api_key']}"
    
    return config


def recognize_image(image_path: str, question: str = "请识别这张图片中的内容。如果有文字，请提取所有文字内容。", config: dict = None) -> str:
    """
    识别图片内容
    
    Args:
        image_path: 图片文件路径
        question: 问题提示（可选）
        config: 模型配置（可选，默认自动检测）
    
    Returns:
        识别结果字符串
    """
    # 检查文件是否存在
    if not os.path.exists(image_path):
        return f"Error: 文件不存在 - {image_path}"
    
    # 获取配置
    if config is None:
        config = get_model_config()
    
    # 读取图片并转换为 base64
    try:
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
    except Exception as e:
        return f"Error: 读取图片失败 - {str(e)}"
    
    # 构建请求
    payload = {
        "model": config["model"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ],
        "max_tokens": 2048
    }
    
    # 发送请求
    try:
        response = requests.post(
            config["endpoint"],
            headers=config["headers"],
            json=payload,
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
            return content
        else:
            return f"Error: HTTP {response.status_code} - {response.text[:200]}"
    
    except requests.exceptions.Timeout:
        return "Error: 请求超时（90 秒）"
    except requests.exceptions.RequestException as e:
        return f"Error: 网络错误 - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python3 recognize.py <图片路径> [问题]")
        print("\n环境变量（可选）:")
        print("  IMAGE_MODEL_PROVIDER: 模型提供商 (bailian, openrouter, openai)")
        print("  IMAGE_MODEL_API_KEY: API Key")
        print("  IMAGE_MODEL_NAME: 模型名称")
        print("  IMAGE_MODEL_ENDPOINT: API 端点")
        print("\n示例:")
        print("  python3 recognize.py /path/to/image.jpg")
        print('  python3 recognize.py /path/to/image.jpg "提取图片中的所有文字"')
        print("\n默认会自动使用 OpenClaw 配置的视觉模型")
        sys.exit(1)
    
    image_path = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "请识别这张图片中的内容。如果有文字，请提取所有文字内容。"
    
    # 获取配置信息
    config = get_model_config()
    print(f"使用模型：{config['provider']}/{config['model']}", file=sys.stderr)
    
    # 执行识别
    result = recognize_image(image_path, question, config)
    
    # 输出结果
    print(result)


if __name__ == "__main__":
    main()
