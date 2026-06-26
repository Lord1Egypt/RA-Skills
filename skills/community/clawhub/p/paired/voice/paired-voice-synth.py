#!/usr/bin/env python3
"""paired-voice-synth — Voice synthesis with cloned-voice support.

A drop-in TTS wrapper that synthesises text in the user's own cloned voice
when configured, with graceful fallback through multiple engines.

Fallback ladder (each level engaged automatically if previous fails):
  1. VoxCPM2 HTTP service  — 48kHz studio-quality voice cloning (best)
  2. XTTS HTTP service     — 24kHz cloned voice (good)
  3. Local CPU XTTS        — slow but works without GPU (if installed)
  4. piper                 — generic neural TTS (no cloning)
  5. espeak-ng             — last-resort robotic TTS

Supports word-level audio splicing: pre-recorded clips of specific words
(e.g. the user's own name) are spliced directly into the output for 100%
accurate pronunciation.

Usage:
  paired-voice-synth [--reference PATH] [--config PATH] <text> <output.wav>

Configuration file (default ~/.config/paired/voice.conf):
  VOXCPM_URL=http://localhost:8056
  XTTS_URL=http://localhost:8055
  VOICE_REFERENCE=/path/to/your-reference.wav
  WORD_CLIPS_DIR=/path/to/name-clips
  FALLBACK_PIPER_VOICE=en_GB-northern_english_male-medium

The reference WAV and WORD_CLIPS are NEVER bundled with this skill; users
provide their own via paired-voice-setup (see docs/VOICE-SETUP.md).
"""
import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/paired/voice.conf")
DEFAULT_VOXCPM_URL = "http://localhost:8056"
DEFAULT_XTTS_URL = "http://localhost:8055"


def log(msg):
    sys.stderr.write("[paired-voice] " + msg + "\n")
    sys.stderr.flush()


def load_config(path):
    """Parse a simple KEY=value config file, return dict."""
    config = {}
    p = Path(path)
    if not p.is_file():
        return config
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            config[k.strip()] = v.strip().strip('"').strip("'")
    return config


def service_healthy(url, timeout=3, require_loaded=False):
    """Check if a paired voice HTTP service is alive and ready."""
    try:
        with urllib.request.urlopen(url + "/health", timeout=timeout) as r:
            data = json.loads(r.read())
        if require_loaded:
            return bool(data.get("model_loaded"))
        return bool(data.get("ok"))
    except Exception:
        return False


def call_voxcpm(text, out_path, reference, service_url):
    """Call VoxCPM2 service. Reference path is from the SERVICE container's view."""
    body = json.dumps({
        "text": text,
        "reference": reference,
        "output": "/tmp/paired-voxcpm-segment.wav",
    }).encode()
    req = urllib.request.Request(
        service_url + "/synth",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        if not d.get("ok"):
            log("VoxCPM error: " + str(d.get("error")))
            return False
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(d["audio_base64"]))
        log("VoxCPM2 segment in " + str(d.get("elapsed_sec")) + "s")
        return True
    except Exception as e:
        log("VoxCPM exception: " + str(e))
        return False


def call_xtts(text, out_path, reference, service_url):
    """Call XTTS HTTP service (fallback)."""
    body = json.dumps({
        "text": text,
        "reference": reference,
        "output": "/tmp/paired-xtts-segment.wav",
    }).encode()
    req = urllib.request.Request(
        service_url + "/synth",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        if not d.get("ok"):
            log("XTTS error: " + str(d.get("error")))
            return False
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(d["audio_base64"]))
        log("XTTS segment in " + str(d.get("elapsed_sec")) + "s")
        return True
    except Exception as e:
        log("XTTS exception: " + str(e))
        return False


def fallback_piper(text, out_path, piper_voice):
    """Generate via piper (no voice cloning, but reliable)."""
    if not shutil.which("piper"):
        return False
    try:
        result = subprocess.run(
            ["piper", "--model", piper_voice, "--output_file", out_path],
            input=text.encode(),
            capture_output=True,
            timeout=30,
        )
        if result.returncode == 0 and Path(out_path).exists():
            log("Generated via piper fallback")
            return True
        log("piper failed: " + result.stderr.decode()[:200])
    except Exception as e:
        log("piper exception: " + str(e))
    return False


def fallback_espeak(text, out_path):
    """Last resort: espeak-ng."""
    if not shutil.which("espeak-ng"):
        return False
    try:
        subprocess.run(
            ["espeak-ng", "-w", out_path, "-v", "en-gb", text],
            check=True, capture_output=True, timeout=20,
        )
        log("Generated via espeak-ng (final fallback)")
        return True
    except Exception as e:
        log("espeak exception: " + str(e))
    return False


def chunk_text(text, max_chars=400):
    """Split text into chunks <= max_chars at sentence boundaries.

    Long inputs would overflow voice-cloning service token limits and may
    cause GPU OOM. Splitting at natural prosody boundaries keeps audio
    sounding continuous.
    """
    if len(text) <= max_chars:
        return [text]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip() if current else s
        else:
            if current:
                chunks.append(current)
            if len(s) > max_chars:
                sub = re.split(r"(?<=,)\s+", s)
                cur = ""
                for piece in sub:
                    if len(cur) + len(piece) + 1 <= max_chars:
                        cur = (cur + " " + piece).strip() if cur else piece
                    else:
                        if cur:
                            chunks.append(cur)
                        cur = piece
                if cur:
                    chunks.append(cur)
                current = ""
            else:
                current = s
    if current:
        chunks.append(current)
    return chunks


