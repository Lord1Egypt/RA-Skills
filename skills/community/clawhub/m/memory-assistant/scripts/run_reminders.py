#!/usr/bin/env python3
"""
定时提醒播报：检查 reminders.json 中到点的提醒，用 SenseAudio TTS 合成并播放语音，并将状态标为已播报。

用法:
  python run_reminders.py              # 单次检查并播报到点提醒
  python run_reminders.py --daemon    # 常驻，每分钟检查一次
  python run_reminders.py --dry-run   # 只列出将播报的提醒，不请求 TTS

数据目录：项目 .memory-assistant/ 或 ~/.memory-assistant/，与 speak.py 一致。
依赖: 环境变量 SENSEAUDIO_API_KEY；pip install requests
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: pip install requests", file=sys.stderr)
    sys.exit(1)

TTS_URL = "https://api.senseaudio.cn/v1/t2a_v2"
DEFAULT_VOICE = "male_0004_a"


def get_data_dir():
    """与 speak.py 一致：项目 .memory-assistant 优先，否则 ~/.memory-assistant"""
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


def load_reminders(data_dir: Path) -> list:
    path = data_dir / "reminders.json"
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    return data.get("reminders", [])


def save_reminders(data_dir: Path, reminders: list) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "reminders.json"
    path.write_text(json.dumps({"reminders": reminders}, ensure_ascii=False, indent=2), encoding="utf-8")


def tts_and_save(text: str, out_path: Path, api_key: str, voice_id: str = DEFAULT_VOICE) -> Path:
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


def now_utc():
    return datetime.now(timezone.utc)


def parse_notify_at(s: str) -> datetime | None:
    """将 ISO 字符串转为可比较的 datetime（带时区或视为本地）。"""
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def run_once(data_dir: Path, api_key: str, dry_run: bool, voice_id: str) -> int:
    reminders = load_reminders(data_dir)
    now = now_utc()
    to_notify = []
    for r in reminders:
        if r.get("status") != "pending":
            continue
        notify_at = parse_notify_at(r.get("notify_at") or r.get("at"))
        if notify_at and notify_at <= now:
            to_notify.append(r)

    if not to_notify:
        return 0

    for r in to_notify:
        event = r.get("event", "提醒")
        text = f"提醒：{event}"
        if dry_run:
            print(f"[dry-run] would speak: {text}", file=sys.stderr)
            continue
        out_path = data_dir / "audio" / f"reminder_{r.get('id', '')}.mp3"
        try:
            tts_and_save(text, out_path, api_key, voice_id)
            play_audio(out_path)
        except Exception as e:
            print(f"TTS/play failed for reminder {r.get('id')}: {e}", file=sys.stderr)
            continue
        r["status"] = "notified"

    if not dry_run and to_notify:
        save_reminders(data_dir, reminders)
    return len(to_notify)


def main():
    parser = argparse.ArgumentParser(description="检查到点提醒并语音播报")
    parser.add_argument("--daemon", action="store_true", help="常驻运行，每分钟检查一次")
    parser.add_argument("--dry-run", action="store_true", help="只列出将播报的提醒，不调用 TTS")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help=f"音色 ID，默认 {DEFAULT_VOICE}")
    parser.add_argument("--interval", type=int, default=60, help="daemon 模式下检查间隔（秒），默认 60")
    args = parser.parse_args()

    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    api_key = get_api_key() if not args.dry_run else ""

    if args.daemon:
        while True:
            n = run_once(data_dir, api_key, args.dry_run, args.voice)
            if n > 0:
                print(f"Played {n} reminder(s).", file=sys.stderr)
            time.sleep(args.interval)
    else:
        run_once(data_dir, api_key, args.dry_run, args.voice)


if __name__ == "__main__":
    main()
