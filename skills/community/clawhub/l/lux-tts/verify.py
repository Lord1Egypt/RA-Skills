#!/usr/bin/env python3
"""
LuxTTS 验证脚本 - 最小化输出
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("LuxTTS Verification")
    print("=" * 40)
    
    try:
        # 导入模块
        from lux_tts_ready import get_ready_client
        
        print("[1/3] Importing module... OK")
        
        # 创建客户端
        client = get_ready_client()
        print("[2/3] Creating client... OK")
        
        # 生成音频
        test_text = "LuxTTS verification test"
        result = client.generate(test_text)
        
        if result.get("success"):
            print("[3/3] Audio generation... SUCCESS")
            print()
            print("Verification Results:")
            print(f"  Duration: {result.get('duration', 0):.2f} seconds")
            print(f"  Format: {result.get('format', 'unknown')}")
            print(f"  Size: {result.get('file_size', 0)} bytes")
            print(f"  Text: {result.get('text', '')[:50]}...")
            return True
        else:
            print("[3/3] Audio generation... FAILED")
            print(f"  Error: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print()
    print("=" * 40)
    print("Overall Status: " + ("PASS" if success else "FAIL"))
    sys.exit(0 if success else 1)