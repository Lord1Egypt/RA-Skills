#!/usr/bin/env python3
"""
Jarvis TTS 语音合成
用法：python3 jarvis-tts.py "要说的内容"
"""
import subprocess
import sys
import os
import tempfile

def speak(text, voice="zh-CN-YunxiNeural"):
    """生成并播放语音"""
    # 创建临时文件
    tmpfile = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmpfile.close()
    
    try:
        # 生成语音（等待完成）
        print(f"🔊 生成语音...")
        result = subprocess.run([
            sys.executable, "-m", "edge_tts",
            "--voice", voice,
            "--text", text,
            "--write-media", tmpfile.name
        ], capture_output=True, timeout=60)
        
        # 检查生成是否成功
        if not os.path.exists(tmpfile.name) or os.path.getsize(tmpfile.name) == 0:
            print("❌ 音频生成失败")
            return False
        
        print(f"✅ 生成成功，播放中...")
        
        # 播放音频（等待完成）
        subprocess.run(["afplay", tmpfile.name], timeout=120)
        
        print("✅ 播放完成")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ 超时")
        return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(tmpfile.name):
            os.unlink(tmpfile.name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 jarvis-tts.py \"要说的内容\" [--voice 语音名称]")
        sys.exit(1)
    
    # 解析参数
    text = sys.argv[1]
    voice = "zh-CN-YunxiNeural"  # 默认语音
    
    if "--voice" in sys.argv:
        voice_idx = sys.argv.index("--voice")
        if voice_idx + 1 < len(sys.argv):
            voice = sys.argv[voice_idx + 1]
    
    success = speak(text, voice)
    sys.exit(0 if success else 1)
