#!/usr/bin/env python3
"""Generate emergency health card."""
import json
import os
import argparse
from datetime import datetime

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")

def load_json(filename):
    filepath = os.path.join(HEALTH_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def get_emergency_data():
    """Collect all emergency-relevant data."""
    history = load_json("history.json")
    meds = load_json("medications.json")
    
    data = {
        "name": history.get('personal_info', {}).get('full_name', ''),
        "dob": history.get('personal_info', {}).get('date_of_birth', ''),
        "blood_type": history.get('personal_info', {}).get('blood_type', 'Unknown'),
        "organ_donor": history.get('personal_info', {}).get('organ_donor', False),
        "allergies": history.get('allergies', {}),
        "conditions": [c.get('condition') for c in history.get('conditions', [])],
        "medications": [],
        "emergency_contacts": history.get('emergency_contacts', []),
        "primary_physician": history.get('physicians', [{}])[0] if history.get('physicians') else {}
    }
    
    # Get current medications
    for med in meds.get('medications', []):
        if med.get('ongoing', True):
            data['medications'].append({
                'name': med['name'],
                'dose': f"{med['dosage']} {med['frequency']}"
            })
    
    return data

def generate_phone_format(data):
    """Generate phone lock screen optimized format."""
    donor = "Y" if data['organ_donor'] else "N"
    
    output = []
    output.append("╔" + "═" * 46 + "╗")
    output.append("║" + " ⚠️  EMERGENCY HEALTH INFO  ⚠️ ".center(46) + "║")
    output.append("╠" + "═" * 46 + "╣")
    
    name_line = f" {data['name'][:25]} • DOB: {data['dob']}".ljust(46) + "║"
    output.append("║" + name_line)
    output.append(f"║  Blood Type: {data['blood_type']} • Organ Donor: {donor}".ljust(47) + "║")
    
    # Allergies
    allergies = data['allergies'].get('medications', [])
    if allergies:
        output.append("╠" + "═" * 46 + "╣")
        output.append("║" + " 🚨 ALLERGIES:".ljust(47) + "║")
        for allergy in allergies[:3]:  # Limit to 3
            reaction = allergy.get('reaction', '')[:15]
            line = f"   • {allergy['allergen'][:20]} = {reaction}".ljust(46) + "║"
            output.append("║" + line)
    
    # Conditions
    if data['conditions']:
        output.append("╠" + "═" * 46 + "╣")
        conds = ", ".join(data['conditions'][:4])
        output.append("║" + f" CONDITIONS: {conds[:40]}".ljust(47) + "║")
    
    # Medications
    if data['medications']:
        output.append("╠" + "═" * 46 + "╣")
        output.append("║" + " MEDICATIONS:".ljust(47) + "║")
        for med in data['medications'][:5]:
            line = f"   • {med['name'][:15]} {med['dose'][:20]}".ljust(46) + "║"
            output.append("║" + line)
    
    # Emergency contact
    if data['emergency_contacts']:
        output.append("╠" + "═" * 46 + "╣")
        contact = data['emergency_contacts'][0]
        line = f" ICE: {contact.get('name', '')} {contact.get('phone', '')}".ljust(46) + "║"
        output.append("║" + line)
    
    if data['primary_physician']:
        doc = data['primary_physician']
        line = f" Dr: {doc.get('name', '')[:15]} {doc.get('phone', '')}".ljust(46) + "║"
        output.append("║" + line)
    
    output.append("╚" + "═" * 46 + "╝")
    
    return "\n".join(output)

def generate_wallet_format(data):
    """Generate wallet card format."""
    lines = []
    lines.append("=" * 48)
    lines.append("EMERGENCY HEALTH INFORMATION")
    lines.append("-" * 48)
    lines.append(f"{data['name'][:30]} • DOB: {data['dob']}")
    lines.append(f"Blood Type: {data['blood_type']} • Organ Donor: {'Yes' if data['organ_donor'] else 'No'}")
    lines.append("-" * 48)
    
    allergies = data['allergies'].get('medications', [])
    if allergies:
        lines.append("ALLERGIES:")
        for a in allergies[:3]:
            lines.append(f"  • {a['allergen']}: {a.get('reaction', 'Unknown')}")
    
    if data['conditions']:
        lines.append("CONDITIONS: " + ", ".join(data['conditions'][:5]))
    
    if data['medications']:
        lines.append("MEDICATIONS:")
        for m in data['medications'][:4]:
            lines.append(f"  • {m['name']} {m['dose']}")
    
    if data['emergency_contacts']:
        c = data['emergency_contacts'][0]
        lines.append(f"EMERGENCY: {c.get('name', '')} {c.get('phone', '')}")
    
    lines.append("=" * 48)
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Generate emergency health card')
    parser.add_argument('--format', choices=['phone', 'wallet', 'json'], 
                        default='phone', help='Output format')
    parser.add_argument('--output', help='Save to file')
    
    args = parser.parse_args()
    
    data = get_emergency_data()
    
    if not data['name']:
        print("⚠️  No personal info found.")
        print("Add your details to history.json first:")
        print('  scripts/add_history_record.py --type personal-info ...')
        return
    
    if args.format == 'phone':
        output = generate_phone_format(data)
    elif args.format == 'wallet':
        output = generate_wallet_format(data)
    else:
        output = json.dumps(data, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✓ Emergency card saved to: {args.output}")
    else:
        print(output)
    
    print("\n💡 Tips:")
    print("  • Screenshot the phone format for your lock screen")
    print("  • Print the wallet format to keep in your wallet")
    print("  • Update whenever medications or allergies change")

if __name__ == '__main__':
    main()
