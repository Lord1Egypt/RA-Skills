"""
JS Render Scraper - Playwright-based web scraper for JavaScript-rendered pages
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from bs4 import BeautifulSoup


@dataclass
class ScrapeConfig:
    """Configuration for JS render scraper"""
    url: str
    wait_for_selector: Optional[str] = None
    scroll: bool = False
    scroll_delay: int = 2000
    max_scrolls: int = 10
    click_buttons: List[str] = None
    wait_time: int = 3000
    extract_method: str = "html"  # html, text, json
    javascript_data_key: Optional[str] = None  # For extracting window.* data

    def __post_init__(self):
        if self.click_buttons is None:
            self.click_buttons = []


@dataclass
class ScrapeResult:
    """Result of scraping operation"""
    url: str
    timestamp: str
    status: str
    title: Optional[str] = None
    content: Optional[str] = None
    links: List[Dict[str, str]] = None
    images: List[str] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.links is None:
            self.links = []
        if self.images is None:
            self.images = []

    def to_dict(self) -> dict:
        return asdict(self)


class JSRenderScraper:
    """Scraper for JavaScript-rendered pages using Playwright"""

    def __init__(self, headless: bool = True, viewport: tuple = (1920, 1080)):
        self.headless = headless
        self.viewport = {"width": viewport[0], "height": viewport[1]}
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    def __enter__(self):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("playwright is not installed. Run: pip install playwright && playwright install")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(viewport=self.viewport)
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()

    def scrape(self, config: ScrapeConfig) -> ScrapeResult:
        """Execute scraping with given configuration"""
        result = ScrapeResult(
            url=config.url,
            timestamp=datetime.now().isoformat(),
            status="pending"
        )

        try:
            # Navigate to page
            self.page.goto(config.url, wait_until="networkidle")

            # Initial wait for JS execution
            self.page.wait_for_timeout(config.wait_time)

            # Handle scroll loading
            if config.scroll:
                self._handle_scroll_loading(config)

            # Handle button clicks
            for button_selector in config.click_buttons:
                self._safe_click(button_selector)

            # Wait for target element
            if config.wait_for_selector:
                self.page.wait_for_selector(config.wait_for_selector, timeout=10000)

            # Extract content based on method
            content = self._extract_content(config)

            # Parse and structure the content
            parsed = self._parse_html(content)

            result.status = "success"
            result.title = parsed["title"]
            result.content = parsed["content"]
            result.links = parsed["links"]
            result.images = parsed["images"]

        except Exception as e:
            result.status = "error"
            result.error = str(e)

        return result

    def _handle_scroll_loading(self, config: ScrapeConfig):
        """Handle infinite scroll pages"""
        last_height = 0

        for _ in range(config.max_scrolls):
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(config.scroll_delay)

            new_height = self.page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _safe_click(self, selector: str):
        """Safely click an element, ignoring if not found"""
        try:
            self.page.click(selector)
            self.page.wait_for_timeout(1000)
        except Exception:
            pass

    def _extract_content(self, config: ScrapeConfig) -> str:
        """Extract content based on configured method"""
        if config.javascript_data_key:
            # Extract JavaScript global data
            return self.page.evaluate(
                f"() => JSON.stringify(window.{config.javascript_data_key} || null)"
            )
        elif config.extract_method == "json":
            # Try to find JSON data in page
            return self.page.evaluate("() => { const scripts = document.querySelectorAll('script'); for (const s of scripts) { try { return s.textContent; } catch(e) {} } return ''; }")
        else:
            # Extract from DOM
            element = self.page.query_selector(config.wait_for_selector or "body")
            if config.extract_method == "text":
                return element.inner_text()
            return element.inner_html()

    def _parse_html(self, html_content: str) -> dict:
        """Parse HTML content into structured data"""
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        return {
            "title": soup.find("title").text if soup.find("title") else "",
            "content": soup.get_text(separator="\n", strip=True),
            "links": [
                {"text": a.text.strip(), "href": a.get("href", "")}
                for a in soup.find_all("a", href=True) if a.get("href")
            ],
            "images": [
                img.get("src") or img.get("data-src")
                for img in soup.find_all("img")
                if img.get("src") or img.get("data-src")
            ]
        }

    def save_result(self, result: ScrapeResult, filepath: str):
        """Save result to JSON file"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)


def scrape_infinite_scroll(url: str, item_selector: str, max_scrolls: int = 10) -> List[dict]:
    """Scrape items from infinite scroll page"""
    items = []

    with JSRenderScraper() as scraper:
        scraper.page.goto(url, wait_until="networkidle")
        scraper.page.wait_for_timeout(2000)

        last_count = 0

        for _ in range(max_scrolls):
            scraper.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            scraper.page.wait_for_timeout(2000)

            current_items = scraper.page.query_selector_all(item_selector)
            current_count = len(current_items)

            if current_count == last_count:
                break
            last_count = current_count

        for item in current_items:
            items.append({
                "text": item.inner_text().strip(),
                "html": item.inner_html()
            })

    return items


def scrape_with_login(url: str, login_config: dict, username: str, password: str) -> str:
    """Scrape page requiring login"""
    with JSRenderScraper() as scraper:
        # Navigate to login page
        scraper.page.goto(login_config["login_url"], wait_until="networkidle")

        # Fill credentials
        scraper.page.fill(login_config["username_input"], username)
        scraper.page.fill(login_config["password_input"], password)
        scraper.page.click(login_config["submit_button"])
        scraper.page.wait_for_load_state("networkidle")

        # Navigate to target page
        scraper.page.goto(url, wait_until="networkidle")

        return scraper.page.content()


def scrape_shadow_dom(url: str, shadow_host_selector: str) -> str:
    """Scrape content from Shadow DOM"""
    with JSRenderScraper() as scraper:
        scraper.page.goto(url, wait_until="networkidle")

        content = scraper.page.evaluate("""
            (selector) => {
                const host = document.querySelector(selector);
                if (!host || !host.shadowRoot) return '';
                return host.shadowRoot.innerHTML;
            }
        """, shadow_host_selector)

    return content


# Example usage
if __name__ == "__main__":
    # Example 1: Basic scraping
    config = ScrapeConfig(
        url="https://example.com",
        wait_for_selector=".content",
        wait_time=5000,
        scroll=True
    )

    with JSRenderScraper() as scraper:
        result = scraper.scrape(config)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

    # Example 2: Infinite scroll
    # items = scrape_infinite_scroll("https://example.com/feed", ".post-item", max_scrolls=20)
    # print(f"Found {len(items)} items")

    # Example 3: With login
    # content = scrape_with_login(
    #     "https://example.com/protected",
    #     {
    #         "login_url": "https://example.com/login",
    #         "username_input": "#username",
    #         "password_input": "#password",
    #         "submit_button": "button[type='submit']"
    #     },
    #     "user@example.com",
    #     "password123"
    # )
