#!/usr/bin/env python3
"""
macOS 语音控制 - Vosk 离线语音识别
完全免费、离线运行、隐私保护
"""

import sys
import os
import wave
import json
import subprocess
import tempfile
from pathlib import Path

# 检查 Vosk
try:
    from vosk import Model, KaldiRecognizer
except ImportError:
    print("❌ Vosk 未安装")
    print("")
    print("请安装：")
    print("  pip3 install --user --break-system-packages vosk")
    sys.exit(1)

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

# 模型路径
MODEL_PATH = Path.home() / ".openclaw" / "vosk-models" / "vosk-model-small-zh-cn-0.22"

def check_model():
    """检查语音模型是否存在"""
    if not MODEL_PATH.exists():
        print_color(Colors.YELLOW, "⚠️  语音模型未下载")
        print("")
        print("📥 下载中文语音模型（约 50MB）:")
        print("")
        print("方法 1: 自动下载")
        print("  python3 scripts/download_vosk_model.py")
        print("")
        print("方法 2: 手动下载")
        print("  1. 访问：https://alphacephei.com/vosk/models")
        print("  2. 下载：vosk-model-small-zh-cn-0.22.zip")
        print("  3. 解压到：~/.openclaw/vosk-models/")
        print("")
        return False
    return True

def check_microphone():
    """检查麦克风"""
    # macOS 检查麦克风
    result = subprocess.run(
        ["system_profiler", "SPAudioDataType"],
        capture_output=True,
        text=True
    )
    if "Input" not in result.stdout:
        print_color(Colors.RED, "❌ 未检测到麦克风")
        return False
    return True

def record_audio(duration=5, output_file=None):
    """录音函数"""
    if output_file is None:
        output_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    
    print_color(Colors.YELLOW, f"🎤 正在录音...（{duration}秒）")
    print("   请说话...")
    print("")
    
    # 使用 arecord 或 rec 录音
    try:
        # 尝试使用 sox 的 rec 命令
        subprocess.run(
            ["rec", "-r", "16000", "-c", "1", "-d", output_file],
            timeout=duration + 2,
            capture_output=True
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # 尝试使用 arecord
        try:
            subprocess.run(
                ["arecord", "-r", "16000", "-c", "1", "-d", str(duration), "-f", "cd", output_file],
                timeout=duration + 2,
                capture_output=True
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print_color(Colors.RED, "❌ 找不到录音工具")
            print("")
            print("请安装 sox:")
            print("  brew install sox")
            return None
    
    print_color(Colors.GREEN, "✅ 录音完成")
    return output_file

def recognize_speech(audio_file, model=None):
    """语音识别"""
    if model is None:
        print_color(Colors.BLUE, "🧠 加载语音模型...")
        model = Model(str(MODEL_PATH))
    
    print_color(Colors.BLUE, "🧠 正在识别语音...")
    
    # 读取音频文件
    with wave.open(audio_file, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            print_color(Colors.RED, "❌ 音频格式不正确（需要 16kHz 单声道 16bit）")
            return None
        
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)
        
        full_text = ""
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result:
                    full_text += result["text"] + " "
        
        # 获取最后部分
        final_result = json.loads(recognizer.FinalResult())
        if "text" in final_result:
            full_text += final_result["text"]
    
    return full_text.strip()

def main():
    """主函数"""
    print_color(Colors.BLUE, "🎤 Vosk 语音控制")
    print("")
    
    # 检查模型
    if not check_model():
        sys.exit(1)
    
    # 检查麦克风
    if not check_microphone():
        sys.exit(1)
    
    # 加载模型
    print_color(Colors.BLUE, "🧠 加载语音模型...")
    model = Model(str(MODEL_PATH))
    print_color(Colors.GREEN, "✅ 模型加载完成")
    print("")
    
    # 录音
    audio_file = record_audio(duration=5)
    if not audio_file:
        sys.exit(1)
    
    try:
        # 识别
        text = recognize_speech(audio_file, model)
        
        if text:
            print_color(Colors.GREEN, f"✅ 识别结果：\"{text}\"")
            print("")
            
            # 执行自然语言命令
            print_color(Colors.BLUE, "🚀 执行命令...")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            natural_lang_script = os.path.join(script_dir, "natural_language.py")
            
            if os.path.exists(natural_lang_script):
                subprocess.run(["python3", natural_lang_script, text])
            else:
                print_color(Colors.YELLOW, "⚠️  找不到自然语言脚本")
                print("   请确保 natural_language.py 在同一目录")
        else:
            print_color(Colors.YELLOW, "⚠️  未识别到有效语音")
    
    finally:
        # 清理临时文件
        if os.path.exists(audio_file):
            os.unlink(audio_file)

if __name__ == "__main__":
    main()
