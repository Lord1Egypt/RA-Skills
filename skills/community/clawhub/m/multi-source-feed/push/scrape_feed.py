import json
import os
import re
import time
import signal
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

# ============================================================
#  Configuration
# ============================================================
TARGET_POSTS_PER_TAB = 15   # Quick mode: target posts per tab
MAX_SCROLLS = 12            # Quick mode: max scroll attempts per tab
WAIT_SECONDS = 2            # Wait time (seconds) after each scroll
SCRAPE_TRENDING = False     # Quick mode: skip Trending, only scrape posts
TRENDING_TOPIC_COUNT = 0    # Quick mode: not needed

# Robustness settings
MAX_RETRIES = 2             # Page load retry count
RETRY_DELAY = 3             # Retry interval in seconds
STALE_SCROLL_LIMIT = 3      # Exit early after this many consecutive scrolls with no new posts
GLOBAL_TIMEOUT = 180         # Global timeout in seconds (3 minutes, sufficient for quick mode)


# ============================================================
#  Global timeout protection
# ============================================================
def timeout_handler(signum, frame):
    print("\n[ERROR] Global timeout! Saving existing data and exiting...")
    raise TimeoutError("Global timeout reached")

# Only set on systems that support SIGALRM (Linux/macOS)
if hasattr(signal, 'SIGALRM'):
    signal.signal(signal.SIGALRM, timeout_handler)


# ============================================================
#  Retry utility
# ============================================================
def retry(func, *args, retries=MAX_RETRIES, delay=RETRY_DELAY, desc="operation"):
    """Generic retry wrapper"""
    for attempt in range(1, retries + 1):
        try:
            return func(*args)
        except Exception as e:
            print(f"   [WARN] {desc} attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"   [WAIT] Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"   [ERROR] {desc} reached max retries ({retries})")
                raise

# ============================================================
#  Main flow
# ============================================================
def scrape_feed():
    # Start global timeout
    if hasattr(signal, 'SIGALRM'):
        signal.alarm(GLOBAL_TIMEOUT)

    # Store partial results so data is saved even on crash
    partial_result = {
        "scraped_at": datetime.now().isoformat(),
        "stats": {},
        "trending": [],
        "posts": [],
    }

    browser = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                storage_state=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "x_session.json"),
                viewport={"width": 1280, "height": 900},
            )
            page = context.new_page()
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """)

            # ---------- 1. Open home page (with retry) ----------
            print("[INFO] Opening X home page...")
            retry(
                lambda: page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000),
                retries=MAX_RETRIES, delay=RETRY_DELAY, desc="open home page"
            )
            time.sleep(6)

            # ---------- 2. Scrape For You (default tab) ----------
            print("\n[INFO] ===== Scraping For You tab =====")
            wait_for_tweets(page)
            for_you_posts = collect_posts(page, source="for_you")
            print(f"[OK] For You scraping done: {len(for_you_posts)} posts")

            # Save immediately to prevent data loss on subsequent crash
            partial_result["posts"] = for_you_posts
            save_partial(partial_result, "feed_raw_partial.json")

            # ---------- 3. Switch to Following tab ----------
            print("\n[INFO] ===== Switching to Following tab =====")
            following_posts = []
            try:
                tab = page.locator('[role="tab"]:has-text("Following")')
                tab.first.click()
                time.sleep(4)

                # Force scroll to top to avoid starting from the middle
                page.evaluate("window.scrollTo(0, 0)")
                time.sleep(2)

                # Verify tab switch: check aria-selected attribute
                try:
                    is_selected = tab.first.get_attribute("aria-selected")
                    if is_selected == "true":
                        print("   [OK] Confirmed switch to Following")
                    else:
                        print("   [WARN] Tab clicked but aria-selected is not true, switch may have failed")
                except Exception:
                    pass

                wait_for_tweets(page)
                following_posts = collect_posts(page, source="following")
                print(f"[OK] Following scraping done: {len(following_posts)} posts")
            except Exception as e:
                print(f"   [ERROR] Following scraping failed: {e}, continuing with For You data")

            # ---------- 4. Merge and deduplicate ----------
            merged = merge_posts(for_you_posts, following_posts)
            print(f"\n[INFO] Total after merge and dedup: {len(merged)} posts")
            partial_result["posts"] = merged
            save_partial(partial_result, "feed_raw_partial.json")

            # ---------- 5. Scrape Trending (optional) ----------
            trending = []
            if SCRAPE_TRENDING:
                print("\n[INFO] ===== Scraping Trending =====")
                try:
                    trending = scrape_trending(page)
                    print(f"[OK] Trending scraping done: {len(trending)} topics")
                except Exception as e:
                    print(f"   [ERROR] Trending scraping failed: {e}, skipping")

            # ---------- 6. Output ----------
            output = {
                "scraped_at": datetime.now().isoformat(),
                "stats": {
                    "for_you_raw": len(for_you_posts),
                    "following_raw": len(following_posts),
                    "merged_total": len(merged),
                    "trending_topics": len(trending),
                },
                "trending": trending,
                "posts": merged,
            }

            with open("feed_raw.json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print("\n[OK] Saved to feed_raw.json")

            browser.close()

            # Cancel global timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)

            return output

    except TimeoutError:
        print("[WARN] Global timeout triggered, saving existing data...")
        save_partial(partial_result, "feed_raw.json")
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        return partial_result

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        print("[INFO] Attempting to save existing data...")
        save_partial(partial_result, "feed_raw.json")
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        raise


def save_partial(data, filename):
    """Save partial results to file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"   [OK] Partial results saved to {filename}")
    except Exception as e:
        print(f"   [WARN] Failed to save partial results: {e}")


