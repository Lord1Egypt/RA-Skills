#!/usr/bin/env python3
"""Generate opus voice audio using NoizAI TTS for Feishu delivery.

Usage:
    python voice.py "text to speak" [output_path] [voice_id]

Args:
    text       - Text to convert to speech (required)
    output     - Output opus file path (default: temp file in workspace media dir)
    voice_id   - NoizAI voice ID (default: b4775100 = 悦悦)

Returns:
    Prints the output file path to stdout on success.
    Exit code 0 = success, 1 = failure.
    All diagnostic messages go to stderr.
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TTS_SCRIPT = SCRIPT_DIR.parent / "noizai-tts" / "scripts" / "tts.py"
WORKSPACE_MEDIA = Path.home() / ".openclaw" / "workspace" / "media"

DEFAULT_VOICE = "b4775100"  # 悦悦｜社交分享

def main():
    if len(sys.argv) < 2:
        print("Usage: python voice.py <text> [output.opus] [voice_id]", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    if not text.strip():
        print("Error: empty text", file=sys.stderr)
        sys.exit(1)

    # Output path
    if len(sys.argv) >= 3:
        output = Path(sys.argv[2])
    else:
        WORKSPACE_MEDIA.mkdir(parents=True, exist_ok=True)
        import time
        ts = int(time.time() * 1000)
        output = WORKSPACE_MEDIA / f"voice_{ts}.opus"

    # Voice ID
    voice_id = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_VOICE

    # Find Python
    python = sys.executable

    # Find TTS script
    if not TTS_SCRIPT.exists():
        # Try alternate path
        alt = SCRIPT_DIR.parent.parent / "noizai-tts" / "scripts" / "tts.py"
        if alt.exists():
            tts_script = alt
        else:
            print(f"Error: tts.py not found at {TTS_SCRIPT} or {alt}", file=sys.stderr)
            sys.exit(1)
    else:
        tts_script = TTS_SCRIPT

    # Build command
    cmd = [
        python, str(tts_script),
        "-t", text,
        "--voice-id", voice_id,
        "--format", "opus",
        "-o", str(output)
    ]

    # Run — capture stderr separately so it doesn't pollute stdout
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    # Check output file
    if output.exists() and output.stat().st_size > 100:
        # Success — print path to stdout
        print(str(output))
        sys.exit(0)
    else:
        # Failed
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        if result.stdout:
            print(result.stdout.strip(), file=sys.stderr)
        print(f"Error: output file missing or too small: {output}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
