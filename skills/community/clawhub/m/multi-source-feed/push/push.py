"""X Push — scrape + dedup, write new posts to new_posts.json for the cron agent to filter and push."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ============================================================
#  Configuration
# ============================================================
PUSH_DIR = Path(__file__).parent
FEED_RAW = PUSH_DIR / "feed_raw.json"
SEEN_FILE = PUSH_DIR / "seen_posts.json"
NEW_POSTS_FILE = PUSH_DIR / "new_posts.json"
SEEN_TTL_HOURS = 24

# ============================================================
#  Seen posts management
# ============================================================
def load_seen() -> set[str]:
    if not SEEN_FILE.exists():
        return set()
    data = json.loads(SEEN_FILE.read_text())
    cutoff = datetime.now(timezone.utc) - timedelta(hours=SEEN_TTL_HOURS)
    return {
        e["url"]
        for e in data.get("seen", [])
        if e.get("url") and datetime.fromisoformat(e["ts"]) > cutoff
    }

def save_seen(new_urls: set[str]) -> None:
    existing = []
    if SEEN_FILE.exists():
        data = json.loads(SEEN_FILE.read_text())
        cutoff = datetime.now(timezone.utc) - timedelta(hours=SEEN_TTL_HOURS)
        existing = [
            e for e in data.get("seen", [])
            if datetime.fromisoformat(e["ts"]) > cutoff
        ]
    existing_urls = {e["url"] for e in existing}
    now_iso = datetime.now(timezone.utc).isoformat()
    for url in new_urls:
        if url and url not in existing_urls:
            existing.append({"url": url, "ts": now_iso})
    SEEN_FILE.write_text(json.dumps({"seen": existing}, ensure_ascii=False, indent=2))

# ============================================================
#  Run scraper
# ============================================================
def run_scraper() -> bool:
    print("🕷️  Running scraper (quick mode)...")
    try:
        proc = subprocess.Popen(
            [sys.executable, str(PUSH_DIR / "scrape_feed.py")],
            cwd=str(PUSH_DIR),
            start_new_session=True,  # own process group for clean kill
        )
        retcode = proc.wait(timeout=200)
        if retcode == 0:
            print("✅ Scraper done")
            return True
        print(f"⚠️  Scraper exited {retcode}")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Scraper timed out, killing process group...")
        import os, signal as _sig
        try:
            os.killpg(proc.pid, _sig.SIGTERM)
            proc.wait(timeout=5)
        except Exception:
            os.killpg(proc.pid, _sig.SIGKILL)
        return False
    except Exception as e:
        print(f"⚠️  Scraper error: {e}")
        return False

# ============================================================
#  Main flow
# ============================================================
def main():
    # 1. Scrape
    if not run_scraper():
        print("❌ Scraper failed, aborting")
        sys.exit(1)

    # 2. Load posts
    if not FEED_RAW.exists():
        print("ℹ️  feed_raw.json not found")
        sys.exit(0)

    data = json.loads(FEED_RAW.read_text())
    posts = data.get("posts", [])
    print(f"📦 Loaded {len(posts)} posts")

    # 3. Dedup
    seen = load_seen()
    new_posts = [p for p in posts if p.get("url", "") not in seen]
    print(f"🆕 {len(new_posts)} new posts after dedup")

    # 4. Update seen (record all scraped posts to avoid repeats next run)
    all_urls = {p.get("url", "") for p in posts if p.get("url")}
    save_seen(all_urls)

    # 5. Slim down fields before writing (reduce agent token usage)
    KEEP_FIELDS = {"author_handle", "text", "url", "views", "external_links", "is_retweet", "retweeted_by", "timestamp"}
    slim_posts = [{k: v for k, v in p.items() if k in KEEP_FIELDS} for p in new_posts]
    NEW_POSTS_FILE.write_text(
        json.dumps({"scraped_at": data.get("scraped_at", ""), "posts": slim_posts}, ensure_ascii=False, indent=2)
    )

    if not new_posts:
        print("✅ No new posts, agent will stay silent")
    else:
        print(f"✅ Wrote {len(new_posts)} new posts to new_posts.json")

if __name__ == "__main__":
    main()
