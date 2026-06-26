#!/usr/bin/env python3
"""
Gmail Link Archiver - Core Module

Connects to Gmail via IMAP, filters emails by subject prefix,
extracts links, crawls them with Playwright, converts to Markdown,
and saves to the workspace.
"""

import imaplib
import email
import re
import os
import sys
import json
import hashlib
import argparse
import subprocess
import getpass
from email.header import decode_header
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

CONFIG_DIR = os.path.expanduser("~/.config/gmail-link-archiver")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config() -> Optional[dict]:
    """Load saved config from local file. Returns None if not found."""
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def save_config(cfg: dict):
    """Save config to local file with restricted permissions."""
    os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)
    print(f"[OK] Config saved to {CONFIG_FILE}")


def interview() -> dict:
    """Interactive interview to collect IMAP credentials and settings."""
    print("=" * 60)
    print("  Gmail Link Archiver - First-Run Setup")
    print("=" * 60)
    print()
    print("This skill connects to your Gmail via IMAP to filter emails,")
    print("crawl links found in them, and save the content as Markdown.")
    print()
    print("You need a Gmail App Password (not your regular password).")
    print("Generate one at: https://myaccount.google.com/apppasswords")
    print()

    imap_server = input("IMAP server [imap.gmail.com]: ").strip() or "imap.gmail.com"
    imap_port = input("IMAP port [993]: ").strip() or "993"
    imap_user = input("Gmail address: ").strip()
    if not imap_user:
        print("[ERROR] Gmail address is required.")
        sys.exit(1)
    imap_password = getpass.getpass("App password: ").strip()
    if not imap_password:
        print("[ERROR] App password is required.")
        sys.exit(1)

    default_mailbox = input("Default mailbox [INBOX]: ").strip() or "INBOX"
    subject_prefix = input("Subject prefix to filter (e.g. '[Archive]'): ").strip()
    workspace_path = input(
        f"Workspace save path [{os.path.expanduser('~/openclaw-workspace/mail-archive')}]: "
    ).strip() or os.path.expanduser("~/openclaw-workspace/mail-archive")

    cfg = {
        "imap_server": imap_server,
        "imap_port": int(imap_port),
        "imap_user": imap_user,
        "imap_password": imap_password,
        "default_mailbox": default_mailbox,
        "subject_prefix": subject_prefix,
        "workspace_path": workspace_path,
    }
    save_config(cfg)
    return cfg


# ---------------------------------------------------------------------------
# IMAP helpers
# ---------------------------------------------------------------------------


