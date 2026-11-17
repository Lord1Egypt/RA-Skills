#!/usr/bin/env python3
"""
Taste skill - complete implementation with historical scanning and enrichment
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Scan email/calendar for consumption signals; extract, dedup, promote to signals.')
    print("Usage: taste_scan.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import json
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import base64
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 taste_scan.py")
    sys.exit(0)


# Google API imports
try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    from google.auth.transport.requests import Request
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("Warning: Google API libraries not available. Install with: pip install google-api-python-client google-auth-oauthlib")


class TasteSkill:
    """Taste skill implementation for consumption signal extraction and enrichment"""

    def __init__(self, data_dir: str = None):
        if not data_dir:
            # Resolve real data dir; commons -> profiles/indigo/commons on this profile
            _root = os.environ.get("AGENT_ROOT", os.environ.get("AGENT_ROOT", os.path.join(os.path.expanduser("~"), ".hermes")))
            data_dir = os.path.join(_root, "commons", "data", "ocas-taste")
        self.data_dir = Path(data_dir)
        self.config_file = self.data_dir / "config.json"
        self.signals_file = self.data_dir / "signals.jsonl"
        self.items_file = self.data_dir / "items.jsonl"
        self.extractions_file = self.data_dir / "extractions.jsonl"
        self.decisions_file = self.data_dir / "decisions.jsonl"
        self.music_dir = self.data_dir / "music"
        self.checkpoint_file = self.music_dir / "sync_checkpoint.json"

        self.config = self._load_config()
        self.gmail_service = None
        self.calendar_service = None
        self.maps_service = None

    def _load_config(self) -> Dict:
        """Load configuration from config.json"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {}

    def _save_config(self):
        """Save configuration to config.json"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def _append_jsonl(self, file_path: Path, data: Dict):
        """Append a record to a JSONL file"""
        with open(file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')

    def _read_jsonl(self, file_path: Path) -> List[Dict]:
        """Read all records from a JSONL file"""
        records = []
        if file_path.exists():
            with open(file_path) as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        return records

    def _normalize_venue_name(self, name: str) -> str:
        """Normalize venue name for deduplication"""
        name = name.lower()
        name = re.sub(r'\bthe\b', '', name)
        name = re.sub(r'\s+', ' ', name)
        name = re.sub(r'[^\w\s]', '', name)
        return name.strip()

    def _normalize_calendar_venue(self, summary: str) -> str:
        """Normalize calendar event summary to clean venue name.
        Strips 'Reservation at ' prefix, 'for N' suffix, city suffixes,
        and holiday/emoji decorations."""
        name = summary.strip()
        # Strip 'Reservation at ' prefix
        name = re.sub(r'^Reservation at\s+', '', name, flags=re.IGNORECASE)
        # Strip trailing ' for N' (party size)
        name = re.sub(r'\s+for\s+\d+$', '', name, flags=re.IGNORECASE)
        # Strip city suffixes like ' - San Francisco', ' – Daly City'
        name = re.sub(r'\s*[-–—]\s*(San Francisco|Daly City|Oakland|SF|Dallas|Austin|Palo Alto|Burlingame|Palm Springs|New York|Providence|Honolulu|Santa Cruz|San Antonio)$', '', name, flags=re.IGNORECASE)
        # Strip emoji and decorative characters
        name = re.sub(r'[🌟🎄🎉🎊🎁🌴🎸🎭🎨🎪🎤🎬🎶🎵🌮🍕🍷🥂🍸🌯🥗🍜🍣🍱🥟🍝🍛🍲🍤🎂🍰🧁🥧🍦🍨🍩🍪🍫🍬🍭🍮🍯🍿🏖️🏔️🗺️🏠🛒🛍️💳✨]', '', name)
        # Collapse multiple spaces
        name = re.sub(r'\s+', ' ', name).strip()
        # Strip trailing 'know you are coming' or similar calendar notes
        name = re.sub(r'\s+know you are coming$', '', name, flags=re.IGNORECASE)
        return name if name else summary.strip()

    def _compute_dedup_key(self, service: str, order_id: str, event_date: str, venue_name: str) -> str:
        """Compute deduplication key for an extraction"""
        normalized_venue = self._normalize_venue_name(venue_name)
        return f"{service}:{order_id}:{event_date}:{normalized_venue}"

    def _init_google_services(self):
        """Initialize Gmail, Calendar, and Maps services"""
        if not GOOGLE_API_AVAILABLE:
            print("Google API libraries not available")
            return False

        # Google Workspace MCP credentials — each account uses its own OAuth client
        token_paths = [
            Path(os.environ.get("GOOGLE_CREDS_DIR", os.path.expanduser("~/.google_workspace_mcp/credentials"))) / "operator_email.json",   # operator (user) — primary for email/calendar
            Path(os.environ.get("GOOGLE_CREDS_DIR", os.path.expanduser("~/.google_workspace_mcp/credentials"))) / "agent_email.json",   # Indigo Karasu (agent) — fallback
        ]

        for token_path in token_paths:
            if not token_path.exists():
                continue

            try:
                token_data = json.loads(Path(token_path).read_text())
                token_scopes = token_data.get('scopes', ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly'])
                creds = Credentials.from_authorized_user_file(str(token_path), token_scopes)

                if not creds.valid:
                    if creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                        try:
                            with open(token_path, 'w') as f:
                                f.write(creds.to_json())
                        except PermissionError:
                            print(f"Warning: cannot write refreshed token to {token_path} (read-only), continuing with in-memory token")
                    else:
                        print(f"Skipping {token_path.name}: credentials invalid and cannot be refreshed")
                        continue

                self.gmail_service = build('gmail', 'v1', credentials=creds)
                self.calendar_service = build('calendar', 'v3', credentials=creds)
                print(f"Initialized Gmail and Calendar with {token_path.name}")
                return True

            except Exception as e:
                print(f"Error with {token_path.name}: {e}")
                continue

        print("No Google token file found (tried all paths)")

        # Fall back to service account for Maps
        service_account_path = Path("<hermes-home>/credentials/hermes-ocigcp.json")
        if service_account_path.exists():
            try:
                scopes = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/maps']
                creds = ServiceAccountCredentials.from_service_account_file(str(service_account_path), scopes=scopes)
                
                if not self.gmail_service:
                    self.gmail_service = build('gmail', 'v1', credentials=creds)
                if not self.calendar_service:
                    self.calendar_service = build('calendar', 'v3', credentials=creds)
                self.maps_service = build('maps', 'v1', credentials=creds)
                
                print("Initialized services with service account")
                return True

            except Exception as e:
                print(f"Error initializing with service account: {e}")

        return False

    def scan_email_historical(self, days_back: int = 365, batch_size: int = 100) -> Dict:
        """Scan Gmail for ALL historical consumption signals, batched"""
        if not self._init_google_services():
            return {"error": "Failed to initialize Google services"}

        results = {
            "extractions": [],
            "signals_created": 0,
            "cancellations": 0,
            "services_scanned": [],
            "total_messages_processed": 0,
            "scan_complete": False
        }

        # Historical scan: always go back full days_back from now
        last_scan_dt = datetime.now() - timedelta(days=days_back)

        # Build query for each service
        email_sources = self.config.get("email_sources", {})

        for service_name, service_config in email_sources.items():
            sender_patterns = service_config.get("sender_patterns", [])
            domain = service_config.get("domain")
            source_type = service_config.get("source_type")

            if not sender_patterns:
                continue

            # Build Gmail search query
            # Group sender patterns with OR, then AND with date filter
            sender_query = " OR ".join([f"from:{p}" for p in sender_patterns])
            # Add date filter - scan ALL history, not just recent
            date_str = last_scan_dt.strftime("%Y/%m/%d")
            # Parenthesize the OR group and AND with date filter
            query = f"({sender_query}) after:{date_str}"

            try:
                # Search messages with pagination
                page_token = None
                total_processed = 0

                while True:
                    messages_result = self.gmail_service.users().messages().list(
                        userId='me',
                        q=query,
                        maxResults=batch_size,
                        pageToken=page_token
                    ).execute()

                    messages = messages_result.get('messages', [])
                    
                    if not messages:
                        break

                    for msg in messages:
                        msg_data = self.gmail_service.users().messages().get(
                            userId='me',
                            id=msg['id'],
                            format='full'
                        ).execute()

                        extraction = self._extract_from_email(msg_data, service_name, domain, source_type)
                        if extraction:
                            results["extractions"].append(extraction)

                        total_processed += 1

                    results["total_messages_processed"] += len(messages)
                    page_token = messages_result.get('nextPageToken')

                    if not page_token:
                        break

                results["services_scanned"].append(service_name)
                print(f"Processed {total_processed} messages from {service_name}")

            except Exception as e:
                print(f"Error scanning {service_name}: {e}")

        # Deduplicate and promote to signals
        signals, cancellations = self._process_extractions(results["extractions"])
        results["signals_created"] = len(signals)
        results["cancellations"] = cancellations

        # Update last scan timestamp
        self.config.setdefault("email_scan", {})["last_scan_timestamp"] = datetime.now().isoformat()
        self._save_config()

        results["scan_complete"] = True
        return results

    def scan_email_incremental(self, hours_back: int = 24) -> Dict:
        """Scan Gmail for recent consumption signals (incremental)"""
        if not self._init_google_services():
            return {"error": "Failed to initialize Google services"}

        results = {
            "extractions": [],
            "signals_created": 0,
            "cancellations": 0,
            "services_scanned": []
        }

        # Get last scan timestamp
        last_scan = self.config.get("email_scan", {}).get("last_scan_timestamp")
        if last_scan:
            last_scan_dt = datetime.fromisoformat(last_scan)
        else:
            last_scan_dt = datetime.now() - timedelta(hours=hours_back)

        # Build query for each service
        email_sources = self.config.get("email_sources", {})

        for service_name, service_config in email_sources.items():
            sender_patterns = service_config.get("sender_patterns", [])
            domain = service_config.get("domain")
            source_type = service_config.get("source_type")

            if not sender_patterns:
                continue

            # Build Gmail search query
            # Group sender patterns with OR, then AND with date filter
            sender_query = " OR ".join([f"from:{p}" for p in sender_patterns])

            # Add date filter
            date_str = last_scan_dt.strftime("%Y/%m/%d")
            # Parenthesize the OR group and AND with date filter
            query = f"({sender_query}) after:{date_str}"

            try:
                # Search messages
                messages_result = self.gmail_service.users().messages().list(
                    userId='me',
                    q=query
                ).execute()

                messages = messages_result.get('messages', [])

                for msg in messages:
                    msg_data = self.gmail_service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='full'
                    ).execute()

                    extraction = self._extract_from_email(msg_data, service_name, domain, source_type)
                    if extraction:
                        results["extractions"].append(extraction)

                results["services_scanned"].append(service_name)

            except Exception as e:
                print(f"Error scanning {service_name}: {e}")

        # Deduplicate and promote to signals
        signals, cancellations = self._process_extractions(results["extractions"])
        results["signals_created"] = len(signals)
        results["cancellations"] = cancellations

        # Update last scan timestamp
        self.config.setdefault("email_scan", {})["last_scan_timestamp"] = datetime.now().isoformat()
        self._save_config()

        return results

    def _extract_from_email(self, msg_data: Dict, service: str, domain: str, source_type: str) -> Optional[Dict]:
        """Extract consumption signal from email message"""
        try:
            headers = {h['name']: h['value'] for h in msg_data['payload'].get('headers', [])}
            subject = headers.get('Subject', '')
            from_addr = headers.get('From', '')
            date_str = headers.get('Date', '')

            # Parse date
            try:
                email_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            except:
                email_date = datetime.now()

            # Get email body
            body = self._get_email_body(msg_data['payload'])

            # Extract structured data based on service
            extraction = {
                "service": service,
                "domain": domain,
                "source_type": source_type,
                "from": from_addr,
                "subject": subject,
                "date": email_date.isoformat(),
                "body": body[:5000],  # Truncate to avoid huge records
                "email_type": self._classify_email_type(subject, body),
                "cancelled": False
            }

            # Service-specific extraction
            if service == "doordash":
                extraction.update(self._extract_doordash(subject, body))
            elif service == "instacart":
                extraction.update(self._extract_instacart(subject, body))
            elif service in ["tock", "opentable", "yelp"]:
                extraction.update(self._extract_reservation(subject, body))
            elif service == "amazon":
                extraction.update(self._extract_amazon(subject, body))
            elif service == "hotels":
                extraction.update(self._extract_hotel(subject, body))

            # Filter out garbage extractions with no real venue name
            if extraction.get("venue_name") in (None, "Unknown", ""):
                return None

            # Filter out emails that aren't actually from the expected service
            # (catches wildcard pattern matches on unrelated emails)
            expected_senders = self.config.get("email_sources", {}).get(service, {}).get("sender_patterns", [])
            from_lower = from_addr.lower()
            actual_service_email = any(
                pat.replace("*", "").lower() in from_lower
                for pat in expected_senders
                if pat
            )
            if not actual_service_email and expected_senders:
                return None

            return extraction

        except Exception as e:
            print(f"Error extracting from email: {e}")
            return None

    def _get_email_body(self, payload: Dict) -> str:
        """Extract email body from message payload"""
        body = ""

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif 'parts' in part:
                    body += self._get_email_body(part)

        elif 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        return body

    def _classify_email_type(self, subject: str, body: str) -> str:
        """Classify email type (confirmation, reminder, cancellation, receipt)"""
        subject_lower = subject.lower()
        body_lower = body.lower()

        if any(word in subject_lower for word in ['cancelled', 'canceled', 'cancel']):
            return 'cancellation'
        elif any(word in subject_lower for word in ['receipt', 'order complete', 'delivered']):
            return 'receipt'
        elif any(word in subject_lower for word in ['reminder', 'upcoming', 'tomorrow']):
            return 'reminder'
        elif any(word in subject_lower for word in ['confirmation', 'confirmed', 'booked']):
            return 'confirmation'
        else:
            return 'unknown'

    def _extract_doordash(self, subject: str, body: str) -> Dict:
        """Extract DoorDash order details"""
        venue_match = re.search(r'from\s+([^\n]+)', subject, re.IGNORECASE)
        venue = venue_match.group(1).strip() if venue_match else "Unknown"

        total_match = re.search(r'\$[\d,]+\.\d{2}', body)
        total = total_match.group(0) if total_match else None

        order_id_match = re.search(r'order\s+#?\s*[\w-]+', body, re.IGNORECASE)
        order_id = order_id_match.group(0) if order_id_match else None

        return {
            "venue_name": venue,
            "order_id": order_id or "unknown",
            "total": total,
            "items": []
        }

    def _extract_instacart(self, subject: str, body: str) -> Dict:
        """Extract Instacart order details"""
        store_match = re.search(r'from\s+([^\n]+)', subject, re.IGNORECASE)
        store = store_match.group(1).strip() if store_match else "Unknown"

        total_match = re.search(r'\$[\d,]+\.\d{2}', body)
        total = total_match.group(0) if total_match else None

        return {
            "venue_name": store,
            "order_id": "unknown",
            "total": total,
            "items": []
        }

    def _extract_reservation(self, subject: str, body: str) -> Dict:
        """Extract restaurant reservation details"""
        venue_match = re.search(r'at\s+([^\n,]+)', subject, re.IGNORECASE)
        venue = venue_match.group(1).strip() if venue_match else "Unknown"

        date_match = re.search(r'on\s+([A-Za-z]+,\s+[A-Za-z]+\s+\d+)', subject, re.IGNORECASE)
        date_str = date_match.group(1) if date_match else None

        party_size_match = re.search(r'(\d+)\s+people?', subject, re.IGNORECASE)
        party_size = int(party_size_match.group(1)) if party_size_match else None

        confirmation_match = re.search(r'confirmation\s+#?\s*([\w-]+)', body, re.IGNORECASE)
        confirmation = confirmation_match.group(1) if confirmation_match else None

        return {
            "venue_name": venue,
            "order_id": confirmation or "unknown",
            "event_date": date_str,
            "party_size": party_size
        }

    def _extract_amazon(self, subject: str, body: str) -> Dict:
        """Extract Amazon order details"""
        product_match = re.search(r'Amazon\.com\s+[:\s]+([^\n]+)', subject, re.IGNORECASE)
        product = product_match.group(1).strip() if product_match else "Unknown"

        order_id_match = re.search(r'order\s+#?\s*([\d-]+)', subject, re.IGNORECASE)
        order_id = order_id_match.group(1) if order_id_match else None

        return {
            "venue_name": product,
            "order_id": order_id or "unknown",
            "total": None,
            "items": []
        }

    def _extract_hotel(self, subject: str, body: str) -> Dict:
        """Extract hotel booking details"""
        hotel_match = re.search(r'at\s+([^\n,]+)', subject, re.IGNORECASE)
        hotel = hotel_match.group(1).strip() if hotel_match else "Unknown"

        confirmation_match = re.search(r'confirmation\s+#?\s*([\w-]+)', body, re.IGNORECASE)
        confirmation = confirmation_match.group(1) if confirmation_match else None

        return {
            "venue_name": hotel,
            "order_id": confirmation or "unknown",
            "check_in": None,
            "check_out": None
        }

    def _process_extractions(self, extractions: List[Dict], cross_calendar_dedup: bool = True) -> tuple:
        """Deduplicate extractions and promote to signals.
        
        Args:
            extractions: List of extraction records
            cross_calendar_dedup: If True, dedup across calendars by {service}:{normalized_venue}:{date}
        """
        # Group by dedup key
        groups = {}
        for extraction in extractions:
            dedup_key = self._compute_dedup_key(
                extraction['service'],
                extraction.get('order_id', 'unknown'),
                extraction['date'],
                extraction.get('venue_name', 'unknown')
            )
            if dedup_key not in groups:
                groups[dedup_key] = []
            groups[dedup_key].append(extraction)

        # Cross-calendar dedup: same venue + same date from different calendars
        seen_cross_cal = set()
        filtered_groups = {}
        for dedup_key, group in groups.items():
            if cross_calendar_dedup and group:
                first = group[0]
                normalized = self._normalize_venue_name(first.get('venue_name', ''))
                date_str = first.get('date', '')[:10]  # YYYY-MM-DD
                cross_key = f"{first.get('service', 'unknown')}:{normalized}:{date_str}"
                if cross_key in seen_cross_cal:
                    continue
                seen_cross_cal.add(cross_key)
            filtered_groups[dedup_key] = group

        signals = []
        cancellations = 0

        for dedup_key, group in filtered_groups.items():
            # Check for cancellations
            if any(e.get('email_type') == 'cancellation' for e in group):
                cancellations += 1
                continue

            # Select richest extraction
            canonical = max(group, key=lambda e: len(e))

            # Create signal
            signal = {
                "signal_id": f"sig-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}",
                "domain": canonical['domain'],
                "source_type": canonical['source_type'],
                "venue_name": canonical.get('venue_name'),
                "event_date": canonical['date'],
                "strength": self._compute_base_strength(canonical['source_type']),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "extraction_source": canonical['service']
            }

            signals.append(signal)
            self._append_jsonl(self.signals_file, signal)

            # Create/update item record
            self._update_item_record(canonical)

        return signals, cancellations

    def _compute_base_strength(self, source_type: str) -> float:
        """Compute base strength for a signal type"""
        strength_config = self.config.get("strength", {})
        return strength_config.get(f"base_{source_type}", 0.70)

    def _update_item_record(self, extraction: Dict):
        """Create or update item record"""
        venue_name = extraction.get('venue_name')
        if not venue_name:
            return

        # Read existing items
        items = self._read_jsonl(self.items_file)

        # Find existing item
        existing_item = None
        for item in items:
            if item.get('venue_name') == venue_name:
                existing_item = item
                break

        if existing_item:
            # Update existing
            existing_item['signal_count'] = existing_item.get('signal_count', 0) + 1
            existing_item['last_seen'] = extraction['date']
            if 'visit_dates' not in existing_item:
                existing_item['visit_dates'] = []
            existing_item['visit_dates'].append(extraction['date'])
        else:
            # Create new
            item = {
                "item_id": f"item-{uuid.uuid4().hex}",
                "venue_name": venue_name,
                "domain": extraction['domain'],
                "signal_count": 1,
                "first_seen": extraction['date'],
                "last_seen": extraction['date'],
                "visit_dates": [extraction['date']],
                "enriched": False
            }
            items.append(item)

        # Write back
        with open(self.items_file, 'w') as f:
            for item in items:
                f.write(json.dumps(item) + '\n')

    def scan_calendar_historical(self, days_back: int = 365) -> Dict:
        """Scan ALL writable Google Calendars for restaurant reservations and hotel bookings"""
        if not self._init_google_services():
            return {"error": "Failed to initialize Google services"}

        results = {
            "extractions": [],
            "signals_created": 0,
            "total_events_processed": 0,
            "calendars_scanned": []
        }

        try:
            # Calculate time range - scan ALL history
            time_min = (datetime.now() - timedelta(days=days_back)).isoformat() + 'Z'
            time_max = datetime.now().isoformat() + 'Z'

            # Get all calendars (owner/writer access)
            cal_list = self.calendar_service.calendarList().list().execute()
            calendars = cal_list.get('items', [])
            scannable_cals = [c for c in calendars if c.get('accessRole') in ('owner', 'writer')]

            for cal in scannable_cals:
                cal_id = cal['id']
                cal_name = cal['summary']
                page_token = None
                cal_events = 0

                while True:
                    events_result = self.calendar_service.events().list(
                        calendarId=cal_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        singleEvents=True,
                        orderBy='startTime',
                        maxResults=250,
                        pageToken=page_token
                    ).execute()

                    events = events_result.get('items', [])

                    for event in events:
                        extraction = self._extract_from_calendar(event)
                        if extraction:
                            extraction['calendar_source'] = cal_name
                            results["extractions"].append(extraction)
                        cal_events += 1

                    results["total_events_processed"] += len(events)
                    page_token = events_result.get('nextPageToken')

                    if not page_token:
                        break

                results["calendars_scanned"].append(cal_name)
                print(f"Processed {cal_events} events from {cal_name}")

            # Process extractions
            signals, _ = self._process_extractions(results["extractions"])
            results["signals_created"] = len(signals)

        except Exception as e:
            print(f"Error scanning calendar: {e}")
            results["error"] = str(e)

        return results

    def _extract_from_calendar(self, event: Dict) -> Optional[Dict]:
        """Extract consumption signal from calendar event"""
        try:
            summary = event.get('summary', '')
            location = event.get('location', '')
            description = event.get('description', '')

            # Check if this looks like a restaurant or hotel
            if not self._is_venue_event(summary, location, description):
                return None

            start = event.get('start', {})
            event_date = start.get('dateTime') or start.get('date')

            return {
                "service": "calendar",
                "domain": self._infer_domain(summary, location),
                "source_type": "visit",
                "venue_name": self._normalize_calendar_venue(summary),
                "date": event_date,
                "location": location,
                "email_type": "confirmation",
                "cancelled": False,
                "order_id": f"cal-{event.get('id', 'unknown')}"
            }

        except Exception as e:
            print(f"Error extracting from calendar: {e}")
            return None

    def _is_venue_event(self, summary: str, location: str, description: str) -> bool:
        """Check if calendar event is a venue event (real restaurant/hotel, not medical/zoom)"""
        text = f"{summary} {location} {description}".lower()

        # Exclude medical appointments, doctor visits, video calls
        exclude_keywords = ['appointment', 'video visit', 'video appointment', 'doctor', 'dr.', 'checkup',
                           'medical', 'one medical', 'bodyspec', 'telehealth']
        if any(kw in text for kw in exclude_keywords):
            return False

        # Exclude generic digital meetings (Zoom/Teams links without venue addresses)
        meeting_indicators = ['zoom.us', 'teams.microsoft', 'google meet', 'connecting via', 'we connected']
        if any(kw in text for kw in meeting_indicators):
            return False

        # Exclude generic meal keywords without a named venue
        # e.g. "Breakfast", "Lunch", "Dinner", "Brunch" alone are noise
        generic_meal_keywords = {'breakfast', 'lunch', 'dinner', 'brunch', 'snack', 'coffee'}
        summary_stripped = summary.strip().lower()
        if summary_stripped in generic_meal_keywords:
            return False

        # Restaurant keywords — must have a specific venue indicator
        restaurant_keywords = ['reservation at', 'restaurant', 'cafe']
        if any(kw in text for kw in restaurant_keywords):
            return True

        # Meal keywords that need a specific named venue or location
        meal_keywords = ['dinner', 'lunch', 'brunch', 'breakfast']
        # Require location to contain an address or named venue for generic meal events
        has_specific_venue = any(indicator in location.lower() for indicator in
                                 ['st', 'street', 'ave', 'blvd', 'drive', 'road', 'hotel', 'restaurant',
                                  'cafe', 'bar', 'kitchen']) or 'reservation' in text.lower()

        if any(kw in text for kw in meal_keywords) and has_specific_venue:
            return True

        # Hotel keywords — always specific
        hotel_keywords = ['stay at', 'hotel', 'airbnb', 'booking.com']
        if any(kw in text for kw in hotel_keywords):
            return True

        return False

    def _infer_domain(self, summary: str, location: str) -> str:
        """Infer domain from event details"""
        text = f"{summary} {location}".lower()

        if any(kw in text for kw in ['hotel', 'stay', 'airbnb']):
            return 'travel'
        else:
            return 'restaurant'

    def enrich_items(self, limit: int = 50) -> Dict:
        """Enrich unenriched items using Google Places API (v1) via direct HTTP.
        
        Uses the Places API v1 searchText endpoint which requires the Places API
        to be enabled in the GCP project. Falls back to web search if Maps fails.
        """
        results = {
            "enriched": 0,
            "failed": 0,
            "skipped": 0
        }

        # Read items
        items = self._read_jsonl(self.items_file)

        # Find unenriched items, prioritizing by signal count (highest first)
        unenriched = sorted(
            [item for item in items if not item.get('enriched', False)],
            key=lambda x: x.get('signal_count', 0),
            reverse=True
        )

        if not unenriched:
            return {"message": "All items already enriched"}

        # Get API key from credentials
        api_key = self._get_maps_api_key()
        if not api_key:
            return {"error": "No Google Maps API key available. Set GOOGLE_MAPS_API_KEY in environment or .env file."}

        # Enrich up to limit items
        for item in unenriched[:limit]:
            venue_name = item.get('venue_name')
            domain = item.get('domain')

            if not venue_name:
                results["skipped"] += 1
                continue

            try:
                enrichment = self._enrich_single_item(venue_name, domain, api_key)
                if enrichment:
                    item.update(enrichment)
                    results["enriched"] += 1
                else:
                    results["failed"] += 1

            except Exception as e:
                print(f"Error enriching {venue_name}: {e}")
                results["failed"] += 1

        # Write back all items
        with open(self.items_file, 'w') as f:
            for item in items:
                f.write(json.dumps(item) + '\n')

        return results

    def _get_maps_api_key(self) -> Optional[str]:
        """Get Google Maps API key from environment or .env file."""
        import os
        # Check environment first
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if api_key:
            return api_key
        # Check .env file
        env_path = Path("<hermes-home>/.env")
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GOOGLE_MAPS_API_KEY='):
                        return line.split('=', 1)[1].strip()
        return None

    def _enrich_single_item(self, venue_name: str, domain: str, api_key: str) -> Optional[Dict]:
        """Enrich a single item using Google Places API v1."""
        import urllib.request
        import urllib.parse

        # Build the Places API v1 searchText request
        url = "https://places.googleapis.com/v1/places:searchText"
        
        # Build the text query
        query = venue_name
        if domain == 'restaurant':
            query = f"{venue_name} restaurant"
        
        payload = json.dumps({
            "textQuery": query,
            "maxResultCount": 1
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': api_key,
                'X-Goog-FieldMask': 'places.name,places.placeId,places.formattedAddress,places.rating,places.priceLevel,places.types,places.editorialSummary'
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        places = data.get('places', [])
        if not places:
            return None

        place = places[0]
        enrichment = {
            "enriched": True,
            "enriched_at": datetime.now(timezone.utc).isoformat(),
            "maps_place_id": place.get('placeId'),
            "rating": place.get('rating'),
            "formatted_address": place.get('formatted_address')
        }

        if domain == 'restaurant':
            enrichment['price_level'] = self._parse_price_level(place.get('priceLevel'))
            enrichment['cuisine'] = self._extract_cuisine_from_types(place.get('types', []))
            if place.get('editorialSummary'):
                enrichment['description'] = place['editorialSummary']
        elif domain == 'travel':
            enrichment['hotel_class'] = self._extract_hotel_class_from_types(place.get('types', []))

        return enrichment

    def _parse_price_level(self, price_level_str: Optional[str]) -> Optional[int]:
        """Parse Google Places price level string to integer."""
        if not price_level_str:
            return None
        # Price levels: PRICE_LEVEL_FREE, PRICE_LEVEL_INEXPENSIVE, PRICE_LEVEL_MODERATE, PRICE_LEVEL_EXPENSIVE, PRICE_LEVEL_VERY_EXPENSIVE
        mapping = {
            'PRICE_LEVEL_FREE': 0,
            'PRICE_LEVEL_INEXPENSIVE': 1,
            'PRICE_LEVEL_MODERATE': 2,
            'PRICE_LEVEL_EXPENSIVE': 3,
            'PRICE_LEVEL_VERY_EXPENSIVE': 4
        }
        return mapping.get(price_level_str, None)

    def _extract_cuisine_from_types(self, types: List[str]) -> List[str]:
        """Extract cuisine types from Google Maps place types"""
        cuisine_keywords = ['restaurant', 'cafe', 'bar', 'bakery', 'pizza', 'sushi', 'thai', 'indian', 'chinese', 'mexican', 'italian', 'american', 'french', 'japanese', 'korean', 'vietnamese']
        return [t for t in types if any(kw in t.lower() for kw in cuisine_keywords)]

    def _extract_hotel_class_from_types(self, types: List[str]) -> Optional[int]:
        """Extract hotel class from place types"""
        if 'lodging' in types:
            return 3  # Default to 3-star
        return None

    def get_status(self) -> Dict:
        """Get current status of the taste model"""
        signals = self._read_jsonl(self.signals_file)
        items = self._read_jsonl(self.items_file)

        # Count by domain
        domain_counts = {}
        for signal in signals:
            domain = signal.get('domain', 'unknown')
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        # Count enriched items
        enriched_count = sum(1 for item in items if item.get('enriched', False))

        return {
            "total_signals": len(signals),
            "total_items": len(items),
            "enriched_items": enriched_count,
            "enrichment_pct": round(enriched_count / len(items) * 100, 1) if items else 0,
            "domain_breakdown": domain_counts,
            "last_scan": self.config.get("email_scan", {}).get("last_scan_timestamp"),
            "email_scan_enabled": self.config.get("email_scan", {}).get("enabled", False)
        }

    def data_quality_report(self) -> Dict:
        """Generate a comprehensive data quality report."""
        from collections import Counter

        signals = self._read_jsonl(self.signals_file)
        items = self._read_jsonl(self.items_file)

        # Enrichment coverage
        enriched_count = sum(1 for item in items if item.get('enriched', False))
        enrichment_pct = round(enriched_count / len(items) * 100, 1) if items else 0

        # Noise signals (generic meal keywords without named venues)
        noise_names = {'breakfast', 'lunch', 'dinner', 'brunch', 'snack', 'coffee'}
        noise_count = sum(1 for s in signals if s.get('venue_name', '').lower() in noise_names)

        # Naive datetime check
        naive_count = sum(1 for s in signals if 'created_at' in s and '+' not in s.get('created_at', '') and 'Z' not in s.get('created_at', ''))

        # Duplicate item names
        item_name_counts = Counter(i.get('venue_name', '?') for i in items)
        name_dupes = [(n, c) for n, c in item_name_counts.items() if c > 1]

        # Duplicate item IDs
        item_id_counts = Counter(i.get('item_id', '?') for i in items)
        id_dupes = [(iid, c) for iid, c in item_id_counts.items() if c > 1]

        # Top venues by signal count
        venue_counts = Counter(s.get('venue_name', '?') for s in signals)
        top_venues = venue_counts.most_common(10)

        # Signal freshness (within 180-day half-life)
        now = datetime.now(timezone.utc)
        fresh_count = 0
        for s in signals:
            created = s.get('created_at', '')
            if not created:
                continue
            try:
                # Handle both naive and aware timestamps
                if '+' in created or created.endswith('Z'):
                    ts = datetime.fromisoformat(created.replace('Z', '+00:00'))
                else:
                    ts = datetime.fromisoformat(created)
                    ts = ts.replace(tzinfo=timezone.utc)
                days_old = (now - ts).days
                if days_old <= 180:
                    fresh_count += 1
            except (ValueError, TypeError):
                pass

        freshness_pct = round(fresh_count / len(signals) * 100, 1) if signals else 0

        return {
            "signals": {
                "total": len(signals),
                "noise_count": noise_count,
                "noise_names": list(noise_names),
                "naive_timestamps": naive_count,
                "fresh_within_180d": fresh_count,
                "freshness_pct": freshness_pct,
            },
            "items": {
                "total": len(items),
                "enriched": enriched_count,
                "enrichment_pct": enrichment_pct,
                "duplicate_names": len(name_dupes),
                "duplicate_name_details": [{"name": n, "count": c} for n, c in sorted(name_dupes, key=lambda x: -x[1])[:10]],
                "duplicate_ids": len(id_dupes),
            },
            "top_venues_by_signals": [{"name": n, "count": c} for n, c in top_venues],
            "last_scan": self.config.get("email_scan", {}).get("last_scan_timestamp"),
            "recommendations": []
        }


def main():
    """CLI entry point"""
    import sys

    skill = TasteSkill()

    if len(sys.argv) < 2:
        print("Usage: taste.py <command>")
        print("Commands: scan-historical, scan-incremental, scan-calendar, enrich, status, data-quality")
        sys.exit(1)

    command = sys.argv[1]

    if command == "scan-historical":
        days_back = int(sys.argv[2]) if len(sys.argv) > 2 else 365
        result = skill.scan_email_historical(days_back)
        print(json.dumps(result, indent=2))

    elif command == "scan-incremental":
        hours_back = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        result = skill.scan_email_incremental(hours_back)
        print(json.dumps(result, indent=2))

    elif command == "scan-calendar":
        days_back = int(sys.argv[2]) if len(sys.argv) > 2 else 365
        result = skill.scan_calendar_historical(days_back)
        print(json.dumps(result, indent=2))

    elif command == "enrich":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        result = skill.enrich_items(limit)
        print(json.dumps(result, indent=2))

    elif command == "status":
        status = skill.get_status()
        print(json.dumps(status, indent=2))

    elif command == "data-quality":
        report = skill.data_quality_report()
        print(json.dumps(report, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()