def load_word_clips(clips_dir):
    """Return {lowercase_word: path_to_wav} for all WAVs in the clips dir."""
    clips = {}
    if not clips_dir:
        return clips
    d = Path(clips_dir)
    if not d.is_dir():
        return clips
    for wav in d.glob("*.wav"):
        word = wav.stem.lower()
        if word and not word.startswith("."):
            clips[word] = str(wav)
    return clips


def split_text_with_clips(text, word_clips):
    """Yield (kind, content) where kind is 'tts' or 'clip:<word>'."""
    if not word_clips:
        return [("tts", text)]
    keys = "|".join(re.escape(k) for k in word_clips.keys())
    pattern = re.compile(rf"\b({keys})\b", re.IGNORECASE)
    segments = []
    last_end = 0
    for m in pattern.finditer(text):
        if m.start() > last_end:
            pre = text[last_end:m.start()]
            if pre.strip():
                segments.append(("tts", pre))
        segments.append((f"clip:{m.group(1).lower()}", m.group(0)))
        last_end = m.end()
    if last_end < len(text):
        tail = text[last_end:]
        if tail.strip():
            segments.append(("tts", tail))
    return segments


def synth_tts(text, out_path, config):
    """Try each TTS backend in order. Returns True on success."""
    reference = config.get("VOICE_REFERENCE")
    voxcpm_url = config.get("VOXCPM_URL", DEFAULT_VOXCPM_URL)
    xtts_url = config.get("XTTS_URL", DEFAULT_XTTS_URL)
    piper_voice = config.get(
        "FALLBACK_PIPER_VOICE",
        "en_GB-northern_english_male-medium",
    )
    service_reference = config.get("VOICE_REFERENCE_SERVICE", reference)

    if reference and service_reference and service_healthy(voxcpm_url, require_loaded=True):
        if call_voxcpm(text, out_path, service_reference, voxcpm_url):
            return True

    if reference and service_reference and service_healthy(xtts_url):
        if call_xtts(text, out_path, service_reference, xtts_url):
            return True

    if fallback_piper(text, out_path, piper_voice):
        return True

    if fallback_espeak(text, out_path):
        return True

    return False


def main():
    p = argparse.ArgumentParser(
        description="Voice synthesis with cloned-voice support and splicing.",
    )
    p.add_argument("--config", default=DEFAULT_CONFIG_PATH,
                   help="Path to voice config file")
    p.add_argument("--reference",
                   help="Override reference WAV path (else use config)")
    p.add_argument("text", help="Text to synthesise")
    p.add_argument("output", help="Output WAV path")
    args = p.parse_args()

    config = load_config(args.config)
    if args.reference:
        config["VOICE_REFERENCE"] = args.reference

    clips_dir = config.get("WORD_CLIPS_DIR")
    word_clips = load_word_clips(clips_dir)

    if word_clips:
        log("Word-clip splicing active for: " + ",".join(word_clips.keys()))

    segments = split_text_with_clips(args.text, word_clips)

    if len(segments) == 1 and segments[0][0] == "tts" and len(args.text) <= 400:
        if synth_tts(args.text, args.output, config):
            sys.exit(0)
        log("All TTS backends failed")
        sys.exit(1)

    tmpdir = tempfile.mkdtemp(prefix="paired-voice-")
    seg_files = []
    seg_idx = 0
    try:
        for kind, content in segments:
            if kind.startswith("clip:"):
                clip_word = kind.split(":", 1)[1]
                src = word_clips[clip_word]
                dst = f"{tmpdir}/seg_{seg_idx:03d}.wav"
                shutil.copy(src, dst)
                log(f"  seg_{seg_idx:03d}: clip '{clip_word}' from {src}")
                seg_files.append(dst)
                seg_idx += 1
            else:
                for sub in chunk_text(content):
                    dst = f"{tmpdir}/seg_{seg_idx:03d}.wav"
                    if not synth_tts(sub, dst, config):
                        log(f"  seg_{seg_idx:03d}: ALL backends failed")
                        sys.exit(1)
                    log(f"  seg_{seg_idx:03d}: tts ({len(sub)} chars)")
                    seg_files.append(dst)
                    seg_idx += 1

        norm = []
        for f in seg_files:
            n = f.replace(".wav", "_n.wav")
            subprocess.run(
                ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-i", f, "-ar", "24000", "-ac", "1", n],
                check=True,
            )
            norm.append(n)

        manifest = f"{tmpdir}/concat.txt"
        with open(manifest, "w") as fh:
            for n in norm:
                fh.write(f"file '{n}'\n")

        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "concat", "-safe", "0", "-i", manifest,
             "-ar", "24000", "-ac", "1", args.output],
            check=True,
        )
        log(f"OK spliced output: {args.output}")
        sys.exit(0)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
