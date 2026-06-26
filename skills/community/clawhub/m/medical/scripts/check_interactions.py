#!/usr/bin/env python3
"""Check for drug interactions."""
import json
import os
import argparse

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
MEDS_FILE = os.path.join(HEALTH_DIR, "medications.json")

# Simplified interaction database - for informational use only
INTERACTIONS = {
    "warfarin": {
        "interacts_with": ["aspirin", "ibuprofen", "naproxen", "amiodarone", "metronidazole"],
        "category": "Major",
        "effect": "Increased bleeding risk"
    },
    "lisinopril": {
        "interacts_with": ["potassium supplements", "spironolactone", "losartan"],
        "category": "Moderate",
        "effect": "Increased potassium levels (hyperkalemia)"
    },
    "metformin": {
        "interacts_with": ["contrast dye", "cimetidine", "furosemide"],
        "category": "Moderate",
        "effect": "Increased side effects or kidney concerns"
    },
    "atorvastatin": {
        "interacts_with": ["gemfibrozil", "clarithromycin", "itraconazole", "cyclosporine"],
        "category": "Major",
        "effect": "Increased muscle damage risk (rhabdomyolysis)"
    },
    "simvastatin": {
        "interacts_with": ["gemfibrozil", "clarithromycin", "amiodarone", "verapamil"],
        "category": "Major",
        "effect": "Increased muscle damage risk"
    },
    "digoxin": {
        "interacts_with": ["amiodarone", "verapamil", "quinidine"],
        "category": "Major",
        "effect": "Increased digoxin toxicity"
    }
}

def load_meds():
    if not os.path.exists(MEDS_FILE):
        return {"medications": []}
    with open(MEDS_FILE, 'r') as f:
        return json.load(f)

def check_interactions(med_name, existing_meds):
    """Check a medication against interaction database."""
    warnings = []
    med_lower = med_name.lower()
    
    # Check if new med is in interaction database
    for drug, info in INTERACTIONS.items():
        if drug in med_lower:
            for existing in existing_meds:
                existing_lower = existing['name'].lower()
                for interact in info['interacts_with']:
                    if interact in existing_lower:
                        warnings.append({
                            'drug1': med_name,
                            'drug2': existing['name'],
                            'category': info['category'],
                            'effect': info['effect']
                        })
        
        # Check reverse - existing med in database, new med in interacts_with
        for existing in existing_meds:
            existing_lower = existing['name'].lower()
            if drug in existing_lower:
                for interact in info['interacts_with']:
                    if interact in med_lower:
                        warnings.append({
                            'drug1': existing['name'],
                            'drug2': med_name,
                            'category': info['category'],
                            'effect': info['effect']
                        })
    
    return warnings

def main():
    parser = argparse.ArgumentParser(description='Check drug interactions')
    parser.add_argument('--new', help='New medication to check')
    parser.add_argument('--drug1', help='First drug to compare')
    parser.add_argument('--drug2', help='Second drug to compare')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("DRUG INTERACTION CHECK")
    print("⚠️  For informational purposes only - consult pharmacist/doctor")
    print("=" * 60)
    
    if args.drug1 and args.drug2:
        # Direct comparison
        warnings = check_interactions(args.drug1, [{'name': args.drug2}])
        if warnings:
            for w in warnings:
                print(f"\n🔴 {w['category'].upper()} INTERACTION")
                print(f"   {w['drug1']} + {w['drug2']}")
                print(f"   Potential effect: {w['effect']}")
        else:
            print(f"\n✓ No known major interactions between {args.drug1} and {args.drug2}")
            print("  (Limited database - always verify with pharmacist)")
    
    elif args.new:
        # Check against current medications
        data = load_meds()
        current_meds = [m for m in data.get('medications', []) if m.get('ongoing', True)]
        
        if not current_meds:
            print(f"\nNo current medications on file.")
            print(f"Would check interactions between {args.new} and your medication list.")
            return
        
        print(f"\nChecking {args.new} against {len(current_meds)} current medications...")
        
        warnings = check_interactions(args.new, current_meds)
        
        if warnings:
            print(f"\n⚠️  Found {len(warnings)} potential interaction(s):\n")
            for w in warnings:
                print(f"🔴 {w['category'].upper()}")
                print(f"   {w['drug1']} + {w['drug2']}")
                print(f"   Effect: {w['effect']}")
                print()
        else:
            print(f"\n✓ No major interactions detected with {args.new}")
            print("  (Limited database - always verify with pharmacist)")
        
        print("\nCurrent medications:")
        for m in current_meds:
            print(f"  • {m['name']} {m['dosage']}")
    
    else:
        print("\nUsage:")
        print("  Check new med: python check_interactions.py --new 'Medication Name'")
        print("  Compare two:   python check_interactions.py --drug1 'A' --drug2 'B'")
    
    print("\n" + "=" * 60)
    print("IMPORTANT: This check uses a limited database.")
    print("Always consult your doctor or pharmacist before starting,")
    print("stopping, or changing any medication.")
    print("=" * 60)

if __name__ == '__main__':
    main()
