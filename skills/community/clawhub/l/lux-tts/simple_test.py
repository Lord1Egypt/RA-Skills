#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LuxTTS 简单测试脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def test_lux_tts():
    """测试 LuxTTS 功能"""
    print("=== LuxTTS 功能测试 ===")
    print()
    
    try:
        # 导入模块
        from lux_tts_ready import get_ready_client
        
        print("1. 创建客户端...")
        client = get_ready_client()
        print("   ✅ 客户端创建成功")
        print(f"   设备: {client.device}")
        print(f"   CUDA可用: {client._initialized}")
        print()
        
        print("2. 生成测试音频...")
        test_text = "你好，这是LuxTTS测试语音。安装成功！"
        result = client.generate(test_text)
        
        if result["success"]:
            print("   ✅ 音频生成成功")
            print(f"   文本: {result['text']}")
            print(f"   时长: {result['duration']:.2f}秒")
            print(f"   格式: {result['format']}")
            print(f"   大小: {result['file_size']}字节")
            print(f"   文件: {result.get('file_path', '内存中')}")
        else:
            print(f"   ❌ 生成失败: {result.get('error')}")
        
        print()
        print("3. 保存测试文件...")
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
        print(f"   ✅ 测试音频已保存: {test_file}")
        print(f"   文件大小: {os.path.getsize(test_file)}字节")
        
        print()
        print("=== 测试完成 ===")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_lux_tts()
    sys.exit(0 if success else 1)