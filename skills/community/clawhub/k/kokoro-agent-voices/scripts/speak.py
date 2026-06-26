#!/usr/bin/env /Users/loki/.kokoro-venv/bin/python3
"""Agent voice synthesis via Kokoro TTS.

Usage:
    speak.py "Text to speak" [--voice af_bella] [--speed 1.0] [--output /tmp/out.wav]
    speak.py --agent loki "Text to speak"
    speak.py --list-voices
    speak.py --list-agents
"""
import argparse
import json
import os
import sys
from pathlib import Path

VOICE_PROFILES = {
    "loki": {
        "voice": "am_fenrir",  # Norse wolf — fits a cat named after a Norse god
        "speed": 1.05,
        "description": "Curious, playful, sharp. The digital cat.",
    },
    "analyst": {
        "voice": "bm_george",  # British male, measured and precise
        "speed": 0.95,
        "description": "Methodical, data-driven, dry wit.",
    },
    "content": {
        "voice": "af_bella",  # Warm female, storyteller energy
        "speed": 1.0,
        "description": "Creative, warm, voice-conscious. The writer.",
    },
    "engineer": {
        "voice": "am_echo",  # Clear, technical, focused
        "speed": 1.1,
        "description": "Fast, precise, no-nonsense. Ships code.",
    },
    "marketing": {
        "voice": "af_sarah",  # Confident, commanding female — Olivia Pope energy
        "speed": 1.05,
        "description": "Direct, decisive, warm but no-nonsense. The fixer.",
    },
}

def list_voices():
    """List all available Kokoro voices."""
    from kokoro import KPipeline
    import huggingface_hub, glob
    path = huggingface_hub.snapshot_download('hexgrad/Kokoro-82M', allow_patterns='voices/*')
    voices = sorted(glob.glob(os.path.join(path, 'voices', '*.pt')))
    print("Available Kokoro voices:")
    for v in voices:
        name = os.path.basename(v).replace('.pt', '')
        prefix = name[:2]
        lang = {'af': '🇺🇸F', 'am': '🇺🇸M', 'bf': '🇬🇧F', 'bm': '🇬🇧M',
                'ef': '🇪🇸F', 'em': '🇪🇸M', 'ff': '🇫🇷F', 'hf': '🇮🇳F',
                'hm': '🇮🇳M', 'if': '🇮🇹F', 'im': '🇮🇹M', 'jf': '🇯🇵F',
                'jm': '🇯🇵M', 'pf': '🇧🇷F', 'pm': '🇧🇷M', 'zf': '🇨🇳F',
                'zm': '🇨🇳M'}.get(prefix, '??')
        print(f"  {name:20s} {lang}")

def list_agents():
    """List configured agent voice profiles."""
    print("Agent voice profiles:")
    for name, profile in VOICE_PROFILES.items():
        print(f"  {name:12s} → {profile['voice']:15s} speed={profile['speed']}  {profile['description']}")

def speak(text: str, voice: str = "af_bella", speed: float = 1.0, output: str = "/tmp/agent_speech.wav"):
    """Generate speech and save to WAV."""
    from kokoro import KPipeline
    import soundfile as sf
    import numpy as np

    lang_code = voice[0] if voice[0] in 'abefhijpz' else 'a'
    pipeline = KPipeline(lang_code=lang_code, repo_id='hexgrad/Kokoro-82M')

    all_audio = []
    for _, _, audio in pipeline(text, voice=voice, speed=speed):
        all_audio.append(audio)

    if all_audio:
        combined = np.concatenate(all_audio)
        sf.write(output, combined, 24000)
        duration = len(combined) / 24000
        print(f"✅ {duration:.1f}s audio → {output}")
        return output
    else:
        print("❌ No audio generated")
        return None

def main():
    parser = argparse.ArgumentParser(description="Agent voice synthesis via Kokoro TTS")
    parser.add_argument("text", nargs="?", help="Text to speak")
    parser.add_argument("--voice", default="af_bella", help="Kokoro voice name")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.5-2.0)")
    parser.add_argument("--output", "-o", default="/tmp/agent_speech.wav", help="Output WAV path")
    parser.add_argument("--agent", help="Use agent voice profile (loki/analyst/content/engineer)")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--list-agents", action="store_true", help="List agent voice profiles")
    parser.add_argument("--play", action="store_true", help="Play audio after generation (macOS)")

    args = parser.parse_args()

    if args.list_voices:
        list_voices()
        return
    if args.list_agents:
        list_agents()
        return

    if not args.text:
        parser.error("Text is required unless using --list-voices or --list-agents")

    voice = args.voice
    speed = args.speed

    if args.agent:
        profile = VOICE_PROFILES.get(args.agent)
        if not profile:
            print(f"❌ Unknown agent: {args.agent}. Available: {', '.join(VOICE_PROFILES.keys())}")
            sys.exit(1)
        voice = profile["voice"]
        speed = profile["speed"]

    out = speak(args.text, voice=voice, speed=speed, output=args.output)

    if args.play and out:
        os.system(f"afplay {out}")

if __name__ == "__main__":
    main()
