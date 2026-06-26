#!/usr/bin/env python3
"""TTS entrypoint — replaces tts.sh.

Supports Python 3.6-3.11.
Default mode: speak (no subcommand required).
Other subcommands: render, to-srt, config
"""
import argparse
import base64
import binascii
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

NOIZ_KEY_FILE = Path.home() / ".config" / "noiz" / "api_key"
_LEGACY_KEY_FILE = Path.home() / ".noiz_api_key"
DEFAULT_NOIZ_REF_AUDIO_URL_CN = (
    "https://storage.googleapis.com/noiz_audio_public/resource/audio/ref_cn_fm1.WAV"
)
DEFAULT_NOIZ_REF_AUDIO_URL_EN = (
    "https://noiz.ai/resource/img/tts/landing_creative1.mp3"
)

# ── API key helpers ───────────────────────────────────────────────────


def normalize_api_key_base64(value: str) -> str:
    key = value.strip()
    if not key:
        return key
    padded = key + ("=" * (-len(key) % 4))
    try:
        decoded = base64.b64decode(padded, validate=True)
        canonical = base64.b64encode(decoded).decode("ascii").rstrip("=")
        if decoded and canonical == key.rstrip("="):
            return key
    except binascii.Error:
        pass
    return base64.b64encode(key.encode("utf-8")).decode("ascii")


def _migrate_legacy_key() -> None:
    """One-time migration from ~/.noiz_api_key to XDG path (non-destructive)."""
    if _LEGACY_KEY_FILE.exists() and not NOIZ_KEY_FILE.exists():
        NOIZ_KEY_FILE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        raw = _LEGACY_KEY_FILE.read_text(encoding="utf-8").strip()
        if raw:
            NOIZ_KEY_FILE.write_text(raw, encoding="utf-8")
            os.chmod(str(NOIZ_KEY_FILE), 0o600)
        print(
            "[config] Copied API key from {} to {}. "
            "You can remove the old file manually if desired.".format(
                _LEGACY_KEY_FILE, NOIZ_KEY_FILE
            ),
            file=sys.stderr,
        )


def load_api_key() -> Optional[str]:
    env_key = os.environ.get("NOIZ_API_KEY", "")
    if env_key:
        normalized = normalize_api_key_base64(env_key)
        os.environ["NOIZ_API_KEY"] = normalized
        return normalized
    _migrate_legacy_key()
    if NOIZ_KEY_FILE.exists():
        mode = NOIZ_KEY_FILE.stat().st_mode & 0o777
        if mode & 0o077:
            print(
                "[security] Warning: {} has too-open permissions ({:o}). "
                "Fixing to 600.".format(NOIZ_KEY_FILE, mode),
                file=sys.stderr,
            )
            os.chmod(str(NOIZ_KEY_FILE), 0o600)
        raw = NOIZ_KEY_FILE.read_text(encoding="utf-8").strip()
        if raw:
            normalized = normalize_api_key_base64(raw)
            os.environ["NOIZ_API_KEY"] = normalized
            return normalized
    return None


def save_api_key(key: str) -> None:
    normalized = normalize_api_key_base64(key)
    NOIZ_KEY_FILE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    NOIZ_KEY_FILE.write_text(normalized, encoding="utf-8")
    os.chmod(str(NOIZ_KEY_FILE), 0o600)


# ── Backend detection ─────────────────────────────────────────────────


def detect_backend(explicit: str = "") -> str:
    if explicit:
        return explicit
    return "noiz" if load_api_key() else "noiz-guest"


# ── Misc utilities ────────────────────────────────────────────────────


def mktemp_suffixed(suffix: str) -> Path:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return Path(path)


def unlink_silent(path: Optional[Path]) -> None:
    if path is None:
        return
    try:
        path.unlink()
    except OSError:
        pass


def ensure_noiz_ready() -> None:
    if importlib.util.find_spec("requests") is None:
        print(
            "Error: 'requests' package is required for Noiz backend but not installed.\n"
            "  Install it with:  uv pip install requests\n"
            "  Or use the local Kokoro backend:  --backend kokoro",
            file=sys.stderr,
        )
        raise SystemExit(1)


def detect_text_lang(text: str) -> str:
    if re.search(r"[\u4e00-\u9fff\u3400-\u4dbf]", text):
        return "zh"
    return "en"


def prepare_ref_audio(ref_audio_input: str) -> str:
    """Download ref audio if URL; return local path."""
    if ref_audio_input.startswith("http://") or ref_audio_input.startswith("https://"):
        import urllib.request

        tmp = mktemp_suffixed(".wav")
        print(
            "[noiz] Downloading reference audio: {}".format(ref_audio_input),
            file=sys.stderr,
        )
        urllib.request.urlretrieve(ref_audio_input, str(tmp))
        return str(tmp)
    return ref_audio_input


