#!/usr/bin/env python3
"""
LuxTTS ASCII测试脚本 - 无Unicode字符
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def test_lux_tts():
    """测试 LuxTTS 功能"""
    print("=== LuxTTS Function Test ===")
    print()
    
    try:
        # 导入模块
        from lux_tts_ready import get_ready_client
        
        print("1. Creating client...")
        client = get_ready_client()
        print("   [OK] Client created")
        print(f"   Model repo: {client.model_repo}")
        print(f"   Initialized: {client._initialized}")
        print()
        
        print("2. Generating test audio...")
        test_text = "Hello, this is LuxTTS test voice. Installation successful!"
        result = client.generate(test_text)
        
        if result["success"]:
            print("   [OK] Audio generated")
            print(f"   Text: {result['text']}")
            print(f"   Duration: {result['duration']:.2f}s")
            print(f"   Format: {result['format']}")
            print(f"   Size: {result['file_size']} bytes")
            print(f"   File: {result.get('file_path', 'in memory')}")
        else:
            print(f"   [ERROR] Generation failed: {result.get('error')}")
        
        print()
        print("3. Testing audio file creation...")
        import soundfile as sf
        import numpy as np
        
        # 创建测试目录
        test_dir = "D:/lux-tts/test_output"
        os.makedirs(test_dir, exist_ok=True)
        
        # 生成简单的测试音频
        sample_rate = 48000
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        test_file = os.path.join(test_dir, "test_tone.wav")
        sf.write(test_file, audio, sample_rate)
        print(f"   [OK] Test audio saved: {test_file}")
        print(f"   File size: {os.path.getsize(test_file)} bytes")
        
        print()
        print("=== Test Complete ===")
        print("Status: SUCCESS")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        print("Status: FAILED")
        return False

if __name__ == "__main__":
    success = test_lux_tts()
    sys.exit(0 if success else 1)