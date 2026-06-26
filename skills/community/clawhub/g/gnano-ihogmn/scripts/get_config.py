#!/usr/bin/env python3
"""
GNano Ihogmn 配置获取脚本
根据 API Token 获取账户可用功能和参数
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "未找到 requests 模块。请安装: pip install requests"
    }, ensure_ascii=False))
    sys.exit(1)


DEFAULT_API_URL = "https://gnano.ihogmn.top"

KNOWN_MODELS = [
    "gemini-3-pro-image-preview",
    "gemini-3.1-flash-image-preview"
]


def detect_capabilities(api_url: str, token: str) -> dict:
    """探测 API 能力"""
    capabilities = {
        "api_url": api_url,
        "token_valid": False,
        "models": [],
        "default_model": None,
        "resolutions": ["1K", "2K", "4K"],
        "default_resolution": "2K",
        "max_reference_images": 2,
        "max_reference_size_mb": 2,
        "rate_limit_per_minute": 2,
        "supports_text_to_image": True,
        "supports_image_editing": True,
        "error": None
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    models_url = f"{api_url}/v1beta/models"
    
    try:
        response = requests.get(models_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            capabilities["token_valid"] = True
            
            if "models" in result:
                for model in result["models"]:
                    model_name = model.get("name", "")
                    if "gemini" in model_name.lower() and "image" in model_name.lower():
                        model_id = model_name.split("/")[-1] if "/" in model_name else model_name
                        capabilities["models"].append(model_id)
            
            if not capabilities["models"]:
                capabilities["models"] = KNOWN_MODELS.copy()
                
        elif response.status_code == 401:
            capabilities["error"] = "API Token 无效或已过期"
            return capabilities
        elif response.status_code == 403:
            capabilities["error"] = "API Token 没有访问权限"
            return capabilities
        else:
            capabilities["token_valid"] = True
            capabilities["models"] = KNOWN_MODELS.copy()
            
    except requests.exceptions.RequestException as e:
        capabilities["token_valid"] = True
        capabilities["models"] = KNOWN_MODELS.copy()
        capabilities["error"] = f"无法连接到 API 服务器: {e}"
    
    if capabilities["models"]:
        if "gemini-3.1-flash-image-preview" in capabilities["models"]:
            capabilities["default_model"] = "gemini-3.1-flash-image-preview"
        else:
            capabilities["default_model"] = capabilities["models"][0]
    
    return capabilities


def get_full_config(token: str, api_url: str = None) -> dict:
    """获取完整的配置信息"""
    api_url = api_url or DEFAULT_API_URL
    api_url = api_url.rstrip("/")
    
    capabilities = detect_capabilities(api_url, token)
    
    if capabilities["error"] and not capabilities["token_valid"]:
        return {
            "success": False,
            "error": capabilities["error"],
            "api_url": api_url
        }
    
    return {
        "success": True,
        "api_token": token,
        "api_url": api_url,
        "models": capabilities["models"],
        "default_model": capabilities["default_model"],
        "resolutions": capabilities["resolutions"],
        "default_resolution": capabilities["default_resolution"],
        "max_reference_images": capabilities["max_reference_images"],
        "max_reference_size_mb": capabilities["max_reference_size_mb"],
        "rate_limit_per_minute": capabilities["rate_limit_per_minute"],
        "supports_text_to_image": capabilities["supports_text_to_image"],
        "supports_image_editing": capabilities["supports_image_editing"],
        "warning": capabilities.get("error")
    }


def main():
    parser = argparse.ArgumentParser(
        description="获取 GNano API 配置信息"
    )
    parser.add_argument("--token", "-t", required=True, help="API Token")
    parser.add_argument("--api-url", "-u", default=DEFAULT_API_URL, help="API 地址")
    
    args = parser.parse_args()
    
    config = get_full_config(args.token, args.api_url)
    
    print(json.dumps(config, ensure_ascii=False, indent=2))
    
    sys.exit(0 if config.get("success") else 1)


if __name__ == "__main__":
    main()
