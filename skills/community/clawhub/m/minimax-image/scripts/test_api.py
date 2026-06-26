#!/usr/bin/env python3
"""
MiniMax图像生成 - 快捷测试脚本
用于验证API Key是否配置正确
"""

import os
import sys

def test_connection(api_key):
    """测试API连接"""
    import requests
    
    url = "https://api.minimaxi.com/v1/image_generation"
    payload = {
        "model": "image-01",
        "prompt": "简单蓝色背景，科技风格，PPT用图",
        "aspect_ratio": "16:9",
        "response_format": "url",
        "n": 1,
        "prompt_optimizer": True
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        print("🔍 测试连接 MiniMax API...")
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "data" in result and len(result["data"]) > 0:
                print("✅ API连接成功！")
                print(f"📋 图片URL: {result['data'][0].get('url', 'N/A')}")
                return True
            else:
                print(f"❌ 响应格式异常: {result}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"📋 响应: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


if __name__ == "__main__":
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    
    if not api_key:
        print("❌ 请先设置环境变量 MINIMAX_API_KEY")
        print("示例: export MINIMAX_API_KEY='your-key-here'")
        sys.exit(1)
    
    success = test_connection(api_key)
    sys.exit(0 if success else 1)