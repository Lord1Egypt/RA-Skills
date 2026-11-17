#!/usr/bin/env python3
"""
Instagram Downloader v2.2 — Sessionid + Apify media downloader
================================================================
Downloads all media (reels MP4, carousel JPG, photo JPG) from an
Instagram profile. Supports three operation modes:

  1. Sessionid (instagrapi, recommended) — Full access via Instagram
     session cookie. No date cutoff. Full carousel extraction.
     Requires browser login once (via --setup or manual cookie).
     → Flags: --sessionid STR | --setup

  2. Apify (no login) — Uses Apify Actor dataset as source.
     GQL enhancement for recent carousels (<4 weeks).
     → Flags: --dataset ID --api-token KEY | --toon-file PATH

  3. Setup wizard — Opens Playwright-controlled browser, detects
     sessionid cookie automatically, saves to config.
     → Flag: --setup

For carousels:
  - Sessionid mode: always extracts ALL images
  - Apify mode: tries GQL first (~3w), falls back to single thumbnail
  - Setup mode: walks user through login → captures sessionid

⚠ NOTE: --login mode is BROKEN. Meta deprecated the underlying login
  endpoint server-side (404). Use --setup or --sessionid instead.
  The --login, --password, and --totp flags exist but do NOT work.

Usage:
  # Mode 1: Sessionid (from config file, after --setup)
  python instagram_downloader.py -u username --output ./downloads

  # Mode 1: Sessionid (direct flag)
  python instagram_downloader.py -u username --sessionid "1234..."
      --output ./downloads

  # Mode 2: Sessionid (direct flag)
  python instagram_downloader.py -u username --sessionid "1234..."
      --output ./downloads

  # Mode 2: Sessionid (from config, no flag needed)
  python instagram_downloader.py -u username --output ./downloads

  # Mode 3: Apify dataset (with API token)
  python instagram_downloader.py \\
      --dataset <DATASET_ID> --api-token apify_api_xxx \\
      -u username --date-start YYYY-MM-DD --date-end YYYY-MM-DD \\
      --output ./downloads

  # Mode 3: Apify toon-file (no token)
  python instagram_downloader.py \\
      --toon-file ./data.txt \\
      -u username --type reel --own-only \\
      --output ./reels_only

  # Mode 4: Setup wizard (first time)
  python instagram_downloader.py --setup
"""
import os, sys, re, json, argparse, getpass
from datetime import datetime, timezone, date
from urllib.parse import urlparse
from pathlib import Path
import time, sqlite3, shutil
import subprocess

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)

# ── Optional: instagrapi for carousel full extraction ──────────
try:
    from instagrapi import Client as InstaClient
    from instagrapi.exceptions import ClientError, LoginRequired
    HAS_INSTAGRAPI = True
except ImportError:
    HAS_INSTAGRAPI = False

# ── UTF-8 output ──────────────────────────────────────────────
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ── Constants ─────────────────────────────────────────────────
VERSION = "2.2.0"
CONFIG_DIR = Path.home() / ".ig-downloader"
CONFIG_FILE = CONFIG_DIR / "config.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
APIFY_API_BASE = "https://api.apify.com/v2"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)
INSTA_HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.instagram.com/",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "image",
}


# ═══════════════════════════════════════════════════════════════
#  CHROME COOKIE HELPER
# ═══════════════════════════════════════════════════════════════

def _get_chrome_key():
    """Retrieve Chrome's AES-GCM decryption key via DPAPI."""
    try:
        import win32crypt  # pywin32
    except ImportError:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            import win32crypt
        except ImportError:
            # Fallback: try system DPAPI
            pass
    try:
        from win32crypt import CryptUnprotectData
    except ImportError:
        return None

    local_state = Path(os.environ['LOCALAPPDATA']) / (
        "Google/Chrome/User Data/Local State"
    )
    if not local_state.exists():
        return None
    try:
        data = json.loads(local_state.read_text(encoding='utf-8'))
        encrypted_key = data.get('os_crypt', {}).get('encrypted_key')
        if not encrypted_key:
            return None
        encrypted_key = bytes(encrypted_key, 'utf-8') if isinstance(encrypted_key, str) else encrypted_key
        encrypted_key = encrypted_key.removeprefix(b'DPAPI')
        key, _ = CryptUnprotectData(encrypted_key, None, None, None, 0)
        return key
    except Exception:
        return None


