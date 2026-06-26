#!/usr/bin/env python3
"""
Extract a clean audio-only track from any media file.

Common workflow: feed a video into a transcription model, a podcast editor,
or a music-analysis tool that wants just the audio. This script picks the
right ffmpeg flags for the target codec, validates that the source actually
has audio, and prints a one-line summary of what it produced.

Usage:
  python3 extract_audio.py <input> <output> [options]

Output codec is auto-detected from the output extension:
  .mp3   -> libmp3lame  (default 192k VBR-quality 2)
  .m4a   -> aac         (default 192k)
  .aac   -> aac         (default 192k, raw ADTS)
  .wav   -> pcm_s16le   (uncompressed, lossless)
  .flac  -> flac        (lossless, compressed)
  .opus  -> libopus     (default 96k, best small-file quality)
  .ogg   -> libvorbis   (default 192k)

Options:
  --bitrate <rate>      Override bitrate for lossy codecs (e.g. 128k, 256k).
                        Ignored for wav/flac.
  --sample-rate <hz>    Resample to this rate (e.g. 16000 for transcription,
                        44100 for music, 48000 for video). Default: keep source.
  --channels <n>        Force channel count (1 = mono, 2 = stereo).
                        Default: keep source.
  --start <seconds>     Trim audio start (input seek before extraction).
  --duration <seconds>  Limit extraction to this many seconds from --start.
  --normalize           Apply a single-pass loudness normalization
                        (loudnorm I=-16 LUFS, fast preset). For
                        broadcast-quality normalization use
                        loudnorm_two_pass.py instead.
  --quiet               Suppress non-error stdout.

Exit codes:
  0 = success
  1 = ffmpeg/ffprobe failure mid-extraction
  2 = bad arguments / missing input / unsafe path / no audio stream /
      unsupported output extension
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


# Map output extension -> (ffmpeg codec, default bitrate, extra flags).
# "wav" and "flac" ignore --bitrate (lossless).
CODEC_MAP: Dict[str, Dict] = {
    ".mp3":  {"codec": "libmp3lame",   "default_bitrate": "192k",
              "extra": ["-q:a", "2"]},
    ".m4a":  {"codec": "aac",          "default_bitrate": "192k",
              "extra": ["-movflags", "+faststart"]},
    ".aac":  {"codec": "aac",          "default_bitrate": "192k",
              "extra": []},
    ".wav":  {"codec": "pcm_s16le",    "default_bitrate": None,
              "extra": []},
    ".flac": {"codec": "flac",         "default_bitrate": None,
              "extra": ["-compression_level", "5"]},
    ".opus": {"codec": "libopus",      "default_bitrate": "96k",
              "extra": ["-application", "audio"]},
    ".ogg":  {"codec": "libvorbis",    "default_bitrate": "192k",
              "extra": []},
}


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def has_audio_stream(path: Path) -> bool:
    """Return True if the file contains at least one audio stream."""
    res = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=codec_type",
            "-of", "csv=p=0",
            str(path),
        ],
        check=False, capture_output=True, text=True,
    )
    if res.returncode != 0:
        return False
    return bool(res.stdout.strip())


def probe_audio_info(path: Path) -> Optional[Dict[str, str]]:
    """Return basic info about the first audio stream, or None on failure."""
    res = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=codec_name,sample_rate,channels,duration",
            "-of", "default=noprint_wrappers=1",
            str(path),
        ],
        check=False, capture_output=True, text=True,
    )
    if res.returncode != 0:
        return None
    info: Dict[str, str] = {}
    for line in res.stdout.splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            info[k.strip()] = v.strip()
    return info or None


def positive_float(name: str, value: str) -> float:
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{name}: not a number: {value!r}")
    if f <= 0:
        raise argparse.ArgumentTypeError(f"{name}: must be > 0")
    return f


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n", 1)[1] if __doc__ else "",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Source media path")
    parser.add_argument("output", help="Output audio path (extension picks codec)")
    parser.add_argument("--bitrate",
                        help="Override bitrate for lossy codecs (e.g. 128k, 256k)")
    parser.add_argument("--sample-rate", type=int,
                        help="Resample to this rate in Hz (e.g. 16000 for transcription)")
    parser.add_argument("--channels", type=int, choices=(1, 2),
                        help="Force 1 (mono) or 2 (stereo)")
    parser.add_argument("--start", type=lambda v: positive_float("--start", v),
                        help="Skip the first <seconds> of audio")
    parser.add_argument("--duration", type=lambda v: positive_float("--duration", v),
                        help="Limit extraction to <seconds>")
    parser.add_argument("--normalize", action="store_true",
                        help="Apply single-pass loudnorm I=-16 (fast preset)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Suppress non-error stdout")
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out = safe_path(args.output).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2

    ext = out.suffix.lower()
    if ext not in CODEC_MAP:
        print(
            f"error: unsupported output extension {ext!r}. "
            f"Allowed: {', '.join(sorted(CODEC_MAP.keys()))}.",
            file=sys.stderr,
        )
        return 2

    if not has_audio_stream(src):
        print(
            f"error: input has no audio stream: {src}. "
            f"Use a media file with at least one audio track.",
            file=sys.stderr,
        )
        return 2

    if args.sample_rate is not None and args.sample_rate <= 0:
        print("error: --sample-rate must be > 0", file=sys.stderr)
        return 2

    if args.bitrate and not re.match(r"^\d+[kKmM]?$", args.bitrate):
        print(f"error: --bitrate must look like '128k' or '256000', got {args.bitrate!r}",
              file=sys.stderr)
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)

    codec_info = CODEC_MAP[ext]
    cmd: List[str] = ["ffmpeg", "-hide_banner", "-y"]

    # Input seek (before -i) is much faster than output seek.
    if args.start:
        cmd += ["-ss", f"{args.start}"]
    cmd += ["-i", str(src)]
    if args.duration:
        cmd += ["-t", f"{args.duration}"]

    # Drop video and subtitle streams; keep only audio.
    cmd += ["-vn", "-sn"]

    # Audio filter chain (optional resample + optional normalize).
    af_parts: List[str] = []
    if args.normalize:
        af_parts.append("loudnorm=I=-16:TP=-1.5:LRA=11")
    if args.sample_rate:
        af_parts.append(f"aresample={args.sample_rate}")
    if af_parts:
        cmd += ["-af", ",".join(af_parts)]

    if args.channels:
        cmd += ["-ac", str(args.channels)]

    if args.sample_rate:
        cmd += ["-ar", str(args.sample_rate)]

    # Codec selection.
    cmd += ["-c:a", codec_info["codec"]]

    # Bitrate only for lossy codecs (default_bitrate is None for wav/flac).
    bitrate = args.bitrate or codec_info["default_bitrate"]
    if bitrate and codec_info["default_bitrate"] is not None:
        cmd += ["-b:a", bitrate]

    cmd += codec_info["extra"]
    cmd += [str(out)]

    if not args.quiet:
        print(f"Extracting audio: {src.name} -> {out.name} "
              f"(codec={codec_info['codec']}"
              + (f", bitrate={bitrate}" if bitrate and codec_info["default_bitrate"] else "")
              + (f", sr={args.sample_rate}" if args.sample_rate else "")
              + (f", ch={args.channels}" if args.channels else "")
              + (", normalized" if args.normalize else "")
              + ")",
              file=sys.stderr)

    res = subprocess.run(cmd, check=False, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        # Surface the most useful ffmpeg error line.
        last_lines = [
            ln for ln in (res.stderr or "").splitlines()
            if ln.strip() and not ln.startswith("[")
        ]
        msg = last_lines[-1] if last_lines else "ffmpeg failed"
        print(f"error: ffmpeg failed: {msg}", file=sys.stderr)
        return 1

    info = probe_audio_info(out)
    if not args.quiet:
        if info:
            print(
                f"Wrote {out} "
                f"({info.get('codec_name','?')}, "
                f"{info.get('sample_rate','?')} Hz, "
                f"{info.get('channels','?')} ch, "
                f"{info.get('duration','?')}s)",
                file=sys.stderr,
            )
        else:
            print(f"Wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
