#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
COMMAND_MAP = {
    "tts": SCRIPT_DIR / "minimax_tts.py",
    "music": SCRIPT_DIR / "minimax_music.py",
    "video": SCRIPT_DIR / "minimax_video.py",
    "image": SCRIPT_DIR / "minimax_image.py",
    "voice": SCRIPT_DIR / "minimax_voice.py",
}


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(
            """MiniMax unified CLI

Usage:
  python3 skills/minimax-tools/scripts/minimax.py tts   [args...]
  python3 skills/minimax-tools/scripts/minimax.py music [args...]
  python3 skills/minimax-tools/scripts/minimax.py video [args...]
  python3 skills/minimax-tools/scripts/minimax.py image [args...]
  python3 skills/minimax-tools/scripts/minimax.py voice [args...]

Examples:
  python3 skills/minimax-tools/scripts/minimax.py tts --text \"你好\" --voice \"Chinese (Mandarin)_Lyrical_Voice\"
  python3 skills/minimax-tools/scripts/minimax.py music --prompt \"lofi, rainy night\" --instrumental
  python3 skills/minimax-tools/scripts/minimax.py video create --prompt \"一只橘猫看雨\" --wait --download
  python3 skills/minimax-tools/scripts/minimax.py image --prompt \"赛博朋克城市夜景\" --aspect-ratio 16:9
  python3 skills/minimax-tools/scripts/minimax.py voice clone-from-files --clone-file voice.wav --voice-id MyVoice001 --text \"你好呀\" --download-demo
"""
        )
        return 0

    cmd = argv[0]
    target = COMMAND_MAP.get(cmd)
    if not target:
        print(f"Unknown subcommand: {cmd}", file=sys.stderr)
        print(f"Available: {', '.join(COMMAND_MAP)}", file=sys.stderr)
        return 2

    proc = subprocess.run([sys.executable, str(target), *argv[1:]], env=os.environ.copy())
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
