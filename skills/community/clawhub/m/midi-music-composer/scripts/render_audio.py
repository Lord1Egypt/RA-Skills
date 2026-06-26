#!/usr/bin/env python3
"""Render a MIDI file to WAV when a local renderer is available."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def render(midi_path: Path, out_path: Path, soundfont: Optional[Path] = None) -> str:
    fluidsynth = shutil.which("fluidsynth")
    timidity = shutil.which("timidity")
    if fluidsynth and soundfont and soundfont.exists():
        subprocess.run(
            [fluidsynth, "-ni", str(soundfont), str(midi_path), "-F", str(out_path), "-r", "44100"],
            check=True,
        )
        return "fluidsynth"
    if timidity:
        subprocess.run([timidity, str(midi_path), "-Ow", "-o", str(out_path)], check=True)
        return "timidity"
    raise SystemExit("No MIDI renderer found. Install timidity, or fluidsynth plus a soundfont.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render MIDI to WAV when local tools are installed.")
    parser.add_argument("midi", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--soundfont", type=Path, default=None)
    args = parser.parse_args()

    out_path = args.out or args.midi.with_suffix(".wav")
    renderer = render(args.midi, out_path, args.soundfont)
    print(f"Rendered {out_path} with {renderer}")


if __name__ == "__main__":
    main()
