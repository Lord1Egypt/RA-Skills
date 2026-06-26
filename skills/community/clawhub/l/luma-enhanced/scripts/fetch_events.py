#!/usr/bin/env python3
"""
Fetch Luma events from city pages by extracting __NEXT_DATA__ JSON.
No API key required.
"""

import os
import sys
import urllib.request
import json
import re
import argparse
from datetime import datetime, timedelta, timezone
from html import unescape

# OpenClaw workspace memory path
WORKSPACE = os.getenv('OPENCLAW_WORKSPACE') or os.path.expanduser('~/.openclaw/workspace')
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')
EVENTS_FILE = os.path.join(MEMORY_DIR, 'luma-events.json')

def ensure_memory_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def load_events():
    """Load persisted events from JSON file."""
    ensure_memory_dir()
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_events(events):
    """Save events to JSON file, overwriting."""
    ensure_memory_dir()
    with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

def prune_old_events(events, hours=24):
    """Remove events that ended more than N hours ago."""
    if not events:
        return events
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    kept = []
    for ev in events:
        # Try both 'start' and 'start_at' keys for compatibility
        start_str = ev.get('start') or ev.get('start_at')
        if not start_str:
            kept.append(ev)
            continue
        try:
            # Parse ISO format; handle Z or timezone offset
            if start_str.endswith('Z'):
                dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(start_str)
            # If naive, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt >= cutoff:
                kept.append(ev)
        except Exception:
            kept.append(ev)
    return kept

def merge_events(existing_events, new_events):
    """Merge new events into existing list by event URL, unique by 'url' or 'event.url'."""
    by_url = {}
    for ev in existing_events:
        url = ev.get('url') or (ev.get('event', {}).get('url'))
        if url:
            by_url[url] = ev
    for ev in new_events:
        url = ev.get('url') or (ev.get('event', {}).get('url'))
        if url:
            by_url[url] = ev
    # Convert back to list, add lastFetched to new ones
    now = datetime.now(timezone.utc).isoformat()
    merged = []
    for ev in by_url.values():
        # Ensure lastFetched exists
        if 'lastFetched' not in ev:
            ev['lastFetched'] = now
        merged.append(ev)
    return merged

def fetch_luma_events(city_slug):
    """Fetch events for a city from Luma."""
    url = f"https://lu.ma/{city_slug}"
    
    try:
        # Add headers to avoid 403
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # Extract __NEXT_DATA__ JSON
        match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if not match:
            return {"error": f"Could not find __NEXT_DATA__ in {url}", "city": city_slug}
        
        data = json.loads(unescape(match.group(1)))
        
        # direct events array
        try:
            events = data['props']['pageProps']['initialData']['data']['events']
            return {"city": city_slug, "events": events, "url": url}
        except KeyError:
            # City page exists but no events array (unsupported format)
            return {"city": city_slug, "events": [], "url": url}
    
    except Exception as e:
        return {"error": str(e), "url": f"https://lu.ma/{city_slug}"}

