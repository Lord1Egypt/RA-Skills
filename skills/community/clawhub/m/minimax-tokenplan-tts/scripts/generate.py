#!/usr/bin/env python3
"""
MiniMax TTS (speech-2.8-hd) wrapper.

Usage:
  python3 generate.py --text "描述" [--voice male-qn-jingying] \
      [--speed 1.0] [--vol 1.0] [--pitch 1.0] \
      [--output /path/to/output.wav]

Rules:
  - text: 要转换的文本，最长 10000 字符，超出会报错
  - voice: 声优 ID，默认 male-qn-jingying，共327个音色（完整列表见 SKILL.md）
    - 常用：male-qn-jingying（精英青年）、female-tianmei（甜美女性）、male-qn-badao（霸道青年）
  - speed: 语速 0.5-2.0，默认 1.0
  - vol: 音量 0-10（0不含），默认 1.0
  - pitch: 音调 -12 到 12，默认 0
  - audio_setting: 固定值 sample_rate=32000, bitrate=128000, format=wav, channel=1
  - API 返回的 audio 字段是 HEX 编码（不是 base64），脚本自动解码
  - 输出: WAV 格式，32000Hz，128kbps，mono，16-bit PCM
  - 输出文件名: tts-YYYY-MM-DD-slug.wav
  - subtitle_enable: 固定 False（不生成字幕）
  - 输出目录: ~/.openclaw/media/minimax/tts/
"""

import argparse
import json
import os
import re
import sys
import wave
from datetime import date

try:
    import requests
except ImportError:
    print("[ERROR] 缺少 requests 库，请运行: pip3 install requests", file=sys.stderr)
    sys.exit(1)

# ------------------ 配置区（可被命令行参数覆盖）------------------
# TODO: 初始化时填入实际值
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.minimaxi.com"  # CN: api.minimaxi.com
# ----------------------------------------------------------------

DEFAULT_VOICE = "male-qn-jingying"
DEFAULT_SPEED = 1.0
DEFAULT_VOL = 1.0
DEFAULT_PITCH = 0
OUTPUT_DIR = os.path.expanduser("~/.openclaw/media/minimax/tts/")

# ------------------ 常用声优（不完整，仅供参考）------------------
# 完整327个音色列表见 SKILL.md 中的 ## 音色列表
# 以下列出最常用的几个，实际使用时参考 SKILL.md 选择
COMMON_VOICES = {
    "male-qn-jingying": "精英青年音色（推荐）",
    "female-tianmei": "甜美女性音色",
    "male-qn-badao": "霸道青年音色",
    "female-yujie": "御姐音色",
    "male-qn-daxuesheng": "青年大学生音色",
    "female-shaonv": "少女音色",
}


def make_slug(text: str) -> str:
    """将 text 转换为 safe 文件名：取前20字符，保留中文、英文、数字。

    注意：Python 3 的 isalnum() 对中文返回 True，因此中文字符会被保留在文件名中。
    这在 macOS/Linux 上通常没有问题。如需纯 ASCII，请改用 c.isascii() and c.isalnum()。
    """
    slug = text[:20]
    slug = slug.replace(" ", "-")
    slug = ''.join(c for c in slug if c.isalnum() or c in '-_')
    slug = slug[:40] or "tts"
    return slug


