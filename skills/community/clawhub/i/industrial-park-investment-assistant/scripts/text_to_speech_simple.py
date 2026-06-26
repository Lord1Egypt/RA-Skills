#!/usr/bin/env python3
"""
会前简报语音播报功能（简化版）
将生成的会前简报转换为语音，方便招商人员路上收听
使用macOS系统自带的say命令（无需安装额外库）
"""

import os
import sys
import subprocess
from pathlib import Path

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

def generate_briefing_audio(briefing_file, output_dir=None):
    """将会前简报文件转换为语音"""
    # 读取会前简报文件
    if not os.path.exists(briefing_file):
        print(f"❌ 简报文件不存在: {briefing_file}")
        return False
    
    with open(briefing_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取关键部分（简化版，实际应该更智能）
    # 这里提取企业背景、扩张信号、对话剧本的关键内容
    lines = content.split('\n')
    speech_sections = []
    
    for i, line in enumerate(lines):
        # 提取重要部分：企业背景、扩张信号、对话剧本
        if any(keyword in line for keyword in ["企业名称", "行业地位", "招聘信号", "融资信号", "破冰话题", "关键问题", "价值传递"]):
            # 包含后续几行
            start = max(0, i)
            end = min(len(lines), i + 5)
            section = '\n'.join(lines[start:end])
            speech_sections.append(section)
    
    if not speech_sections:
        speech_sections.append(content[:1000])  #  fallback：前1000字符
    
    speech_text = '\n\n'.join(speech_sections)
    
    # 生成输出文件名
    if output_dir is None:
        output_dir = os.path.dirname(briefing_file)
    
    briefing_name = Path(briefing_file).stem
    output_file = os.path.join(output_dir, f"{briefing_name}.aiff")  # macOS say命令默认生成aiff格式
    
    print(f"🎤 开始生成语音...")
    print(f"📄 简报文件: {briefing_file}")
    print(f"🎵 输出文件: {output_file}")
    
    # 使用say命令生成语音
    success = text_to_speech_say(speech_text, output_file)
    
    if success:
        print(f"🎉 语音生成完成！")
        print(f"💡 使用建议:")
        print(f"   1. 将语音文件下载到手机，路上收听")
        print(f"   2. 使用语音播放软件循环播放")
        print(f"   3. 分享给团队成员，提前了解客户背景")
        return output_file
    else:
        print(f"❌ 语音生成失败")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 text_to_speech_simple.py <会前简报文件> [输出目录]")
        print("示例: python3 text_to_speech_simple.py 会前简报_XX公司_20260602.md")
        sys.exit(1)
    
    briefing_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_briefing_audio(briefing_file, output_dir)

if __name__ == "__main__":
    main()
