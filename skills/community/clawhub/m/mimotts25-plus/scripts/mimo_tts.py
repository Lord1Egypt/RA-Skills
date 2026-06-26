#!/usr/bin/env python3
"""MiMo V2.5 TTS — 预置音色语音合成 (mimo-v2.5-tts)"""

import argparse
import base64
import os
import sys
from pathlib import Path

# 优先使用 openai 库（官方方式），fallback 到 urllib（兼容无 openai 环境）
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    import json
    import urllib.request

PRESET_VOICES = [
    "mimo_default", "冰糖", "茉莉", "苏打", "白桦",
    "Mia", "Chloe", "Milo", "Dean",
]

# 支持国内 token-plan-cn 集群和公网
API_BASE = os.getenv("MIMO_API_BASE", "https://token-plan-cn.xiaomimimo.com/v1")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MiMo V2.5 TTS 预置音色语音合成")
    parser.add_argument("--text", required=True, help="要合成的文本")
    parser.add_argument("--voice", required=True, choices=PRESET_VOICES, help="预置音色")
    parser.add_argument("--context", default="", help="自然语言风格控制指令 / 导演模式")
    parser.add_argument("--output",
                        default=os.getenv("MIMO_OUTPUT", "output.mp3"),
                        help="输出音频路径 (默认: output.mp3)")
    parser.add_argument("--format", default="mp3", choices=["wav", "mp3", "ogg"],
                        help="音频格式 (默认: mp3)")
    return parser.parse_args()


def _get_api_key() -> str:
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("MIMO_API_KEY is not set. Get your key at https://platform.xiaomimimo.com/", file=sys.stderr)
        sys.exit(1)
    return api_key


def _call_api_via_urllib(api_key: str, payload: dict) -> bytes:
    """使用 urllib 调用 API（备用路径，无需 openai 库）"""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{API_BASE}/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode(errors="replace")
        print(f"API error {exc.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"API call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    audio_b64 = body.get("choices", [{}])[0].get("message", {}).get("audio", {}).get("data")
    if not audio_b64:
        print("No audio data returned", file=sys.stderr)
        sys.exit(1)
    return base64.b64decode(audio_b64)


def main() -> None:
    args = parse_args()
    api_key = _get_api_key()
    fmt = args.format

    messages = []
    if args.context:
        messages.append({"role": "user", "content": args.context})
    messages.append({"role": "assistant", "content": args.text})

    payload = {
        "model": "mimo-v2.5-tts",
        "messages": messages,
        "audio": {"format": fmt, "voice": args.voice},
    }

    if HAS_OPENAI:
        client = OpenAI(api_key=api_key, base_url=API_BASE)
        try:
            completion = client.chat.completions.create(**payload)
        except Exception as exc:
            print(f"API call failed: {exc}", file=sys.stderr)
            sys.exit(1)
        message = completion.choices[0].message
        if message.audio is None or not getattr(message.audio, "data", None):
            print("No audio data returned", file=sys.stderr)
            sys.exit(1)
        audio_data = base64.b64decode(message.audio.data)
    else:
        audio_data = _call_api_via_urllib(api_key, payload)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio_data)
    print(output_path)


if __name__ == "__main__":
    main()