def play_audio(path: str) -> None:
    for player in ("afplay", "aplay", "paplay"):
        if shutil.which(player):
            print("[tts] Playing audio...", file=sys.stderr)
            subprocess.call([player, path])
            return
    print(
        "[tts] No audio player found (tried afplay, aplay, paplay). "
        "Audio saved to: {}".format(path),
        file=sys.stderr,
    )


# ── speak ─────────────────────────────────────────────────────────────


def cmd_speak(args: argparse.Namespace) -> int:
    fmt = "opus" if args.format == "ogg" else args.format

    play_mode = args.output is None
    tmp_output = None  # type: Optional[Path]
    if play_mode:
        tmp_output = mktemp_suffixed(".wav")
        output = str(tmp_output)
    else:
        output = args.output

    if not args.text and not args.text_file:
        print("Error: --text (-t) or --text-file (-f) is required.", file=sys.stderr)
        return 1

    backend = detect_backend(args.backend or "")

    # ── kokoro ──────────────────────────────────────────────────────
    if backend == "kokoro":
        input_path = args.text_file
        tmp_input = None  # type: Optional[Path]
        if args.text:
            tmp_input = mktemp_suffixed(".txt")
            tmp_input.write_text(args.text, encoding="utf-8")
            input_path = str(tmp_input)

        cmd = ["kokoro-tts", input_path, output, "--format", fmt]  # type: List[str]
        if args.voice:
            cmd += ["--voice", args.voice]
        if args.lang:
            cmd += ["--lang", args.lang]
        if args.speed is not None:
            cmd += ["--speed", str(args.speed)]

        try:
            subprocess.check_call(cmd)
        finally:
            unlink_silent(tmp_input)

    # ── noiz-guest ───────────────────────────────────────────────────
    elif backend == "noiz-guest":
        ensure_noiz_ready()
        if not args.voice_id:
            print(
                "Error: --voice-id is required in guest mode (no API key configured).",
                file=sys.stderr,
            )
            print("", file=sys.stderr)
            print(
                "  To unlock all features (voice cloning, emotion, etc.), "
                "configure your API key:",
                file=sys.stderr,
            )
            print(
                "    1. Get your API key from https://developers.noiz.ai/api-keys",
                file=sys.stderr,
            )
            print(
                "    2. Run: python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY",
                file=sys.stderr,
            )
            print("", file=sys.stderr)
            print("  Or use Kokoro for offline local TTS:", file=sys.stderr)
            print("    uv tool install kokoro-tts", file=sys.stderr)
            print("    Then pass --backend kokoro", file=sys.stderr)
            return 1

        print(
            "[noiz-guest] Using guest mode (limited features, no API key required)",
            file=sys.stderr,
        )
        from noiz_tts import synthesize_guest as _noiz_guest_synthesize

        text = args.text
        if not text and args.text_file:
            text = Path(args.text_file).read_text(encoding="utf-8").strip()
        _noiz_guest_synthesize(
            base_url="https://noiz.ai/v1",
            text=text,
            voice_id=args.voice_id,
            output_format=fmt,
            speed=args.speed or 1.0,
            timeout=120,
            out_path=Path(output),
        )

    # ── noiz (authenticated) ─────────────────────────────────────────
    else:
        api_key = load_api_key()
        if not api_key:
            print("Error: NOIZ_API_KEY not configured.", file=sys.stderr)
            print(
                "  Get your key at https://developers.noiz.ai/api-keys", file=sys.stderr
            )
            print(
                "  Then run: python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY",
                file=sys.stderr,
            )
            return 1
        ensure_noiz_ready()

        ref_audio = args.ref_audio or ""
        downloaded_ref_path = None  # type: Optional[str]

        if not args.voice_id and not ref_audio:
            ref_lang = args.lang or ""
            if not ref_lang:
                sample = args.text or ""
                if not sample and args.text_file:
                    with open(args.text_file, encoding="utf-8") as f:
                        sample = f.read(500)
                ref_lang = detect_text_lang(sample)
            ref_audio = (
                DEFAULT_NOIZ_REF_AUDIO_URL_CN
                if ref_lang == "zh"
                else DEFAULT_NOIZ_REF_AUDIO_URL_EN
            )
            print("[noiz] Using default reference audio: {}".format(ref_audio), file=sys.stderr)

        if ref_audio and (
            ref_audio.startswith("http://") or ref_audio.startswith("https://")
        ):
            downloaded_ref_path = prepare_ref_audio(ref_audio)
            ref_audio = downloaded_ref_path

        from noiz_tts import synthesize as _noiz_synthesize, call_emotion_enhance as _noiz_emotion_enhance

        text = args.text
        if not text and args.text_file:
            text = Path(args.text_file).read_text(encoding="utf-8").strip()

        if args.auto_emotion:
            text = _noiz_emotion_enhance("https://noiz.ai/v1", api_key, text, 120)

        try:
            _noiz_synthesize(
                base_url="https://noiz.ai/v1",
                api_key=api_key,
                text=text,
                voice_id=args.voice_id,
                reference_audio=Path(ref_audio) if ref_audio else None,
                output_format=fmt,
                speed=args.speed or 1.0,
                emo=args.emo,
                target_lang=args.lang,
                similarity_enh=args.similarity_enh,
                save_voice=args.save_voice,
                duration=args.duration,
                timeout=120,
                out_path=Path(output),
            )
        finally:
            if downloaded_ref_path and downloaded_ref_path != (args.ref_audio or ""):
                try:
                    os.unlink(downloaded_ref_path)
                except OSError:
                    pass

    if play_mode:
        play_audio(output)
        unlink_silent(tmp_output)

    return 0


