#!/usr/bin/env python3
"""Track and manage visa applications."""
import json
import os
import uuid
import argparse
from datetime import datetime

IMMIGRATION_DIR = os.path.expanduser("~/.openclaw/workspace/memory/immigration")
APPLICATIONS_FILE = os.path.join(IMMIGRATION_DIR, "applications.json")

def ensure_dir():
    os.makedirs(IMMIGRATION_DIR, exist_ok=True)

def load_applications():
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r') as f:
            return json.load(f)
    return {"applications": []}

def save_applications(data):
    ensure_dir()
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Track visa application')
    parser.add_argument('--action', choices=['add', 'update', 'view', 'list'],
                        default='list', help='Action to perform')
    parser.add_argument('--id', help='Application ID')
    parser.add_argument('--visa-type', help='Visa type')
    parser.add_argument('--country', help 'Destination country')
    parser.add_argument('--status', help='Application status')
    parser.add_argument('--notes', help='Update notes')
    
    args = parser.parse_args()
    
    data = load_applications()
    
    if args.action == 'add':
        if not args.visa_type or not args.country:
            print("Error: --visa-type and --country required for add")
            return
        
        app_id = f"APP-{str(uuid.uuid4())[:6].upper()}"
        application = {
            "id": app_id,
            "visa_type": args.visa_type,
            "country": args.country,
            "status": "started",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "notes": args.notes or "",
            "milestones": []
        }
        data['applications'].append(application)
        save_applications(data)
        print(f"\n✓ Application added: {app_id}")
        print(f"  Visa: {args.visa_type}")
        print(f"  Country: {args.country}")
    
    elif args.action == 'update':
        if not args.id:
            print("Error: --id required for update")
            return
        
        for app in data['applications']:
            if app['id'] == args.id:
                if args.status:
                    app['status'] = args.status
                    app['milestones'].append({
                        "status": args.status,
                        "date": datetime.now().isoformat()
                    })
                if args.notes:
                    app['notes'] += f"\n{datetime.now().strftime('%Y-%m-%d')}: {args.notes}"
                app['updated_at'] = datetime.now().isoformat()
                save_applications(data)
                print(f"\n✓ Updated application: {args.id}")
                print(f"  Status: {app['status']}")
                return
        print(f"Error: Application {args.id} not found")
    
    elif args.action == 'view':
        if not args.id:
            print("Error: --id required for view")
            return
        
        for app in data['applications']:
            if app['id'] == args.id:
                print(f"\nAPPLICATION: {app['id']}")
                print("=" * 50)
                print(f"Visa Type: {app['visa_type']}")
                print(f"Country: {app['country']}")
                print(f"Status: {app['status']}")
                print(f"Created: {app['created_at'][:10]}")
                print(f"Last Updated: {app['updated_at'][:10]}")
                if app['notes']:
                    print(f"\nNotes:\n{app['notes']}")
                if app['milestones']:
                    print(f"\nMilestones:")
                    for m in app['milestones']:
                        print(f"  • {m['date'][:10]}: {m['status']}")
                return
        print(f"Error: Application {args.id} not found")
    
    else:  # list
        if not data['applications']:
            print("\nNo applications tracked.")
            return
        
        print(f"\nVISA APPLICATIONS ({len(data['applications'])})")
        print("=" * 60)
        
        for app in data['applications']:
            print(f"\n{app['id']}: {app['visa_type']} ({app['country']})")
            print(f"  Status: {app['status']}")
            print(f"  Started: {app['created_at'][:10]}")

if __name__ == '__main__':
    main()
