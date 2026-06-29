#!/usr/bin/env python3
"""
Cookie Bridge: Copy login session cookies from user's default Chrome to the
OpenClaw-managed browser (Edge).

Usage:
    python cookie_bridge.py --db ieee            # Bridge IEEE cookies only
    python cookie_bridge.py --db all             # Bridge all supported databases
    python cookie_bridge.py --db ieee,scopus     # Bridge specific databases
    python cookie_bridge.py --check              # Check which databases have cookies

Prerequisites:
    pip install pycryptodome pywin32
"""

import argparse
import base64
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import win32crypt
except ImportError:
    print("[ERROR] Missing pywin32. Run: pip install pywin32")
    sys.exit(1)

try:
    from Crypto.Cipher import AES
except ImportError:
    print("[ERROR] Missing pycryptodome. Run: pip install pycryptodome")
    sys.exit(1)

# ── Configuration ──────────────────────────────────────────────

CHROME_DATA = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
CHROME_COOKIES = os.path.join(CHROME_DATA, "Default", "Network", "Cookies")

EDGE_DATA = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")
EDGE_COOKIES = os.path.join(EDGE_DATA, "Default", "Network", "Cookies")

OC_DATA = os.path.expandvars(r"%USERPROFILE%\.openclaw\browser\openclaw\user-data")
OC_COOKIES = os.path.join(OC_DATA, "Default", "Network", "Cookies")

DB_DOMAINS = {
    "ieee": ["%ieeexplore.ieee.org%", "%ieee.org%"],
    "engineering_village": ["%engineeringvillage.com%", "%elsevier.com%"],
    "scopus": ["%scopus.com%", "%elsevier.com%"],
    "wos": ["%webofscience.com%", "%clarivate.com%"],
    "acm": ["%acm.org%", "%dl.acm.org%"],
    "cnki": ["%cnki.net%", "%ki.net%"],
}

# ── AES Key ────────────────────────────────────────────────────

def get_aes_key(browser_data_dir):
    """Extract the AES-256-GCM key from a Chromium browser's Local State."""
    state_path = os.path.join(browser_data_dir, "Local State")
    if not os.path.exists(state_path):
        raise FileNotFoundError(f"Local State not found at {state_path}")
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    encrypted_key_b64 = state.get("os_crypt", {}).get("encrypted_key")
    if not encrypted_key_b64:
        raise ValueError("No encrypted_key in Local State -> os_crypt")
    encrypted_key = base64.b64decode(encrypted_key_b64)
    if encrypted_key[:5] != b"DPAPI":
        raise ValueError("Unexpected encrypted_key prefix")
    encrypted_key = encrypted_key[5:]
    aes_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)
    return aes_key[1]


# ── Cookie Crypto ──────────────────────────────────────────────

def decrypt_cookie(encrypted_value, aes_key):
    """Decrypt a single Chromium v10 cookie value."""
    if not encrypted_value or len(encrypted_value) < 3:
        return ""
    if encrypted_value[:3] != b"v10":
        return encrypted_value.decode("utf-8", errors="replace")
    nonce = encrypted_value[3:15]
    ciphertext = encrypted_value[15:-16]
    tag = encrypted_value[-16:]
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    try:
        return cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8", errors="replace")
    except Exception:
        return ""


def encrypt_cookie(plaintext, aes_key):
    """Encrypt a value in Chromium v10 format."""
    nonce = os.urandom(12)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    return b"v10" + nonce + ciphertext + tag


# ── Cookie DB I/O ─────────────────────────────────────────────