def _decrypt_cookie(encrypted_val, key):
    """Decrypt AES-GCM encrypted cookie value."""
    if not encrypted_val or not key:
        return None
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        nonce = encrypted_val[3:15]
        ciphertext = encrypted_val[15:]
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
    except ImportError:
        return None
    except Exception:
        return None


def get_chrome_cookie(domain_like='instagram', name='sessionid'):
    """Extract a cookie from Chrome's SQLite database."""
    key = _get_chrome_key()
    if not key:
        return None

    profiles = [
        Path(os.environ['LOCALAPPDATA']) / "Google/Chrome/User Data/Default",
        Path(os.environ['LOCALAPPDATA']) / "Google/Chrome/User Data/Profile 1",
    ]
    for profile in profiles:
        db_path = profile / "Network/Cookies"
        if not db_path.exists():
            continue
        tmp = db_path.parent / f"Cookies_copy_{int(time.time())}.tmp"
        try:
            shutil.copy2(str(db_path), str(tmp))
            conn = sqlite3.connect(str(tmp))
            c = conn.cursor()
            c.execute(
                "SELECT encrypted_value FROM cookies "
                "WHERE host_key LIKE ? AND name=?",
                (f'%{domain_like}%', name)
            )
            row = c.fetchone()
            conn.close()
            os.unlink(str(tmp))
            if row:
                val = _decrypt_cookie(row[0], key)
                if val:
                    return val
        except Exception:
            try:
                os.unlink(str(tmp))
            except Exception:
                pass
    return None


# ═══════════════════════════════════════════════════════════════
#  CONFIG MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def load_config():
    """Load saved sessionid from config file."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {}


def save_config(data):
    """Save sessionid to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f"  [OK] Config saved to: {CONFIG_FILE}")


def resolve_sessionid(args):
    """Resolve sessionid from all sources:
    Priority: --sessionid flag > SESSIONID env var > config file > Chrome cookies
    """
    if args.sessionid:
        return args.sessionid, "CLI flag"
    env = os.environ.get('SESSIONID')
    if env:
        return env, "env var SESSIONID"
    cfg = load_config()
    if cfg.get('sessionid'):
        return cfg['sessionid'], f"config file"
    if args.setup:
        return None, "setup mode"
    sid = get_chrome_cookie()
    if sid:
        return sid, "Chrome cookies"
    return None, None


# ═══════════════════════════════════════════════════════════════
#  INTERACTIVE SETUP (Playwright + legacy Chrome + manual fallback)
# ═══════════════════════════════════════════════════════════════

