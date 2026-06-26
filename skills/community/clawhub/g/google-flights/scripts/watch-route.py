#!/usr/bin/env python3
"""
Route price watcher for regular travel patterns.
Monitors prices between home bases and alerts on good deals.
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

sys.path.insert(0, script_dir)
from search import search_flights, parse_date, extract_flights_with_details, load_preferences

# State file - customize path as needed
STATE_FILE = os.path.expanduser("~/clawd/memory/route-watch-state.json")


def ensure_dir():
    Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    """Load route watch state."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {
        "routes": [],
        "current_location": None,
        "last_check": None,
        "price_history": []
    }


def save_state(state: dict):
    ensure_dir()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def check_route_prices(from_apt: str, to_apt: str, days_out: int = 28) -> list:
    """Check flight prices for upcoming dates on a route."""
    prefs = load_preferences()
    results = []
    
    # Check weekly intervals
    check_days = [7, 14, 21, 28]
    
    for days in check_days:
        if days > days_out:
            break
        
        target_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        try:
            result = search_flights(from_apt, to_apt, target_date, seat='economy')
            flights = extract_flights_with_details(result.flights, prefs)
            
            if flights:
                nonstops = [f for f in flights if 'nonstop' in str(f.get('stops', '')).lower() or f.get('stops') == 0]
                best_overall = min(flights, key=lambda x: x['price_numeric'])
                best_nonstop = min(nonstops, key=lambda x: x['price_numeric']) if nonstops else None
                
                results.append({
                    'date': target_date,
                    'days_out': days,
                    'best_price': best_overall['price'],
                    'best_price_numeric': best_overall['price_numeric'],
                    'best_airline': best_overall['airline'],
                    'best_nonstop_price': best_nonstop['price'] if best_nonstop else None,
                    'best_nonstop_numeric': best_nonstop['price_numeric'] if best_nonstop else None,
                    'trend': result.current_price,
                    'options': len(flights)
                })
        except Exception as e:
            pass
    
    return results


def add_route(args) -> str:
    """Add a route to watch."""
    state = load_state()
    
    from_apt = args.from_airport.upper()
    to_apt = args.to_airport.upper()
    route_key = f"{from_apt}-{to_apt}"
    
    # Check if already watching
    for r in state['routes']:
        if r['key'] == route_key:
            return f"⚠️  Already watching {route_key}"
    
    route = {
        "key": route_key,
        "from": from_apt,
        "to": to_apt,
        "alert_below": args.alert_below or 400,
        "added_at": datetime.now().isoformat(),
        "last_price": None
    }
    
    state['routes'].append(route)
    save_state(state)
    
    return f"✅ Now watching {route_key} (alert if < ${route['alert_below']})"


def list_routes(args) -> str:
    """List watched routes."""
    state = load_state()
    
    if not state['routes']:
        return "📭 No routes being watched.\nUse: watch-route.py add YYC LAX --alert-below 400"
    
    lines = ["📋 **Watched Routes**\n"]
    
    for r in state['routes']:
        route = f"{r['from']} → {r['to']}"
        price_info = f"Last: ${r['last_price']}" if r.get('last_price') else "Not checked"
        alert_info = f" 🔔<${r['alert_below']}" if r.get('alert_below') else ""
        lines.append(f"• {route} | {price_info}{alert_info}")
    
    if state.get('last_check'):
        lines.append(f"\nLast check: {state['last_check'][:16]}")
    
    return "\n".join(lines)


def watch(args) -> str:
    """Check prices for all watched routes."""
    state = load_state()
    
    if not state['routes']:
        return "📭 No routes to watch. Add one first:\nwatch-route.py add YYC LAX --alert-below 400"
    
    alerts = []
    updates = []
    
    for route in state['routes']:
        from_apt = route['from']
        to_apt = route['to']
        threshold = route.get('alert_below', 400)
        
        results = check_route_prices(from_apt, to_apt, days_out=args.days)
        
        if not results:
            updates.append(f"⚠️  {route['key']}: Couldn't fetch prices")
            continue
        
        # Find best price across all dates
        best = min(results, key=lambda x: x['best_price_numeric'])
        price = best['best_price_numeric']
        price_str = best['best_price']
        best_date = datetime.strptime(best['date'], '%Y-%m-%d').strftime('%b %d')
        
        prev_price = route.get('last_price')
        route['last_price'] = price
        route['last_check'] = datetime.now().isoformat()
        
        # Check for alerts
        if price < threshold:
            alerts.append(f"🔥 **{route['key']}** {best_date}: {price_str} (target: <${threshold})")
        elif prev_price and price < prev_price:
            diff = prev_price - price
            updates.append(f"📉 {route['key']}: {price_str} on {best_date} (down ${diff})")
        elif prev_price and price > prev_price:
            diff = price - prev_price
            updates.append(f"📈 {route['key']}: {price_str} on {best_date} (up ${diff})")
        else:
            updates.append(f"➡️  {route['key']}: {price_str} on {best_date}")
    
    state['last_check'] = datetime.now().isoformat()
    save_state(state)
    
    output = []
    if alerts:
        output.extend(alerts)
        output.append("")
    output.extend(updates)
    
    return "\n".join(output) if output else "No updates."


def remove_route(args) -> str:
    """Remove a route from watching."""
    state = load_state()
    
    key = args.key.upper()
    initial_count = len(state['routes'])
    state['routes'] = [r for r in state['routes'] if r['key'] != key]
    
    if len(state['routes']) < initial_count:
        save_state(state)
        return f"✅ Removed {key} from watch list"
    else:
        return f"⚠️  {key} not found"


def main():
    parser = argparse.ArgumentParser(description="Watch flight prices on regular routes")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add route
    add_parser = subparsers.add_parser("add", help="Add a route to watch")
    add_parser.add_argument("from_airport", help="Departure airport")
    add_parser.add_argument("to_airport", help="Arrival airport")
    add_parser.add_argument("--alert-below", "-a", type=int, default=400, help="Alert when price drops below")
    
    # List routes
    subparsers.add_parser("list", help="List watched routes")
    
    # Watch (check prices)
    watch_parser = subparsers.add_parser("watch", help="Check prices for all routes")
    watch_parser.add_argument("--days", "-d", type=int, default=28, help="Days to look ahead")
    
    # Remove route
    remove_parser = subparsers.add_parser("remove", help="Remove a route")
    remove_parser.add_argument("key", help="Route key (e.g., YYC-LAX)")
    
    args = parser.parse_args()
    
    if args.command == "add":
        print(add_route(args))
    elif args.command == "list":
        print(list_routes(args))
    elif args.command == "watch":
        print(watch(args))
    elif args.command == "remove":
        print(remove_route(args))
    else:
        # Default: list then watch
        print(list_routes(args))
        print()
        args.days = 28
        print(watch(args))


if __name__ == "__main__":
    main()