# ============================================================
#  Post collection (generic, supports both tabs)
# ============================================================
def collect_posts(page, source="unknown"):
    """Scroll and collect posts from the current tab"""
    all_posts = []
    seen_urls = set()      # URL-based dedup is more reliable than text-based
    seen_texts = set()     # Text-based dedup as fallback
    scroll_count = 0
    stale_count = 0        # Consecutive no-new-post scroll counter

    while len(all_posts) < TARGET_POSTS_PER_TAB and scroll_count < MAX_SCROLLS:
        scroll_count += 1
        prev_count = len(all_posts)
        print(f"   [SCROLL] #{scroll_count}, collected {len(all_posts)}/{TARGET_POSTS_PER_TAB} posts...")

        articles = page.locator("article[data-testid='tweet']")
        count = articles.count()

        for j in range(count):
            try:
                article = articles.nth(j)
                post = extract_post(article)
                if post is None:
                    continue

                # Dedup: prefer URL, fallback to text
                dedup_key = post["url"] if post["url"] else post["text"]
                if dedup_key in seen_urls or post["text"] in seen_texts:
                    continue

                post["source"] = source  # Tag the source tab
                seen_urls.add(dedup_key)
                seen_texts.add(post["text"])
                all_posts.append(post)

                if len(all_posts) >= TARGET_POSTS_PER_TAB:
                    break
            except Exception:
                continue

        if len(all_posts) >= TARGET_POSTS_PER_TAB:
            break

        # Prevent infinite loop: exit early after consecutive scrolls with no new posts
        if len(all_posts) == prev_count:
            stale_count += 1
            if stale_count >= STALE_SCROLL_LIMIT:
                print(f"   [WARN] No new posts after {STALE_SCROLL_LIMIT} consecutive scrolls, exiting early")
                break
        else:
            stale_count = 0

        page.evaluate("window.scrollBy(0, window.innerHeight * 3)")
        time.sleep(WAIT_SECONDS)

    return all_posts


# ============================================================
#  Merge posts from both tabs, deduplicate and tag dual-source
# ============================================================
def merge_posts(for_you_posts, following_posts):
    """Merge posts from both tabs; duplicates are tagged with source='both'"""
    merged = {}

    for post in for_you_posts:
        key = post["url"] if post["url"] else post["text"]
        merged[key] = post

    for post in following_posts:
        key = post["url"] if post["url"] else post["text"]
        if key in merged:
            # Same post appeared in both tabs, tag as 'both'
            merged[key]["source"] = "both"
            # Keep the higher view count (numbers may differ slightly between scrapes)
            merged[key]["views"] = max(merged[key]["views"], post["views"])
        else:
            merged[key] = post

    # Sort by views descending
    result = sorted(merged.values(), key=lambda x: x.get("views", 0), reverse=True)
    return result