def try_playwright_setup(args, timeout=300):
    """Capture sessionid via Playwright (no Chrome profile dependency).
    Launches a clean Chromium, waits for user login, extracts sessionid cookie."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  Playwright not installed. Install with:")
        print("      pip install playwright && playwright install chromium")
        print("  Falling back to Chrome extraction...")
        return None

    print("  Launching browser (Chromium)...")
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=DEFAULT_USER_AGENT,
            )
            page = context.new_page()
            page.goto("https://www.instagram.com/accounts/login/",
                      wait_until="domcontentloaded")

            start = time.time()
            poll_interval = 2
            while time.time() - start < timeout:
                cookies = context.cookies()
                for c in cookies:
                    if c["name"] == "sessionid" and c.get("value"):
                        elapsed = int(time.time() - start)
                        browser.close()
                        print(f"  [OK] sessionid detected! ({len(c['value'])} chars, {elapsed}s)")
                        return c["value"]
                time.sleep(poll_interval)
                elapsed = int(time.time() - start)
                if elapsed % 10 == 0 and elapsed > 0:
                    remaining = timeout - elapsed
                    print(f"  Waiting... ({remaining}s remaining)")

            browser.close()
            print(f"  Timeout: no login detected in {timeout//60} minutes.")
            return None
    except Exception as e:
        print(f"  Playwright error: {e}")
        return None


def try_manual_paste():
    """Ask user to paste sessionid cookie manually."""
    print("\n  Alternative: Paste your sessionid cookie manually.")
    print("  (Get it from Chrome DevTools → Application → Cookies → www.instagram.com)")
    val = input("  sessionid: ").strip()
    return val if val else None


def interactive_setup(args):
    """Interactive login setup. Tries Playwright first, then Chrome extraction,
    then manual paste. Saves sessionid to config on success."""
    print()
    print("=" * 55)
    print("  Instagram Login Setup")
    print("=" * 55)

    sid = try_playwright_setup(args)

    if not sid:
        print("\n  Trying Chrome cookie extraction (legacy)...")
        sid = get_chrome_cookie()

    if not sid:
        sid = try_manual_paste()

    if sid:
        save_config({'sessionid': sid})
        if args.username:
            return sid
        print("  Setup complete. Re-run with --username to download.")
        return None

    print("  ERROR: Could not obtain sessionid.")
    return None


# ═══════════════════════════════════════════════════════════════
#  INSTAGRAPI HELPER (legacy GQL, no login)
# ═══════════════════════════════════════════════════════════════

class InstagrapiHelper:
    """Lazy wrapper around instagrapi for GQL carousel extraction + CDN download."""

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = InstaClient()
        return self._client

    def is_available(self) -> bool:
        return HAS_INSTAGRAPI

    def get_carousel_images(self, shortcode: str, timeout_s: int = 20) -> list[str] | None:
        """Fetch all carousel image URLs via instagrapi GQL (no login).
        Returns a list of fbcdn.net URLs, or None on failure."""
        if not self.is_available():
            return None
        try:
            import signal
            signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError))
            signal.alarm(timeout_s)
        except (AttributeError, ValueError):
            pass  # not POSIX or Windows

        try:
            pk = self.client.media_pk_from_code(shortcode)
            info = self.client.media_info_gql(pk)

            if info.media_type == 8 and hasattr(info, "resources") and info.resources:
                # Carousel: extract all image URLs
                images = []
                for r in info.resources:
                    url = str(r.thumbnail_url) if r.thumbnail_url else None
                    if url:
                        images.append(url)
                return images if images else None

            # Not a carousel or no resources — might be a single photo
            if info.thumbnail_url:
                return [str(info.thumbnail_url)]

            return None

        except Exception:
            return None
        finally:
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass

    def download_url(self, url: str, filepath: str) -> bool:
        """Download a CDN URL using instagrapi's browser-like HTTP session.
        Required for fbcdn.net URLs which block requests.get()."""
        if not self.is_available():
            return False
        try:
            resp = self.client.public.get(url, timeout=60, stream=True)
            if resp.status_code == 200:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
        except Exception:
            pass
        return False


# ═══════════════════════════════════════════════════════════════
#  LOGIN MODE (instagrapi full auth)
# ═══════════════════════════════════════════════════════════════

def challenge_code_handler(username, choice):
    """Prompt user for challenge code (SMS/email verification)."""
    print(f"\n  Instagram requires verification for @{username}.")
    print(f"  A code was sent via {choice.name}.")
    code = input("  Enter verification code: ").strip()
    return code


def load_or_login_client(args) -> tuple:
    """Get an authenticated instagrapi Client.
    
    Priority:
      1. Saved settings.json (from previous --login)
      2. --sessionid flag
      3. --login flag (full login)
    
    Returns (client, auth_method) or (None, reason) on failure.
    """
    if not HAS_INSTAGRAPI:
        return None, "instagrapi not installed"

    client = InstaClient()
    client.delay_range = [1, 3]  # polite delay

    # ── Priority 1: Saved settings ──
    if not args.login and SETTINGS_FILE.exists():
        try:
            loaded = client.load_settings(str(SETTINGS_FILE))
            client.login_by_sessionid(loaded.get("sessionid", ""))
            return client, "saved settings"
        except Exception:
            client = InstaClient()
            client.delay_range = [1, 3]

    # ── Priority 2: Sessionid from any source ──
    if not args.login:
        sid, src = resolve_sessionid(args)
        if sid:
            try:
                client.login_by_sessionid(sid)
                return client, f"sessionid ({src})"
            except Exception:
                client = InstaClient()
                client.delay_range = [1, 3]

    # ── Priority 3: Full login ──
    if args.login:
        username = args.username
        if not username:
            username = input("  Instagram username: ").strip()
            if not username:
                return None, "no username provided"

        password = args.password
        if not password:
            password = getpass.getpass(f"  Password for @{username}: ")

        verification_code = args.totp or ""

        print(f"  Logging in as @{username}...")
        try:
            client.challenge_code_handler = challenge_code_handler
            logged_in = client.login(
                username=username,
                password=password,
                verification_code=verification_code,
            )
            if logged_in:
                # Save full session for future use
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                client.dump_settings(str(SETTINGS_FILE))
                print(f"  [OK] Session saved to {SETTINGS_FILE}")
                return client, "login"
            return None, "login returned false"
        except Exception as e:
            return None, f"login failed: {e}"

    return None, "no auth method available"


def instagrapi_medias_to_items(medias: list) -> list[dict]:
    """Convert instagrapi Media objects to normalized item dicts."""
    items = []
    for m in medias:
        item = {
            "shortcode": m.code,
            "type": {1: "photo", 2: "reel", 8: "carousel"}.get(m.media_type, "unknown"),
            "created_at": m.taken_at,
            "created_at_str": m.taken_at.isoformat() if m.taken_at else "",
            "author_handle": m.user.username if m.user else "unknown",
            "video_url": getattr(m, "video_url", None),
            "thumbnail_url": getattr(m, "thumbnail_url", None),
            "raw": m,
        }
        items.append(item)
    return items


def download_from_session(client, username: str, args) -> dict:
    """Download all media from an Instagram user via authenticated session."""
    print(f"\n  Fetching media for @{username}...")
    try:
        user_id = client.user_id_from_username(username)
    except Exception as e:
        print(f"  ERROR: Cannot resolve @{username}: {e}")
        return {"ok": 0, "skip": 0, "fail": 0, "total": 0}

    # If the user wants their OWN posts, we can get them from user_medias
    # If the user wants a DIFFERENT profile, user_medias still works (public)
    try:
        medias = client.user_medias(user_id, amount=0)  # 0 = all
    except Exception as e:
        print(f"  ERROR fetching media for @{username}: {e}")
        return {"ok": 0, "skip": 0, "fail": 0, "total": 0}

    if not medias:
        print(f"  No posts found for @{username}.")
        return {"ok": 0, "skip": 0, "fail": 0, "total": 0}

    print(f"  {len(medias)} posts fetched\n")

    # Convert to standard format, then use existing processing pipeline
    items = instagrapi_medias_to_items(medias)

    # We set profile = username so OWN/MENTION classification works
    args.profile = args.profile or username

    # Process via existing pipeline (instagrapi helper disabled to avoid GQL overlap)
    return process_items(items, args, insta_helper=None)


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

def build_parser():
    p = argparse.ArgumentParser(
        description="Download Instagram media via Apify dataset + optional instagrapi enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input sources (mutually exclusive)
    src = p.add_argument_group("Input Sources (choose one)")
    src.add_argument("--dataset", metavar="ID",
        help="Apify dataset ID (e.g. DATASET_ID). Requires --api-token.")
    src.add_argument("--api-token", metavar="KEY",
        help="Apify API token (required with --dataset).")
    src.add_argument("--toon-file", metavar="PATH",
        help="Path to a toon/YAML file from MCP get-dataset-items output.")

    # Filters
    flt = p.add_argument_group("Filters")
    flt.add_argument("--profile", metavar="HANDLE", default=None,
        help="Target Instagram handle. Used to classify OWN vs MENTION.")
    flt.add_argument("--date-start", metavar="YYYY-MM-DD", default=None,
        help="Earliest post date (inclusive).")
    flt.add_argument("--date-end", metavar="YYYY-MM-DD", default=None,
        help="Latest post date (inclusive).")
    flt.add_argument("--type", metavar="T", choices=["reel","carousel","photo","all"],
        default="all", help="Filter by post type (default: all).")
    flt.add_argument("--own-only", action="store_true",
        help="Download only posts authored by --profile (exclude mentions).")
    flt.add_argument("--mentions-only", action="store_true",
        help="Download only mentions from other accounts.")

    # Output
    out = p.add_argument_group("Output")
    out.add_argument("--output", "-o", metavar="DIR", default="instagram_downloads",
        help="Output directory (default: ./instagram_downloads).")
    out.add_argument("--flat", action="store_true",
        help="Flatten: single folder instead of YYYY-MM-DD/shortcode/.")

    # Instagrapi control
    p.add_argument("--no-instagrapi", action="store_true",
        help="Skip instagrapi carousel enhancement (use Apify thumbnails only).")

    # Misc
    p.add_argument("--no-verify", action="store_true",
        help="Skip SSL verification (not recommended).")

    # Login / Session modes
    p.add_argument("--login", action="store_true",
        help="Full login mode: username/password (handles 2FA, challenges).")
    p.add_argument("--password", metavar="PASS",
        help="Instagram password (for --login). Omits to prompt securely.")
    p.add_argument("--totp", metavar="CODE",
        help="2FA verification code (for --login with two-factor auth).")
    p.add_argument("--sessionid", metavar="COOKIE",
        help="Instagram sessionid cookie (bypasses Apify).")
    p.add_argument("--setup", action="store_true",
        help="Interactive login: open browser, save sessionid to config.")
    p.add_argument("-u", "--username", metavar="HANDLE",
        help="Target Instagram username.")
    p.add_argument("--version", action="version",
        version=f"ig-downloader v{VERSION}",
        help="Show version and exit.")

    return p


# ═══════════════════════════════════════════════════════════════
#  DATA FETCHING
# ═══════════════════════════════════════════════════════════════

def fetch_from_api(dataset_id: str, api_token: str) -> list[dict]:
    """Fetch dataset items from Apify API directly."""
    url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
    resp = requests.get(url, params={"token": api_token}, timeout=120)
    resp.raise_for_status()
    return resp.json()


def fetch_from_toon(filepath: str) -> list[dict]:
    """Parse the toon/YAML-like format produced by MCP get-dataset-items."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    items_raw = re.split(r"\n  - ", content)
    items = []

    for item_str in items_raw:
        item = {}
        for line in item_str.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                line = line[2:]
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value in ("null", "~", ""):
                value = None

            if "." in key:
                parts = key.split(".")
                if parts[0] not in item or not isinstance(item[parts[0]], dict):
                    item[parts[0]] = {}
                item[parts[0]][parts[1]] = value
            else:
                item[key] = value

        if item.get("shortcode"):
            items.append(item)

    return items


