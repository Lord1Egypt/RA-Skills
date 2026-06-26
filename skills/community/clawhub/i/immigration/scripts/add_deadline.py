#!/usr/bin/env python3
"""Add and track immigration deadlines."""
import json
import os
import uuid
import argparse
from datetime import datetime, timedelta

IMMIGRATION_DIR = os.path.expanduser("~/.openclaw/workspace/memory/immigration")
DEADLINES_FILE = os.path.join(IMMIGRATION_DIR, "deadlines.json")

def ensure_dir():
    os.makedirs(IMMIGRATION_DIR, exist_ok=True)

def load_deadlines():
    if os.path.exists(DEADLINES_FILE):
        with open(DEADLINES_FILE, 'r') as f:
            return json.load(f)
    return {"deadlines": []}

def save_deadlines(data):
    ensure_dir()
    with open(DEADLINES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_alert_dates(deadline_date, priority):
    """Calculate alert dates based on priority."""
    deadline = datetime.strptime(deadline_date, '%Y-%m-%d')
    
    alerts = {
        'urgent': [7, 1],
        'high': [30, 7],
        'normal': [60, 30],
        'low': [90, 60]
    }
    
    alert_dates = []
    for days in alerts.get(priority, ['normal']):
        alert_date = deadline - timedelta(days=days)
        alert_dates.append(alert_date.strftime('%Y-%m-%d'))
    
    return alert_dates

def main():
    parser = argparse.ArgumentParser(description='Add immigration deadline')
    parser.add_argument('--type', required=True,
                        choices=['document-expiry', 'submission-deadline', 'interview',
                                'biometrics', 'response-deadline', 'payment-due', 'other'],
                        help='Type of deadline')
    parser.add_argument('--date', required=True, help='Deadline date (YYYY-MM-DD)')
    parser.add_argument('--title', required=True, help='Deadline title')
    parser.add_argument('--description', default='', help='Additional details')
    parser.add_argument('--priority', choices=['urgent', 'high', 'normal', 'low'],
                        default='normal', help='Priority level')
    parser.add_argument('--application-id', default='', help='Link to application')
    
    args = parser.parse_args()
    
    # Validate date
    try:
        deadline_date = datetime.strptime(args.date, '%Y-%m-%d')
        if deadline_date < datetime.now():
            print(f"⚠️  Warning: Deadline is in the past ({args.date})")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format")
        return
    
    deadline_id = str(uuid.uuid4())[:8]
    alert_dates = calculate_alert_dates(args.date, args.priority)
    
    deadline = {
        "id": deadline_id,
        "type": args.type,
        "title": args.title,
        "description": args.description,
        "date": args.date,
        "priority": args.priority,
        "alert_dates": alert_dates,
        "status": "active",
        "application_id": args.application_id,
        "created_at": datetime.now().isoformat()
    }
    
    data = load_deadlines()
    data["deadlines"].append(deadline)
    save_deadlines(data)
    
    days_until = (deadline_date - datetime.now()).days
    
    print(f"\n✓ Deadline added: {args.title}")
    print(f"  Date: {args.date}")
    print(f"  Days until: {days_until}")
    print(f"  Priority: {args.priority.upper()}")
    print(f"  Alerts set for: {', '.join(alert_dates)}")
    print(f"\nSaved to: {DEADLINES_FILE}")

if __name__ == '__main__':
    main()
