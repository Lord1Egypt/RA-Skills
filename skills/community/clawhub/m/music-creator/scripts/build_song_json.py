#!/usr/bin/env python3
"""
生成 song.json 歌曲信息文件

用法：
  python3 build_song_json.py \
    --title "歌名" \
    --subtitle "副标题" \
    --artist "microsnow" \
    --credits-lyrics "microsnow" \
    --credits-compose "microsnow" \
    --credits-sing "microsnow" \
    --credits-produce "microsnow" \
    --output /path/to/song.json
"""

import argparse
import json
import os


def build(title, subtitle, artist, credits, output_path):
    data = {
        "title": title,
        "subtitle": subtitle or "",
        "artist": artist or "",
        "credits": {
            "lyrics": credits.get("lyrics", artist),
            "compose": credits.get("compose", artist),
            "sing": credits.get("sing", artist),
            "produce": credits.get("produce", artist),
        }
    }
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ song.json saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Build song.json')
    parser.add_argument('--title', required=True)
    parser.add_argument('--subtitle', default='')
    parser.add_argument('--artist', default='')
    parser.add_argument('--credits-lyrics', default='')
    parser.add_argument('--credits-compose', default='')
    parser.add_argument('--credits-sing', default='')
    parser.add_argument('--credits-produce', default='')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    credits = {
        'lyrics': args.credits_lyrics,
        'compose': args.credits_compose,
        'sing': args.credits_sing,
        'produce': args.credits_produce,
    }
    # Use artist as default for any empty credit
    for k, v in credits.items():
        if not v:
            credits[k] = args.artist

    build(args.title, args.subtitle, args.artist, credits, args.output)


if __name__ == '__main__':
    main()
