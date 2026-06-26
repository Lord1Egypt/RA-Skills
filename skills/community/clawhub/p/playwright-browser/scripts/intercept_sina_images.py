#!/usr/bin/env python3
"""
Intercept all requests on sina.com.cn and save all images to Desktop/sina/
"""

import asyncio
import os
import re
import hashlib
from urllib.parse import urlparse, unquote
from playwright.async_api import async_playwright


# Target directory
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "sina")

# Track saved files to avoid duplicates
saved_urls = set()
file_counter = 0


def get_filename_from_url(url, content_type=""):
    """Extract a meaningful filename from URL"""
    global file_counter
    file_counter += 1
    
    parsed = urlparse(url)
    path = unquote(parsed.path)
    basename = os.path.basename(path)
    
    # Clean up the filename
    basename = re.sub(r'[<>:"/\\|?*]', '_', basename)
    
    # If no extension, guess from content-type
    if '.' not in basename or len(basename) > 100:
        ext_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg',
            'image/x-icon': '.ico',
            'image/bmp': '.bmp',
            'image/avif': '.avif',
        }
        ext = ext_map.get(content_type, '.jpg')
        # Use hash of URL for unique name
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        basename = f"img_{file_counter:04d}_{url_hash}{ext}"
    else:
        # Prepend counter for ordering
        name, ext = os.path.splitext(basename)
        if len(name) > 60:
            name = name[:60]
        basename = f"{file_counter:04d}_{name}{ext}"
    
    return basename


async def main():
    # Create save directory
    os.makedirs(SAVE_DIR, exist_ok=True)
    print(f"[*] Save directory: {SAVE_DIR}")
    
    print("[*] Launching Chrome (non-headless)...")
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,
        slow_mo=50,
        channel="chrome",
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
        ]
    )
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = await context.new_page()

    # Stats
    stats = {
        "total_requests": 0,
        "image_requests": 0,
        "saved": 0,
        "failed": 0,
        "skipped_duplicate": 0,
        "total_bytes": 0,
    }

    async def on_response(response):
        """Intercept every response and save images"""
        stats["total_requests"] += 1
        
        try:
            url = response.url
            resource_type = response.request.resource_type
            content_type = response.headers.get('content-type', '')
            
            # Check if this is an image
            is_image = (
                resource_type == 'image' or
                content_type.startswith('image/') or
                any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico', '.bmp', '.avif'])
            )
            
            if not is_image:
                return
            
            stats["image_requests"] += 1
            
            # Skip duplicates
            if url in saved_urls:
                stats["skipped_duplicate"] += 1
                return
            saved_urls.add(url)
            
            # Skip tiny tracking pixels and data URIs
            if url.startswith('data:'):
                return
            
            # Get image binary data
            body = await response.body()
            
            if not body or len(body) < 100:  # Skip very small files (likely tracking pixels)
                return
            
            # Generate filename and save
            filename = get_filename_from_url(url, content_type)
            filepath = os.path.join(SAVE_DIR, filename)
            
            with open(filepath, 'wb') as f:
                f.write(body)
            
            size_kb = len(body) / 1024
            stats["saved"] += 1
            stats["total_bytes"] += len(body)
            
            print(f"  [SAVED] {stats['saved']:3d} | {size_kb:7.1f} KB | {filename}")
            
        except Exception as e:
            stats["failed"] += 1
            # Silently skip errors (some responses may not have body)

    page.on("response", on_response)

    # Navigate to sina.com.cn
    print("\n[*] Navigating to https://www.sina.com.cn ...")
    await page.goto("https://www.sina.com.cn", wait_until="domcontentloaded", timeout=30000)
    print("[*] Page loaded. Waiting for images...")
    await asyncio.sleep(3)

    # Scroll down to trigger lazy-loaded images
    print("\n[*] Scrolling page to load lazy images...")
    viewport_height = await page.evaluate("window.innerHeight")
    total_height = await page.evaluate("document.body.scrollHeight")
    
    scroll_pos = 0
    scroll_step = viewport_height
    scroll_count = 0
    max_scrolls = 15  # Limit scrolling
    
    while scroll_pos < total_height and scroll_count < max_scrolls:
        scroll_pos += scroll_step
        await page.evaluate(f'window.scrollTo({{top: {scroll_pos}, behavior: "smooth"}})')
        await asyncio.sleep(1.5)  # Wait for images to load
        scroll_count += 1
        # Re-check total height (may increase as content loads)
        total_height = await page.evaluate("document.body.scrollHeight")
        print(f"  [SCROLL] {scroll_count}/{max_scrolls} | position: {scroll_pos}/{total_height}")

    # Wait a bit more for any remaining images
    print("\n[*] Waiting for remaining images to load...")
    await asyncio.sleep(3)

    # Also extract images from <img> src that might not have triggered network requests
    print("\n[*] Checking for inline/cached images...")
    img_srcs = await page.evaluate('''
        () => {
            return Array.from(document.querySelectorAll('img'))
                .map(img => img.src || img.dataset.src || '')
                .filter(src => src && src.startsWith('http'));
        }
    ''')
    
    # Print final stats
    total_mb = stats["total_bytes"] / (1024 * 1024)
    print(f"\n{'='*60}")
    print(f"  RESULT SUMMARY")
    print(f"{'='*60}")
    print(f"  Total requests intercepted : {stats['total_requests']}")
    print(f"  Image requests detected    : {stats['image_requests']}")
    print(f"  Images saved               : {stats['saved']}")
    print(f"  Duplicates skipped         : {stats['skipped_duplicate']}")
    print(f"  Failed                     : {stats['failed']}")
    print(f"  Total size                 : {total_mb:.2f} MB")
    print(f"  Save location              : {SAVE_DIR}")
    print(f"{'='*60}")

    # List saved files
    saved_files = sorted(os.listdir(SAVE_DIR))
    print(f"\n  Files saved ({len(saved_files)}):")
    for f in saved_files[:20]:
        fpath = os.path.join(SAVE_DIR, f)
        fsize = os.path.getsize(fpath) / 1024
        print(f"    {f} ({fsize:.1f} KB)")
    if len(saved_files) > 20:
        print(f"    ... and {len(saved_files) - 20} more files")

    # Keep browser open briefly
    print("\n[*] Browser will stay open for 10 seconds...")
    await asyncio.sleep(10)

    await browser.close()
    await pw.stop()
    print("[*] Done. Browser closed.")


if __name__ == "__main__":
    asyncio.run(main())
