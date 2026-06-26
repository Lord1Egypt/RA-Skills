#!/usr/bin/env python3
"""
MiniMax Music Generation CLI

Generate AI music using MiniMax Music 2.5 API.
Supports instrumental music and songs with lyrics.

Usage:
    python3 minimax_music.py create --prompt "Piano, Relaxing" [--lyrics "lyrics text"] [--download OUTPUT_DIR]
    python3 minimax_music.py create --prompt "Pop, Upbeat" --lyrics-file lyrics.txt --download ~/Music
    python3 minimax_music.py create --prompt "Instrumental" --instrumental --download ~/Desktop
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = "https://api.minimaxi.com/v1"
MUSIC_GENERATION_URL = f"{API_BASE_URL}/music_generation"
LYRICS_GENERATION_URL = f"{API_BASE_URL}/lyrics_generation"
DEFAULT_MODEL = "music-2.5"
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_BITRATE = 256000
DEFAULT_FORMAT = "mp3"

# ============================================================================
# API Client
# ============================================================================

class MiniMaxMusicClient:
    """Client for MiniMax Music Generation API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        if not self.api_key:
            raise ValueError(
                "MINIMAX_API_KEY not set. "
                "Set it via environment variable or pass --api-key argument."
            )
    
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_music(
        self,
        prompt: str,
        lyrics: str = "",
        model: str = DEFAULT_MODEL,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        bitrate: int = DEFAULT_BITRATE,
        audio_format: str = DEFAULT_FORMAT,
        output_format: str = "url"
    ) -> dict:
        """
        Generate music from prompt and optional lyrics.
        
        Args:
            prompt: Music style description (e.g., "Piano, Relaxing, Meditative")
            lyrics: Lyrics text with [Verse], [Chorus] markers. Use "[Instrumental]" for pure music.
            model: Model ID (default: music-2.5)
            sample_rate: Audio sample rate (default: 44100)
            bitrate: Audio bitrate (default: 256000)
            audio_format: Output format (default: mp3)
            output_format: Response format ("url" or "hex")
        
        Returns:
            API response with audio URL
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "lyrics": lyrics,
            "audio_setting": {
                "sample_rate": sample_rate,
                "bitrate": bitrate,
                "format": audio_format
            },
            "output_format": output_format
        }
        
        response = requests.post(
            MUSIC_GENERATION_URL,
            json=payload,
            headers=self._headers(),
            timeout=120
        )
        
        result = response.json()
        
        if response.status_code != 200 or result.get("base_resp", {}).get("status_code", 0) != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "Unknown error")
            raise RuntimeError(f"Music generation failed: {error_msg}")
        
        return result
    
    def generate_lyrics(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL
    ) -> dict:
        """
        Generate lyrics from prompt.
        
        Args:
            prompt: Lyrics theme or topic
            model: Model ID
        
        Returns:
            API response with generated lyrics
        """
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        response = requests.post(
            LYRICS_GENERATION_URL,
            json=payload,
            headers=self._headers(),
            timeout=60
        )
        
        result = response.json()
        
        if response.status_code != 200 or result.get("base_resp", {}).get("status_code", 0) != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "Unknown error")
            raise RuntimeError(f"Lyrics generation failed: {error_msg}")
        
        return result

# ============================================================================
# Utility Functions
# ============================================================================

def download_audio(url: str, output_path: str) -> str:
    """Download audio file from URL."""
    print(f"Downloading audio to: {output_path}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    file_size = os.path.getsize(output_path)
    print(f"Downloaded: {output_path} ({file_size / 1024 / 1024:.2f} MB)")
    return output_path

def parse_lyrics_file(file_path: str) -> str:
    """Read lyrics from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def format_duration(seconds: int) -> str:
    """Format duration in seconds to MM:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

# ============================================================================
# CLI Commands
# ============================================================================

def cmd_create(args):
    """Create music from prompt."""
    client = MiniMaxMusicClient(args.api_key)
    
    # Prepare lyrics
    lyrics = ""
    if args.instrumental:
        lyrics = "[Instrumental]"
    elif args.lyrics:
        lyrics = args.lyrics
    elif args.lyrics_file:
        lyrics = parse_lyrics_file(args.lyrics_file)
    
    # Generate music
    print(f"Generating music...")
    print(f"  Prompt: {args.prompt}")
    print(f"  Lyrics: {lyrics[:50]}{'...' if len(lyrics) > 50 else ''}")
    
    try:
        result = client.generate_music(
            prompt=args.prompt,
            lyrics=lyrics,
            model=args.model,
            sample_rate=args.sample_rate,
            bitrate=args.bitrate,
            audio_format=args.format
        )
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    # Extract audio info
    data = result.get("data", {})
    audio_url = data.get("audio", "")
    extra_info = result.get("extra_info", {})
    
    duration_ms = extra_info.get("music_duration", 0)
    duration_sec = duration_ms / 1000 if duration_ms else 0
    
    print(f"\n✅ Music generated successfully!")
    print(f"  Duration: {format_duration(int(duration_sec))}")
    print(f"  Sample rate: {extra_info.get('music_sample_rate', 'N/A')} Hz")
    print(f"  Bitrate: {extra_info.get('bitrate', 'N/A')} bps")
    print(f"  Audio URL: {audio_url[:80]}{'...' if len(audio_url) > 80 else ''}")
    
    # Download if requested
    if args.download and audio_url:
        os.makedirs(args.download, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"minimax_music_{timestamp}.{args.format}"
        output_path = os.path.join(args.download, filename)
        download_audio(audio_url, output_path)
    
    # Output JSON if requested
    if args.json:
        output = {
            "audio_url": audio_url,
            "duration_seconds": duration_sec,
            "sample_rate": extra_info.get("music_sample_rate"),
            "bitrate": extra_info.get("bitrate"),
            "file_size": extra_info.get("music_size")
        }
        print(f"\n{json.dumps(output, indent=2)}")
    
    return 0

def cmd_lyrics(args):
    """Generate lyrics from prompt."""
    client = MiniMaxMusicClient(args.api_key)
    
    print(f"Generating lyrics...")
    print(f"  Prompt: {args.prompt}")
    
    try:
        result = client.generate_lyrics(prompt=args.prompt, model=args.model)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    lyrics = result.get("data", {}).get("lyrics", "")
    
    print(f"\n✅ Lyrics generated:")
    print("-" * 40)
    print(lyrics)
    print("-" * 40)
    
    # Save if requested
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(lyrics)
        print(f"Saved to: {args.output}")
    
    return 0

# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="MiniMax Music Generation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate instrumental music
  python3 minimax_music.py create --prompt "Piano, Relaxing, Ambient" --instrumental --download ~/Music

  # Generate song with lyrics
  python3 minimax_music.py create --prompt "Pop, Upbeat, Celebratory" --lyrics "[Verse]\\nHappy days are here\\n[Chorus]\\nCelebrate!"

  # Generate lyrics first, then music
  python3 minimax_music.py lyrics --prompt "A song about springtime" --output lyrics.txt
  python3 minimax_music.py create --prompt "Folk, Gentle" --lyrics-file lyrics.txt --download ~/Music
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # create command
    create_parser = subparsers.add_parser("create", help="Generate music")
    create_parser.add_argument("--api-key", help="MiniMax API key (or set MINIMAX_API_KEY env var)")
    create_parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    create_parser.add_argument("--prompt", required=True, help="Music style prompt")
    create_parser.add_argument("--lyrics", help="Lyrics text (use \\\\n for line breaks)")
    create_parser.add_argument("--lyrics-file", help="Path to lyrics file")
    create_parser.add_argument("--instrumental", action="store_true", help="Generate instrumental music (no lyrics)")
    create_parser.add_argument("--sample-rate", type=int, default=DEFAULT_SAMPLE_RATE, help=f"Sample rate (default: {DEFAULT_SAMPLE_RATE})")
    create_parser.add_argument("--bitrate", type=int, default=DEFAULT_BITRATE, help=f"Bitrate (default: {DEFAULT_BITRATE})")
    create_parser.add_argument("--format", default=DEFAULT_FORMAT, choices=["mp3", "wav", "flac"], help="Audio format")
    create_parser.add_argument("--download", help="Download audio to directory")
    create_parser.add_argument("--json", action="store_true", help="Output result as JSON")
    create_parser.set_defaults(func=cmd_create)
    
    # lyrics command
    lyrics_parser = subparsers.add_parser("lyrics", help="Generate lyrics")
    lyrics_parser.add_argument("--api-key", help="MiniMax API key (or set MINIMAX_API_KEY env var)")
    lyrics_parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    lyrics_parser.add_argument("--prompt", required=True, help="Lyrics theme or topic")
    lyrics_parser.add_argument("--output", help="Save lyrics to file")
    lyrics_parser.set_defaults(func=cmd_lyrics)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())