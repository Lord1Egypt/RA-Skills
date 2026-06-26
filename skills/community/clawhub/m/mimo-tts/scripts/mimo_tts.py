#!/usr/bin/env python3
"""
小米 MiMo TTS 语音合成脚本
用法: python3 mimo_tts.py "要合成的话" [--voice default_zh] [--style "夹子音"] [--output output.wav]
"""

import os
import sys
import base64
import argparse
import json
from openai import OpenAI

DEFAULT_VOICE = "default_zh"  # 默认中文女声
DEFAULT_STYLE = "夹子音"       # 默认夹子音风格

def synthesize_speech(text: str, voice: str = DEFAULT_VOICE, style: str = None, output_path: str = None):
    """调用 MiMo TTS API 进行语音合成"""
    
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        # 尝试从配置文件读取
        config_path = os.path.expanduser("~/.openclaw/config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    api_key = config.get("mimo_api_key") or config.get("MIMO_API_KEY")
            except:
                pass
        
        if not api_key:
            print("错误: 请设置 MIMO_API_KEY 环境变量", file=sys.stderr)
            print("  export MIMO_API_KEY='你的API密钥'", file=sys.stderr)
            sys.exit(1)
    
    # 构建完整的style标签
    if style:
        full_text = f"<style>{style}</style>{text}"
    else:
        full_text = text
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.xiaomimimo.com/v1"
    )
    
    try:
        completion = client.chat.completions.create(
            model="mimo-v2-tts",
            messages=[
                {"role": "user", "content": "你好"},  # user消息可选，但可影响语气风格
                {"role": "assistant", "content": full_text}
            ],
            audio={"format": "wav", "voice": voice}
        )
        
        audio_data = completion.choices[0].message.audio.data
        audio_bytes = base64.b64decode(audio_data)
        
        if output_path:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            print(f"音频已保存到: {output_path}")
            return output_path
        else:
            # 返回字节数据
            return audio_bytes
            
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="小米 MiMo TTS 语音合成")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE, 
                        help=f"音色 (默认: {DEFAULT_VOICE})")
    parser.add_argument("--style", "-s", default=None,
                        help=f"风格标签，如: 夹子音、开心、东北话 等")
    parser.add_argument("--output", "-o", default=None,
                        help="输出文件路径 (默认: stdout)")
    parser.add_argument("--api-key", "-k", default=None,
                        help="API密钥 (也可通过 MIMO_API_KEY 环境变量设置)")
    
    args = parser.parse_args()
    
    if args.api_key:
        os.environ["MIMO_API_KEY"] = args.api_key
    
    # 如果没有指定style但用户提到夹子音，使用夹子音
    if not args.style:
        # 简单检测：如果文本里有～或者语气词多，用夹子音
        if "～" in args.text or "呀" in args.text or "啦" in args.text:
            args.style = DEFAULT_STYLE
    
    result = synthesize_speech(args.text, args.voice, args.style, args.output)
    
    if not args.output:
        # 输出到 stdout 作为二进制
        sys.stdout.buffer.write(result)


if __name__ == "__main__":
    main()
