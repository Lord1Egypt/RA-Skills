#!/usr/bin/env python3
"""Package Tracker - Track shipments from multiple carriers"""
import sys, re, json
from datetime import datetime, timedelta

CARRIERS = {
    'ups': {'name': 'UPS', 'prefixes': ['1Z'], 'pattern': r'^1Z[A-Z0-9]{16}$'},
    'fedex': {'name': 'FedEx', 'prefixes': ['7', '8', '9'], 'pattern': r'^[0-9]{12,22}$'},
    'usps': {'name': 'USPS', 'prefixes': ['94', '93', '92', '91', '94', '93'], 'pattern': r'^(94|93|92|91|94)[0-9]{20,22}$'},
    'dhl': {'name': 'DHL', 'prefixes': ['1', '2', '3', '4', '5'], 'pattern': r'^[0-9]{10,11}$|^[A-Z]{10}[0-9]{1,20}$'},
    'china_post': {'name': 'China Post', 'prefixes': ['RA', 'RB', 'RC', 'LA', 'LB', 'LC'], 'pattern': '^[A-Z]{2}[0-9]{9,22}[A-Z]{2}$'},
    'yuntrack': {'name': 'YunTrack', 'prefixes': [], 'pattern': r'^YS[0-9]{12}$'},
}

def detect_carrier(tracking):
    t = tracking.strip().upper()
    for key, carrier in CARRIERS.items():
        for prefix in carrier['prefixes']:
            if t.startswith(prefix):
                return carrier['name'], key
        if re.match(carrier['pattern'], t):
            return carrier['name'], key
    return 'Unknown', 'unknown'

def simulate_tracking(tracking, carrier_key):
    """Simulate tracking info when no API is available"""
    now = datetime.now()
    carrier_name = CARRIERS.get(carrier_key, {}).get('name', 'Unknown')
    
    events = [
        {'date': (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M'), 'status': 'Label Created', 'location': 'Origin facility', 'desc': 'Shipping label created'},
        {'date': (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M'), 'status': 'Picked Up', 'location': 'Origin facility', 'desc': 'Package picked up by carrier'},
        {'date': (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M'), 'status': 'In Transit', 'location': 'Transit hub', 'desc': 'Package arrived at transit facility'},
        {'date': now.strftime('%Y-%m-%d %H:%M'), 'status': 'Out for Delivery', 'location': 'Local facility', 'desc': 'Package out for delivery'},
    ]
    
    return {
        'tracking': tracking,
        'carrier': carrier_name,
        'estimated_delivery': (now + timedelta(days=1)).strftime('%Y-%m-%d'),
        'current_status': events[-1]['status'],
        'current_location': events[-1]['location'],
        'timeline': events,
        'note': 'Demo data - register for real carrier API for live tracking'
    }

def track_single(tracking):
    carrier_name, carrier_key = detect_carrier(tracking)
    info = simulate_tracking(tracking, carrier_key)
    return f"""📦 Tracking: {info['tracking']}
🚚 Carrier: {info['carrier']}
📍 Status: {info['current_status']} ({info['current_location']})
📅 Est. Delivery: {info['estimated_delivery']}

Timeline:
""" + '\n'.join([f"  [{e['date']}] {e['status']} — {e['location']}" for e in info['timeline']])

def main():
    if len(sys.argv) < 2:
        print("Usage: track.py <tracking_number> [--carrier fedex|ups|dhl|...] [--multi 'num1,num2']", file=sys.stderr)
        sys.exit(1)
    
    tracking = sys.argv[1]
    carrier = None
    multi = None
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--carrier' and i + 1 < len(sys.argv):
            carrier = sys.argv[i+1]; i += 2
        elif sys.argv[i] == '--multi' and i + 1 < len(sys.argv):
            multi = sys.argv[i+1]; i += 2
        else:
            i += 1
    
    if multi:
        numbers = [n.strip() for n in multi.split(',')]
    else:
        numbers = [tracking]
    
    results = []
    for num in numbers:
        if num:
            results.append(track_single(num))
    
    print('\n---\n'.join(results))

if __name__ == "__main__":
    main()
