#!/usr/bin/env python3
"""
Voice Reply Skill - 语音回复技能
当用户说"语音回复"或"/voice"时，自动将回复转为语音气泡

依赖：
  pip install requests

环境变量（优先）或配置文件（二选一）：
  export MINIMAX_VOICE_API_KEY="your-api-key"
  
  或创建 config.txt 填入 API Key

用法：
  python voice_reply.py "要转换的文字" [输出路径]

输出：
  生成的OGG文件路径（直接打印到stdout）
"""

import os
import sys
import subprocess
import requests

# ========== 配置区 ==========
# MiniMax TTS API 端点
API_URL = "https://api.minimaxi.com/v1/t2a_v2"

# 默认输出路径
DEFAULT_OUTPUT = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "voice_reply.ogg")

# 默认音色（可修改）
DEFAULT_VOICE_ID = "male-qn-qingse"

# 配置文件路径（skill 根目录，与 SKILL.md 说明一致）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)  # 父目录 = skill 根目录
CONFIG_FILE = os.path.join(SKILL_DIR, "config.txt")
# ========== 配置区结束 ==========


def get_api_key():
    """获取 API Key，优先级：环境变量 > 配置文件"""
    # 优先从环境变量读取
    api_key = os.environ.get("MINIMAX_VOICE_API_KEY")
    if api_key:
        return api_key
    
    # 其次从配置文件读取
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    
    print(f"错误：未找到 API Key", file=sys.stderr)
    print(f"请设置环境变量 MINIMAX_VOICE_API_KEY 或创建 {CONFIG_FILE}", file=sys.stderr)
    sys.exit(1)


def tts_to_ogg(text, output_path=None, voice_id=None):
    """调用 MiniMax TTS API，输出 OGG 格式"""
    if output_path is None:
        output_path = DEFAULT_OUTPUT
    if voice_id is None:
        voice_id = DEFAULT_VOICE_ID
    
    api_key = get_api_key()
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Step 1: 调用 TTS API 获取 MP3
    mp3_path = output_path.replace(".ogg", ".mp3")
    
    request_data = {
        "model": "speech-2.8-hd",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id
        }
    }
    
    try:
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=request_data,
            timeout=60
        )
        result = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    if result.get("data", {}).get("status") != 2:
        print(f"API返回错误: {result}", file=sys.stderr)
        sys.exit(1)
    
    # 解码 hex → MP3
    audio_hex = result["data"]["audio"]
    audio_bytes = bytes.fromhex(audio_hex)
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)
    
    # Step 2: 转 OGG (Opus) - 先重采样到48000Hz（opus支持）
    ffmpeg_result = subprocess.run([
        "ffmpeg", "-i", mp3_path,
        "-c:a", "libopus", "-b:a", "128k",
        "-ar", "48000",
        output_path, "-y"
    ], capture_output=True, text=True)
    
    # 删除 MP3
    try:
        os.remove(mp3_path)
    except OSError:
        pass
    
    if ffmpeg_result.returncode != 0:
        print(f"FFmpeg转换失败: {ffmpeg_result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python voice_reply.py \"要转换的文字\" [输出路径]", file=sys.stderr)
        print("", file=sys.stderr)
        print("首次使用请先配置 API Key：", file=sys.stderr)
        print("  export MINIMAX_VOICE_API_KEY=\"your-api-key\"", file=sys.stderr)
        print(f"  或创建 {CONFIG_FILE} 填入 API Key", file=sys.stderr)
        sys.exit(1)
    
    text = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    result_path = tts_to_ogg(text, output)
    print(result_path)
