#!/usr/bin/env python3
"""Draft follow-up email after pitch/meeting."""
import json
import os
import argparse
from datetime import datetime

PITCH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/pitch")
MEETINGS_FILE = os.path.join(PITCH_DIR, "meetings.json")

def ensure_dir():
    os.makedirs(PITCH_DIR, exist_ok=True)

def load_meetings():
    if os.path.exists(MEETINGS_FILE):
        with open(MEETINGS_FILE, 'r') as f:
            return json.load(f)
    return {"meetings": []}

def save_meetings(data):
    ensure_dir()
    with open(MEETINGS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Draft follow-up email')
    parser.add_argument('--company', required=True, help='Company/person name')
    parser.add_argument('--meeting-type', required=True,
                        choices=['investor', 'customer', 'partner'],
                        help='Type of meeting')
    parser.add_argument('--key-point', help='Key topic discussed')
    parser.add_argument('--next-step', help='Agreed next step')
    parser.add_argument('--tone', default='professional',
                        choices=['professional', 'casual', 'enthusiastic'],
                        help='Email tone')
    
    args = parser.parse_args()
    
    print(f"\nFOLLOW-UP EMAIL DRAFT")
    print(f"To: {args.company}")
    print(f"Tone: {args.tone}")
    print("=" * 60)
    
    if args.meeting_type == 'investor':
        print(f"\nSubject: Thanks + [Specific Point from Meeting]")
        print(f"\nHi [Name],")
        print(f"\nThanks for taking the time to meet today.")
        
        if args.key_point:
            print(f"\nI appreciated your question about {args.key_point}.")
            print(f"I've attached our [relevant doc] that addresses this in detail.")
        
        print(f"\nAs discussed, {args.next_step or 'I\'ll follow up with our deck and financial model'}.")
        
        print(f"\nBest,")
        print(f"[Your name]")
    
    elif args.meeting_type == 'customer':
        print(f"\nSubject: Next steps from our conversation")
        print(f"\nHi [Name],")
        print(f"\nGreat speaking with you today about {args.key_point or 'your workflow challenges'}.")
        print(f"\nI'm attaching:")
        print(f"  • Product overview relevant to your use case")
        print(f"  • Case study from [similar company]")
        print(f"  • Pricing details we discussed")
        
        if args.next_step:
            print(f"\n{args.next_step}")
        else:
            print(f"\nCan we schedule a 30-minute demo next Tuesday or Wednesday?")
        
        print(f"\nBest,")
        print(f"[Your name]")
    
    elif args.meeting_type == 'partner':
        print(f"\nSubject: Excited about potential partnership")
        print(f"\nHi [Name],")
        print(f"\nThanks for the conversation about partnering.")
        print(f"\nI'm excited about the opportunity to [specific mutual benefit].")
        
        if args.next_step:
            print(f"\n{args.next_step}")
        
        print(f"\nBest,")
        print(f"[Your name]")
    
    print("\n" + "=" * 60)
    print("⚠️  REVIEW BEFORE SENDING:")
    print("  • Customize with specific details from conversation")
    print("  • Attach relevant documents")
    print("  • Proofread for errors")
    print("  • Ensure tone matches relationship")
    
    # Save meeting record
    meeting = {
        "company": args.company,
        "type": args.meeting_type,
        "date": datetime.now().isoformat(),
        "key_point": args.key_point,
        "next_step": args.next_step
    }
    
    data = load_meetings()
    data['meetings'].append(meeting)
    save_meetings(data)

if __name__ == '__main__':
    main()
