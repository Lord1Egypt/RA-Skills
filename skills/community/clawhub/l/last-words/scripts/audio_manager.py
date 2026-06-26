#!/usr/bin/env python3
"""
Manage audio/voice message for last-words.
Usage:
  python3 audio_manager.py save /path/to/audio.wav
  python3 audio_manager.py record                    # Record from microphone
  python3 audio_manager.py list                      # List saved audio
  python3 audio_manager.py play                      # Play saved audio
"""

import argparse
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from database import get_message, save_message, init_db

AUDIO_DIR = Path.home() / ".openclaw" / "last-words" / "audio"

def ensure_audio_dir():
    """Create audio directory if not exists."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def save_audio(source_path: str):
    """Save audio file to storage."""
    ensure_audio_dir()

    source = Path(source_path)
    if not source.exists():
        print(f"✗ Audio file not found: {source_path}")
        return False

    # Copy to storage with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_name = f"last_words_{timestamp}{source.suffix}"
    dest = AUDIO_DIR / dest_name

    shutil.copy2(source, dest)

    # Update message with audio path
    message = get_message()
    text = message['content'] if message else "爸爸妈妈我爱你们"

    save_message(text, str(dest))

    print(f"✓ Audio saved: {dest}")
    print(f"  Original: {source}")
    print(f"  Size: {dest.stat().st_size / 1024:.1f} KB")
    return True


def record_audio():
    """Record audio from microphone."""
    ensure_audio_dir()

    # Check for recording tools
    recorder = None
    if shutil.which("arecord"):
        recorder = "arecord"
    elif shutil.which("rec"):
        recorder = "rec"
    elif shutil.which("ffmpeg"):
        recorder = "ffmpeg"
    else:
        print("✗ No audio recording tool found.")
        print("  Please install one of: sox, alsa-utils, ffmpeg")
        print("  Or use: save /path/to/existing/audio.wav")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = AUDIO_DIR / f"last_words_{timestamp}.wav"

    print("🎙️  Recording... Press Ctrl+C to stop")
    print("   Speak now (说你想对父母说的话)...")

    try:
        if recorder == "arecord":
            subprocess.run(["arecord", "-f", "cd", "-t", "wav", str(output)], check=True)
        elif recorder == "rec":
            subprocess.run(["rec", str(output)], check=True)
        elif recorder == "ffmpeg":
            subprocess.run(["ffmpeg", "-f", "alsa", "-i", "default", str(output)], check=True)

        print(f"\n✓ Recording saved: {output}")

        # Update message
        message = get_message()
        text = message['content'] if message else "爸爸妈妈我爱你们"
        save_message(text, str(output))
        print("✓ Audio attached to your message")
        return True

    except KeyboardInterrupt:
        print(f"\n✓ Recording saved: {output}")
        message = get_message()
        text = message['content'] if message else "爸爸妈妈我爱你们"
        save_message(text, str(output))
        return True
    except Exception as e:
        print(f"✗ Recording failed: {e}")
        return False


def list_audio():
    """List all saved audio files."""
    ensure_audio_dir()

    files = sorted(AUDIO_DIR.glob("*.wav")) + sorted(AUDIO_DIR.glob("*.mp3")) + sorted(AUDIO_DIR.glob("*.m4a"))

    if not files:
        print("No audio files found.")
        return

    print("Saved audio files:")
    for i, f in enumerate(files, 1):
        size = f.stat().st_size / 1024
        print(f"  {i}. {f.name} ({size:.1f} KB)")


def play_audio():
    """Play the saved audio."""
    message = get_message()
    if not message or not message.get('audio_path'):
        print("✗ No audio attached to message.")
        return

    audio_path = Path(message['audio_path'])
    if not audio_path.exists():
        print(f"✗ Audio file not found: {audio_path}")
        return

    player = None
    for cmd in ["aplay", "afplay", "mpg123", "ffplay"]:
        if shutil.which(cmd):
            player = cmd
            break

    if not player:
        print("✗ No audio player found. Install: aplay, afplay, mpg123, or ffplay")
        return

    print(f"▶️  Playing: {audio_path.name}")
    try:
        if player == "ffplay":
            subprocess.run([player, "-nodisp", "-autoexit", str(audio_path)], check=True)
        else:
            subprocess.run([player, str(audio_path)], check=True)
    except Exception as e:
        print(f"✗ Playback failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Manage voice/audio for last-words")
    subparsers = parser.add_subparsers(dest='command', help='Command')

    # save command
    save_parser = subparsers.add_parser('save', help='Save audio file')
    save_parser.add_argument('path', help='Path to audio file')

    # record command
    subparsers.add_parser('record', help='Record from microphone')

    # list command
    subparsers.add_parser('list', help='List saved audio files')

    # play command
    subparsers.add_parser('play', help='Play saved audio')

    args = parser.parse_args()

    init_db()

    if args.command == 'save':
        save_audio(args.path)
    elif args.command == 'record':
        record_audio()
    elif args.command == 'list':
        list_audio()
    elif args.command == 'play':
        play_audio()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
