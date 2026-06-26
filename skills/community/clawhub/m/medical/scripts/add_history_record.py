#!/usr/bin/env python3
"""Add record to medical history."""
import json
import os
import uuid
import argparse
from datetime import datetime

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
HISTORY_FILE = os.path.join(HEALTH_DIR, "history.json")

def ensure_dir():
    os.makedirs(HEALTH_DIR, exist_ok=True)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {
        "personal_info": {},
        "conditions": [],
        "surgeries": [],
        "hospitalizations": [],
        "allergies": {"medications": [], "foods": [], "environmental": []},
        "immunizations": [],
        "family_history": {},
        "physicians": [],
        "emergency_contacts": []
    }

def save_history(data):
    ensure_dir()
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Add to medical history')
    parser.add_argument('--type', required=True,
                        choices=['personal-info', 'condition', 'surgery', 
                                'hospitalization', 'allergy', 'immunization',
                                'physician', 'emergency-contact'],
                        help='Type of record')
    
    # Common fields
    parser.add_argument('--name', help='Name (medication, condition, etc)')
    parser.add_argument('--date', help='Date (YYYY-MM-DD)')
    parser.add_argument('--notes', default='', help='Additional notes')
    
    # Specific fields
    parser.add_argument('--allergen', help='Allergen name')
    parser.add_argument('--reaction', help='Allergic reaction')
    parser.add_argument('--severity', choices=['mild', 'moderate', 'severe'],
                        help='Allergy severity')
    parser.add_argument('--category', choices=['medications', 'foods', 'environmental'],
                        default='medications', help='Allergy category')
    parser.add_argument('--vaccine', help='Vaccine name')
    parser.add_argument('--next-due', help='Next due date for vaccine')
    parser.add_argument('--physician', help='Doctor name')
    parser.add_argument('--specialty', help='Medical specialty')
    parser.add_argument('--phone', help='Phone number')
    parser.add_argument('--relationship', help='Relationship (for emergency contacts)')
    parser.add_argument('--dob', help='Date of birth (for personal info)')
    parser.add_argument('--blood-type', help='Blood type')
    
    args = parser.parse_args()
    
    data = load_history()
    record_id = str(uuid.uuid4())[:8]
    
    if args.type == 'personal-info':
        if args.name:
            data['personal_info']['full_name'] = args.name
        if args.dob:
            data['personal_info']['date_of_birth'] = args.dob
        if args.blood_type:
            data['personal_info']['blood_type'] = args.blood_type
        print(f"✓ Updated personal info")
    
    elif args.type == 'condition':
        if not args.name:
            print("Error: Condition requires --name")
            return
        record = {
            "id": record_id,
            "condition": args.name,
            "diagnosed_date": args.date or datetime.now().strftime('%Y-%m-%d'),
            "status": "active",
            "notes": args.notes
        }
        data['conditions'].append(record)
        print(f"✓ Added condition: {args.name}")
    
    elif args.type == 'surgery':
        if not args.name:
            print("Error: Surgery requires --name")
            return
        record = {
            "id": record_id,
            "procedure": args.name,
            "date": args.date,
            "notes": args.notes
        }
        data['surgeries'].append(record)
        print(f"✓ Added surgery: {args.name}")
    
    elif args.type == 'allergy':
        if not args.allergen:
            print("Error: Allergy requires --allergen")
            return
        record = {
            "allergen": args.allergen,
            "reaction": args.reaction or 'Unknown',
            "severity": args.severity or 'moderate'
        }
        if 'allergies' not in data:
            data['allergies'] = {"medications": [], "foods": [], "environmental": []}
        if args.category not in data['allergies']:
            data['allergies'][args.category] = []
        data['allergies'][args.category].append(record)
        print(f"✓ Added allergy: {args.allergen} ({args.category})")
        print("⚠️  Remember to update your emergency card!")
    
    elif args.type == 'immunization':
        if not args.vaccine:
            print("Error: Immunization requires --vaccine")
            return
        record = {
            "vaccine": args.vaccine,
            "date": args.date or datetime.now().strftime('%Y-%m-%d'),
            "next_due": args.next_due
        }
        data['immunizations'].append(record)
        print(f"✓ Added immunization: {args.vaccine}")
    
    elif args.type == 'physician':
        if not args.name:
            print("Error: Physician requires --name")
            return
        record = {
            "name": args.name,
            "specialty": args.specialty or 'Primary Care',
            "phone": args.phone or ''
        }
        data['physicians'].append(record)
        print(f"✓ Added physician: {args.name}")
    
    elif args.type == 'emergency-contact':
        if not args.name:
            print("Error: Emergency contact requires --name")
            return
        record = {
            "name": args.name,
            "relationship": args.relationship or '',
            "phone": args.phone or ''
        }
        data['emergency_contacts'].append(record)
        print(f"✓ Added emergency contact: {args.name}")
    
    save_history(data)
    print(f"\nStored in: {HISTORY_FILE}")

if __name__ == '__main__':
    main()