def filter_events(events, days=None, max_events=None):
    """Filter events by date range and limit."""
    filtered = []
    cutoff = None
    
    if days:
        cutoff = datetime.now() + timedelta(days=days)
    
    for event_data in events:
        event = event_data.get('event', {})
        start = event.get('start_at')
        
        # Filter by date
        if start and cutoff:
            try:
                dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                if dt.replace(tzinfo=None) > cutoff:
                    continue
            except:
                pass
        
        filtered.append(event_data)
        
        # Limit results
        if max_events and len(filtered) >= max_events:
            break
    
    return filtered

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Luma events from city pages"
    )
    parser.add_argument(
        'cities',
        nargs='+',
        help='City slugs (e.g., bengaluru, mumbai, san-francisco)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Only show events within N days (default: 30)'
    )
    parser.add_argument(
        '--max',
        type=int,
        default=20,
        help='Maximum events per city (default: 20)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON instead of formatted text'
    )
    
    args = parser.parse_args()
    
    all_results = []
    
    # Load existing persisted events and prune old ones
    existing_events = load_events()
    existing_events = prune_old_events(existing_events, hours=24)
    save_events(existing_events)
    
    for city in args.cities:
        result = fetch_luma_events(city)
        
        if 'error' in result:
            print(f"\n❌ {city}: {result['error']}", flush=True)
            if args.json:
                all_results.append(result)
            continue
        
        events = result.get('events', [])
        filtered = filter_events(events, args.days, args.max)
        
        # If no events found (either empty or city not supported), print friendly message
        if not filtered and not args.json:
            if 'note' in result:
                print(f"\nℹ️ {city}: {result['note']}", flush=True)
            else:
                print(f"\n🤷 {city}: No upcoming events found.", flush=True)
            continue
        
        # Transform to persisted format and merge into existing
        now = datetime.now(timezone.utc).isoformat()
        new_formatted = []
        for event_data in filtered:
            event = event_data.get('event', {})
            hosts = event_data.get('hosts', [])
            ticket = event_data.get('ticket_info', {})
            guest_count = event_data.get('guest_count', 0)
            
            start = event.get('start_at')
            try:
                dt = datetime.fromisoformat(start.replace('Z', '+00:00')) if start else None
                date_str = dt.strftime('%b %d, %Y %I:%M %p %Z') if dt else "TBA"
            except:
                date_str = start or "TBA"
            
            geo = event.get('geo_address_info', {})
            venue = geo.get('address', 'Online')
            city_name = geo.get('city', city.title())
            url_slug = event.get('url', '')
            
            formatted = {
                "city": city,
                "name": event.get('name', 'Unnamed Event'),
                "start": start,
                "end": event.get('end_at'),
                "url": f"https://lu.ma/{url_slug}" if url_slug else "",
                "venue": f"{venue}, {city_name}",
                "hosts": [h.get('name', '') for h in hosts[:2]],
                "guestCount": guest_count,
                "ticketStatus": "sold_out" if ticket.get('is_sold_out') else ("free" if ticket.get('is_free') else "paid"),
                "spotsRemaining": ticket.get('spots_remaining'),
                "isFree": ticket.get('is_free', False),
                "lastFetched": now
            }
            new_formatted.append(formatted)
        
        # Merge into existing and save
        merged = merge_events(existing_events, new_formatted)
        merged = prune_old_events(merged, hours=24)
        save_events(merged)
        existing_events = merged  # update for subsequent cities
        
        if args.json:
            all_results.append({
                "city": city,
                "count": len(filtered),
                "events": filtered
            })
        else:
            print(f"\n{'='*60}", flush=True)
            print(f"📍 {city.upper()} — {len(filtered)} events", flush=True)
            print(f"{'='*60}", flush=True)
            
            for ev in new_formatted:
                # Print human-friendly format
                print(f"🎯 {ev['name']}", flush=True)
                print(f"📍 {ev['venue']}", flush=True)
                start_dt = datetime.fromisoformat(ev['start'].replace('Z', '+00:00')) if ev.get('start') else None
                if start_dt:
                    date_str = start_dt.strftime('%b %d, %Y %I:%M %p %Z')
                else:
                    date_str = "TBA"
                print(f"📅 {date_str}", flush=True)
                if ev['hosts']:
                    print(f"👥 {', '.join(ev['hosts'])}", flush=True)
                if ev['guestCount'] > 0:
                    print(f"👤 {ev['guestCount']} going", flush=True)
                # Ticket status
                ticket = ev
                if ticket['ticketStatus'] == 'sold_out':
                    ticket_str = "🔴 Sold Out"
                elif ticket['isFree']:
                    spots = ticket.get('spotsRemaining')
                    if spots and spots > 0:
                        ticket_str = f"🟢 Free ({spots} spots)"
                    else:
                        ticket_str = "🟢 Free"
                else:
                    spots = ticket.get('spotsRemaining')
                    if spots and spots > 0:
                        ticket_str = f"🎫 Available ({spots} spots)"
                    else:
                        ticket_str = "🎫 Paid"
                print(f"{ticket_str}", flush=True)
                print(f"🔗 {ev['url']}", flush=True)
                print("", flush=True)
    
    if args.json:
        print(json.dumps(all_results, indent=2), flush=True)

if __name__ == '__main__':
    main()
