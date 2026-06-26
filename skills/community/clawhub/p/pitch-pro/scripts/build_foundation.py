#!/usr/bin/env python3
"""Build pitch foundation."""
import json
import os
import uuid
import argparse
from datetime import datetime

PITCH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/pitch")
FOUNDATION_FILE = os.path.join(PITCH_DIR, "foundations.json")

def ensure_dir():
    os.makedirs(PITCH_DIR, exist_ok=True)

def load_foundations():
    if os.path.exists(FOUNDATION_FILE):
        with open(FOUNDATION_FILE, 'r') as f:
            return json.load(f)
    return {"foundations": []}

def save_foundations(data):
    ensure_dir()
    with open(FOUNDATION_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Build pitch foundation')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--problem', required=True, help='Problem statement')
    parser.add_argument('--solution', required=True, help='Solution description')
    parser.add_argument('--market', help='Market size')
    
    args = parser.parse_args()
    
    foundation_id = f"FOUND-{str(uuid.uuid4())[:6].upper()}"
    
    foundation = {
        "id": foundation_id,
        "company_name": args.company,
        "created_at": datetime.now().isoformat(),
        "problem": {
            "statement": args.problem,
            "evidence": "",
            "pain_level": ""
        },
        "solution": {
            "description": args.solution,
            "key_differentiator": "",
            "why_now": ""
        },
        "target_customer": {
            "primary": "",
            "size": "",
            "willingness_to_pay": ""
        },
        "business_model": {
            "revenue_model": "",
            "pricing": "",
            "market_size": args.market or ""
        },
        "traction": {
            "metrics": []
        },
        "team": {
            "founders": [],
            "why_now": ""
        }
    }
    
    data = load_foundations()
    data['foundations'].append(foundation)
    save_foundations(data)
    
    print(f"✓ Foundation created: {foundation_id}")
    print(f"  Company: {args.company}")
    print(f"  Problem: {args.problem}")
    print(f"\nNext steps:")
    print(f"  1. Add evidence for problem statement")
    print(f"  2. Define target customer details")
    print(f"  3. Add traction metrics")
    print(f"  4. Run: prep_objections.py to prepare for Q&A")

if __name__ == '__main__':
    main()