# ── render ────────────────────────────────────────────────────────────


def cmd_render(args: argparse.Namespace, extra: List[str]) -> int:
    backend = detect_backend(args.backend or "")

    if backend == "noiz-guest":
        print(
            "Error: render mode requires a Noiz API key or Kokoro backend.",
            file=sys.stderr,
        )
        print("  Guest mode does not support timeline rendering.", file=sys.stderr)
        print("", file=sys.stderr)
        print("  Option A — Noiz (recommended):", file=sys.stderr)
        print(
            "    1. Get your API key from https://developers.noiz.ai/api-keys",
            file=sys.stderr,
        )
        print(
            "    2. Run: python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY",
            file=sys.stderr,
        )
        print("", file=sys.stderr)
        print("  Option B — Kokoro (offline, local):", file=sys.stderr)
        print("    uv tool install kokoro-tts", file=sys.stderr)
        print("    Then pass --backend kokoro", file=sys.stderr)
        return 1

    if backend == "noiz":
        api_key = load_api_key()
        if not api_key:
            print("Error: NOIZ_API_KEY not configured.", file=sys.stderr)
            print(
                "  Get your key at https://developers.noiz.ai/api-keys", file=sys.stderr
            )
            print(
                "  Then run: python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY",
                file=sys.stderr,
            )
            return 1
    else:
        api_key = None

    render_argv = ["--srt", args.srt, "--voice-map", args.voice_map,
                    "--output", args.output, "--backend", backend]
    if api_key:
        render_argv += ["--api-key", api_key]
    render_argv += extra

    from render_timeline import main as _render_main
    old_argv = sys.argv
    try:
        sys.argv = ["render_timeline.py"] + render_argv
        return _render_main()
    finally:
        sys.argv = old_argv


# ── to-srt ────────────────────────────────────────────────────────────


def cmd_to_srt(args: argparse.Namespace) -> int:
    from text_to_srt import split_sentences, estimate_timings, write_srt

    text = Path(args.input).read_text(encoding="utf-8").strip()
    if not text:
        print("Error: Input text is empty.", file=sys.stderr)
        return 1
    sentences = split_sentences(text)
    if not sentences:
        print("Error: No sentences found after splitting.", file=sys.stderr)
        return 1
    cps = args.cps if args.cps is not None else 4.0
    gap = args.gap if args.gap is not None else 300
    entries = estimate_timings(sentences, chars_per_second=cps, gap_ms=gap)
    write_srt(entries, Path(args.output))
    print("Done. {} segments written to {}".format(len(entries), args.output))
    return 0


# ── config ────────────────────────────────────────────────────────────


def cmd_config(args: argparse.Namespace) -> int:
    if args.set_api_key:
        save_api_key(args.set_api_key)
        print("API key saved to {}".format(NOIZ_KEY_FILE))
        return 0

    api_key = load_api_key()
    if api_key:
        masked = "{}****{}".format(api_key[:4], api_key[-4:])
        print("NOIZ_API_KEY is configured: {}".format(masked))
        print("  Backend: noiz (full features)")
    else:
        print(
            "NOIZ_API_KEY is not configured.\n"
            "  Current fallback: noiz-guest (limited features, no API key required)\n"
            "\n"
            "Option A — Noiz with API key (recommended, full features):\n"
            "  1. Get your API key from https://developers.noiz.ai/api-keys\n"
            "  2. Run:\n"
            "     python3 skills/tts/scripts/tts.py config --set-api-key YOUR_KEY\n"
            "  The key will be saved to {key_file} and loaded automatically.\n"
            "\n"
            "Option B — Kokoro (offline, local):\n"
            "  uv tool install kokoro-tts\n"
            "  Then pass --backend kokoro".format(key_file=NOIZ_KEY_FILE)
        )
    return 0


