#!/usr/bin/env python3
"""
Flight price tracker with alerts.
Stores price history and notifies on price drops.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add venv to path
script_dir = os.path.dirname(os.path.abspath(__file__))
venv_site = os.path.join(script_dir, '..', '.venv', 'lib')
if os.path.exists(venv_site):
    for d in os.listdir(venv_site):
        if d.startswith('python'):
            sys.path.insert(0, os.path.join(venv_site, d, 'site-packages'))
            break

# Import search functionality
sys.path.insert(0, script_dir)
from search import search_flights, parse_date, extract_flights_with_details, load_preferences

# Default tracking file
TRACKING_FILE = os.path.expanduser("~/clawd/memory/flight-tracking.json")
PRICE_HISTORY_FILE = os.path.expanduser("~/clawd/memory/flight-prices.jsonl")


def ensure_tracking_dir():
    """Ensure memory directory exists."""
    Path(TRACKING_FILE).parent.mkdir(parents=True, exist_ok=True)


def load_tracked_flights() -> dict:
    """Load tracked flights from JSON file."""
    if os.path.exists(TRACKING_FILE):
        try:
            with open(TRACKING_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"flights": [], "last_check": None}


def save_tracked_flights(data: dict):
    """Save tracked flights to JSON file."""
    ensure_tracking_dir()
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def append_price_history(entry: dict):
    """Append a price check to history."""
    ensure_tracking_dir()
    with open(PRICE_HISTORY_FILE, 'a') as f:
        f.write(json.dumps(entry) + "\n")


def get_price_history(flight_key: str, limit: int = 30) -> list:
    """Get price history for a specific flight."""
    history = []
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('key') == flight_key:
                        history.append(entry)
                except:
                    continue
    return history[-limit:]


def generate_flight_key(from_apt: str, to_apt: str, date: str, ret_date: str = None) -> str:
    """Generate unique key for a flight route."""
    key = f"{from_apt}-{to_apt}-{date}"
    if ret_date:
        key += f"-{ret_date}"
    return key


def check_flight_price(flight_config: dict) -> dict:
    """Check current price for a tracked flight."""
    prefs = load_preferences()
    
    try:
        result = search_flights(
            flight_config['from'],
            flight_config['to'],
            flight_config['date'],
            flight_config.get('return_date'),
            flight_config.get('seat', 'economy'),
            flight_config.get('adults', 1),
            flight_config.get('children', 0)
        )
        
        flights = extract_flights_with_details(result.flights, prefs)
        
        if not flights:
            return {"error": "No flights found"}
        
        # Get lowest price
        lowest = min(flights, key=lambda x: x['price_numeric'])
        
        return {
            "lowest_price": lowest['price'],
            "lowest_price_numeric": lowest['price_numeric'],
            "airline": lowest['airline'],
            "price_trend": result.current_price,
            "options_count": len(flights),
            "checked_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": str(e)}


def add_tracking(args) -> str:
    """Add a new flight to track."""
    data = load_tracked_flights()
    
    date = parse_date(args.date)
    ret_date = parse_date(args.return_date) if args.return_date else None
    key = generate_flight_key(args.from_airport.upper(), args.to_airport.upper(), date, ret_date)
    
    # Check if already tracking
    for f in data['flights']:
        if f['key'] == key:
            return f"⚠️  Already tracking {key}"
    
    flight_config = {
        "key": key,
        "from": args.from_airport.upper(),
        "to": args.to_airport.upper(),
        "date": date,
        "return_date": ret_date,
        "seat": args.seat,
        "adults": args.adults,
        "children": args.children,
        "alert_below": args.alert_below,
        "added_at": datetime.now().isoformat(),
        "last_price": None,
        "lowest_seen": None,
    }
    
    # Do initial price check
    result = check_flight_price(flight_config)
    if 'lowest_price_numeric' in result:
        flight_config['last_price'] = result['lowest_price_numeric']
        flight_config['lowest_seen'] = result['lowest_price_numeric']
        flight_config['last_check'] = result['checked_at']
        
        # Log to history
        append_price_history({
            "key": key,
            "price": result['lowest_price_numeric'],
            "price_str": result['lowest_price'],
            "trend": result.get('price_trend'),
            "timestamp": result['checked_at']
        })
    
    data['flights'].append(flight_config)
    save_tracked_flights(data)
    
    price_str = result.get('lowest_price', 'N/A')
    alert_str = f" (alert if < ${args.alert_below})" if args.alert_below else ""
    return f"✅ Now tracking {key}\n   Current lowest: {price_str}{alert_str}"


def list_tracking(args) -> str:
    """List all tracked flights."""
    data = load_tracked_flights()
    
    if not data['flights']:
        return "📭 No flights being tracked.\nUse: track.py add YYC LAX 2026-04-15"
    
    lines = ["📋 **Tracked Flights**\n"]
    
    for f in data['flights']:
        trip_type = "↔" if f.get('return_date') else "→"
        route = f"{f['from']} {trip_type} {f['to']}"
        dates = f['date'] + (f" - {f['return_date']}" if f.get('return_date') else "")
        
        price_info = ""
        if f.get('last_price'):
            price_info = f"${f['last_price']}"
            if f.get('lowest_seen') and f['lowest_seen'] < f['last_price']:
                price_info += f" (lowest: ${f['lowest_seen']})"
        
        alert_info = ""
        if f.get('alert_below'):
            alert_info = f" 🔔<${f['alert_below']}"
        
        lines.append(f"• {route} | {dates} | {price_info}{alert_info}")
    
    if data.get('last_check'):
        lines.append(f"\nLast check: {data['last_check']}")
    
    return "\n".join(lines)


def check_all(args) -> str:
    """Check prices for all tracked flights."""
    data = load_tracked_flights()
    
    if not data['flights']:
        return "📭 No flights being tracked."
    
    alerts = []
    updates = []
    
    for f in data['flights']:
        # Skip expired flights
        flight_date = datetime.strptime(f['date'], "%Y-%m-%d")
        if flight_date.date() < datetime.now().date():
            continue
        
        result = check_flight_price(f)
        
        if 'error' in result:
            updates.append(f"⚠️  {f['key']}: {result['error']}")
            continue
        
        current_price = result['lowest_price_numeric']
        price_str = result['lowest_price']
        prev_price = f.get('last_price')
        
        # Update tracking
        f['last_price'] = current_price
        f['last_check'] = result['checked_at']
        
        if f.get('lowest_seen') is None or current_price < f['lowest_seen']:
            f['lowest_seen'] = current_price
        
        # Log to history
        append_price_history({
            "key": f['key'],
            "price": current_price,
            "price_str": price_str,
            "trend": result.get('price_trend'),
            "timestamp": result['checked_at']
        })
        
        # Check for alerts
        if f.get('alert_below') and current_price < f['alert_below']:
            alerts.append(f"🚨 **PRICE DROP** {f['key']}: {price_str} (target: <${f['alert_below']})")
        elif prev_price and current_price < prev_price:
            diff = prev_price - current_price
            pct = (diff / prev_price) * 100
            updates.append(f"📉 {f['key']}: {price_str} (down ${diff}, {pct:.1f}%)")
        elif prev_price and current_price > prev_price:
            diff = current_price - prev_price
            updates.append(f"📈 {f['key']}: {price_str} (up ${diff})")
        else:
            updates.append(f"➡️  {f['key']}: {price_str}")
    
    data['last_check'] = datetime.now().isoformat()
    save_tracked_flights(data)
    
    output = []
    if alerts:
        output.extend(alerts)
        output.append("")
    output.extend(updates)
    
    return "\n".join(output) if output else "No updates."


def remove_tracking(args) -> str:
    """Remove a flight from tracking."""
    data = load_tracked_flights()
    
    key = args.key.upper()
    initial_count = len(data['flights'])
    data['flights'] = [f for f in data['flights'] if f['key'] != key]
    
    if len(data['flights']) < initial_count:
        save_tracked_flights(data)
        return f"✅ Removed {key} from tracking"
    else:
        return f"⚠️  {key} not found in tracked flights"


def show_history(args) -> str:
    """Show price history for a flight."""
    history = get_price_history(args.key.upper(), args.limit)
    
    if not history:
        return f"No price history for {args.key}"
    
    lines = [f"📊 Price history for {args.key} (last {len(history)} checks)\n"]
    
    for entry in history:
        ts = entry.get('timestamp', '?')[:16]
        price = entry.get('price_str', f"${entry.get('price', '?')}")
        trend = entry.get('trend', '')
        lines.append(f"  {ts} | {price} | {trend}")
    
    # Simple trend analysis
    prices = [e['price'] for e in history if 'price' in e]
    if len(prices) >= 2:
        first = prices[0]
        last = prices[-1]
        lowest = min(prices)
        highest = max(prices)
        
        lines.append(f"\n📈 Range: ${lowest} - ${highest}")
        if last < first:
            lines.append(f"📉 Trending down ({((first-last)/first)*100:.1f}% since first check)")
        elif last > first:
            lines.append(f"📈 Trending up ({((last-first)/first)*100:.1f}% since first check)")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Track flight prices and get alerts")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a flight to track")
    add_parser.add_argument("from_airport", help="Departure airport")
    add_parser.add_argument("to_airport", help="Arrival airport")
    add_parser.add_argument("date", help="Departure date")
    add_parser.add_argument("--return", "-r", dest="return_date", help="Return date")
    add_parser.add_argument("--alert-below", "-a", type=int, help="Alert when price drops below this")
    add_parser.add_argument("--seat", "-s", default="economy", help="Seat class")
    add_parser.add_argument("--adults", type=int, default=1)
    add_parser.add_argument("--children", type=int, default=0)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List tracked flights")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check prices for all tracked flights")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a flight from tracking")
    remove_parser.add_argument("key", help="Flight key (e.g., YYC-LAX-2026-04-15)")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Show price history")
    history_parser.add_argument("key", help="Flight key")
    history_parser.add_argument("--limit", "-l", type=int, default=30, help="Number of entries")
    
    args = parser.parse_args()
    
    if args.command == "add":
        print(add_tracking(args))
    elif args.command == "list":
        print(list_tracking(args))
    elif args.command == "check":
        print(check_all(args))
    elif args.command == "remove":
        print(remove_tracking(args))
    elif args.command == "history":
        print(show_history(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
