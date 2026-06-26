#!/usr/bin/env python3
"""
会前简报语音播报功能
将生成的会前简报转换为语音，方便招商人员路上收听
支持多种TTS引擎：系统自带say命令、pyttsx3、gTTS等
"""

import os
import sys
import subprocess
from pathlib import Path

def check_tts_availability():
    """检查可用的TTS引擎"""
    available_engines = []
    
    # 检查macOS系统自带的say命令
    try:
        subprocess.run(["say", "--version"], capture_output=True, check=True)
        available_engines.append("say")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # 检查pyttsx3库
    try:
        import pyttsx3
        available_engines.append("pyttsx3")
    except ImportError:
        pass
    
    # 检查gTTS库（需要联网）
    try:
        from gtts import gTTS
        available_engines.append("gtts")
    except ImportError:
        pass
    
    return available_engines

def text_to_speech_say(text, output_file=None, voice="Ting-Ting"):
    """使用macOS系统自带的say命令转换语音"""
    try:
        if output_file:
            # 保存为音频文件
            cmd = ["say", "-v", voice, "-o", output_file, text]
            subprocess.run(cmd, check=True)
            print(f"✅ 语音文件已生成: {output_file}")
            return True
        else:
            # 直接播放
            cmd = ["say", "-v", voice, text]
            subprocess.run(cmd, check=True)
            return True
    except Exception as e:
        print(f"❌ say命令执行失败: {e}")
        return False

def text_to_speech_pyttsx3(text, output_file=None):
    """使用pyttsx3库转换语音"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        if output_file:
            engine.save_to_file(text, output_file)
        else:
            engine.say(text)
            engine.runAndWait()
        
        print(f"✅ 语音生成完成: {output_file if output_file else '直接播放'}")
        return True
    except Exception as e:
        print(f"❌ pyttsx3执行失败: {e}")
        return False

def text_to_speech_gtts(text, output_file, lang='zh-cn'):
    """使用gTTS库转换语音（需要联网）"""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang)
        tts.save(output_file)
        print(f"✅ 语音文件已生成: {output_file}")
        return True
    except Exception as e:
        print(f"❌ gTTS执行失败: {e}")
        return False

def generate_briefing_audio(briefing_file, output_dir=None):
    """将会前简报文件转换为语音"""
    # 读取会前简报文件
    if not os.path.exists(briefing_file):
        print(f"❌ 简报文件不存在: {briefing_file}")
        return False
    
    with open(briefing_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取关键部分（简化版，实际应该更智能）
    # 这里简单提取前1000个字符作为示例
    speech_text = content[:1000] + "...（简报内容较长，请查看完整文档）"
    
    # 生成输出文件名
    if output_dir is None:
        output_dir = os.path.dirname(briefing_file)
    
    briefing_name = Path(briefing_file).stem
    output_file = os.path.join(output_dir, f"{briefing_name}.mp3")
    
    # 检查可用的TTS引擎
    available_engines = check_tts_availability()
    
    if not available_engines:
        print("❌ 未找到可用的TTS引擎")
        print("💡 建议安装: pip install pyttsx3 或 pip install gTTS")
        return False
    
    print(f"🔊 可用TTS引擎: {', '.join(available_engines)}")
    
    # 优先使用say命令（macOS系统自带）
    if "say" in available_engines:
        print(f"🎤 使用say命令生成语音...")
        return text_to_speech_say(speech_text, output_file)
    
    # 其次使用pyttsx3
    elif "pyttsx3" in available_engines:
        print(f"🎤 使用pyttsx3生成语音...")
        return text_to_speech_pyttsx3(speech_text, output_file)
    
    # 最后使用gTTS
    elif "gtts" in available_engines:
        print(f"🎤 使用gTTS生成语音...")
        return text_to_speech_gtts(speech_text, output_file)
    
    return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 text_to_speech.py <会前简报文件> [输出目录]")
        print("示例: python3 text_to_speech.py 会前简报_XX公司_20260602.md")
        sys.exit(1)
    
    briefing_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🎤 开始生成会前简报语音...")
    print(f"📄 简报文件: {briefing_file}")
    
    success = generate_briefing_audio(briefing_file, output_dir)
    
    if success:
        print(f"🎉 语音生成完成！")
        print(f"💡 使用建议:")
        print(f"   1. 将语音文件下载到手机，路上收听")
        print(f"   2. 使用语音播放软件循环播放")
        print(f"   3. 分享给团队成员，提前了解客户背景")
    else:
        print(f"❌ 语音生成失败")
        sys.exit(1)

if __name__ == "__main__":
    main()