def decode_subject(subject_raw) -> str:
    """Decode an email subject header."""
    if subject_raw is None:
        return ""
    parts = decode_header(subject_raw)
    decoded = []
    for data, charset in parts:
        if isinstance(data, bytes):
            decoded.append(data.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(data)
    return "".join(decoded)


def connect_imap(cfg: dict) -> imaplib.IMAP4_SSL:
    """Connect and authenticate to IMAP server."""
    print(f"[IMAP] Connecting to {cfg['imap_server']}:{cfg['imap_port']}...")
    mail = imaplib.IMAP4_SSL(cfg["imap_server"], cfg["imap_port"])
    mail.login(cfg["imap_user"], cfg["imap_password"])
    print("[IMAP] Authenticated successfully.")
    return mail


def fetch_filtered_emails(mail: imaplib.IMAP4_SSL, mailbox: str, subject_prefix: str) -> list:
    """
    Select mailbox and search for emails whose subject starts with the prefix.
    Returns list of dicts with 'subject', 'from', 'date', 'links'.
    """
    status, _ = mail.select(f'"{mailbox}"', readonly=True)
    if status != "OK":
        print(f"[ERROR] Cannot select mailbox '{mailbox}'")
        return []

    # IMAP SUBJECT search is substring-based, which works for prefix matching
    search_criterion = f'(SUBJECT "{subject_prefix}")'
    status, data = mail.search(None, search_criterion)
    if status != "OK":
        print("[ERROR] Search failed.")
        return []

    msg_ids = data[0].split()
    if not msg_ids:
        print(f"[INFO] No emails found with subject containing '{subject_prefix}' in '{mailbox}'.")
        return []

    print(f"[IMAP] Found {len(msg_ids)} email(s) matching prefix '{subject_prefix}'.")
    results = []

    for mid in msg_ids:
        status, msg_data = mail.fetch(mid, "(RFC822)")
        if status != "OK":
            continue
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        subject = decode_subject(msg["Subject"])

        # Verify prefix match (IMAP SUBJECT search is substring)
        if not subject.startswith(subject_prefix):
            continue

        links = extract_links_from_email(msg)
        results.append({
            "id": mid.decode(),
            "subject": subject,
            "from": msg["From"],
            "date": msg["Date"],
            "links": links,
        })
        print(f"  -> [{subject}] — {len(links)} link(s)")

    return results


def extract_links_from_email(msg) -> list:
    """Extract HTTP/HTTPS links from email body (HTML and plain text parts)."""
    links = set()
    url_pattern = re.compile(r'https?://[^\s<>"\')\]]+(?<![.,;:])')

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            try:
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                text = payload.decode("utf-8", errors="replace")
            except Exception:
                continue

            if ctype in ("text/plain", "text/html"):
                found = url_pattern.findall(text)
                links.update(found)
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                text = payload.decode("utf-8", errors="replace")
                links.update(url_pattern.findall(text))
        except Exception:
            pass

    # Filter out common tracking / unsubscribe links
    filtered = [
        l for l in links
        if not any(skip in l.lower() for skip in [
            "unsubscribe", "tracking", "click.email", "list-manage",
            "mailchimp", "googleadservices",
        ])
    ]
    return sorted(filtered)


# ---------------------------------------------------------------------------
# Playwright crawling
# ---------------------------------------------------------------------------


def ensure_playwright():
    """Ensure Playwright and Chromium are installed. Returns False on failure."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        print("[SETUP] Installing Playwright...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install Playwright: {e}")
            return False

    print("[SETUP] Installing Chromium browser...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install Chromium: {e}")
        return False

    # Install system deps for headless Chromium on Linux (best-effort)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "playwright", "install-deps", "chromium"],
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        pass  # Non-fatal: system deps may already be present

    return True


def crawl_url(url: str, timeout: int = 30000, browser=None) -> Optional[str]:
    """
    Crawl a URL using Playwright with Chromium (headless).
    If browser is provided, reuse that instance instead of launching a new one.
    Returns the page HTML content or None on failure.
    """
    from playwright.sync_api import sync_playwright

    def _crawl_with_browser(browser_instance) -> str:
        context = browser_instance.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True,
        )
        try:
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout)
            # Wait a bit for JS-rendered content
            page.wait_for_timeout(2000)
            return page.content()
        finally:
            context.close()

    try:
        if browser is not None:
            return _crawl_with_browser(browser)
        else:
            with sync_playwright() as p:
                b = p.chromium.launch(headless=True)
                try:
                    return _crawl_with_browser(b)
                finally:
                    b.close()
    except Exception as e:
        print(f"  [WARN] Failed to crawl {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# HTML to Markdown conversion
# ---------------------------------------------------------------------------


def ensure_html2text():
    """Ensure html2text is installed. Returns False on failure."""
    try:
        import html2text  # noqa: F401
        return True
    except ImportError:
        print("[SETUP] Installing html2text...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "html2text"])
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install html2text: {e}")
            return False
        return True


def html_to_markdown(html: str, url: str = "") -> str:
    """Convert HTML to Markdown using html2text."""
    import html2text

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.ignore_emphasis = False
    converter.body_width = 0  # Don't wrap lines
    converter.protect_links = True
    converter.wrap_links = False
    converter.unicode_snob = True

    md = converter.handle(html)

    # Add source URL header
    header = f"---\nsource: {url}\ncrawled_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
    return header + md.strip() + "\n"


# ---------------------------------------------------------------------------
# Workspace save
# ---------------------------------------------------------------------------


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Create a filesystem-safe filename."""
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    safe = re.sub(r'_+', '_', safe).strip("_. ")
    if len(safe) > max_len:
        safe = safe[:max_len]
    return safe


def save_markdown(md_content: str, url: str, workspace_path: str) -> str:
    """Save markdown content to workspace, return the saved file path."""
    os.makedirs(workspace_path, exist_ok=True)

    # Create filename from URL
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    url_slug = sanitize_filename(url.split("//")[-1].split("?")[0].replace("/", "_"))
    if not url_slug:
        url_slug = "page"
    filename = f"{url_slug}_{url_hash}.md"

    filepath = os.path.join(workspace_path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)

    return filepath


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def run_pipeline(
    mailbox: Optional[str] = None,
    subject_prefix: Optional[str] = None,
    workspace_path: Optional[str] = None,
    max_links: int = 50,
):
    """Run the full E2E pipeline."""
    # Load or create config
    cfg = load_config()
    if cfg is None:
        cfg = interview()
    else:
        print("[OK] Loaded credentials from config.")

    # Override with CLI args if provided
    mailbox = mailbox or cfg.get("default_mailbox", "INBOX")
    subject_prefix = subject_prefix or cfg.get("subject_prefix", "")
    workspace_path = workspace_path or cfg.get("workspace_path",
        os.path.expanduser("~/openclaw-workspace/mail-archive"))

    if not subject_prefix:
        print("[ERROR] No subject prefix specified. Use --subject-prefix or set in config.")
        sys.exit(1)

    # Ensure dependencies
    ensure_playwright()
    ensure_html2text()

    # Step 1: Connect to IMAP and fetch filtered emails
    mail = connect_imap(cfg)
    emails = fetch_filtered_emails(mail, mailbox, subject_prefix)
    mail.logout()

    if not emails:
        print("[DONE] No matching emails found. Nothing to crawl.")
        return

    # Collect all unique links
    all_links = []
    link_subjects = {}
    for em in emails:
        for link in em["links"]:
            if link not in link_subjects:
                link_subjects[link] = em["subject"]
                all_links.append(link)

    print(f"\n[PIPELINE] {len(all_links)} unique link(s) to crawl.")
    if len(all_links) > max_links:
        print(f"[PIPELINE] Limiting to first {max_links} links.")
        all_links = all_links[:max_links]

    # Step 2: Crawl each link with Playwright (single shared browser instance)
    from playwright.sync_api import sync_playwright

    saved_files = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for i, url in enumerate(all_links, 1):
                print(f"\n[{i}/{len(all_links)}] Crawling: {url}")
                html = crawl_url(url, browser=browser)
                if html is None:
                    continue

                # Step 3: Convert to Markdown
                md = html_to_markdown(html, url)
                if len(md.strip().split("\n")) < 5:
                    print(f"  [SKIP] Very little content extracted.")
                    continue

                # Step 4: Save to workspace
                filepath = save_markdown(md, url, workspace_path)
                saved_files.append(filepath)
                print(f"  [SAVED] {filepath}")
        finally:
            browser.close()

    print(f"\n{'=' * 60}")
    print(f"[DONE] Saved {len(saved_files)} Markdown file(s) to {workspace_path}")
    for f in saved_files:
        print(f"  - {f}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Gmail Link Archiver — Crawl links from filtered emails and save as Markdown"
    )
    parser.add_argument("--mailbox", "-m", help="IMAP mailbox to search (default: from config)")
    parser.add_argument("--subject-prefix", "-s", help="Subject prefix to filter")
    parser.add_argument("--workspace", "-w", help="Workspace path to save Markdown files")
    parser.add_argument("--max-links", type=int, default=50, help="Max links to crawl (default: 50)")
    parser.add_argument("--reconfigure", action="store_true", help="Re-run the setup interview")

    args = parser.parse_args()

    if args.reconfigure:
        interview()
        return

    run_pipeline(
        mailbox=args.mailbox,
        subject_prefix=args.subject_prefix,
        workspace_path=args.workspace,
        max_links=args.max_links,
    )


if __name__ == "__main__":
    main()
