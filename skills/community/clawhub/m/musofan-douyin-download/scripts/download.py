"""
Download Douyin video using Playwright + exported Chrome cookies.
Usage: python download.py <video_url> [output_path] [cookie_file]
"""
import sys
import os
import http.cookiejar
import requests

PROXY = 'http://127.0.0.1:7897'

def load_cookies(cookie_file):
    cookies = http.cookiejar.MozillaCookieJar(cookie_file)
    cookies.load(ignore_discard=True, ignore_expires=True)
    return [
        {'name': c.name, 'value': c.value or '', 'domain': c.domain,
         'path': c.path, 'secure': c.secure, 'expires': c.expires, 'httpOnly': False}
        for c in cookies if 'douyin.com' in c.domain or 'tiktok.com' in c.domain
    ]

def download(video_url, output_path, cookie_file):
    os.environ['HTTPS_PROXY'] = PROXY
    os.environ['HTTP_PROXY'] = PROXY

    from playwright.sync_api import sync_playwright

    pw_cookies = load_cookies(cookie_file)
    print(f"Loaded {len(pw_cookies)} Douyin cookies")

    video_url_found = [None]

    def handle_response(response):
        url = response.url
        if video_url_found[0]:
            return
        if 'douyinvod.com' in url and ('video/tos' in url or 'video/m/v' in url):
            video_url_found[0] = url
            print(f"Video URL intercepted: {url[:80]}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        )
        for c in pw_cookies:
            try:
                ctx.add_cookies([c])
            except Exception as e:
                pass

        page = ctx.new_page()
        page.on('response', handle_response)

        print(f"Loading {video_url} ...")
        page.goto(video_url, wait_until='domcontentloaded', timeout=30000)
        page.wait_for_timeout(5000)
        print(f"Page title: {page.title()}")
        browser.close()

    if not video_url_found[0]:
        print("ERROR: Could not find video URL!")
        return False

    # Download
    print("Downloading...")
    s = requests.Session()
    s.proxies = {'http': PROXY, 'https': PROXY}
    r = s.get(video_url_found[0], stream=True, timeout=120, headers={'Referer': 'https://www.douyin.com/'})
    total = int(r.headers.get('Content-Length', 0))
    print(f"Size: {total//1024//1024}MB")

    downloaded = 0
    with open(output_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=65536):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                print(f"\r  {downloaded*100//total}% ({downloaded//1024//1024}MB)", end='', flush=True)
    print(f"\nSaved: {output_path}")
    return True

if __name__ == '__main__':
    video_url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.douyin.com/video/7627894054088461611'
    output_path = sys.argv[2] if len(sys.argv) > 2 else r'C:\Users\musof\clawd\sessions\video-download\video.mp4'
    cookie_file = sys.argv[3] if len(sys.argv) > 3 else r'C:\Users\musof\clawd\sessions\cookies\cookies.txt'

    success = download(video_url, output_path, cookie_file)
    sys.exit(0 if success else 1)
