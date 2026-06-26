#!/usr/bin/env python3
"""Build STAR format story."""
import json
import os
import uuid
import argparse
from datetime import datetime

INTERVIEW_DIR = os.path.expanduser("~/.openclaw/workspace/memory/interview")

def ensure_dir():
    os.makedirs(INTERVIEW_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Build interview story')
    parser.add_argument('--situation', required=True, help='What was the situation/challenge')
    parser.add_argument('--task', help='What was your specific task')
    parser.add_argument('--action', help='What action did you take')
    parser.add_argument('--result', help='What was the result')
    parser.add_argument('--lesson', help='What did you learn')
    
    args = parser.parse_args()
    
    story_id = f"STORY-{str(uuid.uuid4())[:6].upper()}"
    
    story = {
        "id": story_id,
        "situation": args.situation,
        "task": args.task or "",
        "action": args.action or "",
        "result": args.result or "",
        "lesson": args.lesson or "",
        "created_at": datetime.now().isoformat()
    }
    
    stories_file = os.path.join(INTERVIEW_DIR, "stories.json")
    data = {"stories": []}
    if os.path.exists(stories_file):
        with open(stories_file, 'r') as f:
            data = json.load(f)
    
    data['stories'].append(story)
    
    ensure_dir()
    with open(stories_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Story saved: {story_id}")
    print("\nSTAR STORY FRAMEWORK:")
    print("=" * 60)
    print(f"\nSITUATION:\n{args.situation}")
    if args.task:
        print(f"\nTASK:\n{args.task}")
    if args.action:
        print(f"\nACTION:\n{args.action}")
    if args.result:
        print(f"\nRESULT:\n{args.result}")
    if args.lesson:
        print(f"\nLESSON:\n{args.lesson}")
    
    print("\n💡 Tips:")
    print("  • Keep it under 2 minutes when telling")
    print("  • Use specific numbers/metrics")
    print("  • Focus on YOUR contribution")
    print("  • Practice until it feels natural")

if __name__ == '__main__':
    main()
