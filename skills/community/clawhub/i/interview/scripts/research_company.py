#!/usr/bin/env python3
"""Research company for interview."""
import json
import os
import uuid
import argparse
from datetime import datetime

INTERVIEW_DIR = os.path.expanduser("~/.openclaw/workspace/memory/interview")

def ensure_dir():
    os.makedirs(INTERVIEW_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Research company')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--role', required=True, help='Role you are interviewing for')
    
    args = parser.parse_args()
    
    print(f"\n🔍 COMPANY RESEARCH: {args.company}")
    print("=" * 60)
    print(f"Role: {args.role}")
    print()
    
    # Generate research framework
    print("RESEARCH FRAMEWORK:")
    print("-" * 40)
    print("\n1. COMPANY BASICS")
    print("   • What does the company do?")
    print("   • How do they make money?")
    print("   • Who are their customers?")
    print("   • What is their market position?")
    
    print("\n2. RECENT NEWS")
    print("   • Recent product launches")
    print("   • Funding rounds or acquisitions")
    print("   • Leadership changes")
    print("   • Strategic pivots or announcements")
    
    print("\n3. COMPETITIVE LANDSCAPE")
    print("   • Main competitors")
    print("   • Competitive advantages")
    print("   • Industry trends affecting them")
    
    print("\n4. ROLE-SPECIFIC INSIGHTS")
    print(f"   • What would success look like in {args.role}?")
    print("   • What challenges might this role face?")
    print("   • How does this role contribute to company goals?")
    
    print("\n5. QUESTIONS TO ASK")
    print("   • What are the biggest challenges for this team?")
    print("   • How does this role interact with other departments?")
    print("   • What does success look like in the first 90 days?")
    
    # Save research entry
    research = {
        "id": f"RES-{str(uuid.uuid4())[:6].upper()}",
        "company": args.company,
        "role": args.role,
        "researched_at": datetime.now().isoformat(),
        "status": "in_progress"
    }
    
    research_file = os.path.join(INTERVIEW_DIR, "research.json")
    data = {"research": []}
    if os.path.exists(research_file):
        with open(research_file, 'r') as f:
            data = json.load(f)
    
    data['research'].append(research)
    
    ensure_dir()
    with open(research_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Research entry saved: {research['id']}")
    print("\n💡 Next: Fill in each section with your research findings")

if __name__ == '__main__':
    main()
