#!/usr/bin/env python3
"""
Local TTS wrapper for macOS using mlx_audio.

This script provides a simplified interface for Qwen3-TTS on macOS with Apple Silicon.
"""

import argparse
import subprocess
import sys
import os

# Default configurations
DEFAULT_FEMALE_VOICE = "Chelsie"
DEFAULT_MALE_VOICE = "Aiden"

MODELS = {
    "base": "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit",
    "voicedesign": "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit",
    "customvoice": "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit",
    "base-small": "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit",
    "voicedesign-small": "mlx-community/Qwen3-TTS-12Hz-0.6B-VoiceDesign-8bit",
    "customvoice-small": "mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-8bit",
}

PRESET_VOICES = {
    "female": ["Chelsie", "Breeze"],
    "male": ["Ryan", "Aiden"],
}


def run_tts(args):
    """Run TTS with the given arguments."""
    
    # Build command
    cmd = [
        sys.executable, "-m", "mlx_audio.tts.generate",
        "--text", args.text,
        "--model", MODELS.get(args.model, args.model),
    ]
    
    # Add output path
    if args.output:
        cmd.extend(["--output", args.output])
    
    # Add voice (CustomVoice)
    if args.voice:
        cmd.extend(["--voice", args.voice])
    
    # Add instruct (VoiceDesign)
    if args.instruct:
        cmd.extend(["--instruct", args.instruct])
    
    # Add reference audio for cloning
    if args.ref_audio:
        cmd.extend(["--ref_audio", args.ref_audio])
    if args.ref_text:
        cmd.extend(["--ref_text", args.ref_text])
    
    # Add parameters
    if args.speed is not None:
        cmd.extend(["--speed", str(args.speed)])
    if args.gender:
        cmd.extend(["--gender", args.gender])
    if args.pitch is not None:
        cmd.extend(["--pitch", str(args.pitch)])
    if args.lang_code:
        cmd.extend(["--lang_code", args.lang_code])
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Local TTS using Qwen3-TTS with mlx_audio (macOS)"
    )
    
    # Required arguments
    parser.add_argument("text", help="Text to synthesize")
    
    # Model selection
    parser.add_argument(
        "--model", "-m",
        default="customvoice",
        choices=list(MODELS.keys()),
        help="Model to use (default: customvoice)"
    )
    
    # Output
    parser.add_argument(
        "--output", "-o",
        help="Output audio file path"
    )
    
    # Voice selection (mutually exclusive)
    voice_group = parser.add_mutually_exclusive_group()
    voice_group.add_argument(
        "--voice", "-v",
        help="Preset voice name (for CustomVoice model): Chelsie, Breeze, Ryan, Aiden"
    )
    voice_group.add_argument(
        "--instruct", "-i",
        help="Voice description (for VoiceDesign model), e.g., 'A warm female voice'"
    )
    
    # Quick voice presets
    parser.add_argument(
        "--female", "-f",
        action="store_true",
        help="Use default female voice (Chelsie)"
    )
    parser.add_argument(
        "--male", "-M",
        action="store_true",
        help="Use default male voice (Ryan)"
    )
    
    # Voice cloning
    parser.add_argument(
        "--ref_audio", "-r",
        help="Reference audio file for voice cloning"
    )
    parser.add_argument(
        "--ref_text",
        help="Reference text for voice cloning"
    )
    
    # Voice parameters
    parser.add_argument(
        "--speed", "-s",
        type=float,
        help="Speaking speed (0.5-2.0, default: 1.0)"
    )
    parser.add_argument(
        "--gender", "-g",
        choices=["male", "female"],
        help="Voice gender"
    )
    parser.add_argument(
        "--pitch", "-p",
        type=float,
        help="Voice pitch (0.5-2.0, default: 1.0)"
    )
    parser.add_argument(
        "--lang_code", "-l",
        default="en-US",
        help="Language code (default: en-US, use 'zh-CN' for Chinese)"
    )
    
    args = parser.parse_args()
    
    # Handle quick presets
    if args.female:
        if args.model == "voicedesign":
            args.instruct = args.instruct or "A warm female voice, clear and friendly"
        else:
            args.voice = args.voice or DEFAULT_FEMALE_VOICE
    elif args.male:
        if args.model == "voicedesign":
            args.instruct = args.instruct or "A deep male voice, warm and professional"
        else:
            args.voice = args.voice or DEFAULT_MALE_VOICE
    
    # Validate arguments
    if args.model == "voicedesign" and not args.instruct and not (args.female or args.male):
        print("Warning: VoiceDesign model requires --instruct parameter. Use --female/--male for defaults.")
    
    if args.model == "customvoice" and not args.voice and not args.female and not args.male:
        print("Warning: CustomVoice model works best with --voice parameter. Use --female/--male for defaults.")
    
    # Run TTS
    return run_tts(args)


if __name__ == "__main__":
    sys.exit(main())
