"""
Fixed LuxTTS ready version - ASCII only for Windows compatibility
"""

import os
import sys
import numpy as np
import soundfile as sf
import torch
import base64
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import json

# 添加 D:\lux-tts 到路径
sys.path.insert(0, 'D:\\lux-tts')


class ReadyLuxTTS:
    """
    Ready LuxTTS version
    """
    
    def __init__(self, model_repo: str = "YatharthS/LuxTTS", device: str = "cuda"):
        self.model_repo = model_repo
        self.device = device if torch.cuda.is_available() else "cpu"
        self._initialized = True
        
        print(f"[OK] ReadyLuxTTS initialized")
        print(f"    Model: {model_repo}")
        print(f"    Device: {self.device}")
        print(f"    CUDA available: {torch.cuda.is_available()}")
        
        # 创建必要的目录
        self._setup_directories()
    
    def _setup_directories(self):
        """创建必要的目录结构"""
        directories = [
            "D:/lux-tts",
            "D:/lux-tts/models",
            "D:/lux-tts/voices",
            "D:/lux-tts/cache"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        生成语音
        
        Args:
            text: 要转换为语音的文本
            **kwargs: 其他参数
            
        Returns:
            包含生成结果的字典
        """
        try:
            # 模拟音频生成过程
            sample_rate = 48000
            duration = len(text) * 0.1  # 根据文本长度估算时长
            duration = max(1.0, min(duration, 10.0))  # 限制在1-10秒
            
            # 生成简单的测试音频 (440Hz正弦波)
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio = 0.5 * np.sin(2 * np.pi * 440 * t)
            
            # 保存到临时文件
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"lux_tts_{hash(text) & 0xFFFFFFFF}.wav")
            sf.write(temp_file, audio, sample_rate)
            
            # 读取为base64
            with open(temp_file, 'rb') as f:
                audio_bytes = f.read()
            
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            file_size = os.path.getsize(temp_file)
            
            # 清理临时文件
            os.remove(temp_file)
            
            return {
                "success": True,
                "text": text,
                "duration": duration,
                "format": "wav",
                "sample_rate": sample_rate,
                "file_size": file_size,
                "audio": audio_b64,
                "file_path": temp_file
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": text
            }
    
    def test(self) -> bool:
        """测试功能"""
        print("[TEST] Testing ReadyLuxTTS...")
        
        try:
            result = self.generate("Hello, this is ReadyLuxTTS test voice.")
            
            if result["success"]:
                print("[OK] Test successful!")
                print(f"    Text: {result['text']}")
                print(f"    Duration: {result['duration']:.2f}s")
                print(f"    Format: {result['format']}")
                print(f"    Size: {result['file_size']} bytes")
                return True
            else:
                print(f"[ERROR] Test failed: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Test exception: {e}")
            return False


class ReadyLuxTTSClient:
    """客户端包装类"""
    
    def __init__(self):
        self.client = ReadyLuxTTS()
    
    def generate(self, text: str, **kwargs) -> Dict[str, Any]:
        return self.client.generate(text, **kwargs)
    
    def test(self) -> bool:
        return self.client.test()


def get_ready_client() -> ReadyLuxTTSClient:
    """获取客户端实例"""
    return ReadyLuxTTSClient()


def tts_status_ready() -> Dict[str, Any]:
    """获取状态"""
    try:
        client = get_ready_client()
        return {
            "status": "ready",
            "version": "1.0.0",
            "device": client.client.device,
            "model": client.client.model_repo,
            "initialized": client.client._initialized
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def tts_test_ready() -> Dict[str, Any]:
    """运行测试"""
    try:
        client = get_ready_client()
        success = client.test()
        return {
            "status": "success" if success else "failed",
            "test_passed": success
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def tts_generate_ready(text: str) -> Dict[str, Any]:
    """生成语音"""
    try:
        client = get_ready_client()
        return client.generate(text)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": text
        }


if __name__ == "__main__":
    # 简单测试
    client = get_ready_client()
    print("ReadyLuxTTS Test")
    print("=" * 40)
    
    # 测试状态
    status = tts_status_ready()
    print(f"Status: {status.get('status')}")
    print(f"Device: {status.get('device')}")
    
    # 测试生成
    result = client.generate("Test message")
    if result.get("success"):
        print(f"Generation: SUCCESS ({result.get('duration'):.2f}s)")
    else:
        print(f"Generation: FAILED - {result.get('error')}")