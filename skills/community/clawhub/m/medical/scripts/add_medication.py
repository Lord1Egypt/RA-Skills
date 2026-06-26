#!/usr/bin/env python3
"""Add a medication to the health records."""
import json
import os
import sys
import uuid
import argparse
from datetime import datetime

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
MEDS_FILE = os.path.join(HEALTH_DIR, "medications.json")

def ensure_dir():
    os.makedirs(HEALTH_DIR, exist_ok=True)

def load_meds():
    if os.path.exists(MEDS_FILE):
        with open(MEDS_FILE, 'r') as f:
            return json.load(f)
    return {"medications": []}

def save_meds(data):
    ensure_dir()
    with open(MEDS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def check_interaction(new_med, existing_meds):
    """Basic interaction checking - informational only."""
    warnings = []
    new_lower = new_med.lower()
    
    # Common interaction pairs (simplified)
    interactions = {
        "warfarin": ["aspirin", "ibuprofen", "naproxen"],
        "lisinopril": ["potassium supplements", "spironolactone"],
        "metformin": ["contrast dye"],
        "simvastatin": ["gemfibrozil", "clarithromycin"],
    }
    
    for med, interacts_with in interactions.items():
        if med in new_lower:
            for existing in existing_meds:
                existing_lower = existing['name'].lower()
                for interact in interacts_with:
                    if interact in existing_lower:
                        warnings.append(f"{new_med} may interact with {existing['name']}")
        
        # Check reverse
        for existing in existing_meds:
            existing_lower = existing['name'].lower()
            if med in existing_lower:
                for interact in interacts_with:
                    if interact in new_lower:
                        warnings.append(f"{existing['name']} may interact with {new_med}")
    
    return warnings

def main():
    parser = argparse.ArgumentParser(description='Add a medication')
    parser.add_argument('--name', required=True, help='Medication name')
    parser.add_argument('--dosage', required=True, help='Dosage (e.g., 10mg)')
    parser.add_argument('--frequency', required=True, help='Frequency (e.g., once daily)')
    parser.add_argument('--time', default='', help='Time of day (morning/evening/with meals)')
    parser.add_argument('--with-food', action='store_true', help='Take with food')
    parser.add_argument('--purpose', default='', help='What it treats')
    parser.add_argument('--doctor', default='', help='Prescribing doctor')
    parser.add_argument('--start-date', default=datetime.now().strftime('%Y-%m-%d'), 
                        help='Start date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    data = load_meds()
    
    # Check for interactions
    warnings = check_interaction(args.name, data['medications'])
    
    med = {
        "id": str(uuid.uuid4())[:8],
        "name": args.name,
        "dosage": args.dosage,
        "frequency": args.frequency,
        "time_of_day": args.time,
        "with_food": args.with_food,
        "purpose": args.purpose,
        "prescribing_doctor": args.doctor,
        "start_date": args.start_date,
        "end_date": None,
        "ongoing": True,
        "added_at": datetime.now().isoformat()
    }
    
    data['medications'].append(med)
    save_meds(data)
    
    print(f"✓ Added: {args.name} {args.dosage} - {args.frequency}")
    if warnings:
        print("\n⚠️  Interaction warnings (consult doctor/pharmacist):")
        for w in warnings:
            print(f"   • {w}")
    print(f"\nStored in: {MEDS_FILE}")

if __name__ == '__main__':
    main()