def read_cookies(cookie_db_path, domains):
    """Read cookies matching domain patterns from a cookie DB."""
    if not os.path.exists(cookie_db_path):
        return []
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        shutil.copy2(cookie_db_path, tmp.name)
        tmp_path = tmp.name
    try:
        db = sqlite3.connect(f"file:{tmp_path}?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        conditions = " OR ".join(["host_key LIKE ?"] * len(domains))
        query = f"SELECT * FROM cookies WHERE {conditions}"
        rows = db.execute(query, domains).fetchall()
        db.close()
        return [dict(r) for r in rows]
    finally:
        os.unlink(tmp_path)


def write_cookies(cookie_db_path, cookies):
    """Write cookies to a cookie DB (target browser must NOT be running)."""
    if not cookies:
        return 0
    if not os.path.exists(cookie_db_path):
        raise FileNotFoundError(f"Target cookie DB not found: {cookie_db_path}")
    db = sqlite3.connect(cookie_db_path)
    try:
        count = 0
        now_us = int((time.time() + 11644473600) * 1_000_000)
        for c in cookies:
            db.execute(
                "DELETE FROM cookies WHERE host_key = ? AND name = ? AND path = ?",
                (c["host_key"], c["name"], c.get("path", "/")),
            )
            db.execute(
                """INSERT INTO cookies
                   (creation_utc, host_key, top_frame_site_key, name, value,
                    encrypted_value, path, expires_utc, is_secure, is_httponly,
                    last_access_utc, has_expires, is_persistent, priority,
                    samesite, source_scheme, source_port, last_update_utc,
                    source_type, has_cross_site_ancestor)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    c.get("creation_utc", now_us),
                    c["host_key"],
                    c.get("top_frame_site_key", ""),
                    c["name"],
                    c.get("value", ""),
                    sqlite3.Binary(c["encrypted_value"]),
                    c.get("path", "/"),
                    c.get("expires_utc", 0),
                    c.get("is_secure", 0),
                    c.get("is_httponly", 0),
                    c.get("last_access_utc", now_us),
                    c.get("has_expires", 1),
                    c.get("is_persistent", 1),
                    c.get("priority", 1),
                    c.get("samesite", -1),
                    c.get("source_scheme", 0),
                    c.get("source_port", -1),
                    c.get("last_update_utc", now_us),
                    c.get("source_type", 0),
                    c.get("has_cross_site_ancestor", 0),
                ),
            )
            count += 1
        db.commit()
        return count
    finally:
        db.close()


# ── Main Logic ─────────────────────────────────────────────────

def bridge_cookies(db_names, dry_run=False, source="chrome"):
    """Bridge cookies from user browser to OpenClaw browser."""
    src_label = "Edge" if source == "edge" else "Chrome"
    src_data = EDGE_DATA if source == "edge" else CHROME_DATA
    src_cookies_path = EDGE_COOKIES if source == "edge" else CHROME_COOKIES
    print("=" * 60)
    print(f"COOKIE BRIDGE: {src_label} -> OpenClaw browser")
    print("=" * 60)

    if not os.path.exists(src_cookies_path):
        print(f"\n[SKIP] {src_label} cookie DB not found: {src_cookies_path}")
        return False

    domains = []
    for db in db_names:
        domains.extend(DB_DOMAINS.get(db, []))
    if not domains:
        print("[ERROR] No domain patterns for specified databases")
        return False

    print(f"\n[1/4] Reading cookies from {src_label}...")
    src_cookies = read_cookies(src_cookies_path, domains)

    if not src_cookies:
        print(f"  -> No matching cookies found in {src_label}.")
        return False

    print(f"  -> Found {len(src_cookies)} cookies across {len(set(c['host_key'] for c in src_cookies))} domains")
    by_domain = {}
    for c in src_cookies:
        by_domain.setdefault(c["host_key"], []).append(c["name"])
    for host, names in sorted(by_domain.items()):
        print(f"     {host}: {', '.join(names[:5])}{'...' if len(names) > 5 else ''}")

    print(f"\n[2/4] Extracting encryption keys...")
    try:
        src_key = get_aes_key(src_data)
        print(f"  -> {src_label} AES key: OK ({len(src_key) * 8}-bit)")
    except Exception as e:
        print(f"  -> {src_label} key error: {e}")
        return False

    try:
        oc_key = get_aes_key(OC_DATA)
        print(f"  -> OpenClaw AES key: OK ({len(oc_key) * 8}-bit)")
    except Exception as e:
        print(f"  -> OpenClaw key error: {e}")
        return False

    print(f"\n[3/4] Decrypting & re-encrypting {len(src_cookies)} cookies...")
    recrypted = []
    failed = 0
    for c in src_cookies:
        plain = decrypt_cookie(c["encrypted_value"], src_key)
        if plain:
            c["value"] = plain
            c["encrypted_value"] = encrypt_cookie(plain, oc_key)
            recrypted.append(c)
        else:
            failed += 1
    print(f"  -> Success: {len(recrypted)}, Failed: {failed}")
    if not recrypted:
        return False

    print(f"\n[4/4] Writing cookies to OpenClaw browser...")
    lock_file = os.path.join(OC_DATA, "Default", "LOCK")
    if os.path.exists(lock_file):
        print("  !! OpenClaw browser appears to be RUNNING.")
        print("  -> Please close the OpenClaw browser window first, then re-run.")
        print("  -> Or use --dry-run to preview without writing.")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would write {len(recrypted)} cookies:")
        for c in recrypted:
            print(f"     {c['host_key']} | {c['name']}")
        return True

    count = write_cookies(OC_COOKIES, recrypted)
    print(f"  [OK] Written {count} cookies to OpenClaw browser profile.")
    print(f"\n[DONE] Cookies bridged from {src_label}. Start the OpenClaw browser to use them.")
    return True


def check_databases(source="chrome"):
    """Check which databases have cookies in source browser."""
    src_label = "Edge" if source == "edge" else "Chrome"
    src_cookies = EDGE_COOKIES if source == "edge" else CHROME_COOKIES
    print("=" * 60)
    print(f"CHECK: Database cookies in {src_label}")
    print("=" * 60)
    if not os.path.exists(src_cookies):
        print(f"{src_label} cookie DB not found.")
        return
    for db_name, domains in DB_DOMAINS.items():
        cookies = read_cookies(src_cookies, domains)
        if cookies:
            hosts = set(c["host_key"] for c in cookies)
            print(f"  [OK] {db_name}: {len(cookies)} cookies on {len(hosts)} domains")
            for h in sorted(hosts):
                names = [c["name"] for c in cookies if c["host_key"] == h]
                print(f"       {h}: {', '.join(names)}")
        else:
            print(f"  [--] {db_name}: no cookies")


def main():
    parser = argparse.ArgumentParser(
        description="Bridge login cookies from user browser (Chrome/Edge) to OpenClaw browser"
    )
    parser.add_argument("--db", default="all",
                        help="Database(s) to bridge: ieee, engineering_village, scopus, wos, acm, cnki, or 'all'")
    parser.add_argument("--source", default="chrome", choices=["chrome", "edge"],
                        help="Source browser (default: chrome)")
    parser.add_argument("--check", action="store_true",
                        help="Check which databases have cookies in source browser")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing")
    parser.add_argument("--list", action="store_true",
                        help="List available database targets")
    args = parser.parse_args()

    if args.list:
        print("Available database targets:")
        for name, domains in DB_DOMAINS.items():
            print(f"  {name}: {domains}")
        return

    if args.check:
        check_databases(source=args.source)
        return

    db_names = list(DB_DOMAINS.keys()) if args.db == "all" else [d.strip() for d in args.db.split(",")]
    unknown = set(db_names) - set(DB_DOMAINS.keys())
    if unknown:
        print(f"[ERROR] Unknown databases: {unknown}")
        print(f"Available: {', '.join(DB_DOMAINS.keys())}")
        sys.exit(1)

    success = bridge_cookies(db_names, args.dry_run, source=args.source)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
