#!/usr/bin/env python3
"""Capture note from any context."""
import json
import os
import uuid
import argparse
from datetime import datetime

NOTES_DIR = os.path.expanduser("~/.openclaw/workspace/memory/notes")
NOTES_FILE = os.path.join(NOTES_DIR, "notes.json")

def ensure_dir():
    os.makedirs(NOTES_DIR, exist_ok=True)

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return {"notes": []}

def save_notes(data):
    ensure_dir()
    with open(NOTES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Capture note')
    parser.add_argument('--content', required=True, help='Note content')
    parser.add_argument('--context', default='general', help='Context (meeting, reading, thought, etc)')
    parser.add_argument('--project', help='Related project')
    parser.add_argument('--tags', help='Tags (comma-separated)')
    
    args = parser.parse_args()
    
    note_id = f"NOTE-{str(uuid.uuid4())[:6].upper()}"
    
    # Extract topics from content (simplified)
    topics = []
    if args.project:
        topics.append(args.project)
    
    note = {
        "id": note_id,
        "content": args.content,
        "context": args.context,
        "project": args.project,
        "topics": topics,
        "tags": [t.strip() for t in args.tags.split(',') if args.tags],
        "created_at": datetime.now().isoformat(),
        "connections": []
    }
    
    data = load_notes()
    data['notes'].append(note)
    save_notes(data)
    
    print(f"✓ Note captured: {note_id}")
    print(f"  {args.content[:80]}{'...' if len(args.content) > 80 else ''}")
    print(f"  Context: {args.context}")
    if args.project:
        print(f"  Project: {args.project}")

if __name__ == '__main__':
    main()
