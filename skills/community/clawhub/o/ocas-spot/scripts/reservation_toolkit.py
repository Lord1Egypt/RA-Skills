#!/usr/bin/env python3
"""
Free reservation booking toolkit — API-first approach.

Key insights from community tools:
- Resy: Full API available, no browser needed
- OpenTable: Must use Firefox (Chromium blocked by Akamai)
- Tock: Session pre-warming + cookie persistence for Cloudflare
- Yelp: Official Fusion API for business data

All traffic routes through VPN Gate for IP rotation.
"""

import os
import sys
import json
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

HERMES_HOME = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))
DATA_DIR = HERMES_HOME / "commons" / "data" / "ocas-spot"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ─── VPN Management ────────────────────────────────────────────────────────────

class VPNManager:
    """Manages VPN Gate connection."""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or str(DATA_DIR / "vpn_gate.ovpn")
    
    def is_connected(self) -> bool:
        for iface in ["tun0", "tun1", "tun2"]:
            r = subprocess.run(["ip", "addr", "show", iface], capture_output=True, text=True)
            if "inet" in r.stdout:
                return True
        return False
    
    def get_exit_ip(self) -> dict:
        r = subprocess.run(["curl", "-s", "--max-time", "10", "https://ipinfo.io/json"],
                          capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout)
        return {}
    
    def connect(self):
        if self.is_connected():
            return
        
        subprocess.run(["pkill", "-f", "openvpn"], capture_output=True)
        time.sleep(2)
        
        if not Path(self.config_path).exists():
            self._download_config()
        
        subprocess.run(["openvpn", "--config", self.config_path, "--daemon"], check=True)
        time.sleep(6)
        
        if not self.is_connected():
            raise RuntimeError("VPN connection failed")
        
        ip = self.get_exit_ip()
        log.info(f"VPN connected: {ip.get('ip')} ({ip.get('country')})")
    
    def disconnect(self):
        subprocess.run(["pkill", "-f", "openvpn"], capture_output=True)
        time.sleep(2)
    
    def _download_config(self):
        """Download best VPN Gate config with cipher fix."""
        subprocess.run([
            "curl", "-s", "https://www.vpngate.net/api/iphone/",
            "-o", "/tmp/vpn_list.csv"
        ], check=True)
        
        subprocess.run([
            "python3", "-c", f"""
import csv, base64
with open('/tmp/vpn_list.csv', newline='') as f:
    content = f.read()
lines = content.split('\\n')
data_lines = [l for l in lines if not l.startswith('*') and l.strip()]
reader = csv.DictReader(data_lines)
rows = list(reader)
non_us = [r for r in rows if r.get('CountryShort','').strip() != 'US' and r.get('OpenVPN_ConfigData_Base64','').strip()]
best = sorted(non_us, key=lambda s: int(s.get('Score',0)), reverse=True)[0]
config = base64.b64decode(best['OpenVPN_ConfigData_Base64']).decode()
if 'data-ciphers' not in config:
    lines2 = config.split('\\n')
    for i, line in enumerate(lines2):
        if line.startswith('cipher '):
            lines2.insert(i+1, 'data-ciphers AES-128-CBC:AES-256-GCM:AES-128-GCM')
            break
    config = '\\n'.join(lines2)
with open('{self.config_path}', 'w') as f:
    f.write(config)
print(f"Downloaded: {{best['CountryLong']}} {{best['IP']}}")
"""
        ], capture_output=True, text=True, check=True)


# ─── Resy API (no browser needed) ─────────────────────────────────────────────

