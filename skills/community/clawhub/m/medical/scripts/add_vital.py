#!/usr/bin/env python3
"""Add a vital sign reading."""
import json
import os
import uuid
import argparse
from datetime import datetime

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
VITALS_FILE = os.path.join(HEALTH_DIR, "vitals.json")

def ensure_dir():
    os.makedirs(HEALTH_DIR, exist_ok=True)

def load_vitals():
    if os.path.exists(VITALS_FILE):
        with open(VITALS_FILE, 'r') as f:
            return json.load(f)
    return {"vitals": {}, "targets": {}}

def save_vitals(data):
    ensure_dir()
    with open(VITALS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Add vital sign reading')
    parser.add_argument('--type', required=True, 
                        choices=['bp', 'glucose', 'weight', 'hr', 'temp', 'pain', 'o2'],
                        help='Type of vital sign')
    parser.add_argument('--systolic', type=int, help='BP systolic')
    parser.add_argument('--diastolic', type=int, help='BP diastolic')
    parser.add_argument('--value', help='Value (for glucose, weight, etc)')
    parser.add_argument('--unit', default='', help='Unit (mg/dL, lbs, etc)')
    parser.add_argument('--context', default='', help='Context (fasting, resting, etc)')
    parser.add_argument('--location', default='', help='Pain location')
    parser.add_argument('--level', type=int, choices=range(0, 11), help='Pain level 0-10')
    parser.add_argument('--notes', default='', help='Additional notes')
    
    args = parser.parse_args()
    
    data = load_vitals()
    timestamp = datetime.now().isoformat()
    
    reading = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": timestamp,
        "notes": args.notes
    }
    
    vital_type = args.type
    
    if vital_type == 'bp':
        if not args.systolic or not args.diastolic:
            print("Error: BP requires --systolic and --diastolic")
            sys.exit(1)
        reading['systolic'] = args.systolic
        reading['diastolic'] = args.diastolic
        display = f"{args.systolic}/{args.diastolic} mmHg"
        
        # Check against target
        target = data.get('targets', {}).get('bp', {})
        if target:
            sys_max = target.get('systolic_max', 130)
            dia_max = target.get('diastolic_max', 85)
            if args.systolic > sys_max or args.diastolic > dia_max:
                print(f"⚠️  Above target: <{sys_max}/{dia_max}")
    
    elif vital_type == 'glucose':
        if not args.value:
            print("Error: Glucose requires --value")
            sys.exit(1)
        reading['value'] = float(args.value)
        reading['unit'] = args.unit or 'mg/dL'
        reading['context'] = args.context
        display = f"{args.value} {reading['unit']}"
        if args.context:
            display += f" ({args.context})"
    
    elif vital_type == 'weight':
        if not args.value:
            print("Error: Weight requires --value")
            sys.exit(1)
        reading['value'] = float(args.value)
        reading['unit'] = args.unit or 'lbs'
        display = f"{args.value} {reading['unit']}"
    
    elif vital_type == 'hr':
        if not args.value:
            print("Error: Heart rate requires --value")
            sys.exit(1)
        reading['value'] = int(args.value)
        reading['unit'] = 'bpm'
        reading['context'] = args.context or 'resting'
        display = f"{args.value} bpm ({reading['context']})"
    
    elif vital_type == 'pain':
        if args.level is None:
            print("Error: Pain requires --level (0-10)")
            sys.exit(1)
        reading['level'] = args.level
        reading['location'] = args.location
        display = f"Level {args.level}/10"
        if args.location:
            display += f" - {args.location}"
    
    else:
        reading['value'] = args.value
        reading['unit'] = args.unit
        display = f"{args.value} {args.unit}"
    
    if vital_type not in data['vitals']:
        data['vitals'][vital_type] = []
    
    data['vitals'][vital_type].append(reading)
    save_vitals(data)
    
    print(f"✓ Logged: {display}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\nStored in: {VITALS_FILE}")

if __name__ == '__main__':
    import sys
    main()