# ── Argument parser ───────────────────────────────────────────────────


_SUBCOMMANDS = {"speak", "render", "to-srt", "config"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tts.py",
        description=(
            "TTS entrypoint: text-to-speech, timeline rendering, SRT generation.\n\n"
            "speak is the default — the subcommand can be omitted:\n"
            "  tts.py -t 'Hello world'               # same as: tts.py speak -t ...\n"
            "  tts.py -t 'Hi' --ref-audio ./my.wav -o clone.wav\n\n"
            "Other subcommands must be specified explicitly:\n"
            "  tts.py render --srt input.srt --voice-map vm.json -o output.wav\n"
            "  tts.py to-srt -i article.txt -o article.srt\n"
            "  tts.py config --set-api-key YOUR_KEY"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    # speak
    sp = sub.add_parser("speak", help="Text to audio (simple mode)")
    sp.add_argument("-t", "--text", help="Text string to synthesize")
    sp.add_argument("-f", "--text-file", dest="text_file", help="Path to text file")
    sp.add_argument("-v", "--voice", help="Kokoro voice name")
    sp.add_argument("--voice-id", dest="voice_id", help="Noiz voice ID")
    sp.add_argument("-o", "--output", help="Output file path (omit to play immediately)")
    sp.add_argument(
        "--format",
        default="wav",
        choices=["wav", "mp3", "opus", "ogg"],
        help="Audio format (ogg is alias for opus)",
    )
    sp.add_argument("--lang", help="Language code (e.g. zh, en-us)")
    sp.add_argument("--speed", type=float, help="Playback speed multiplier")
    sp.add_argument("--emo", help='Emotion JSON string, e.g. \'{"Joy":0.5}\'')
    sp.add_argument(
        "--duration",
        type=float,
        metavar="SEC",
        help="Target audio duration in seconds (0, 36]",
    )
    sp.add_argument(
        "--backend",
        choices=["kokoro", "noiz", "noiz-guest"],
        help="Force a specific backend (auto-detected by default)",
    )
    sp.add_argument(
        "--ref-audio",
        dest="ref_audio",
        help="Reference audio for voice cloning: local path or URL (Noiz only)",
    )
    sp.add_argument("--auto-emotion", dest="auto_emotion", action="store_true")
    sp.add_argument("--similarity-enh", dest="similarity_enh", action="store_true")
    sp.add_argument("--save-voice", dest="save_voice", action="store_true")

    # render
    rp = sub.add_parser("render", help="SRT to timeline-accurate audio")
    rp.add_argument("--srt", required=True, help="Input SRT file")
    rp.add_argument("--voice-map", dest="voice_map", required=True, help="Voice map JSON file")
    rp.add_argument("-o", "--output", required=True, help="Output audio file")
    rp.add_argument(
        "--backend",
        choices=["kokoro", "noiz"],
        help="Backend to use (auto-detected by default)",
    )

    # to-srt
    tp = sub.add_parser("to-srt", help="Text file to SRT with auto timings")
    tp.add_argument("-i", "--input", required=True, help="Input text file")
    tp.add_argument("-o", "--output", required=True, help="Output SRT file")
    tp.add_argument(
        "--cps",
        type=float,
        help="Characters per second (default 4 for Chinese, ~15 for English)",
    )
    tp.add_argument("--gap", type=int, help="Gap between segments in milliseconds")

    # config
    cp = sub.add_parser("config", help="Check / set NOIZ_API_KEY")
    cp.add_argument("--set-api-key", dest="set_api_key", metavar="KEY")

    return parser


# ── Entry point ───────────────────────────────────────────────────────


def main() -> int:
    # Default to "speak" when no subcommand is given.
    argv = sys.argv[1:]
    if not argv or argv[0] not in _SUBCOMMANDS:
        argv = ["speak"] + argv

    parser = build_parser()
    # parse_known_args: extra unknown args are forwarded to render_timeline.py
    args, extra = parser.parse_known_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "speak":
        if extra:
            print("Unknown options: {}".format(" ".join(extra)), file=sys.stderr)
            return 1
        return cmd_speak(args)
    elif args.command == "render":
        return cmd_render(args, extra)
    elif args.command == "to-srt":
        if extra:
            print("Unknown options: {}".format(" ".join(extra)), file=sys.stderr)
            return 1
        return cmd_to_srt(args)
    elif args.command == "config":
        if extra:
            print("Unknown options: {}".format(" ".join(extra)), file=sys.stderr)
            return 1
        return cmd_config(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
