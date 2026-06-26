#!/usr/bin/env python3
"""
语音播报：用 SenseAudio TTS 合成并播放「物品位置」或「待办提醒」的语音。

用法:
  python speak.py --text "备用电池在电视柜左侧第二个抽屉"
  python speak.py --item 备用电池
  python speak.py --text "下午三点有会议，请提前准备" --play
  python speak.py --text "你好" --out reminder.mp3

选项:
  --text TEXT    要播报的文本（直接合成）
  --item NAME    从 items.json 查询物品位置，合成「XXX 在 YYY」并播报
  --out FILE     输出音频文件路径（默认临时文件）
  --play         合成后调用系统播放器播放（macOS: afplay, Windows: 默认播放器, Linux: paplay/aplay/ffplay）
  --voice ID     音色 ID，默认 male_0004_a

依赖: 环境变量 SENSEAUDIO_API_KEY；pip install requests
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: pip install requests", file=sys.stderr)
    sys.exit(1)

TTS_URL = "https://api.senseaudio.cn/v1/t2a_v2"
DEFAULT_VOICE = "male_0004_a"


def get_data_dir():
    """项目内 .memory-assistant 优先，否则 ~/.memory-assistant"""
    cwd = Path.cwd()
    project_data = cwd / ".memory-assistant"
    if project_data.exists():
        return project_data
    return Path.home() / ".memory-assistant"


def get_api_key():
    key = os.environ.get("SENSEAUDIO_API_KEY")
    if not key:
        print("Error: SENSEAUDIO_API_KEY not set in environment variables.", file=sys.stderr)
        sys.exit(1)
    return key


def tts_senseaudio(text: str, out_path: Path, api_key: str, voice_id: str = DEFAULT_VOICE) -> Path:
    """调用 SenseAudio TTS，将 text 合成为音频并写入 out_path。"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice_id},
    }
    r = requests.post(TTS_URL, headers=headers, json=body, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(data.get("base_resp", {}).get("status_msg", "TTS failed"))
    hex_audio = data.get("data", {}).get("audio")
    if not hex_audio:
        raise RuntimeError("No audio in response")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(bytes.fromhex(hex_audio))
    return out_path


def play_audio(filepath: Path) -> None:
    """用系统默认方式播放音频（macOS / Windows / Linux）。"""
    import platform
    import subprocess
    path = str(filepath.resolve())
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["afplay", path], check=True)
    elif system == "Windows":
        os.startfile(path)
    elif system == "Linux":
        for cmd in (["paplay", path], ["aplay", path], ["ffplay", "-nodisp", "-autoexit", path]):
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                return
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        print("Warning: no paplay/aplay/ffplay found, audio saved only.", file=sys.stderr)
    else:
        print("Warning: play not supported on this OS, audio saved only.", file=sys.stderr)


def find_item_location(item_name: str, data_dir: Path) -> str | None:
    """从 items.json 中查找物品位置，返回 'X 在 Y' 或 None。"""
    items_file = data_dir / "items.json"
    if not items_file.exists():
        return None
    try:
        import json
        raw = items_file.read_text(encoding="utf-8")
        data = json.loads(raw)
        items = data.get("items", [])
        item_name = item_name.strip()
        for rec in reversed(items):  # 优先最新记录
            if rec.get("item", "").strip() == item_name:
                loc = rec.get("location", "").strip()
                if loc:
                    return f"{item_name}在{loc}"
        return None
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="语音播报：物品位置或自定义文本")
    parser.add_argument("--text", type=str, help="要播报的文本")
    parser.add_argument("--item", type=str, help="物品名称，从 items.json 查位置并播报「X 在 Y」")
    parser.add_argument("--out", type=Path, default=None, help="输出音频路径（默认临时文件）")
    parser.add_argument("--play", action="store_true", help="合成后播放")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help=f"音色 ID，默认 {DEFAULT_VOICE}")
    args = parser.parse_args()

    if not args.text and not args.item:
        parser.error("请指定 --text 或 --item")

    if args.item:
        data_dir = get_data_dir()
        text = find_item_location(args.item, data_dir)
        if not text:
            print(f"未找到物品「{args.item}」的位置记录。", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text.strip()
        if not text:
            sys.exit(0)

    api_key = get_api_key()
    out_path = args.out or Path(tempfile.gettempdir()) / "memory_assistant_tts.mp3"
    tts_senseaudio(text, out_path, api_key, args.voice)
    print(out_path.resolve(), file=sys.stderr if args.play else sys.stdout)

    if args.play:
        play_audio(out_path)


if __name__ == "__main__":
    main()
