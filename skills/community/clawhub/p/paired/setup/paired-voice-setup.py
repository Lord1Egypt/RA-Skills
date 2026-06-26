#!/usr/bin/env python3
"""paired-voice-setup — guided voice-clone training.

Walks the user through recording 60-90 second reference audio plus
optional word-clips (for splicing) in a controlled, scriptable way.

Output:
  ~/.config/paired/voice.conf            (config)
  ~/.config/paired/voice/reference.wav   (combined reference)
  ~/.config/paired/voice/word-clips/*.wav (per-word splice clips)

This skill never bundles or transmits your voice anywhere.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_PROMPTS = [
    {"code": "A1", "text": "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs."},
    {"code": "A2", "text": "A complete sentence is a sentence with a subject, a verb, and a complete thought."},
    {"code": "A3", "text": "I am recording this audio so that an artificial intelligence can learn the sound of my voice."},
    {"code": "A4", "text": "Today is a good day to test my voice. The weather is mild and my microphone is ready."},
    {"code": "A5", "text": "Hello. Thank you. Yes, of course. No, not today. Please. Sorry about that. See you soon."},
    {"code": "A6", "text": "Numbers one two three four five six seven eight nine and ten. The year is twenty twenty six."},
]


CONFIG_DIR = Path.home() / ".config" / "paired"
VOICE_DIR = CONFIG_DIR / "voice"
CLIPS_DIR = VOICE_DIR / "word-clips"
CONFIG_FILE = CONFIG_DIR / "voice.conf"


def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)


def have_tool(name):
    return shutil.which(name) is not None


def record_with_arecord(out_path, seconds):
    cmd = ["arecord", "-q", "-f", "S16_LE", "-r", "24000", "-c", "1",
           "-d", str(seconds), str(out_path)]
    subprocess.run(cmd, check=True)


def normalise(in_path, out_path):
    """Resample to 24kHz mono and loudness-normalise."""
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(in_path),
         "-ar", "24000", "-ac", "1",
         "-af", "loudnorm=I=-16:LRA=11:TP=-1.5",
         str(out_path)],
        check=True,
    )


def reference_setup(args):
    ensure_dirs()
    if not have_tool("arecord"):
        print("ERROR: arecord not found (apt install alsa-utils)")
        sys.exit(1)
    if not have_tool("ffmpeg"):
        print("ERROR: ffmpeg not found")
        sys.exit(1)

    print()
    print("================================================================")
    print("paired voice clone setup — recording 6 phrases for your reference")
    print("================================================================")
    print()
    print("Tips for a clean recording:")
    print("  - Quiet room")
    print("  - Same mic distance for every phrase")
    print("  - Read naturally; don't over-articulate")
    print()

    raw_files = []
    for i, prompt in enumerate(SCRIPT_PROMPTS, 1):
        code = prompt["code"]
        text = prompt["text"]
        print("--- Phrase " + str(i) + "/" + str(len(SCRIPT_PROMPTS)) + " (" + code + ") ---")
        print("Text: " + text)
        input("Press Enter when ready to start recording (about 15 seconds)... ")
        out_raw = VOICE_DIR / ("raw-" + code + ".wav")
        out_norm = VOICE_DIR / ("norm-" + code + ".wav")
        try:
            record_with_arecord(out_raw, 15)
            normalise(out_raw, out_norm)
            raw_files.append(out_norm)
            print("  Saved: " + str(out_norm))
        except subprocess.CalledProcessError as e:
            print("  Recording failed: " + str(e))
            sys.exit(1)
        print()

    list_file = VOICE_DIR / "concat.txt"
    with open(list_file, "w") as f:
        for r in raw_files:
            f.write("file '" + str(r) + "'\n")
    ref = VOICE_DIR / "reference.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-ar", "24000", "-ac", "1", str(ref)],
        check=True,
    )
    print("Combined reference: " + str(ref))
    print()
    print("Edit ~/.config/paired/voice.conf and set:")
    print("  VOICE_REFERENCE=" + str(ref))
    print()


def word_setup(args):
    ensure_dirs()
    word = args.word.lower().strip()
    if not word.isalnum():
        print("Word must be alphanumeric only")
        sys.exit(1)
    print("Recording 5 takes of '" + word + "' (~2s each). The cleanest becomes the splice clip.")
    print()
    takes = []
    for i in range(1, 6):
        out_raw = CLIPS_DIR / ("raw-" + word + "-" + str(i) + ".wav")
        out_norm = CLIPS_DIR / ("norm-" + word + "-" + str(i) + ".wav")
        input("Take " + str(i) + "/5 — press Enter, say '" + word + "' clearly, wait... ")
        record_with_arecord(out_raw, 3)
        normalise(out_raw, out_norm)
        takes.append(out_norm)
    print()
    print("Listen to each:")
    for i, t in enumerate(takes, 1):
        print("  Take " + str(i) + ": " + str(t))
    chosen = int(input("Which take is cleanest? [1-5]: "))
    final = CLIPS_DIR / (word + ".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(takes[chosen-1]),
         "-af",
         "silenceremove=start_periods=1:start_silence=0.1:start_threshold=-40dB:"
         "stop_periods=-1:stop_silence=0.1:stop_threshold=-40dB",
         str(final)],
        check=True,
    )
    print("Saved splice clip: " + str(final))


def write_config():
    ensure_dirs()
    if CONFIG_FILE.exists():
        return
    CONFIG_FILE.write_text(
        "# paired voice config (see docs/VOICE-SETUP.md)\n"
        "VOXCPM_URL=http://localhost:8056\n"
        "XTTS_URL=http://localhost:8055\n"
        "VOICE_REFERENCE=" + str(VOICE_DIR / "reference.wav") + "\n"
        "VOICE_REFERENCE_SERVICE=/refs/reference.wav\n"
        "WORD_CLIPS_DIR=" + str(CLIPS_DIR) + "\n"
        "FALLBACK_PIPER_VOICE=en_GB-northern_english_male-medium\n"
    )
    print("Wrote config: " + str(CONFIG_FILE))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="Create config template")
    sub.add_parser("reference", help="Guided reference-audio recording (60-90s)")
    w = sub.add_parser("word", help="Record splice clip for a single word")
    w.add_argument("word")
    args = p.parse_args()

    if args.cmd == "init":
        write_config()
    elif args.cmd == "reference":
        reference_setup(args)
        write_config()
    elif args.cmd == "word":
        word_setup(args)


if __name__ == "__main__":
    main()
