#!/usr/bin/env python3
"""Prepare for likely objections."""
import json
import os
import uuid
import argparse
from datetime import datetime

PITCH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/pitch")
OBJECTIONS_FILE = os.path.join(PITCH_DIR, "objections.json")

def ensure_dir():
    os.makedirs(PITCH_DIR, exist_ok=True)

def load_objections():
    if os.path.exists(OBJECTIONS_FILE):
        with open(OBJECTIONS_FILE, 'r') as f:
            return json.load(f)
    return {"objections": []}

def save_objections(data):
    ensure_dir()
    with open(OBJECTIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_common_objections(audience, stage):
    """Generate common objections based on audience and stage."""
    objections = []
    
    if audience == 'investor':
        if stage == 'seed':
            objections = [
                ("competition", "What if Google/Facebook builds this?", "high"),
                ("traction", "You don't have enough traction yet", "high"),
                ("market", "Is this market big enough?", "medium"),
                ("team", "Does your team have the right experience?", "medium"),
            ]
        elif stage == 'series_a':
            objections = [
                ("growth", "Can you maintain this growth rate?", "high"),
                ("unit_economics", "Your unit economics don't work", "high"),
                ("moat", "What's your defensibility?", "medium"),
            ]
    elif audience == 'customer':
        objections = [
            ("price", "This is too expensive", "high"),
            ("switching", "It's too hard to switch from what we use", "medium"),
            ("trust", "How do we know you'll be around in 2 years?", "medium"),
        ]
    
    return objections

def main():
    parser = argparse.ArgumentParser(description='Prepare for objections')
    parser.add_argument('--foundation-id', required=True, help='Foundation ID')
    parser.add_argument('--audience', required=True,
                        choices=['investor', 'customer', 'partner'],
                        help='Target audience')
    parser.add_argument('--stage', default='seed',
                        choices=['idea', 'seed', 'series_a', 'growth'],
                        help='Company stage')
    
    args = parser.parse_args()
    
    data = load_objections()
    
    generated = generate_common_objections(args.audience, args.stage)
    
    for category, objection, severity in generated:
        obj = {
            "id": f"OBJ-{str(uuid.uuid4())[:6].upper()}",
            "foundation_id": args.foundation_id,
            "category": category,
            "objection": objection,
            "severity": severity,
            "response": {
                "acknowledge": "",
                "context": "",
                "evidence": "",
                "bridge": ""
            },
            "created_at": datetime.now().isoformat()
        }
        data['objections'].append(obj)
    
    save_objections(data)
    
    print(f"✓ Generated {len(generated)} likely objections")
    print(f"  Audience: {args.audience}")
    print(f"  Stage: {args.stage}")
    print(f"\nNext steps:")
    print(f"  1. Edit objections.json to add your responses")
    print(f"  2. Practice responses until natural")
    print(f"  3. Add follow-up questions they might ask")

if __name__ == '__main__':
    main()