# ═══════════════════════════════════════════════════════════════
#  DATA NORMALISATION
# ═══════════════════════════════════════════════════════════════

def normalize_item(raw: dict) -> dict:
    """Normalise a raw item (from API JSON or parsed toon) into consistent form."""
    author_handle = raw.get("author_handle")
    if not author_handle and isinstance(raw.get("author"), dict):
        author_handle = raw["author"].get("handle")

    video_url = raw.get("video_url_no_watermark")
    if not video_url and isinstance(raw.get("video"), dict):
        video_url = raw["video"].get("url_no_watermark")

    created_at_str = raw.get("created_at", "")
    created_at = None
    if created_at_str:
        try:
            created_at = datetime.fromisoformat(
                created_at_str.replace("Z", "+00:00")
            )
        except (ValueError, TypeError):
            pass

    return {
        "shortcode": raw.get("shortcode", ""),
        "type": raw.get("type", "unknown"),
        "created_at": created_at,
        "created_at_str": created_at_str,
        "author_handle": author_handle or "unknown",
        "video_url": video_url,
        "thumbnail_url": raw.get("thumbnail_url"),
        "raw": raw,
    }


# ═══════════════════════════════════════════════════════════════
#  DOWNLOAD
# ═══════════════════════════════════════════════════════════════

