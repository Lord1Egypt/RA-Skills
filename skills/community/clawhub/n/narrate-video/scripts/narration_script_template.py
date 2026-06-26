#!/usr/bin/env python3
"""Video Narration - TTS Generation and Video Assembly

This script generates TTS audio segments using Azure Speech SDK,
positions them at specified timestamps, and merges them onto a video.

Usage:
    1. Fill in VOICE_NAME, INPUT_VIDEO, OUTPUT_VIDEO, and SEGMENTS
    2. Ensure AZURE_SPEECH_KEY is set in environment (or .env file)
    3. Run: python3 narration_script.py
"""

import os
import subprocess
import json
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv(os.path.expanduser("~/.narrate_video.env"))

# ── Configuration ──────────────────────────────────────────────────────────
SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY", "")
SERVICE_REGION = os.environ.get("AZURE_SPEECH_REGION", "eastus2")
VOICE_NAME = "REPLACE_WITH_VOICE"         # e.g. en-US-AndrewMultilingualNeural
INPUT_VIDEO = "REPLACE_WITH_INPUT"        # Relative path only
OUTPUT_VIDEO = "REPLACE_WITH_OUTPUT"      # Relative path only
SEGMENTS_DIR = "narration_segments"       # Relative path only

# ── Narration Segments ─────────────────────────────────────────────────────
# Each entry: (start_seconds, "narration text")
# Fill from Phase 2 script writing
SEGMENTS = []


# ── TTS Generation ─────────────────────────────────────────────────────────
def generate_segment(idx, text, output_path):
    """Generate a single audio segment using Azure TTS."""
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
    speech_config.speech_synthesis_voice_name = VOICE_NAME
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"  [OK] Segment {idx}: {output_path}")
        return True
    details = result.cancellation_details
    print(f"  [FAIL] Segment {idx}: {details.reason} - {details.error_details}")
    return False


def get_audio_duration(path):
    """Get duration of an audio file in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def build_narrated_video():
    """Generate TTS segments, check timing, and assemble the narrated video."""
    os.makedirs(SEGMENTS_DIR, exist_ok=True)

    # Step 1: Generate audio segments (skips existing files)
    print("=== Step 1: Generating audio segments ===")
    segment_files = []
    for i, (start, text) in enumerate(SEGMENTS):
        out_path = os.path.join(SEGMENTS_DIR, f"seg_{i:03d}.mp3")
        if not os.path.exists(out_path):
            if not generate_segment(i, text, out_path):
                return False
        else:
            print(f"  [SKIP] Segment {i}: already exists")
        segment_files.append((start, out_path))

    # Step 2: Get video duration
    video_duration = float(json.loads(subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", INPUT_VIDEO],
        capture_output=True, text=True
    ).stdout)["format"]["duration"])
    print(f"\nVideo duration: {video_duration:.1f}s")

    # Step 3: Check timing overlaps — abort on any overlap
    print("\n=== Step 2: Checking segment timings ===")
    has_overlap = False
    for i, (start, path) in enumerate(segment_files):
        dur = get_audio_duration(path)
        end = start + dur
        next_start = segment_files[i + 1][0] if i + 1 < len(segment_files) else video_duration
        gap = next_start - end
        status = "OK" if gap >= 0 else "OVERLAP"
        print(f"  Seg {i:2d}: {start:6.1f}s - {end:6.1f}s (dur: {dur:5.1f}s) gap: {gap:+.1f}s [{status}]")
        if gap < 0:
            has_overlap = True
            print(f"    WARNING: Overlap of {-gap:.1f}s with next segment!")
    if has_overlap:
        print("\nERROR: Fix overlaps before proceeding.")
        return False

    # Step 4: Build ffmpeg command
    print("\n=== Step 3: Building narrated video ===")
    inputs = ["-i", INPUT_VIDEO]
    for _, path in segment_files:
        inputs.extend(["-i", path])

    filter_parts = []
    n = len(segment_files)
    for i, (start, _) in enumerate(segment_files):
        delay_ms = int(start * 1000)
        filter_parts.append(f"[{i+1}:a]adelay={delay_ms}|{delay_ms}[a{i}]")

    # normalize=0 is essential: without it, amix divides volume by input count,
    # so 20 segments would reduce audio to 1/20th volume — nearly silent.
    mix_inputs = "".join(f"[a{i}]" for i in range(n))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={n}:duration=longest"
        f":dropout_transition=0:normalize=0[final]"
    )

    # Original video audio is completely discarded — only the narration track
    # is mapped. Mixing original audio even at low volume causes audible
    # double-voice artifacts because the narration bleeds through both tracks.
    filter_complex = ";".join(filter_parts)
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[final]",
        "-c:v", "copy",       # Copy video without re-encoding
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]

    print("  Running ffmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg error:\n{result.stderr[-2000:]}")
        return False

    print(f"\n=== Done! Output: {OUTPUT_VIDEO} ===")
    return True


def check_inputs():
    """Validate all required configuration before running."""
    errors = []
    if not SPEECH_KEY:
        errors.append("AZURE_SPEECH_KEY not found. Add it to ~/.narrate_video.env")
    if not os.environ.get("AZURE_SPEECH_REGION"):
        errors.append("AZURE_SPEECH_REGION not found. Add it to ~/.narrate_video.env")
    if VOICE_NAME == "REPLACE_WITH_VOICE":
        errors.append("VOICE_NAME not set. Replace the placeholder with a voice name (e.g. en-US-AndrewMultilingualNeural)")
    if INPUT_VIDEO == "REPLACE_WITH_INPUT":
        errors.append("INPUT_VIDEO not set. Replace the placeholder with the input video path")
    elif not os.path.isfile(INPUT_VIDEO):
        errors.append(f"INPUT_VIDEO not found: {INPUT_VIDEO}")
    if OUTPUT_VIDEO == "REPLACE_WITH_OUTPUT":
        errors.append("OUTPUT_VIDEO not set. Replace the placeholder with the output video path")
    if not SEGMENTS:
        errors.append("SEGMENTS is empty. Add at least one (start_seconds, text) tuple")
    for i, seg in enumerate(SEGMENTS):
        if not isinstance(seg, (list, tuple)) or len(seg) != 2:
            errors.append(f"SEGMENTS[{i}]: must be a (start_seconds, text) tuple")
        elif not isinstance(seg[0], (int, float)) or seg[0] < 0:
            errors.append(f"SEGMENTS[{i}]: start_seconds must be a non-negative number")
        elif not isinstance(seg[1], str) or not seg[1].strip():
            errors.append(f"SEGMENTS[{i}]: text must be a non-empty string")
    if errors:
        print("ERROR: Fix the following before running:\n")
        for e in errors:
            print(f"  - {e}")
        return False
    return True


if __name__ == "__main__":
    if not check_inputs():
        exit(1)
    build_narrated_video()
