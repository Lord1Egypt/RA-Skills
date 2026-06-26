from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from helper import (
    LANG_VOICE_MAP,
    DEFAULT_VOICE,
    synthesize as _helper_synthesize,
    concat as _helper_concat,
)
from feishu_api import list_chats, send_audio_message, upload_opus_file

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def resolve_voice(lang, voice) -> str:
    if voice:
        return voice
    if lang:
        return LANG_VOICE_MAP.get(lang, DEFAULT_VOICE)
    return DEFAULT_VOICE


def _synthesize_text(text, voice_id, speed, pitch, vol, output_path, fmt="wav", sample_rate=24000):
    """Helper: write text to temp file, call helper.py synthesize, return output path."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", encoding="utf-8", delete=False
    ) as tf:
        tf.write(text)
        text_file = tf.name

    try:
        synth_args = argparse.Namespace(
            text_file=text_file,
            voice_id=voice_id,
            speed=speed,
            pitch=pitch,
            vol=vol,
            format=fmt,
            sample_rate=sample_rate,
            bitrate=None,
            channel=1,
            output=output_path,
            debug_log=None,
        )
        _helper_synthesize(synth_args)
    finally:
        try:
            os.unlink(text_file)
        except OSError:
            pass
    return output_path


def _convert_wav_to_opus(input_wav, output_opus=None):
    """Convert WAV to OPUS via ffmpeg."""
    input_path = Path(input_wav).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"WAV file not found: {input_path}")
    opus_path = Path(output_opus).resolve() if output_opus else input_path.with_suffix(".opus")
    opus_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-c:a", "libopus", "-b:a", "32k",
        str(opus_path),
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg WAV->OPUS failed:\n{result.stderr}")
    return str(opus_path)


def cmd_setup(_: argparse.Namespace) -> None:
    print("=== language-helper setup check ===")
    print(f"python3:           {shutil.which('python3') or 'NOT FOUND'}")
    print(f"ffmpeg:            {shutil.which('ffmpeg') or 'NOT FOUND'}")
    print(f"SENSEAUDIO_API_KEY: {'SET' if os.getenv('SENSEAUDIO_API_KEY') else 'NOT SET'}")
    print(f"FEISHU_APP_ID:      {'SET' if os.getenv('FEISHU_APP_ID') else 'NOT SET'}")
    print(f"FEISHU_APP_SECRET:  {'SET' if os.getenv('FEISHU_APP_SECRET') else 'NOT SET'}")
    print(f"FEISHU_CHAT_ID:     {'SET' if os.getenv('FEISHU_CHAT_ID') else 'NOT SET'}")
    print()
    if not os.getenv("SENSEAUDIO_API_KEY"):
        print("Missing SENSEAUDIO_API_KEY:")
        print("  1. Visit https://senseaudio.cn and sign up")
        print("  2. Get your API key from the dashboard")
        print("  3. Add to skills/language-helper/.env:")
        print("     SENSEAUDIO_API_KEY=your_key")
    if not os.getenv("FEISHU_APP_ID"):
        print("Missing Feishu credentials:")
        print("  1. Create app at https://open.feishu.cn/app")
        print("  2. Enable Bot capability")
        print("  3. Add permissions: im:message:send_as_bot, im:resource")
        print("  4. Add to skills/language-helper/.env:")
        print("     FEISHU_APP_ID=cli_xxx")
        print("     FEISHU_APP_SECRET=xxx")
        print("     FEISHU_CHAT_ID=oc_xxx")
        print()
        print("Tip: run `python3 main.py list-chats` to find your chat_id")


def cmd_list_chats(_: argparse.Namespace) -> None:
    chats = list_chats()
    if not chats:
        print("No chats found. Make sure the bot is added to a group or someone has messaged the bot 1-on-1.")
        return
    print(f"Found {len(chats)} chat(s):\n")
    for c in chats:
        mode = "p2p (1-on-1)" if c["chat_mode"] == "p2p" else c["chat_mode"]
        print(f"  chat_id: {c['chat_id']}")
        print(f"  name:    {c['name']}")
        print(f"  type:    {mode}")
        print()
    print("Copy the chat_id you want and add to .env:")
    print("  FEISHU_CHAT_ID=oc_xxx")


def cmd_speak(args: argparse.Namespace) -> None:
    """Synthesize text and play audio locally via afplay/ffplay."""
    text = args.text.strip()
    if not text:
        print("Error: text is empty", file=sys.stderr)
        sys.exit(1)

    voice_id = resolve_voice(args.lang, args.voice)
    output_path = args.out or str(OUTPUT_DIR / "reply.wav")

    _synthesize_text(text, voice_id, args.speed, args.pitch, args.vol, output_path,
                     fmt=args.format, sample_rate=args.sample_rate)

    if not args.no_play:
        _play_audio(output_path)


def cmd_send_voice(args: argparse.Namespace) -> None:
    """TTS + convert to OPUS + send as Feishu native voice bar."""
    text = args.text.strip()
    if not text:
        print("Error: text is empty", file=sys.stderr)
        sys.exit(1)

    chat_id = args.chat_id or os.getenv("FEISHU_CHAT_ID")
    if not chat_id:
        print(
            "Error: chat_id is required.\n"
            "Pass --chat-id oc_xxx or set FEISHU_CHAT_ID in .env",
            file=sys.stderr,
        )
        sys.exit(1)

    voice_id = resolve_voice(args.lang, args.voice)
    base_name = "flashcard_reply"
    wav_out = str(OUTPUT_DIR / f"{base_name}.wav")
    opus_out = str(OUTPUT_DIR / f"{base_name}.opus")

    # 1. TTS -> WAV
    _synthesize_text(text, voice_id, args.speed, args.pitch, args.vol, wav_out)

    # 2. WAV -> OPUS
    opus_path = _convert_wav_to_opus(wav_out, opus_out)

    # 3. Upload OPUS to Feishu
    upload = upload_opus_file(opus_path, file_name=f"{base_name}.opus")

    # 4. Send native voice bar
    send_audio_message(chat_id=chat_id, file_key=upload["file_key"])
    print(f"Voice message sent to {chat_id}")


def _play_audio(path: str) -> None:
    """Play audio file using system player."""
    if sys.platform == "darwin":
        player = shutil.which("afplay")
        if player:
            subprocess.run([player, path], check=False)
            return
    player = shutil.which("ffplay")
    if player:
        subprocess.run([player, "-nodisp", "-autoexit", path], check=False)
        return
    print(f"[LanguageHelper] No audio player found. Audio saved to: {path}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Language Helper (SenseAudio TTS + Feishu)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # setup
    p = sub.add_parser("setup", help="Check environment")
    p.set_defaults(func=cmd_setup)

    # list-chats
    p = sub.add_parser("list-chats", help="List all chats the bot has joined, find your chat_id")
    p.set_defaults(func=cmd_list_chats)

    # speak — synthesize + play locally
    p = sub.add_parser("speak", help="Synthesize text and play locally")
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--out", "-o", default=None, help="Output audio path")
    p.add_argument("--lang", "-l", choices=list(LANG_VOICE_MAP.keys()))
    p.add_argument("--voice", "-v", help="Voice ID override")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--pitch", type=int, default=0)
    p.add_argument("--vol", type=float, default=1.0)
    p.add_argument("--format", default="wav")
    p.add_argument("--sample-rate", type=int, default=24000)
    p.add_argument("--no-play", action="store_true", help="Skip auto-play")
    p.set_defaults(func=cmd_speak)

    # send-voice — TTS + Feishu voice bar
    p = sub.add_parser("send-voice", help="TTS + send as Feishu native voice bar")
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--chat-id")
    p.add_argument("--lang", "-l", choices=list(LANG_VOICE_MAP.keys()))
    p.add_argument("--voice", "-v", help="Voice ID override")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--pitch", type=int, default=0)
    p.add_argument("--vol", type=float, default=1.0)
    p.set_defaults(func=cmd_send_voice)

    # synthesize — raw helper.py synthesize (text-file based)
    synth = sub.add_parser("synthesize", help="Send a TTS request and save audio (text-file input)")
    synth.add_argument("--text-file", required=True)
    synth.add_argument("--voice-id", required=True)
    synth.add_argument("--speed", type=float)
    synth.add_argument("--pitch", type=int)
    synth.add_argument("--vol", type=float)
    synth.add_argument("--format")
    synth.add_argument("--sample-rate", type=int)
    synth.add_argument("--bitrate", type=int)
    synth.add_argument("--channel", type=int)
    synth.add_argument("--output", required=True)
    synth.add_argument("--debug-log")
    synth.set_defaults(func=_helper_synthesize)

    # concat
    merge = sub.add_parser("concat", help="Concatenate audio segments with ffmpeg")
    merge.add_argument("--output", required=True)
    merge.add_argument("inputs", nargs="+")
    merge.set_defaults(func=_helper_concat)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
