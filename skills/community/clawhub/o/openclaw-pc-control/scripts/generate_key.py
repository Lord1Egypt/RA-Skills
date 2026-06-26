import secrets
import string
import hashlib
import json
import os


def generate_api_key(length: int = 32) -> str:
    """生成随机 API Key"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_api_key_with_hash():
    """生成 API Key 并显示 hash 用于验证"""
    api_key = generate_api_key()
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    return {
        "api_key": api_key,
        "api_key_hash": api_key_hash
    }


if __name__ == "__main__":
    print("=" * 50)
    print("   PC Controller - API Key 生成器")
    print("=" * 50)
    print()

    result = generate_api_key_with_hash()

    print(f"生成的 API Key: {result['api_key']}")
    print(f"Key Hash (用于验证): {result['api_key_hash']}")
    print()
    print("使用方式:")
    print(f"  1. 在启动 API 时输入此 Key")
    print(f"  2. 或通过 API 设置: POST /security/mode")
    print()
