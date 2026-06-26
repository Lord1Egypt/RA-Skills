#!/usr/bin/env python3
"""Save AI-sculpted Instagram captions to local workspace."""
import json
import os
import uuid
import argparse
from datetime import datetime

INSTAGRAM_DIR = os.path.expanduser("~/.openclaw/workspace/memory/instagram")
CAPTIONS_FILE = os.path.join(INSTAGRAM_DIR, "captions.json")

def ensure_dir():
    os.makedirs(INSTAGRAM_DIR, exist_ok=True)

def load_captions():
    if os.path.exists(CAPTIONS_FILE):
        with open(CAPTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"captions": []}

def save_captions(data):
    ensure_dir()
    with open(CAPTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='Save optimized Instagram caption locally')
    parser.add_argument('--content', required=True, help='The fully sculpted caption text')
    parser.add_argument('--goal', default='engagement', help='Caption goal (e.g., save, comment, dm)')
    parser.add_argument(
        '--funnel_type',
        default='awareness',
        choices=['awareness', 'trust', 'lead_gen', 'conversion'],
        help='Position in the attention funnel'
    )

    args = parser.parse_args()

    data = load_captions()
    cap_id = f"CAP-{str(uuid.uuid4())[:6].upper()}"

    cap_data = {
        "id": cap_id,
        "funnel_type": args.funnel_type,
        "goal": args.goal,
        "content": args.content,
        "created_at": datetime.now().isoformat()
    }

    data['captions'].append(cap_data)
    save_captions(data)

    print(f"✅ [SUCCESS] Caption {cap_id} saved to local memory.")
    print(f"📁 Path: {CAPTIONS_FILE}")
    print(f"🎯 Funnel: {args.funnel_type.upper()} | Goal: {args.goal}")

if __name__ == '__main__':
    main()
