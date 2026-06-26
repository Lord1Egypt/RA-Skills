#!/usr/bin/env python3
"""List current medications."""
import json
import os
import argparse

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
MEDS_FILE = os.path.join(HEALTH_DIR, "medications.json")

def load_meds():
    if not os.path.exists(MEDS_FILE):
        return {"medications": []}
    with open(MEDS_FILE, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='List medications')
    parser.add_argument('--current-only', action='store_true', 
                        help='Show only active medications')
    parser.add_argument('--format', choices=['table', 'json'], default='table',
                        help='Output format')
    
    args = parser.parse_args()
    
    data = load_meds()
    meds = data.get('medications', [])
    
    if args.current_only:
        meds = [m for m in meds if m.get('ongoing', True)]
    
    if not meds:
        print("No medications recorded.")
        return
    
    if args.format == 'json':
        print(json.dumps(meds, indent=2))
        return
    
    # Table format
    print(f"\n{'Medication':<20} {'Dosage':<12} {'Frequency':<15} {'Notes':<20}")
    print("-" * 70)
    
    for med in meds:
        status = "[STOPPED]" if not med.get('ongoing', True) else ""
        notes = []
        if med.get('with_food'):
            notes.append("with food")
        if med.get('time_of_day'):
            notes.append(med['time_of_day'])
        note_str = ", ".join(notes)
        
        print(f"{med['name']:<20} {med['dosage']:<12} {med['frequency']:<15} {note_str:<15} {status}")
    
    print(f"\nTotal: {len(meds)} medications")
    if args.current_only:
        print("(Showing active medications only)")

if __name__ == '__main__':
    main()
