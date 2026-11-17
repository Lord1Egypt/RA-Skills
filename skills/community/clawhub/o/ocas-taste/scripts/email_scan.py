#!/usr/bin/env python3
"""
Email and calendar scan for Taste skill.
Extracts consumption signals from Gmail and Google Calendar.
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Email-only consumption signal extraction.')
    print("Usage: email_scan.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Auth
AGENT_ROOT = Path(os.environ.get("AGENT_ROOT", Path.home() / ".hermes"))
sys.path.insert(0, str(AGENT_ROOT / 'scripts'))

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 email_scan.py")
    sys.exit(0)

from google_auth import get_service


service = get_service('gmail', 'v1', ['https://www.googleapis.com/auth/gmail.modify'], account=os.environ.get("OCAS_OPERATOR_EMAIL", "operator@example.com"))

def get_calendar_service():
    """Get authenticated Calendar service."""
    return get_service('calendar', 'v3', ['https://www.googleapis.com/auth/calendar'], account=os.environ.get("OCAS_OPERATOR_EMAIL", "operator@example.com"))

def normalize_venue_name(name: str) -> str:
    """Normalize venue name for deduplication."""
    name = name.lower()
    name = re.sub(r'\bthe\b', '', name)
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip()

def compute_dedup_key(service: str, order_id: str, event_date: str, venue_name: str) -> str:
    """Compute deduplication key."""
    normalized = normalize_venue_name(venue_name)
    return f"{service}:{order_id}:{event_date}:{normalized}"

def extract_from_email(service: str, message: Dict, config: Dict) -> Dict:
    """Extract consumption data from email message."""
    subject = message.get('payload', {}).get('headers', [])
    subject_text = next((h['value'] for h in subject if h['name'] == 'Subject'), '')
    
    # Simple extraction based on service patterns
    extraction = {
        "extraction_id": f"email-{message['id']}",
        "source_service": service,
        "email_type": "confirmation",
        "cancelled": False,
        "extracted_at": datetime.utcnow().isoformat(),
        "raw_subject": subject_text
    }
    
    # Service-specific extraction hints would go here
    # For now, this is a placeholder that would need LLM-based extraction
    
    return extraction

def scan_gmail(config: Dict, last_scan: str = None) -> List[Dict]:
    """Scan Gmail for consumption signals."""
    service = get_gmail_service()
    extractions = []
    
    # Build query for configured email sources
    email_sources = config.get('email_sources', {})
    queries = []
    
    for service_name, service_config in email_sources.items():
        for pattern in service_config.get('sender_patterns', []):
            queries.append(f"from:{pattern}")
    
    if not queries:
        print("No email sources configured")
        return extractions
    
    query = " OR ".join(queries)
    
    # Add date filter if last_scan exists
    if last_scan:
        dt = datetime.fromisoformat(last_scan)
        date_str = dt.strftime('%Y/%m/%d')
        query = f"{query} after:{date_str}"
    
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=100
        ).execute()
        
        messages = results.get('messages', [])
        
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            # Determine which service this is from
            from_header = next((h['value'] for h in msg_data.get('payload', {}).get('headers', []) 
                              if h['name'] == 'From'), '')
            
            service_name = None
            for svc, svc_config in email_sources.items():
                for pattern in svc_config.get('sender_patterns', []):
                    if pattern in from_header:
                        service_name = svc
                        break
                if service_name:
                    break
            
            if service_name:
                extraction = extract_from_email(service_name, msg_data, config)
                extractions.append(extraction)
        
        print(f"Found {len(extractions)} emails from configured sources")
        
    except Exception as e:
        print(f"Error scanning Gmail: {e}")
    
    return extractions

def scan_calendar(config: Dict, last_scan: str = None) -> List[Dict]:
    """Scan Google Calendar for restaurant reservations and hotel bookings.
    
    Enumerates all writable calendars, not just 'primary', since shared
    calendars often contain reservation and hotel events.
    """
    service = get_calendar_service()
    extractions = []
    
    try:
        now = datetime.utcnow()
        time_min = now - timedelta(days=30)  # Look back 30 days
        time_max = now + timedelta(days=30)   # Look ahead 30 days
        
        # Enumerate writable calendars
        calendar_list = service.calendarList().list().execute()
        writable_cals = [
            cal['id'] for cal in calendar_list.get('items', [])
            if cal.get('accessRole') in ('owner', 'writer')
        ]
        print(f"Found {len(writable_cals)} writable calendars")
        
        seen_dedup_keys = set()
        
        for cal_id in writable_cals:
            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            for event in events:
                summary = event.get('summary', '')
                location = event.get('location', '')
                
                # Cross-calendar dedup key
                event_date = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date', '')
                dedup_key = f"calendar:{normalize_venue_name(summary)}:{event_date[:10]}"
                if dedup_key in seen_dedup_keys:
                    continue
                seen_dedup_keys.add(dedup_key)
            
            # Simple pattern matching for restaurants and hotels
            # In production, this would use LLM-based extraction
            summary_lower = summary.lower()
            location_lower = location.lower()
            
            # Classify domain based on keywords
            domain = None
            source_type = None
            venue_name = summary
            
            meal_keywords = ['restaurant', 'dinner', 'lunch', 'brunch', 'breakfast', 
                           'omakase', 'tasting', 'chef', 'reservation at']
            hotel_keywords = ['hotel', 'fairmont', 'marriott', 'hilton', 'hyatt', 
                            'ihg', 'airbnb', 'inn', 'resort']
            
            if any(kw in summary_lower for kw in meal_keywords):
                domain = 'restaurant'
                source_type = 'visit'
                # Strip "Reservation at " / "Dinner at " prefixes
                for prefix in ['reservation at ', 'dinner at ', 'lunch at ', 
                              'brunch at ', 'breakfast at ']:
                    if summary_lower.startswith(prefix):
                        venue_name = summary[len(prefix):].strip()
                        break
                # Strip city suffixes
                for suffix in [' - San Francisco', ' – San Francisco', ' - SF', 
                              ' - Oakland', ' - Daly City', ' - Berkeley']:
                    if venue_name.endswith(suffix):
                        venue_name = venue_name[:-len(suffix)]
            elif any(kw in summary_lower for kw in hotel_keywords):
                domain = 'travel'
                source_type = 'stay'
            
            if domain:
                extraction = {
                    "extraction_id": f"calendar-{event['id']}",
                    "source_service": "calendar",
                    "email_type": source_type,
                    "cancelled": False,
                    "extracted_at": datetime.utcnow().isoformat(),
                    "raw_subject": summary,
                    "venue_name": venue_name,
                    "event_date": event.get('start', {}).get('dateTime') or event.get('start', {}).get('date'),
                    "domain_hint": domain
                }
                extractions.append(extraction)
        
        print(f"Found {len(extractions)} calendar events")
        
    except Exception as e:
        print(f"Error scanning Calendar: {e}")
    
    return extractions

def deduplicate_extractions(extractions: List[Dict]) -> Dict:
    """Deduplicate extractions and handle cancellations."""
    groups = {}
    
    for extraction in extractions:
        # Compute dedup key
        service = extraction.get('source_service', 'unknown')
        order_id = extraction.get('order_id', extraction.get('extraction_id'))
        event_date = extraction.get('event_date', extraction.get('extracted_at'))
        venue_name = extraction.get('venue_name', extraction.get('raw_subject', ''))
        
        dedup_key = compute_dedup_key(service, order_id, event_date, venue_name)
        
        if dedup_key not in groups:
            groups[dedup_key] = []
        groups[dedup_key].append(extraction)
    
    # Process groups
    results = {
        "distinct": [],
        "cancelled": [],
        "possible_matches": []
    }
    
    for key, group in groups.items():
        # Check for cancellations
        if any(e.get('cancelled', False) for e in group):
            results["cancelled"].extend(group)
            continue
        
        # Select richest extraction
        richest = max(group, key=lambda e: len(e))
        results["distinct"].append(richest)
    
    return results

def promote_to_signals(extractions: List[Dict], config: Dict) -> List[Dict]:
    """Promote extractions to consumption signals."""
    signals = []
    
    for extraction in extractions:
        # Use domain_hint from extraction if available (calendar events),
        # otherwise fall back to email_sources config
        source_service = extraction.get('source_service', '')
        source_config = config.get('email_sources', {}).get(source_service, {})
        
        domain = extraction.get('domain_hint') or source_config.get('domain', 'unknown')
        source = source_config.get('source_type', extraction.get('email_type', 'unknown'))
        
        # Get strength from config
        strength_key = f"base_{source}"
        strength = config.get('strength', {}).get(strength_key, 0.60)
        
        # Create signal
        signal = {
            "signal_id": f"signal-{extraction['extraction_id']}",
            "item_id": f"item-{extraction['extraction_id']}",
            "domain": domain,
            "source": source,
            "strength": strength,
            "timestamp": extraction.get('event_date') or extraction.get('extracted_at'),
            "metadata": {
                "extraction_id": extraction['extraction_id'],
                "source_service": source_service
            }
        }
        signals.append(signal)
    
    return signals

def main():
    """Main scan function."""
    print("Starting email and calendar scan...")
    
    # Load config
    config = load_config()
    last_scan = config.get('email_scan', {}).get('last_scan_timestamp')
    
    # Scan Gmail
    print("Scanning Gmail...")
    email_extractions = scan_gmail(config, last_scan)
    
    # Scan Calendar
    print("Scanning Google Calendar...")
    calendar_extractions = scan_calendar(config, last_scan)
    
    # Combine extractions
    all_extractions = email_extractions + calendar_extractions
    
    if not all_extractions:
        print("No new extractions found")
        return
    
    # Deduplicate
    print("Deduplicating extractions...")
    dedup_results = deduplicate_extractions(all_extractions)
    
    # Promote to signals
    print("Promoting to signals...")
    signals = promote_to_signals(dedup_results['distinct'], config)
    
    # Write extractions
    with open(EXTRACTIONS_FILE, 'a') as f:
        for extraction in all_extractions:
            f.write(json.dumps(extraction) + '\n')
    
    # Write signals
    if signals:
        with open(SIGNALS_FILE, 'a') as f:
            for signal in signals:
                f.write(json.dumps(signal) + '\n')
        print(f"Created {len(signals)} signals")
    
    # Update last scan timestamp
    config['email_scan']['last_scan_timestamp'] = datetime.utcnow().isoformat()
    save_config(config)
    
    print(f"Scan complete. Last scan: {config['email_scan']['last_scan_timestamp']}")
    print(f"  Extractions: {len(all_extractions)}")
    print(f"  Signals: {len(signals)}")
    print(f"  Cancelled: {len(dedup_results['cancelled'])}")

if __name__ == "__main__":
    main()