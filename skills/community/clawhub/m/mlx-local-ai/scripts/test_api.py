#!/usr/bin/env python3
"""
MLX Local AI API 测试脚本
"""

import json
import urllib.request
import urllib.error

CHAT_URL = "http://localhost:8080/v1/chat/completions"
EMBEDDING_URL = "http://localhost:8081"

def test_chat_api():
    """测试 Chat API"""
    print("【测试 Chat API】")
    
    data = {
        "model": "mlx-community/Qwen3.5-4B-OptiQ-4bit",
        "messages": [{"role": "user", "content": "你好，请简短自我介绍"}],
        "max_tokens": 50
    }
    
    try:
        req = urllib.request.Request(
            CHAT_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            print(f"✓ Chat API 正常")
            print(f"  回复: {content[:100]}...")
            return True
    except Exception as e:
        print(f"❌ Chat API 错误: {e}")
        return False

def test_embedding_api():
    """测试 Embedding API"""
    print("\n【测试 Embedding API】")
    
    data = {"texts": ["你好", "世界"]}
    
    try:
        req = urllib.request.Request(
            f"{EMBEDDING_URL}/embed",
            data=json.dumps(data).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            embeddings = result['embeddings']
            print(f"✓ Embedding API 正常")
            print(f"  向量维度: {len(embeddings[0])}")
            return True
    except Exception as e:
        print(f"❌ Embedding API 错误: {e}")
        return False

def test_health():
    """测试健康检查"""
    print("\n【测试健康检查】")
    
    try:
        req = urllib.request.Request(f"{EMBEDDING_URL}/health", method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✓ Embedding 服务健康: {result['status']}")
            return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def main():
    print("=" * 50)
    print("MLX Local AI API 测试")
    print("=" * 50)
    print()
    
    results = []
    results.append(("Chat API", test_chat_api()))
    results.append(("Embedding API", test_embedding_api()))
    results.append(("健康检查", test_health()))
    
    print("\n" + "=" * 50)
    print("测试结果:")
    for name, passed in results:
        status = "✓ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
    print("=" * 50)

if __name__ == "__main__":
    main()
