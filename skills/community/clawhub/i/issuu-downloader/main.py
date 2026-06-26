import os
import re
import requests
import img2pdf
import time
from typing import Optional, Dict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class IssuuDownloader:
    def __init__(self, output_dir: str = "downloads", proxies: Optional[Dict] = None):
        self.output_dir = os.path.abspath(output_dir)
        self.session = requests.Session()
        
        # If no proxy provided, try to detect local common ports (Clash/V2Ray)
        if not proxies:
            for port in ['7890', '1080', '1087']:
                try:
                    test_proxy = {"http": f"http://127.0.0.1:{port}", "https": f"http://127.0.0.1:{port}"}
                    # Quick test to see if proxy is alive
                    requests.get("https://www.google.com", proxies=test_proxy, timeout=1)
                    self.session.proxies.update(test_proxy)
                    print(f"Auto-detected proxy on port {port}")
                    break
                except:
                    continue
        else:
            self.session.proxies.update(proxies)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        
        # Aggressive retry for 503 errors
        retry_strategy = Retry(total=5, backoff_factor=3, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        os.makedirs(self.output_dir, exist_ok=True)

    def get_document_info(self, url: str) -> Optional[Dict]:
        try:
            # Adding a small sleep to look more "human"
            time.sleep(1)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            html = response.text
            
            doc_hash = None
            patterns = [r'image\.isu\.pub/(\d+-[a-f0-9]+)/', r'"documentId":"([^"]+)"']
            for p in patterns:
                match = re.search(p, html)
                if match:
                    doc_hash = match.group(1)
                    break
            
            if not doc_hash: return None

            # Probe page count (Simplified linear probe for reliability)
            # Starting with a safer increment to avoid 503s
            last_valid = 1
            for page in [1, 10, 20, 50, 100, 200, 500]:
                test_url = f"https://image.isu.pub/{doc_hash}/jpg/page_{page}.jpg"
                if self.session.head(test_url, timeout=10).status_code == 200:
                    last_valid = page
                else:
                    break
            
            # Refine from last_valid
            final_pages = last_valid
            for p in range(last_valid, last_valid + 10):
                if self.session.head(f"https://image.isu.pub/{doc_hash}/jpg/page_{p}.jpg", timeout=5).status_code == 200:
                    final_pages = p
                else:
                    break

            return {
                'title': "issuu_document",
                'pages': final_pages,
                'url_template': f"https://image.isu.pub/{doc_hash}/jpg/page_{{}}.jpg"
            }
        except Exception as e:
            print(f"Debug: {e}")
            return None

    def download(self, url: str) -> str:
        info = self.get_document_info(url)
        if not info: raise Exception("Blocked by Issuu (503). Try switching your proxy node.")
        
        pdf_path = os.path.join(self.output_dir, "downloaded_file.pdf")
        image_contents = []
        for p in range(1, info['pages'] + 1):
            img = self.session.get(info['url_template'].format(p), timeout=20).content
            image_contents.append(img)
            print(f"Downloaded page {p}/{info['pages']}")

        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_contents))
        return pdf_path

def run_skill(url: str, proxy: str = None):
    p = {"http": proxy, "https": proxy} if proxy else None
    return IssuuDownloader(proxies=p).download(url)

