#!/usr/bin/env python3
"""Generate elevator pitch."""
import json
import os
import argparse

PITCH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/pitch")
FOUNDATION_FILE = os.path.join(PITCH_DIR, "foundations.json")

def load_foundations():
    if not os.path.exists(FOUNDATION_FILE):
        return {"foundations": []}
    with open(FOUNDATION_FILE, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='Create elevator pitch')
    parser.add_argument('--foundation-id', required=True, help='Foundation ID')
    parser.add_argument('--audience', required=True,
                        choices=['investor', 'customer', 'partner', 'employee'],
                        help='Target audience')
    parser.add_argument('--length', type=int, default=60,
                        help='Length in seconds (30, 60, 120)')
    
    args = parser.parse_args()
    
    data = load_foundations()
    
    foundation = None
    for f in data.get('foundations', []):
        if f['id'] == args.foundation_id:
            foundation = f
            break
    
    if not foundation:
        print(f"Error: Foundation {args.foundation_id} not found")
        return
    
    company = foundation['company_name']
    problem = foundation['problem']['statement']
    solution = foundation['solution']['description']
    
    print(f"\nELEVATOR PITCH: {company}")
    print(f"Audience: {args.audience} | Length: {args.length} seconds")
    print("=" * 60)
    
    if args.length == 30:
        print(f"\n[HOOK]")
        print(f"{problem}")
        print(f"\n[SOLUTION]")
        print(f"{company} {solution}")
        print(f"\n[ASK]")
        if args.audience == 'investor':
            print("We're raising a seed round and looking for partners")
        elif args.audience == 'customer':
            print("I'd love to show you how it works")
    
    elif args.length == 60:
        print(f"\n[HOOK - 10 sec]")
        print(f"{problem}")
        print(f"\n[SOLUTION - 20 sec]")
        print(f"{company} {solution}")
        print(f"\n[TRACTION - 20 sec]")
        print("We've signed 12 customers and are growing 20% monthly")
        print(f"\n[ASK - 10 sec]")
        if args.audience == 'investor':
            print("We're raising $500K to hit $30K MRR. Are you interested?")
        elif args.audience == 'customer':
            print("Can I show you a 5-minute demo next week?")
    
    else:  # 120 seconds
        print(f"\n[HOOK - 15 sec]")
        print(f"{problem}")
        print(f"\n[SOLUTION - 30 sec]")
        print(f"{company} {solution}")
        print(f"\n[MARKET - 20 sec]")
        print("This is a $2B market growing 30% annually")
        print(f"\n[TRACTION - 30 sec]")
        print("12 customers, $15K MRR, growing 20% monthly, 58 NPS")
        print(f"\n[TEAM - 15 sec]")
        print("Ex-Stripe and Google engineers")
        print(f"\n[ASK - 10 sec]")
        if args.audience == 'investor':
            print("We're raising $500K. Can I send you our deck?")
    
    print("\n" + "=" * 60)
    print("💡 Tips:")
    print("  • Practice until it feels natural, not rehearsed")
    print("  • Adjust based on audience reaction")
    print("  • Always end with a clear ask")

if __name__ == '__main__':
    main()
