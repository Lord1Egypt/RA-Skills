#!/usr/bin/env python3
"""
Voice provider configuration and testing.
Configures ElevenLabs, Grok TTS, or built-in TTS in openclaw.json.

Usage:
    python3 voice-setup.py --provider elevenlabs --voice-id abc123 --config ~/.openclaw/openclaw.json
    python3 voice-setup.py --provider builtin --voice nova
    python3 voice-setup.py --interactive
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.providers import get_voice_provider_config, VOICE_PRESETS
from lib.config import merge_config, set_tts_config


def interactive_setup(config_path):
    """Run interactive voice setup."""
    print("\n🔊 Voice Setup\n")
    print("  Choose a voice provider:")
    print("    [1] ElevenLabs (best quality, custom voices, cloning)")
    print("    [2] Grok TTS (xAI, integrated with Grok models)")
    print("    [3] Built-in OpenClaw TTS (no API key needed)")
    print("    [4] None (text only)")

    choice = input("  > ").strip()
    provider_map = {"1": "elevenlabs", "2": "grok", "3": "builtin", "4": "none"}
    provider = provider_map.get(choice, "none")

    if provider == "none":
        print("  Voice disabled.")
        return

    kwargs = {}

    if provider == "elevenlabs":
        voice_id = input("  ElevenLabs Voice ID: ").strip()
        if voice_id:
            kwargs["voice_id"] = voice_id
        model = input("  Model ID [eleven_v3]: ").strip() or "eleven_v3"
        kwargs["model_id"] = model

        print("\n  Configure voice presets? (y/n)")
        if input("  > ").strip().lower().startswith("y"):
            kwargs["stability"] = float(input("  Stability (0.0-1.0) [0.5]: ").strip() or "0.5")
            kwargs["similarity_boost"] = float(input("  Similarity Boost (0.0-1.0) [0.75]: ").strip() or "0.75")
            kwargs["style"] = float(input("  Style (0.0-1.0) [0.0]: ").strip() or "0.0")

    elif provider == "grok":
        model = input("  Model ID [grok-3-tts]: ").strip() or "grok-3-tts"
        kwargs["model_id"] = model

    elif provider == "builtin":
        voice = input("  Voice name [nova]: ").strip() or "nova"
        kwargs["voice"] = voice

    voice_config = get_voice_provider_config(provider, **kwargs)
    if voice_config:
        set_tts_config(voice_config, config_path)
        # Also store in persona.voice
        merge_config({"persona": {"voice": voice_config}}, config_path)
        print(f"\n  ✅ Voice configured: {provider}")


def non_interactive_setup(provider, config_path, **kwargs):
    """Configure voice provider non-interactively."""
    if provider == "none":
        return

    voice_config = get_voice_provider_config(provider, **kwargs)
    if voice_config:
        set_tts_config(voice_config, config_path)
        merge_config({"persona": {"voice": voice_config}}, config_path)
        print(f"Voice configured: {provider}", file=sys.stderr)


def audition_voices(provider="elevenlabs", gender=None, accent=None):
    """Generate the same test phrase with multiple voice configurations for comparison."""
    test_phrase = "Hello! I'm your new AI assistant. I'm here to help you with whatever you need — whether that's planning your day, answering questions, or just having a conversation."

    print("\n🎧 Voice Audition\n")
    print(f"  Test phrase: \"{test_phrase[:60]}...\"\n")

    if provider == "elevenlabs":
        # ElevenLabs voice catalog (curated defaults)
        voices = [
            {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "desc": "Calm, warm female voice", "gender": "female", "accent": "american"},
            {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi", "desc": "Strong, confident female voice", "gender": "female", "accent": "american"},
            {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "desc": "Soft, gentle female voice", "gender": "female", "accent": "american"},
            {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni", "desc": "Well-rounded male voice", "gender": "male", "accent": "american"},
            {"id": "VR6AewLTigWG4xSOukaG", "name": "Arnold", "desc": "Deep, authoritative male voice", "gender": "male", "accent": "american"},
            {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam", "desc": "Versatile male narrator", "gender": "male", "accent": "american"},
            {"id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam", "desc": "Warm, articulate male voice", "gender": "male", "accent": "american"},
            {"id": "jBpfuIE2acCO8z3wKNLl", "name": "Gigi", "desc": "Energetic, youthful female", "gender": "female", "accent": "american"},
        ]

        # Filter by gender/accent
        filtered = voices
        if gender:
            filtered = [v for v in filtered if v["gender"] == gender.lower()]
        if accent:
            filtered = [v for v in filtered if accent.lower() in v["accent"].lower()]

        # Take top 5
        candidates = filtered[:5] if filtered else voices[:5]

        print(f"  Provider: ElevenLabs")
        if gender:
            print(f"  Filter: gender={gender}")
        if accent:
            print(f"  Filter: accent={accent}")
        print(f"  Candidates: {len(candidates)}\n")

        for i, voice in enumerate(candidates, 1):
            print(f"  Voice {i}: {voice['name']}")
            print(f"    {voice['desc']}")
            print(f"    ID: {voice['id']}")
            print(f"    To select: --voice-id {voice['id']}")
            print()

        results = []
        for v in candidates:
            results.append({
                "number": candidates.index(v) + 1,
                "name": v["name"],
                "id": v["id"],
                "description": v["desc"],
            })

        return results

    elif provider == "builtin":
        builtin_voices = [
            {"name": "nova", "desc": "Warm, versatile female voice"},
            {"name": "alloy", "desc": "Neutral, balanced voice"},
            {"name": "echo", "desc": "Clear, articulate male voice"},
            {"name": "fable", "desc": "Expressive, storytelling voice"},
            {"name": "onyx", "desc": "Deep, authoritative male voice"},
            {"name": "shimmer", "desc": "Bright, energetic female voice"},
        ]

        print(f"  Provider: Built-in OpenClaw TTS\n")

        for i, voice in enumerate(builtin_voices, 1):
            print(f"  Voice {i}: {voice['name']}")
            print(f"    {voice['desc']}")
            print(f"    To select: --voice {voice['name']}")
            print()

        return [{"number": i + 1, "name": v["name"], "description": v["desc"]}
                for i, v in enumerate(builtin_voices)]

    else:
        print(f"  Audition not available for provider: {provider}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Voice provider setup")
    parser.add_argument("--provider", choices=["elevenlabs", "grok", "builtin", "none"])
    parser.add_argument("--voice-id", default="")
    parser.add_argument("--model-id", default="")
    parser.add_argument("--voice", default="nova", help="Built-in voice name")
    parser.add_argument("--stability", type=float, default=0.5)
    parser.add_argument("--similarity-boost", type=float, default=0.75)
    parser.add_argument("--style", type=float, default=0.0)
    parser.add_argument("--config", default=str(Path.home() / ".openclaw" / "openclaw.json"))
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--audition", action="store_true", help="Audition multiple voices")
    parser.add_argument("--gender", help="Filter voices by gender (male/female)")
    parser.add_argument("--accent", help="Filter voices by accent (american/british)")
    args = parser.parse_args()

    if args.audition:
        provider = args.provider or "elevenlabs"
        audition_voices(provider, gender=args.gender, accent=args.accent)
    elif args.interactive:
        interactive_setup(args.config)
    elif args.provider:
        kwargs = {}
        if args.voice_id:
            kwargs["voice_id"] = args.voice_id
        if args.model_id:
            kwargs["model_id"] = args.model_id
        if args.provider == "builtin":
            kwargs["voice"] = args.voice
        kwargs["stability"] = args.stability
        kwargs["similarity_boost"] = args.similarity_boost
        kwargs["style"] = args.style
        non_interactive_setup(args.provider, args.config, **kwargs)
    else:
        interactive_setup(args.config)


if __name__ == "__main__":
    main()
