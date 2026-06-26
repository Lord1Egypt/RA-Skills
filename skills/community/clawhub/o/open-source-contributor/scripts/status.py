#!/usr/bin/env python3
"""Check contribution status and enforce rules"""

import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/wahaj/.openclaw/workspace/contrib-scout")
LOG_FILE = WORKSPACE / "logs" / "contributions.jsonl"

def parse_log_file():
    """Parse contributions log (handles both JSON array and JSONL)"""
    contributions = []
    
    if not LOG_FILE.exists():
        return contributions
    
    with open(LOG_FILE) as f:
        content = f.read().strip()
        if not content:
            return contributions
        
        # Try JSON array first
        if content.startswith('['):
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    return [e for e in data if isinstance(e, dict)]
            except json.JSONDecodeError:
                pass
        
        # Try JSONL
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, dict):
                    contributions.append(entry)
            except json.JSONDecodeError:
                continue
    
    return contributions

def check_rules():
    """Check if rules are being followed"""
    today = datetime.now().strftime("%Y-%m-%d")
    contributions = parse_log_file()
    
    today_count = sum(1 for c in contributions if c.get("date") == today)
    pending_count = sum(1 for c in contributions if c.get("status") == "pending")
    
    print(f"📊 Contribution Status")
    print(f"=" * 40)
    print(f"Today: {today_count}/3")
    print(f"Pending PRs: {pending_count}")
    print(f"Total tracked: {len(contributions)}")
    print()
    
    if today_count < 3:
        print(f"⚠️  Need {3 - today_count} more contributions tonight")
        print("   • Must be NEW issues")
        print("   • No existing PRs")
        print("   • Proper scouting required")
    else:
        print("✅ Daily quota met")
    
    print()
    print("Recent contributions:")
    for c in contributions[-5:]:
        status_icon = "✅" if c.get("status") == "merged" else "⏳" if c.get("status") == "pending" else "❌"
        repo = c.get('repo', c.get('repository', 'unknown'))
        issue = c.get('issue', c.get('issue_number', '?'))
        print(f"  {status_icon} {repo} #{issue} - {c.get('status', 'unknown')}")

if __name__ == '__main__':
    check_rules()