def generate(
    text: str,
    output: str = None,
    voice: str = DEFAULT_VOICE,
    speed: float = DEFAULT_SPEED,
    vol: float = DEFAULT_VOL,
    pitch: float = DEFAULT_PITCH,
    api_key: str = API_KEY,
    base_url: str = BASE_URL,
    timeout: int = 60,
):
    """调用 MiniMax TTS API，生成语音文件。"""

    # 检查 API Key 是否已配置
    if api_key == "YOUR_API_KEY_HERE" or not api_key:
        print("[ERROR] API Key 未配置，请先运行 init 流程", file=sys.stderr)
        sys.exit(1)

    # 参数校验
    if not text or len(text.strip()) == 0:
        print("[ERROR] 文本不能为空", file=sys.stderr)
        sys.exit(1)

    if len(text) > 10000:
        print(f"[ERROR] 文本长度 {len(text)} 超过 10000 字符限制", file=sys.stderr)
        sys.exit(1)

    if voice not in COMMON_VOICES:
        # 不在常用列表里不报错，由 API 验证是否支持
        print(f"[WARN] 非常见声优: {voice}，由 API 验证是否支持", file=sys.stderr)

    # 构建请求 payload
    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "wav",
            "channel": 1,
        },
        "subtitle_enable": False,
    }

    voice_name = COMMON_VOICES.get(voice, voice)
    print(f"[INFO] 使用声优: {voice} ({voice_name})", file=sys.stderr)
    print(f"[INFO] 语速: {speed}, 音量: {vol}, 音调: {pitch}", file=sys.stderr)
    print(f"[INFO] 采样率: 32000Hz, bitrate: 128000", file=sys.stderr)

    # 发送请求
    try:
        resp = requests.post(
            f"{base_url}/v1/t2a_v2",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
    except Exception as e:
        print(f"[ERROR] 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 解析响应
    try:
        data = resp.json()
    except Exception as e:
        print(f"[ERROR] 响应解析失败: {e}", file=sys.stderr)
        print(f"[ERROR] 响应内容: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        code = data.get("base_resp", {}).get("status_code", resp.status_code)
        msg = data.get("base_resp", {}).get("status_msg", resp.text)
        print(f"[ERROR] API 返回错误: code={code}, msg={msg}", file=sys.stderr)
        # 错误码友好提示
        error_messages = {
            1002: "限流，请稍后重试",
            1004: "鉴权失败，请检查 API Key",
            1008: "余额不足，请充值",
            2049: "无效 Key，请检查 API Key",
        }
        if code in error_messages:
            print(f"[HINT] {error_messages[code]}", file=sys.stderr)
        sys.exit(1)

    # 检查业务状态码（在 base_resp.status_code 中，0 表示成功）
    base_resp = data.get("base_resp", {})
    status_code = base_resp.get("status_code")
    if status_code is not None and status_code != 0:
        msg = base_resp.get("status_msg", "未知错误")
        print(f"[ERROR] API 返回: code={status_code}, msg={msg}", file=sys.stderr)
        sys.exit(1)

    # 提取 audio 字段（HEX 编码，不是 base64）
    audio_hex = data.get("data", {}).get("audio")
    if not audio_hex:
        print("[ERROR] 响应中缺少 audio 字段", file=sys.stderr)
        sys.exit(1)

    # HEX 解码为 bytes
    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except Exception as e:
        print(f"[ERROR] HEX 解码失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 音频大小: {len(audio_bytes)} bytes ({len(audio_hex)} hex chars)", file=sys.stderr)

    # 生成输出路径
    if output is None:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        slug = make_slug(text)
        today = date.today().isoformat()
        output = os.path.join(OUTPUT_DIR, f"tts-{today}-{slug}.wav")

    # 确保输出目录存在
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 写入 WAV 文件（自动检测：如已是完整 WAV 则直接写入，否则包装 PCM 为 WAV）
    try:
        if audio_bytes[:4] == b'RIFF':
            # 已是完整 WAV 文件，直接写入
            with open(output, 'wb') as f:
                f.write(audio_bytes)
        else:
            # Raw PCM 数据，包装成 WAV
            with wave.open(output, 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit = 2 bytes
                wav_file.setframerate(32000)
                wav_file.writeframes(audio_bytes)
        print(f"[SUCCESS] 音频已保存: {output}", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] 保存文件失败: {e}", file=sys.stderr)
        sys.exit(1)

    return output


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax TTS - Text to Speech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="要转换的文本（最长 10000 字符）"
    )
    parser.add_argument(
        "--voice", "-v",
        default=DEFAULT_VOICE,
        help=f"声优 ID（默认: {DEFAULT_VOICE}），完整列表见 SKILL.md"
    )
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=DEFAULT_SPEED,
        help=f"语速 0.5-2.0（默认: {DEFAULT_SPEED}）"
    )
    parser.add_argument(
        "--vol",
        type=float,
        default=DEFAULT_VOL,
        help=f"音量 0-10（默认: {DEFAULT_VOL}）"
    )
    parser.add_argument(
        "--pitch",
        type=float,
        default=DEFAULT_PITCH,
        help=f"音调 -12 到 12（默认: {DEFAULT_PITCH}）"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出路径（默认自动生成）"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API Key（默认使用文件顶部配置）"
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="API Base URL（默认使用文件顶部配置）"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="API 请求超时时间（秒，默认: 60）"
    )

    args = parser.parse_args()

    # 覆盖全局配置
    final_api_key = args.api_key if args.api_key else API_KEY
    final_base_url = args.base_url if args.base_url else BASE_URL

    # 验证参数范围
    if not 0.5 <= args.speed <= 2.0:
        print("[ERROR] 语速必须在 0.5-2.0 之间", file=sys.stderr)
        sys.exit(1)
    if not 0 < args.vol <= 10:
        print("[ERROR] 音量必须在 0-10 之间（0不含）", file=sys.stderr)
        sys.exit(1)
    if not -12 <= args.pitch <= 12:
        print("[ERROR] 音调必须在 -12 到 12 之间", file=sys.stderr)
        sys.exit(1)

    output_path = generate(
        text=args.text,
        output=args.output,
        voice=args.voice,
        speed=args.speed,
        vol=args.vol,
        pitch=args.pitch,
        api_key=final_api_key,
        base_url=final_base_url,
        timeout=args.timeout,
    )

    # stdout 只输出路径（方便调用方捕获）
    print(output_path)


if __name__ == "__main__":
    main()
