#!/usr/bin/env python3
"""List upcoming immigration deadlines."""
import json
import os
import argparse
from datetime import datetime, timedelta

IMMIGRATION_DIR = os.path.expanduser("~/.openclaw/workspace/memory/immigration")
DEADLINES_FILE = os.path.join(IMMIGRATION_DIR, "deadlines.json")

def load_deadlines():
    if not os.path.exists(DEADLINES_FILE):
        return {"deadlines": []}
    with open(DEADLINES_FILE, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='List immigration deadlines')
    parser.add_argument('--days', type=int, default=90, help='Show deadlines within N days')
    parser.add_argument('--priority', help='Filter by priority (urgent,high,normal,low)')
    parser.add_argument('--type', help='Filter by type')
    parser.add_argument('--status', default='active', help='Filter by status')
    
    args = parser.parse_args()
    
    data = load_deadlines()
    deadlines = data.get('deadlines', [])
    
    # Filter active deadlines within timeframe
    cutoff = datetime.now() + timedelta(days=args.days)
    
    filtered = []
    for d in deadlines:
        deadline_date = datetime.strptime(d['date'], '%Y-%m-%d')
        if d['status'] == args.status and deadline_date <= cutoff:
            if args.priority and d['priority'] != args.priority:
                continue
            if args.type and d['type'] != args.type:
                continue
            filtered.append(d)
    
    # Sort by date
    filtered.sort(key=lambda x: x['date'])
    
    if not filtered:
        print(f"\nNo deadlines found within {args.days} days.")
        return
    
    print(f"\nUPCOMING DEADLINES (Next {args.days} days)")
    print("=" * 60)
    
    # Group by urgency
    urgent = [d for d in filtered if d['priority'] == 'urgent']
    high = [d for d in filtered if d['priority'] == 'high']
    normal = [d for d in filtered if d['priority'] == 'normal']
    low = [d for d in filtered if d['priority'] == 'low']
    
    if urgent:
        print("\n🚨 URGENT")
        print("-" * 40)
        for d in urgent:
            days = (datetime.strptime(d['date'], '%Y-%m-%d') - datetime.now()).days
            print(f"• {d['title']}")
            print(f"  Due: {d['date']} ({days} days)")
            if d['description']:
                print(f"  Note: {d['description']}")
    
    if high:
        print("\n⚠️  HIGH PRIORITY")
        print("-" * 40)
        for d in high:
            days = (datetime.strptime(d['date'], '%Y-%m-%d') - datetime.now()).days
            print(f"• {d['title']} - {d['date']} ({days} days)")
    
    if normal:
        print("\n📅 NORMAL")
        print("-" * 40)
        for d in normal:
            days = (datetime.strptime(d['date'], '%Y-%m-%d') - datetime.now()).days
            print(f"• {d['title']} - {d['date']} ({days} days)")
    
    if low:
        print("\nℹ️  LOW PRIORITY")
        print("-" * 40)
        for d in low:
            days = (datetime.strptime(d['date'], '%Y-%m-%d') - datetime.now()).days
            print(f"• {d['title']} - {d['date']} ({days} days)")
    
    print(f"\nTotal: {len(filtered)} deadline(s)")

if __name__ == '__main__':
    main()
