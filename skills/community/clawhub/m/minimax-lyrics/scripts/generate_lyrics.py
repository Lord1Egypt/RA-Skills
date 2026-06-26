#!/usr/bin/env python3
"""
Generate song lyrics using MiniMax lyrics_generation API.

Usage:
  python3 generate_lyrics.py --prompt "<style description>" --title "<song title>"

Example:
  python3 generate_lyrics.py --prompt "轻柔抒情流行，温柔女声，慢节奏，深情浪漫" --title "夏日海风"
"""

import sys
import json
import argparse
import os

def get_minimax_key() -> str:
    """Extract MiniMax API key from this skill's lyrics_config.json."""
    config_path = os.path.expanduser('~/.openclaw/workspace/skills/minimax-lyrics/lyrics_config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    api_key = config.get('api_key')
    if not api_key:
        raise ValueError(f"No 'api_key' found in {config_path}")
    return api_key

def generate_lyrics(prompt: str, api_key: str, title: str = None, mode: str = "write_full_song", existing_lyrics: str = None) -> dict:
    """Generate lyrics via MiniMax API. Returns dict with song_title, style_tags, lyrics."""
    import urllib.request

    url = "https://api.minimaxi.com/v1/lyrics_generation"
    payload = {
        "mode": mode,
        "prompt": prompt,
    }
    if title:
        payload["title"] = title
    if mode == "edit" and existing_lyrics:
        payload["lyrics"] = existing_lyrics

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        method='POST'
    )

    print(f"Calling MiniMax lyrics API...", file=sys.stderr)
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    if result.get('base_resp', {}).get('status_code') != 0:
        raise ValueError(f"Lyrics API error: {result}")

    return {
        'song_title': result.get('song_title'),
        'style_tags': result.get('style_tags'),
        'lyrics': result.get('lyrics')
    }

def main():
    parser = argparse.ArgumentParser(description='Generate song lyrics via MiniMax API')
    parser.add_argument('--prompt', required=True, help='Song style/theme description')
    parser.add_argument('--title', help='Song title (optional)')
    parser.add_argument('--mode', default='write_full_song', help='Generation mode: write_full_song or edit')
    parser.add_argument('--lyrics', help='Existing lyrics for edit mode')
    args = parser.parse_args()

    api_key = get_minimax_key()
    result = generate_lyrics(args.prompt, api_key, args.title, args.mode, args.lyrics)

    # Print as formatted output for human reading
    print(f"\n=== Generated Lyrics ===", file=sys.stderr)
    print(f"Title: {result['song_title']}", file=sys.stderr)
    print(f"Style: {result['style_tags']}", file=sys.stderr)
    print(f"\n{result['lyrics']}", file=sys.stderr)

    # Also output clean JSON for parsing
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