# ============================================================
#  Trending scraper
# ============================================================
def scrape_trending(page):
    """Visit the Explore page and scrape trending topics"""
    trending = []
    try:
        page.goto("https://x.com/explore/tabs/trending", wait_until="domcontentloaded", timeout=20000)
        time.sleep(5)

        # Trending entries are usually in [data-testid="trend"] or cellInnerDiv
        trends = page.locator('[data-testid="trend"]')
        count = min(trends.count(), TRENDING_TOPIC_COUNT)

        for i in range(count):
            try:
                trend = trends.nth(i)
                entry = {}

                # Topic name: usually the most prominent text in the trend element
                texts = trend.locator("span").all()
                text_contents = []
                for t in texts:
                    try:
                        txt = t.inner_text(timeout=1000).strip()
                        if txt:
                            text_contents.append(txt)
                    except Exception:
                        continue

                # Try to extract the topic name (usually the longest/most prominent span)
                entry["topic"] = ""
                entry["category"] = ""
                entry["post_count"] = ""

                for txt in text_contents:
                    txt_lower = txt.lower()
                    # Category line usually contains "· Trending" or a specific category
                    if "trending" in txt_lower or "·" in txt:
                        entry["category"] = txt
                    # Post count: contains "posts"/"tweets", or standalone number format (e.g. "21K", "1,234")
                    elif ("post" in txt_lower or "tweet" in txt_lower
                          or _looks_like_count(txt)):
                        entry["post_count"] = txt
                    # Otherwise, use the longest text as the topic name
                    elif len(txt) > len(entry["topic"]):
                        entry["topic"] = txt

                if entry["topic"]:
                    trending.append(entry)
            except Exception:
                continue

    except Exception as e:
        print(f"   [WARN] Trending scraping failed: {e}")

    return trending


# ============================================================
#  Single post extraction
# ============================================================
def extract_post(article):
    post = {}

    # --- Check if this is an ad ---
    try:
        ad_indicators = article.locator('span:has-text("Ad")').all()
        for indicator in ad_indicators:
            txt = indicator.inner_text(timeout=500).strip()
            if txt == "Ad":
                return None  # Skip ads
    except Exception:
        pass

    # --- Check if this is a retweet ---
    post["is_retweet"] = False
    post["retweeted_by"] = ""
    try:
        # Retweets show "XXX reposted" social context above the post
        social_context = article.locator('[data-testid="socialContext"]')
        if social_context.count() > 0:
            context_text = social_context.inner_text(timeout=2000)
            if "reposted" in context_text.lower():
                post["is_retweet"] = True
                post["retweeted_by"] = context_text.replace(" reposted", "").strip()
    except Exception:
        pass

    # --- Author handle ---
    try:
        for link in article.locator('a[role="link"]').all():
            href = link.get_attribute("href") or ""
            if href.startswith("/") and href.count("/") == 1 and href != "/":
                post["author_handle"] = href.strip("/")
                break
    except Exception:
        post["author_handle"] = ""

    # --- Author display name ---
    try:
        post["author_name"] = article.locator('a[role="link"] span').first.inner_text(timeout=2000)
    except Exception:
        post["author_name"] = ""

    # --- Post body text ---
    try:
        text_el = article.locator("div[data-testid='tweetText']")
        post["text"] = text_el.inner_text(timeout=2000) if text_el.count() > 0 else ""
    except Exception:
        post["text"] = ""

    if not post["text"]:
        return None

    # --- Post URL and timestamp ---
    try:
        time_el = article.locator("time")
        href = time_el.locator("..").first.get_attribute("href") or ""
        post["url"] = f"https://x.com{href}" if href else ""
    except Exception:
        post["url"] = ""

    try:
        post["timestamp"] = article.locator("time").get_attribute("datetime") or ""
    except Exception:
        post["timestamp"] = ""

    # --- Engagement metrics ---
    try:
        buttons = article.locator('[role="group"] button').all()
        labels = []
        for btn in buttons:
            try:
                labels.append(btn.get_attribute("aria-label") or "")
            except Exception:
                continue
        post.update(parse_metrics(labels))
    except Exception:
        post.update({"replies": 0, "reposts": 0, "likes": 0, "bookmarks": 0})

    # --- Views (multi-strategy extraction) ---
    post["views"] = extract_views(article)

    # --- External links ---
    try:
        seen_hrefs = set()
        links = []
        for a in article.locator("a[href]").all():
            href = a.get_attribute("href") or ""
            if (href.startswith("http")
                    and "x.com" not in href
                    and "twitter.com" not in href
                    and "t.co" not in href      # Exclude t.co short links (they usually expand)
                    and href not in seen_hrefs):
                link_text = ""
                try:
                    link_text = a.inner_text(timeout=1000).strip()
                except Exception:
                    pass
                links.append({
                    "url": href,
                    "text": link_text if link_text else ""
                })
                seen_hrefs.add(href)
        post["external_links"] = links
    except Exception:
        post["external_links"] = []

    # --- Quoted tweet ---
    try:
        quoted = article.locator('[data-testid="tweet"] [data-testid="tweet"]')
        if quoted.count() > 0:
            q = quoted.first.locator("div[data-testid='tweetText']")
            post["quoted_tweet"] = q.inner_text(timeout=2000) if q.count() > 0 else ""
        else:
            post["quoted_tweet"] = ""
    except Exception:
        post["quoted_tweet"] = ""

    # --- Has media ---
    post["has_media"] = False
    try:
        media_selectors = [
            '[data-testid="tweetPhoto"]',
            '[data-testid="videoPlayer"]',
            '[data-testid="card.wrapper"]',
        ]
        for sel in media_selectors:
            if article.locator(sel).count() > 0:
                post["has_media"] = True
                break
    except Exception:
        pass

    return post