def download_file(url: str, filepath: str, *,
                  verify: bool = True,
                  insta_helper: InstagrapiHelper | None = None,
                  max_retries: int = 3) -> bool:
    """Download a file with retries. Uses instagrapi for fbcdn.net URLs when available."""
    for attempt in range(1, max_retries + 1):
        try:
            # ── Try instagrapi first (handles fbcdn.net 403s) ──
            if insta_helper and insta_helper.is_available():
                if insta_helper.download_url(url, filepath):
                    size_kb = os.path.getsize(filepath) / 1024
                    print(f"  [OK] {os.path.basename(filepath)} ({size_kb:.1f} KB)")
                    return True

            # ── Fallback: plain requests ──
            resp = requests.get(url, headers={
                "User-Agent": DEFAULT_USER_AGENT,
                "Accept": "*/*",
                "Referer": "https://www.instagram.com/",
            }, timeout=60, stream=True, verify=verify)

            if resp.status_code == 200:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                size_kb = os.path.getsize(filepath) / 1024
                print(f"  [OK] {os.path.basename(filepath)} ({size_kb:.1f} KB)")
                return True
            else:
                print(f"  [HTTP {resp.status_code}] {urlparse(url).path[-40:]}")

        except requests.RequestException as e:
            if attempt < max_retries:
                print(f"  [RETRY {attempt}/{max_retries}] {e}")
            else:
                print(f"  [FAIL] {e}")
    return False


