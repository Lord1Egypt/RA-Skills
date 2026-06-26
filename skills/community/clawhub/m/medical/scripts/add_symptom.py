#!/usr/bin/env python3
"""Add a symptom to the tracker."""
import json
import os
import uuid
import argparse
from datetime import datetime

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
SYMPTOMS_FILE = os.path.join(HEALTH_DIR, "symptoms.json")

def ensure_dir():
    os.makedirs(HEALTH_DIR, exist_ok=True)

def load_symptoms():
    if os.path.exists(SYMPTOMS_FILE):
        with open(SYMPTOMS_FILE, 'r') as f:
            return json.load(f)
    return {"symptoms": []}

def save_symptoms(data):
    ensure_dir()
    with open(SYMPTOMS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def check_emergency_red_flags(description):
    """Check for symptoms that suggest emergency."""
    red_flags = [
        "chest pain", "can't breathe", "difficulty breathing", 
        "severe bleeding", "unconscious", "suicidal",
        "worst headache", "stroke", "heart attack"
    ]
    desc_lower = description.lower()
    for flag in red_flags:
        if flag in desc_lower:
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description='Add a symptom')
    parser.add_argument('--description', required=True, help='Symptom description')
    parser.add_argument('--severity', type=int, required=True, 
                        help='Severity 1-10', choices=range(1, 11))
    parser.add_argument('--location', default='', help='Body location')
    parser.add_argument('--triggers', default='', help='Triggers (comma-separated)')
    parser.add_argument('--notes', default='', help='Additional notes')
    
    args = parser.parse_args()
    
    # Check for emergency red flags
    if check_emergency_red_flags(args.description):
        print("🚨 EMERGENCY WARNING 🚨")
        print("Your symptom description may indicate a medical emergency.")
        print("If you are experiencing chest pain, difficulty breathing, severe bleeding,")
        print("or thoughts of self-harm, call 911 or your local emergency number immediately.")
        print("\nDo not wait - seek emergency care now.")
        sys.exit(1)
    
    data = load_symptoms()
    
    symptom = {
        "id": str(uuid.uuid4())[:8],
        "description": args.description,
        "severity": args.severity,
        "location": args.location,
        "triggers": [t.strip() for t in args.triggers.split(',') if t.strip()],
        "notes": args.notes,
        "timestamp": datetime.now().isoformat(),
        "ongoing": True
    }
    
    data['symptoms'].append(symptom)
    save_symptoms(data)
    
    print(f"✓ Logged: {args.description}")
    print(f"  Severity: {args.severity}/10")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if args.location:
        print(f"  Location: {args.location}")
    print(f"\nStored in: {SYMPTOMS_FILE}")

if __name__ == '__main__':
    main()