class ResyAPI:
    """
    Resy booking via official API endpoints.
    Source: https://github.com/JustKong/resy-api, https://github.com/Alkaar/resy-booking-bot
    
    No browser needed — pure API calls.
    """
    
    BASE = "https://api.resy.com"
    
    def __init__(self, email: str, password: str):
        import requests
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Origin": "https://resy.com",
            "Referer": "https://resy.com/",
            "X-Origin": "https://resy.com",
        })
        self.token = None
    
    def login(self) -> bool:
        """Authenticate and get session token."""
        r = self.session.post(f"{self.BASE}/2/user/login", json={
            "email": self.email,
            "password": self.password,
        }, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            self.token = data.get("token")
            if self.token:
                self.session.headers["Authorization"] = f"Bearer {self.token}"
                self.session.headers["X-Resy-Auth-Token"] = self.token
                log.info("Resy login OK")
                return True
        
        log.error(f"Resy login failed: {r.status_code} {r.text[:200]}")
        return False
    
    def search(self, query: str, per_page: int = 10) -> list:
        """Search for restaurants."""
        r = self.session.get(f"{self.BASE}/3/venues/search", params={
            "query": query,
            "per_page": per_page,
        }, timeout=15)
        
        if r.status_code == 200:
            return r.json().get("venues", [])
        return []
    
    def get_venue(self, venue_id: int) -> dict:
        """Get venue details."""
        r = self.session.get(f"{self.BASE}/3/venue", params={
            "venue_id": venue_id,
        }, timeout=15)
        return r.json() if r.status_code == 200 else {}
    
    def find_slots(self, venue_id: int, date: str, party_size: int = 2) -> list:
        """Find available time slots."""
        r = self.session.get(f"{self.BASE}/4/find", params={
            "venue_id": venue_id,
            "datetime": date,
            "party_size": party_size,
        }, timeout=15)
        
        if r.status_code == 200:
            results = r.json()
            slots = []
            for day in results.get("results", {}).get("venues", []):
                for slot in day.get("slots", []):
                    slots.append({
                        "time": slot.get("date", {}).get("start"),
                        "token": slot.get("config", {}).get("token"),
                        "config_id": slot.get("config", {}).get("id"),
                    })
            return slots
        return []
    
    def book(self, booking_token: str) -> dict:
        """Book a reservation."""
        r = self.session.post(f"{self.BASE}/3/book", json={
            "booking_token": booking_token,
        }, timeout=15)
        
        return {
            "success": r.status_code == 200,
            "status": r.status_code,
            "response": r.json() if r.status_code == 200 else r.text,
        }


# ─── OpenTable via Firefox ────────────────────────────────────────────────────

class OpenTableFirefox:
    """
    OpenTable automation using Firefox.
    Key insight: OpenTable blocks Chromium but allows Firefox.
    Source: https://github.com/rajksarkar/reservation-agent
    """
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.pw = None
    
    def start(self):
        from playwright.sync_api import sync_playwright
        self.pw = sync_playwright().start()

        # OpenTable is among the most aggressively bot-gated targets this box
        # touches, so it uses the same shared cascade as every other browser
        # skill: obscura (anti-detect) -> firefox -> chrome -> chromium. The
        # Firefox user-agent and prefs are applied ONLY when the Firefox
        # engine is actually selected — a Firefox UA on a Chrome engine is a
        # detectable contradiction, worse than either on its own.
        # Pin an engine with BROWSER_CASCADE or OBSCURA_ENGINE.
        import os
        import sys
        _scripts = os.path.join(os.environ.get("HERMES_HOME", ""), "scripts")
        if _scripts and _scripts not in sys.path:
            sys.path.insert(0, _scripts)
        try:
            import browser_cascade
            self.browser, self.engine, _attempts = browser_cascade.launch_sync(self.pw)
            log.info(browser_cascade.describe(_attempts))
        except ImportError:
            self.engine = "firefox"
            self.browser = self.pw.firefox.launch(
                headless=True,
                firefox_user_prefs={
                    "media.peerconnection.enabled": False,
                    "general.useragent.override": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0",
                }
            )
        
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/Los_Angeles',
        )
        
        # Load saved session
        session_file = DATA_DIR / "opentable-session.json"
        if session_file.exists():
            self.context.add_cookies(json.loads(session_file.read_text()))
            log.info("Loaded OpenTable session")
    
    def login(self, email: str, password: str) -> bool:
        try:
            page = self.context.new_page()
            page.goto("https://www.opentable.com/login", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)
            
            # Save session
            cookies = self.context.cookies()
            (DATA_DIR / "opentable-session.json").write_text(json.dumps(cookies))
            
            log.info("OpenTable login OK")
            page.close()
            return True
        except Exception as e:
            log.error(f"OpenTable login failed: {e}")
            return False
    
    def check_availability(self, url: str, date: str, party_size: int = 2) -> list:
        try:
            page = self.context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            # Try to select party size and date
            try:
                page.click('[data-testid="party-size-selector"]', timeout=5000)
                page.click(f'[data-testid="party-size-{party_size}"]', timeout=3000)
            except:
                pass
            
            page.wait_for_timeout(2000)
            
            # Extract slots
            slots = page.evaluate('''() => {
                const results = [];
                document.querySelectorAll('[data-testid="time-slot"], .time-slot, [data-time]').forEach(el => {
                    const time = el.getAttribute('data-time') || el.textContent.trim();
                    const available = !el.disabled && !el.classList.contains('unavailable');
                    if (available && time) results.push({time});
                });
                return results;
            }''')
            
            page.close()
            return slots
            
        except Exception as e:
            log.error(f"OpenTable check failed: {e}")
            return []
    
    def stop(self):
        if self.context:
            cookies = self.context.cookies()
            (DATA_DIR / "opentable-session.json").write_text(json.dumps(cookies))
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()


# ─── Tock via Session Warming ─────────────────────────────────────────────────

