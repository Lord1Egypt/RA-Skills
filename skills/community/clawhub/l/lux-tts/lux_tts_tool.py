"""
OpenClaw TTS 工具集成
将 LuxTTS 集成到 OpenClaw 的工具系统中
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import base64

# 导入智能路径管理
from . import LuxTTSClient, get_client


class LuxTTSTool:
    """OpenClaw TTS 工具"""
    
    def __init__(self):
        self.client = None
        self._initialized = False
    
    def initialize(self):
        """初始化工具"""
        if self._initialized:
            return True
        
        try:
            self.client = get_client()
            self._initialized = True
            print(f"✓ LuxTTS 工具初始化成功")
            print(f"  安装位置: {self.client.get_info()['installation']}")
            return True
        except Exception as e:
            print(f"✗ LuxTTS 工具初始化失败: {e}")
            return False
    
    def generate(self, text: str, voice_file: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """生成语音"""
        if not self._initialized and not self.initialize():
            raise RuntimeError("LuxTTS 工具未初始化")
        
        try:
            # 生成语音
            audio = self.client.generate_speech(text, voice_file, **kwargs)
            
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                temp_path = tmp.name
                self.client.save_audio(audio, temp_path)
            
            # 读取音频文件为 base64
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # 清理临时文件
            os.unlink(temp_path)
            
            return {
                "success": True,
                "text": text,
                "audio_base64": base64.b64encode(audio_data).decode('utf-8'),
                "format": "wav",
                "sample_rate": 48000,
                "duration": len(audio.numpy().squeeze()) / 48000  # 秒
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": text
            }
    
    def list_voices(self) -> list:
        """列出可用的语音文件"""
        if not self._initialized and not self.initialize():
            return []
        
        voices_dir = self.client.get_info().get('voices_dir')
        if not voices_dir or not os.path.exists(voices_dir):
            return []
        
        voices = []
        for file in os.listdir(voices_dir):
            if file.lower().endswith(('.wav', '.mp3')):
                voices.append({
                    "name": file,
                    "path": os.path.join(voices_dir, file),
                    "size": os.path.getsize(os.path.join(voices_dir, file))
                })
        
        return voices
    
    def add_voice(self, audio_path: str, name: Optional[str] = None) -> bool:
        """添加语音文件"""
        if not self._initialized and not self.initialize():
            return False
        
        if not os.path.exists(audio_path):
            print(f"错误: 文件不存在: {audio_path}")
            return False
        
        voices_dir = self.client.get_info().get('voices_dir')
        if not voices_dir:
            print("错误: 未找到语音目录")
            return False
        
        # 确定目标文件名
        if not name:
            name = os.path.basename(audio_path)
        
        target_path = os.path.join(voices_dir, name)
        
        try:
            # 复制文件
            import shutil
            shutil.copy2(audio_path, target_path)
            print(f"✓ 语音文件已添加: {name}")
            return True
        except Exception as e:
            print(f"✗ 添加语音文件失败: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取工具状态"""
        if not self._initialized:
            return {"initialized": False, "error": "未初始化"}
        
        try:
            info = self.client.get_info()
            voices = self.list_voices()
            
            return {
                "initialized": True,
                "installation": info['installation'],
                "device": info['device'],
                "cuda_available": info['cuda_available'],
                "voices_count": len(voices),
                "voices": [v['name'] for v in voices],
                "models_dir": info['models_dir'],
                "voices_dir": info['voices_dir']
            }
        except Exception as e:
            return {
                "initialized": False,
                "error": str(e)
            }


# 全局工具实例
_tts_tool = None


def get_tts_tool() -> LuxTTSTool:
    """获取 TTS 工具实例（单例）"""
    global _tts_tool
    if _tts_tool is None:
        _tts_tool = LuxTTSTool()
    return _tts_tool


def tts_generate(text: str, voice: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """生成语音（便捷函数）"""
    tool = get_tts_tool()
    return tool.generate(text, voice, **kwargs)


def tts_status() -> Dict[str, Any]:
    """获取 TTS 状态"""
    tool = get_tts_tool()
    return tool.get_status()


def tts_list_voices() -> list:
    """列出语音"""
    tool = get_tts_tool()
    return tool.list_voices()


# 命令行接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="LuxTTS 命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # status 命令
    subparsers.add_parser("status", help="检查状态")
    
    # list 命令
    subparsers.add_parser("list", help="列出语音")
    
    # generate 命令
    gen_parser = subparsers.add_parser("generate", help="生成语音")
    gen_parser.add_argument("text", help="要转换的文本")
    gen_parser.add_argument("--voice", help="语音文件路径")
    gen_parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    tool = get_tts_tool()
    
    if args.command == "status":
        status = tool.get_status()
        print("LuxTTS 状态:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    elif args.command == "list":
        voices = tool.list_voices()
        print("可用语音:")
        for voice in voices:
            print(f"  - {voice['name']} ({voice['size']} bytes)")
    
    elif args.command == "generate":
        result = tool.generate(args.text, args.voice)
        if result["success"]:
            if args.output:
                # 保存到文件
                audio_data = base64.b64decode(result["audio_base64"])
                with open(args.output, 'wb') as f:
                    f.write(audio_data)
                print(f"✓ 语音已保存到: {args.output}")
            else:
                print(f"✓ 语音生成成功，时长: {result['duration']:.2f}秒")
        else:
            print(f"✗ 语音生成失败: {result['error']}")
    
    else:
        parser.print_help()