# ═══════════════════════════════════════════════════════════════
#  PROCESSING
# ═══════════════════════════════════════════════════════════════

def process_items(items: list[dict], args: argparse.Namespace,
                  insta_helper: InstagrapiHelper | None = None):
    """Apply filters and download media for matching items."""

    # ── Parse date range ──
    dt_start = dt_end = None
    if args.date_start:
        dt_start = datetime.combine(
            date.fromisoformat(args.date_start),
            datetime.min.time(), tzinfo=timezone.utc)
    if args.date_end:
        dt_end = datetime.combine(
            date.fromisoformat(args.date_end),
            datetime.max.time(), tzinfo=timezone.utc)

    # ── Normalise ──
    normed = [normalize_item(it) for it in items]

    # ── Filter ──
    filtered = []
    skipped_no_date = 0
    for item in normed:
        if not item["created_at"]:
            skipped_no_date += 1
            continue
        if dt_start and item["created_at"] < dt_start:
            continue
        if dt_end and item["created_at"] > dt_end:
            continue
        if args.type != "all" and item["type"] != args.type:
            continue
        if args.own_only and item["author_handle"] != args.profile:
            continue
        if args.mentions_only and item["author_handle"] == args.profile:
            continue
        filtered.append(item)

    if skipped_no_date:
        print(f"  ⚠ {skipped_no_date} items skipped (no valid date)\n")
    print(f"  {len(filtered)} posts match filters (out of {len(normed)} total)\n")

    # ── Stats ──
    stats = {"reel": 0, "carousel": 0, "photo": 0, "unknown": 0}
    dl_ok = 0
    dl_fail = 0
    dl_skip = 0
    gql_hits = 0
    gql_misses = 0

    for idx, item in enumerate(filtered):
        post_type = item["type"]
        shortcode = item["shortcode"]
        author = item["author_handle"]
        is_own = author == args.profile
        tag = "OWN" if is_own else "MENTION"

        stats[post_type] = stats.get(post_type, 0) + 1

        # ── Output path ──
        date_str = item["created_at"].strftime("%Y-%m-%d") if item["created_at"] else "no-date"
        if args.flat:
            post_dir = os.path.join(args.output)
        else:
            post_dir = os.path.join(args.output, date_str, shortcode)

        os.makedirs(post_dir, exist_ok=True)

        print(f"\n{idx+1}. {date_str} | {post_type.upper():8s} | {tag} | @{author} | {shortcode}")

        # ── Save post info ──
        info_path = os.path.join(post_dir, "post_info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"shortcode: {shortcode}\n")
            f.write(f"type: {post_type}\n")
            f.write(f"date: {item['created_at_str']}\n")
            f.write(f"author: {author}\n")
            if args.profile:
                f.write(f"relation: {'own_post' if is_own else 'mention'}\n")
            f.write(f"url: https://www.instagram.com/p/{shortcode}/\n")
            if item["video_url"]:
                f.write(f"video_url: {item['video_url']}\n")
            if item["thumbnail_url"]:
                f.write(f"thumbnail_url: {item['thumbnail_url']}\n")

        # ── Download media ──

        # REEL
        if post_type == "reel" and item["video_url"]:
            filepath = os.path.join(post_dir, f"{shortcode}.mp4")
            if os.path.isfile(filepath) and os.path.getsize(filepath) > 10000:
                print(f"  [SKIP] {shortcode}.mp4 exists")
                dl_skip += 1
            elif download_file(item["video_url"], filepath,
                               verify=not args.no_verify,
                               insta_helper=insta_helper):
                dl_ok += 1
            else:
                dl_fail += 1

            # Thumbnail for reels
            if item["thumbnail_url"]:
                thumb_path = os.path.join(post_dir, f"{shortcode}_thumb.jpg")
                if not (os.path.isfile(thumb_path) and os.path.getsize(thumb_path) > 1000):
                    download_file(item["thumbnail_url"], thumb_path,
                                  verify=not args.no_verify,
                                  insta_helper=insta_helper)

        # CAROUSEL — try instagrapi for all images
        elif post_type == "carousel":
            use_gql = (not args.no_instagrapi and insta_helper is not None
                       and insta_helper.is_available())
            carousel_urls = None

            if use_gql:
                carousel_urls = insta_helper.get_carousel_images(shortcode)
                if carousel_urls:
                    gql_hits += 1
                    print(f"  [GQL] {len(carousel_urls)} images from instagrapi")
                else:
                    gql_misses += 1
                    print(f"  [GQL] not available (too old?) — using Apify thumbnail")

            if carousel_urls:
                # GQL success: download ALL carousel images
                for i, url in enumerate(carousel_urls, 1):
                    filepath = os.path.join(post_dir, f"{shortcode}_{i:02d}.jpg")
                    if os.path.isfile(filepath) and os.path.getsize(filepath) > 1000:
                        print(f"  [SKIP] {shortcode}_{i:02d}.jpg exists")
                        dl_skip += 1
                    elif download_file(url, filepath,
                                       verify=not args.no_verify,
                                       insta_helper=insta_helper):
                        dl_ok += 1
                    else:
                        dl_fail += 1
            else:
                # Fallback: Apify thumbnail (first image only)
                if item["thumbnail_url"]:
                    filepath = os.path.join(post_dir, f"{shortcode}_01.jpg")
                    if os.path.isfile(filepath) and os.path.getsize(filepath) > 1000:
                        print(f"  [SKIP] {shortcode}_01.jpg exists")
                        dl_skip += 1
                    elif download_file(item["thumbnail_url"], filepath,
                                       verify=not args.no_verify,
                                       insta_helper=insta_helper):
                        dl_ok += 1
                    else:
                        dl_fail += 1
                else:
                    print(f"  [SKIP] No thumbnail URL for carousel")
                    dl_skip += 1

        # PHOTO
        elif post_type == "photo" and item["thumbnail_url"]:
            filepath = os.path.join(post_dir, f"{shortcode}_01.jpg")
            if os.path.isfile(filepath) and os.path.getsize(filepath) > 1000:
                print(f"  [SKIP] {shortcode}_01.jpg exists")
                dl_skip += 1
            elif download_file(item["thumbnail_url"], filepath,
                               verify=not args.no_verify,
                               insta_helper=insta_helper):
                dl_ok += 1
            else:
                dl_fail += 1

        else:
            print(f"  [SKIP] No downloadable media for type={post_type}")
            dl_skip += 1

    # ── Summary ──
    print("\n" + "=" * 55)
    print(" DOWNLOAD SUMMARY")
    print(f"  Total matched:     {len(filtered)}")
    for t in ("reel", "carousel", "photo", "unknown"):
        if stats.get(t, 0):
            print(f"  {t.capitalize():12s} {stats[t]}")
    if gql_hits or gql_misses:
        print(f"")
        print(f"  GQL carousel hits:  {gql_hits}")
        print(f"  GQL carousel misses: {gql_misses}")
    print(f"  Downloaded:        {dl_ok}")
    print(f"  Already existed:   {dl_skip}")
    print(f"  Failed:            {dl_fail}")
    print(f"  Output folder:     {os.path.abspath(args.output)}")
    print("=" * 55)

    return {"ok": dl_ok, "skip": dl_skip, "fail": dl_fail, "total": len(filtered)}


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = build_parser()
    args = parser.parse_args()

    # ── Detect operation mode ──
    use_login = args.login
    use_api = bool(args.dataset)
    use_toon = bool(args.toon_file)
    use_setup = args.setup

    has_sessionid = bool(args.sessionid) or bool(os.environ.get("SESSIONID"))
    if not has_sessionid:
        cfg = load_config()
        has_sessionid = bool(cfg.get("sessionid"))
    has_saved_settings = SETTINGS_FILE.exists()

    # Determine which mode we're in
    if use_setup:
        # ── Mode S: Interactive setup ──
        sid = interactive_setup(args)
        if sid and args.username:
            # Got sessionid and have username: continue to session mode
            use_login = False
            args.sessionid = sid
            has_sessionid = True
        elif sid:
            print("\n  Setup complete. Re-run with --username to download.")
            return
        else:
            sys.exit(1)

    session_mode = has_saved_settings or has_sessionid or use_login

    if session_mode:
        # ── Mode 1/2: Session or Login ──
        if not args.username:
            print("ERROR: --username is required for login/session mode.")
            print("  python instagram_downloader.py --login -u cripterhack")
            sys.exit(1)

        client, method = load_or_login_client(args)
        if client is None:
            print(f"ERROR: Cannot authenticate: {method}")
            if not HAS_INSTAGRAPI:
                print("  Install instagrapi: pip install instagrapi")
            sys.exit(1)

        print(f"\n  ✅ Authenticated via {method}")
        result = download_from_session(client, args.username, args)

    elif use_api or use_toon:
        # ── Mode 3: Apify (legacy) ──
        if use_api and use_toon:
            print("ERROR: Use --dataset OR --toon-file, not both.")
            sys.exit(1)
        if use_api and not args.api_token:
            print("ERROR: --dataset requires --api-token.")
            sys.exit(1)
        if use_toon and not os.path.isfile(args.toon_file):
            print(f"ERROR: Toon file not found: {args.toon_file}")
            sys.exit(1)

        # Own-only / mentions-only validation
        if args.own_only and args.mentions_only:
            print("ERROR: Cannot use --own-only and --mentions-only together.")
            sys.exit(1)
        if (args.own_only or args.mentions_only) and not args.profile:
            print("ERROR: --own-only / --mentions-only requires --profile.")
            sys.exit(1)

        # Instagrapi helper for GQL carousel enhancement
        insta_helper = None
        if not args.no_instagrapi and HAS_INSTAGRAPI:
            insta_helper = InstagrapiHelper()
            print("✓ instagrapi available — carousel multi-image extraction enabled")
        elif args.no_instagrapi:
            print("  --no-instagrapi: using Apify thumbnails only for carousels")
        else:
            print("  instagrapi not installed. Install with: pip install instagrapi")
            print("  Carousel posts use Apify thumbnails (first image only).\n")

        # Fetch data
        print("\nFetching data...")
        try:
            if use_api:
                print(f"  Mode: Apify API → dataset {args.dataset}")
                raw_items = fetch_from_api(args.dataset, args.api_token)
            else:
                print(f"  Mode: Toon file → {args.toon_file}")
                raw_items = fetch_from_toon(args.toon_file)
        except Exception as e:
            print(f"ERROR fetching data: {e}")
            sys.exit(1)

        if not raw_items:
            print("ERROR: No items found in data source.")
            sys.exit(1)

        print(f"  {len(raw_items)} raw items loaded\n")
        result = process_items(raw_items, args, insta_helper)

    else:
        print("ERROR: No input source specified.")
        print("  Use --login, --sessionid, --dataset, --toon-file, or --setup.")
        print("  Run --help for detailed usage.")
        sys.exit(1)

    # ── Exit code ──
    if result and result.get("fail", 0) > 0:
        sys.exit(2)


if __name__ == "__main__":
    main()
