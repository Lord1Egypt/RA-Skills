#!/usr/bin/env python3
"""
Pinterest Scraper with Infinite Scroll Support
Full-featured with logging, quality options, Telegram, dedup, resume
"""

import re, os, sys, json, hashlib, requests, warnings, argparse, logging
warnings.filterwarnings('ignore')
from playwright.sync_api import sync_playwright

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

URL_TYPES = {
    'board': r'pinterest\.com/([^/]+)/([^/]+)/?$',
    'user': r'pinterest\.com/([^/]+)/?$',
    'search': r'pinterest\.com/search/.*',
}

QUALITY_PATTERNS = {
    'originals': r'https://i\.pinimg\.com/originals/[^"]*\.jpg',
    '736x': r'https://i\.pinimg\.com/736x/[^"]*\.jpg',
    '474x': r'https://i\.pinimg\.com/474x/[^"]*\.jpg',
    '236x': r'https://i\.pinimg\.com/236x/[^"]*\.jpg',
}

class PinterestScraper:
    def __init__(self, url, num_scrolls=50, quality='originals', output_folder='./pinterest_output', 
                 telegram=False, token=None, chat_id=None, resume=False, dedup=True, verbose=False):
        self.url = url
        self.num_scrolls = num_scrolls
        self.quality = quality
        self.output_folder = output_folder
        self.telegram = telegram
        self.token = token
        self.chat_id = chat_id
        self.resume = resume
        self.dedup = dedup
        self.verbose = verbose
        
        # Set logging level
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        self.seen_hashes = set()
        self.downloaded_urls = set()
        self.telegram_sent = set()
        self.state_file = os.path.join(output_folder, '.scrape_state.json')
        self.log_file = os.path.join(output_folder, 'scrape.log')
        
        if self.resume and os.path.exists(self.state_file):
            self.load_state()
        os.makedirs(output_folder, exist_ok=True)
        
        # Setup file logging
        if self.verbose:
            fh = logging.FileHandler(self.log_file)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
    
    def get_url_type(self):
        for url_type, pattern in URL_TYPES.items():
            if re.search(pattern, self.url):
                return url_type
        return 'search'
    
    def save_state(self):
        state = {
            'seen_hashes': list(self.seen_hashes),
            'downloaded_urls': list(self.downloaded_urls),
            'telegram_sent': list(self.telegram_sent),
            'url': self.url,
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
    
    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            self.seen_hashes = set(state.get('seen_hashes', []))
            self.downloaded_urls = set(state.get('downloaded_urls', []))
            self.telegram_sent = set(state.get('telegram_sent', []))
            logger.info(f"Resumed: {len(self.seen_hashes)} hashes, {len(self.downloaded_urls)} URLs, {len(self.telegram_sent)} sent")
        except Exception as e:
            logger.warning(f"Could not load state: {e}")
    
    def get_image_hash(self, img_url):
        return hashlib.md5(img_url.encode()).hexdigest()
    
    def is_duplicate(self, img_url):
        if not self.dedup:
            return False
        return self.get_image_hash(img_url) in self.seen_hashes
    
    def mark_seen(self, img_url):
        if self.dedup:
            self.seen_hashes.add(self.get_image_hash(img_url))
    
    def get_quality_pattern(self):
        if self.quality == 'all':
            return '|'.join(QUALITY_PATTERNS.values())
        return QUALITY_PATTERNS.get(self.quality, QUALITY_PATTERNS['originals'])
    
    def scrape(self):
        logger.info(f"Starting scrape: {self.url}")
        logger.info(f"URL Type: {self.get_url_type()}, Scrolls: {self.num_scrolls}, Quality: {self.quality}")
        
        pattern = self.get_quality_pattern()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            try:
                page.goto(self.url, timeout=30000)
                logger.info(f"Page loaded: {self.url}")
            except Exception as e:
                logger.error(f"Failed to load page: {e}")
                return []
            
            all_images = set()
            for i in range(self.num_scrolls):
                if i % 10 == 0:
                    logger.info(f"Scroll {i}/{self.num_scrolls}...")
                try:
                    page.evaluate("window.scrollBy(0, 2000)")
                    page.wait_for_timeout(1500)
                except Exception as e:
                    logger.debug(f"Scroll error at {i}: {e}")
                
                found = re.findall(pattern, page.content())
                new_found = len(found)
                all_images.update(found)
                
                if i % 10 == 0:
                    logger.info(f"  Found: {len(all_images)} images (new: {new_found})")
                if i % 10 == 0:
                    self.save_state()
            browser.close()
            
            if self.dedup:
                filtered = [img for img in all_images if not self.is_duplicate(img)]
                logger.info(f"Dedup: {len(filtered)} new (was {len(all_images)})")
                return filtered
            return list(all_images)
    
    def convert_quality(self, img_url):
        if self.quality in ['originals', 'all']:
            return img_url
        for q in ['originals', '736x', '474x', '236x']:
            if f'/{q}/' in img_url:
                return img_url.replace(f'/{q}/', f'/{self.quality}/')
        return img_url
    
    def download_images(self, images):
        logger.info(f"Downloading {len(images)} images...")
        downloaded = 0
        failed = 0
        for i, img_url in enumerate(images):
            try:
                img_url = self.convert_quality(img_url)
                if img_url in self.downloaded_urls:
                    logger.debug(f"Skipped (already downloaded): {img_url[:50]}...")
                    continue
                filename = img_url.split("/")[-1][:60]
                r = requests.get(img_url, timeout=15, verify=False)
                if r.status_code == 200:
                    filepath = f"{self.output_folder}/{i:04d}_{self.quality}_{filename}"
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                    self.downloaded_urls.add(img_url)
                    downloaded += 1
                    if downloaded % 50 == 0:
                        logger.info(f"Progress: {downloaded}/{len(images)} downloaded")
                        self.save_state()
                else:
                    failed += 1
                    logger.debug(f"HTTP {r.status_code}: {img_url[:50]}...")
            except Exception as e:
                failed += 1
                logger.debug(f"Download error: {e}")
        
        logger.info(f"Download complete: {downloaded} success, {failed} failed")
        
        # Mark downloaded images as seen for future deduplication
        for img_url in images:
            self.mark_seen(img_url)
        
        self.save_state()
        return downloaded
    
    def send_to_telegram(self, batch_size=10):
        if not self.telegram or not self.token or not self.chat_id:
            logger.info("Telegram not configured")
            return 0
        
        all_files = sorted([f for f in os.listdir(self.output_folder) if f.endswith('.jpg')])
        new_files = [f for f in all_files if f not in self.telegram_sent]
        
        if not new_files:
            logger.info("No new images to send to Telegram")
            return 0
        
        logger.info(f"Sending {len(new_files)} new images to Telegram...")
        sent = 0
        for i in range(0, len(new_files), batch_size):
            batch = new_files[i:i+batch_size]
            media = [{"type": "photo", "media": f"attach://{f}"} for f in batch]
            file_data = {f: open(f"{self.output_folder}/{f}", 'rb') for f in batch}
            try:
                r = requests.post(f"https://api.telegram.org/bot{self.token}/sendMediaGroup",
                                data={"chat_id": self.chat_id, "media": json.dumps(media)},
                                files=file_data, timeout=60)
                if r.status_code == 200:
                    logger.info(f"Batch {i//batch_size + 1}: {len(batch)} sent")
                    for f in batch:
                        self.telegram_sent.add(f)
                    sent += len(batch)
                else:
                    logger.error(f"Telegram error {r.status_code}: {r.text[:100]}")
            except Exception as e:
                logger.error(f"Telegram error: {e}")
            finally:
                for f in file_data: file_data[f].close()
        
        self.save_state()
        logger.info(f"Telegram complete: {sent} images sent")
        return sent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True)
    parser.add_argument('-s', '--scrolls', type=int, default=50)
    parser.add_argument('-o', '--output', default='./pinterest_output')
    parser.add_argument('-q', '--quality', default='originals', choices=['originals','736x','474x','236x','all'])
    parser.add_argument('--telegram', action='store_true')
    parser.add_argument('--token')
    parser.add_argument('--chat')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--dedup', dest='dedup', action='store_true', default=True, help='Enable deduplication (default: on)')
    parser.add_argument('--no-dedup', dest='dedup', action='store_false', help='Disable deduplication')
    parser.add_argument('--telegram-only', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()
    
    if args.telegram_only:
        args.telegram = True
        args.scrolls = 0
    
    scraper = PinterestScraper(args.url, args.scrolls, args.quality, args.output,
                              args.telegram, args.token, args.chat, args.resume, args.dedup, args.verbose)
    
    if args.telegram_only:
        logger.info("Telegram-only mode")
        scraper.send_to_telegram()
    else:
        images = scraper.scrape()
        logger.info(f"Total images: {len(images)}")
        downloaded = scraper.download_images(images)
        if args.telegram and downloaded > 0:
            scraper.send_to_telegram()
    
    logger.info("Done!")

if __name__ == "__main__":
    main()
