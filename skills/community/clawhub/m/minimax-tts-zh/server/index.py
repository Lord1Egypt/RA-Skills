#!/usr/bin/env python3
"""
MiniMax TTS CLI
用法:
    python3 index.py tts --text "文字" [--voice female-tianmei-jingpin] [--speed 1.0] [--output /path/to/output.mp3]
    python3 index.py voices
    python3 index.py save-token --token "your-token"
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, '.env')

VOICES = {
    'female-tianmei-jingpin': '甜美女声 ★精品',
    'female-yujie-jingpin': '御姐 ★精品',
    'male-qn-badao-jingpin': '霸道总裁 ★精品',
    'Chinese (Mandarin)_News_Anchor': '新闻女声',
    'Chinese (Mandarin)_Male_Announcer': '新闻男声',
    'Chinese (Mandarin)_Radio_Host': '电台男声',
}


def load_env():
    if not os.path.exists(ENV_FILE):
        return
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, val = line.partition('=')
            key = key.strip()
            val = val.strip()
            if key and key not in os.environ:
                os.environ[key] = val


def get_token(args):
    return args.get('--token') or os.environ.get('MINIMAX_API_TOKEN')


def cmd_tts(args):
    load_env()

    text = args.get('--text')
    voice = args.get('--voice') or 'female-tianmei-jingpin'
    speed = float(args.get('--speed') or 1.0)
    vol = float(args.get('--vol') or 1.0)
    pitch = int(args.get('--pitch') or 0)
    output = args.get('--output') or f'/tmp/openclaw/tts_{int(time.time())}.mp3'
    token = get_token(args)

    if not text:
        print("错误: --text 参数必填", file=sys.stderr)
        sys.exit(1)

    if not token:
        print("错误: 请先运行 save-token --token <your-token> 或设置 MINIMAX_API_TOKEN", file=sys.stderr)
        sys.exit(1)

    # 限制参数范围
    speed = max(0.5, min(2.0, speed))
    vol = max(0.1, min(2.0, vol))
    pitch = max(-12, min(12, pitch))

    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "voice_setting": {
            "voice_id": voice,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }

    print(f"正在生成音频: {text[:30]}{'...' if len(text) > 30 else ''}")
    print(f"音色: {VOICES.get(voice, voice)}, 语速: {speed}")

    try:
        req = urllib.request.Request(
            "https://api.minimaxi.com/v1/t2a_v2",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"HTTP错误 {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    audio_hex = result.get("data", {}).get("audio", "")
    if not audio_hex:
        msg = result.get("base_resp", {}).get("status_msg", "未知错误")
        print(f"错误: {msg}", file=sys.stderr)
        sys.exit(1)

    audio_bytes = bytes.fromhex(audio_hex)
    with open(output, 'wb') as f:
        f.write(audio_bytes)

    size_kb = len(audio_bytes) // 1024
    print(f"成功! 已保存到: {output} ({size_kb} KB)")


def cmd_voices(args):
    load_env()
    token = get_token(args)

    if token:
        masked = token[:6] + '...' + token[-4:] if len(token) > 10 else '***'
        print(f"Token 状态: 已配置 ({masked})")
    else:
        print("Token 状态: 未配置（请运行 save-token --token <your-token>）")

    print("\n可用音色列表：")
    for i, (vid, name) in enumerate(VOICES.items(), 1):
        print(f"{i}. {vid} - {name}")


def cmd_save_token(args):
    token = args.get('--token')
    if not token:
        print("错误: --token 参数必填", file=sys.stderr)
        sys.exit(1)

    lines = []
    token_written = False
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith('MINIMAX_API_TOKEN='):
                    lines.append(f'MINIMAX_API_TOKEN={token}\n')
                    token_written = True
                else:
                    lines.append(line)

    if not token_written:
        lines.append(f'MINIMAX_API_TOKEN={token}\n')

    with open(ENV_FILE, 'w') as f:
        f.writelines(lines)

    masked = token[:6] + '...' + token[-4:] if len(token) > 10 else '***'
    print(f"Token 已保存 ({masked})")


def parse_args(argv):
    """解析 --key value 格式参数，正确处理负数值"""
    args = {}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg.startswith('--'):
            # 下一个 token 是值：不以 -- 开头，或者是负数
            if i + 1 < len(argv):
                nxt = argv[i + 1]
                is_value = not nxt.startswith('--') or (len(nxt) > 1 and nxt[1:2].lstrip('-').isdigit())
                if is_value:
                    args[arg] = nxt
                    i += 2
                    continue
            args[arg] = 'true'
            i += 1
        else:
            i += 1
    return args


def main():
    if len(sys.argv) < 2:
        print("用法: python3 index.py <command> [选项]")
        print("命令: tts, voices, save-token")
        sys.exit(1)

    cmd = sys.argv[1]
    args = parse_args(sys.argv[2:])

    if cmd == 'tts':
        cmd_tts(args)
    elif cmd == 'voices':
        cmd_voices(args)
    elif cmd == 'save-token':
        cmd_save_token(args)
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        print("可用命令: tts, voices, save-token", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