# ============================================================
#  Views extraction (multi-strategy)
# ============================================================
def extract_views(article):
    """Extract view count using multiple strategies"""

    # Strategy 1: aria-label containing "view"
    try:
        view_candidates = article.locator('a[href*="/analytics"]').all()
        for el in view_candidates:
            label = el.get_attribute("aria-label") or ""
            if "view" in label.lower():
                num = parse_number_from_text(label)
                if num > 0:
                    return num
    except Exception:
        pass

    # Strategy 2: app-text-transition-container (views counter)
    try:
        # Views are usually the last number in the group area
        group = article.locator('[role="group"]')
        if group.count() > 0:
            containers = group.locator('[data-testid="app-text-transition-container"]').all()
            if containers:
                # The last one is usually views
                last = containers[-1]
                txt = last.inner_text(timeout=1000).strip()
                num = parse_abbreviated_number(txt)
                if num > 0:
                    return num
    except Exception:
        pass

    # Strategy 3: directly find analytics link text
    try:
        analytics_links = article.locator('a[href*="/analytics"]').all()
        for link in analytics_links:
            txt = link.inner_text(timeout=1000).strip()
            if txt:
                num = parse_abbreviated_number(txt)
                if num > 0:
                    return num
    except Exception:
        pass

    return 0


# ============================================================
#  Number parsing utilities
# ============================================================
def _looks_like_count(text):
    """Check if text looks like a post count, e.g. '21K', '1,234', '50.2K'"""
    return bool(re.match(r'^[\d,.]+[KkMm]?(\+)?\s*(posts?|tweets?)?$', text.strip()))


def parse_number_from_text(text):
    """Extract a plain number from text"""
    num = "".join(c for c in text.replace(",", "") if c.isdigit())
    return int(num) if num else 0


def parse_abbreviated_number(text):
    """Parse abbreviated numbers, e.g. 1.4M, 102K, 93.5K"""
    text = text.strip().replace(",", "")
    try:
        if "M" in text.upper():
            return int(float(text.upper().replace("M", "")) * 1_000_000)
        elif "K" in text.upper():
            return int(float(text.upper().replace("K", "")) * 1_000)
        else:
            num = "".join(c for c in text if c.isdigit())
            return int(num) if num else 0
    except ValueError:
        return 0


# ============================================================
#  Engagement metrics parsing
# ============================================================
def parse_metrics(labels):
    result = {"replies": 0, "reposts": 0, "likes": 0, "bookmarks": 0}
    for label in labels:
        label_lower = label.lower()
        for key in result:
            if key.rstrip("s") in label_lower or key in label_lower:
                num = parse_number_from_text(label)
                if num:
                    result[key] = num
    return result


# ============================================================
#  Wait for tweets to load
# ============================================================
def wait_for_tweets(page):
    """Wait for tweets to finish loading"""
    print("   [WAIT] Waiting for posts to load...")
    try:
        page.wait_for_selector("article[data-testid='tweet']", timeout=15000)
        time.sleep(2)
    except Exception:
        print("   [WARN] Wait timed out, continuing anyway")


# ============================================================
#  Entry point
# ============================================================
if __name__ == "__main__":
    scrape_feed()