class TockWarm:
    """
    Tock booking with Cloudflare session pre-warming.
    Key insight: navigate the page 15 min before booking to refresh CF cookies.
    Source: https://github.com/charlieyang1557/tock-reservation-bot
    """
    
    def __init__(self):
        self.browser = None
        self.context = None
        self.pw = None
    
    def start(self):
        from playwright.sync_api import sync_playwright
        self.pw = sync_playwright().start()
        
        self.browser = self.pw.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars', '--window-size=1920,1080',
                '--no-first-run', '--no-default-browser-check',
                '--disable-dev-shm-usage',
            ]
        )
        
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/Los_Angeles',
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        )
        
        self.context.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = { runtime: {} };
        ''')
        
        # Load saved session
        session_file = DATA_DIR / "tock-session.json"
        if session_file.exists():
            try:
                self.context.add_cookies(json.loads(session_file.read_text()))
                log.info("Loaded Tock session")
            except:
                pass
    
    def warm_and_login(self, email: str, password: str, restaurant_url: str) -> bool:
        """
        Warm the session: navigate to restaurant page first, then login.
        This refreshes Cloudflare cookies before the booking window.
        """
        try:
            page = self.context.new_page()
            
            # Step 1: Navigate to restaurant page to warm CF cookies
            log.info("Warming Tock session...")
            page.goto(restaurant_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000)
            
            # Check for Cloudflare challenge
            content = page.content().lower()
            if "checking your browser" in content or "cf-turnstile" in content:
                log.info("Cloudflare challenge — waiting...")
                for i in range(12):
                    time.sleep(5)
                    content = page.content().lower()
                    if "checking your browser" not in content:
                        log.info("CF challenge cleared!")
                        break
                else:
                    log.error("CF challenge not resolved")
                    return False
            
            # Step 2: Login
            page.goto("https://www.exploretock.com/login", wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000)
            
            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)
            
            # Save session
            cookies = self.context.cookies()
            (DATA_DIR / "tock-session.json").write_text(json.dumps(cookies))
            
            log.info("Tock warm + login OK")
            page.close()
            return True
            
        except Exception as e:
            log.error(f"Tock warm failed: {e}")
            return False
    
    def check_availability(self, restaurant_url: str, dates: list, party_size: int = 2) -> list:
        slots = []
        try:
            page = self.context.new_page()
            
            for date in dates:
                try:
                    page.goto(f"{restaurant_url}?date={date}", wait_until="domcontentloaded", timeout=20000)
                    page.wait_for_timeout(2000)
                    
                    day_slots = page.evaluate('''() => {
                        const results = [];
                        document.querySelectorAll('[data-testid="time-slot"], .time-slot, button[data-time], [class*="slot"]').forEach(el => {
                            const time = el.getAttribute('data-time') || el.textContent.trim();
                            const available = !el.disabled && !el.classList.contains('unavailable') && !el.classList.contains('sold-out');
                            if (available && time) results.push({time});
                        });
                        return results;
                    }''')
                    
                    for s in day_slots:
                        s["date"] = date
                        slots.append(s)
                    
                    time.sleep(1)
                except:
                    pass
            
            page.close()
        except Exception as e:
            log.error(f"Tock availability failed: {e}")
        
        return slots
    
    def stop(self):
        if self.context:
            cookies = self.context.cookies()
            (DATA_DIR / "tock-session.json").write_text(json.dumps(cookies))
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()


# ─── Yelp Fusion API ──────────────────────────────────────────────────────────

class YelpFusion:
    """
    Yelp access via official Fusion API.
    Source: https://github.com/Yelp/yelp-fusion
    
    The Fusion API provides business search, details, reviews, and availability.
    No browser needed — pure API.
    
    Get API key at: https://www.yelp.com/developers/v3/manage_app
    """
    
    BASE = "https://api.yelp.com/v3"
    
    def __init__(self, api_key: str):
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        })
    
    def search(self, term: str, location: str, limit: int = 10) -> list:
        """Search for businesses."""
        r = self.session.get(f"{self.BASE}/businesses/search", params={
            "term": term,
            "location": location,
            "limit": limit,
        }, timeout=15)
        
        if r.status_code == 200:
            return r.json().get("businesses", [])
        return []
    
    def get_business(self, business_id: str) -> dict:
        """Get business details."""
        r = self.session.get(f"{self.BASE}/businesses/{business_id}", timeout=15)
        return r.json() if r.status_code == 200 else {}
    
    def get_reviews(self, business_id: str) -> list:
        """Get business reviews."""
        r = self.session.get(f"{self.BASE}/businesses/{business_id}/reviews", timeout=15)
        return r.json().get("reviews", []) if r.status_code == 200 else []
    
    def find_reservation_businesses(self, location: str, limit: int = 20) -> list:
        """Find restaurants that accept reservations."""
        r = self.session.get(f"{self.BASE}/businesses/search", params={
            "term": "reservations",
            "location": location,
            "categories": "restaurants",
            "limit": limit,
            "attributes": "reservations",
        }, timeout=15)
        
        if r.status_code == 200:
            return r.json().get("businesses", [])
        return []


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Free reservation booking toolkit")
    sub = parser.add_subparsers(dest="command")
    
    # VPN
    vpn_p = sub.add_parser("vpn", help="Manage VPN")
    vpn_p.add_argument("action", choices=["connect", "disconnect", "status", "rotate"])
    
    # Resy
    resy_p = sub.add_parser("resy", help="Resy API operations")
    resy_p.add_argument("--email", required=True)
    resy_p.add_argument("--password", required=True)
    resy_p.add_argument("--search", help="Search query")
    resy_p.add_argument("--venue-id", type=int, help="Venue ID")
    resy_p.add_argument("--date", help="Date (YYYY-MM-DD)")
    resy_p.add_argument("--party-size", type=int, default=2)
    
    # OpenTable
    ot_p = sub.add_parser("opentable", help="OpenTable via Firefox")
    ot_p.add_argument("--email", required=True)
    ot_p.add_argument("--password", required=True)
    ot_p.add_argument("--url", help="Restaurant URL")
    ot_p.add_argument("--date", help="Date (YYYY-MM-DD)")
    
    # Tock
    tock_p = sub.add_parser("tock", help="Tock via session warming")
    tock_p.add_argument("--email", required=True)
    tock_p.add_argument("--password", required=True)
    tock_p.add_argument("--url", help="Restaurant URL")
    tock_p.add_argument("--dates", nargs="+", help="Dates to check")
    
    # Yelp
    yelp_p = sub.add_parser("yelp", help="Yelp Fusion API")
    yelp_p.add_argument("--api-key", required=True)
    yelp_p.add_argument("--search", help="Search query")
    yelp_p.add_argument("--location", help="Location")
    yelp_p.add_argument("--business-id", help="Business ID")
    
    args = parser.parse_args()
    
    if args.command == "vpn":
        vpn = VPNManager()
        if args.action == "connect":
            vpn.connect()
            print(f"Connected: {vpn.get_exit_ip()}")
        elif args.action == "disconnect":
            vpn.disconnect()
            print("Disconnected")
        elif args.action == "status":
            if vpn.is_connected():
                print(f"Connected: {vpn.get_exit_ip()}")
            else:
                print("Not connected")
        elif args.action == "rotate":
            vpn.disconnect()
            vpn.connect()
            print(f"Rotated: {vpn.get_exit_ip()}")
    
    elif args.command == "resy":
        vpn = VPNManager()
        vpn.connect()
        
        resy = ResyAPI(args.email, args.password)
        if not resy.login():
            sys.exit(1)
        
        if args.search:
            venues = resy.search(args.search)
            for v in venues:
                print(f"  {v.get('name'):40s} ID:{v.get('id')} {v.get('locality','')}")
        
        if args.venue_id and args.date:
            slots = resy.find_slots(args.venue_id, args.date, args.party_size)
            print(f"Found {len(slots)} slots:")
            for s in slots:
                print(f"  {s['time']}  token:{s.get('token','N/A')[:30]}...")
    
    elif args.command == "opentable":
        vpn = VPNManager()
        vpn.connect()
        
        ot = OpenTableFirefox()
        ot.start()
        
        if not ot.login(args.email, args.password):
            ot.stop()
            sys.exit(1)
        
        if args.url and args.date:
            slots = ot.check_availability(args.url, args.date)
            print(f"Found {len(slots)} slots:")
            for s in slots:
                print(f"  {s['time']}")
        
        ot.stop()
    
    elif args.command == "tock":
        vpn = VPNManager()
        vpn.connect()
        
        tock = TockWarm()
        tock.start()
        
        if not tock.warm_and_login(args.email, args.password, args.url or "https://www.exploretock.com"):
            tock.stop()
            sys.exit(1)
        
        if args.url and args.dates:
            slots = tock.check_availability(args.url, args.dates)
            print(f"Found {len(slots)} slots:")
            for s in slots:
                print(f"  {s['date']} {s['time']}")
        
        tock.stop()
    
    elif args.command == "yelp":
        yelp = YelpFusion(args.api_key)
        
        if args.search and args.location:
            businesses = yelp.search(args.search, args.location)
            for b in businesses:
                print(f"  {b['name']:40s} {b.get('id',''):20s} {b.get('location',{}).get('city','')}")
        
        if args.business_id:
            biz = yelp.get_business(args.business_id)
            print(json.dumps(biz, indent=2)[:2000])


if __name__ == "__main__":
    main()