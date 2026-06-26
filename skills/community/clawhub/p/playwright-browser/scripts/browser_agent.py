#!/usr/bin/env python3
"""
Playwright Browser Agent for OpenClaw
Provides non-headless browser automation with network response hooking
"""

import asyncio
import json
import re
import time
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from playwright.async_api import async_playwright, Page, Browser, Response, Locator


@dataclass
class NetworkResponse:
    """Represents a captured network response"""
    url: str
    status: int
    headers: Dict[str, str]
    body: Any
    resource_type: str
    timestamp: float
    
    def to_dict(self):
        return {
            "url": self.url,
            "status": self.status,
            "body": self.body if isinstance(self.body, (dict, list, str, int, float, bool, type(None))) else str(self.body),
            "resource_type": self.resource_type,
            "timestamp": self.timestamp
        }


class BrowserAgent:
    """
    A browser agent that can:
    - Launch non-headless browser
    - Navigate to URLs
    - Extract page content
    - Hook and capture network responses
    - Interact with page elements
    - Search and find content
    """
    
    def __init__(self, headless: bool = False, slow_mo: int = 50):
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.response_handlers: List[Callable] = []
        self.captured_responses: List[NetworkResponse] = []
        self.context = None
        
    async def _init(self):
        """Initialize browser instance"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            channel="chrome",
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0'
        )
        self.page = await self.context.new_page()
        
        # Enable response interception
        self.page.on("response", self._handle_response)
        
    async def _handle_response(self, response: Response):
        """Internal handler for all network responses"""
        try:
            # Get response details
            url = response.url
            status = response.status
            headers = dict(response.headers)
            resource_type = response.request.resource_type
            
            # Try to get body for API responses
            body = None
            if resource_type in ['xhr', 'fetch', 'document']:
                try:
                    content_type = headers.get('content-type', '')
                    if 'application/json' in content_type:
                        body = await response.json()
                    else:
                        body = await response.text()
                except Exception:
                    body = None
            
            network_response = NetworkResponse(
                url=url,
                status=status,
                headers=headers,
                body=body,
                resource_type=resource_type,
                timestamp=time.time()
            )
            
            self.captured_responses.append(network_response)
            
            # Call user-registered handlers
            for handler in self.response_handlers:
                try:
                    handler(network_response)
                except Exception as e:
                    print(f"Handler error: {e}")
                    
        except Exception as e:
            print(f"Response handling error: {e}")
    
    def hook_network_responses(self, handler: Callable[[NetworkResponse], None]):
        """
        Register a callback for network responses
        
        Args:
            handler: Function that receives NetworkResponse objects
        """
        self.response_handlers.append(handler)
        
    def filter_responses(
        self, 
        url_pattern: Optional[str] = None,
        resource_type: Optional[str] = None,
        status_code: Optional[int] = None
    ) -> List[NetworkResponse]:
        """
        Filter captured responses based on criteria
        
        Args:
            url_pattern: Regex pattern to match URL
            resource_type: Filter by resource type (xhr, fetch, document, etc.)
            status_code: Filter by HTTP status code
            
        Returns:
            List of matching NetworkResponse objects
        """
        results = self.captured_responses.copy()
        
        if url_pattern:
            regex = re.compile(url_pattern, re.IGNORECASE)
            results = [r for r in results if regex.search(r.url)]
            
        if resource_type:
            results = [r for r in results if r.resource_type == resource_type]
            
        if status_code:
            results = [r for r in results if r.status == status_code]
            
        return results
    
    async def navigate(self, url: str, wait_until: str = "networkidle"):
        """
        Navigate to a URL
        
        Args:
            url: Target URL
            wait_until: When to consider navigation complete
                       (load, domcontentloaded, networkidle)
        """
        if not self.browser:
            await self._init()
            
        await self.page.goto(url, wait_until=wait_until)
        await asyncio.sleep(1)  # Additional wait for dynamic content
        
    async def get_page_content(self, url: str) -> Dict[str, Any]:
        """
        Get rendered page content
        
        Args:
            url: Target URL
            
        Returns:
            Dict containing title, text content, and metadata
        """
        await self.navigate(url)
        
        # Extract content
        title = await self.page.title()
        
        # Get text content (visible text only)
        text_content = await self.page.evaluate('''
            () => {
                // Remove script and style elements
                const scripts = document.querySelectorAll('script, style, nav, footer');
                scripts.forEach(el => el.remove());
                
                // Get main content or body
                const main = document.querySelector('main, article, [role="main"]');
                const content = main ? main.innerText : document.body.innerText;
                
                return {
                    title: document.title,
                    url: window.location.href,
                    text: content.trim(),
                    links: Array.from(document.querySelectorAll('a[href]'))
                        .map(a => ({text: a.innerText.trim(), href: a.href}))
                        .filter(l => l.text && l.href.startsWith('http')),
                    meta: {
                        description: document.querySelector('meta[name="description"]')?.content || '',
                        keywords: document.querySelector('meta[name="keywords"]')?.content || '',
                    }
                };
            }
        ''')
        
        return {
            "requested_url": url,
            "title": title,
            **text_content
        }
    
    async def find_element_by_text(self, text: str, exact: bool = False) -> Optional[Locator]:
        """
        Find element containing specific text
        
        Args:
            text: Text to search for
            exact: Whether to match exactly
            
        Returns:
            Playwright Locator if found, None otherwise
        """
        if exact:
            locator = self.page.locator(f"text={text}")
        else:
            # Case-insensitive contains search
            locator = self.page.locator(f"text={text}")
        
        count = await locator.count()
        if count > 0:
            return locator.first
        return None
    
    async def find_elements_by_text(self, text: str) -> List[Locator]:
        """Find all elements containing specific text"""
        locator = self.page.get_by_text(text)
        count = await locator.count()
        return [locator.nth(i) for i in range(count)]
    
    async def find_links_by_text(self, text_pattern: str) -> List[Dict]:
        """
        Find all links matching text pattern
        
        Args:
            text_pattern: Text to search for in links
            
        Returns:
            List of dicts with text and href
        """
        links = await self.page.evaluate(f'''
            () => {{
                const pattern = "{text_pattern}".toLowerCase();
                return Array.from(document.querySelectorAll('a'))
                    .filter(a => a.innerText.toLowerCase().includes(pattern))
                    .map(a => ({{
                        text: a.innerText.trim(),
                        href: a.href,
                        selector: Array.from(a.classList).map(c => '.' + c).join('') || 
                                  (a.id ? '#' + a.id : '') ||
                                  a.tagName.toLowerCase()
                    }}));
            }}
        ''')
        return links
    
    async def find_link_and_click(self, text_pattern: str):
        """
        Find a link by text and click it
        
        Args:
            text_pattern: Text pattern to search for
        """
        links = await self.find_links_by_text(text_pattern)
        if links:
            link = links[0]
            print(f"Found link: {link['text']} -> {link['href']}")
            await self.page.goto(link['href'])
            await self.page.wait_for_load_state("networkidle")
            return True
        return False
    
    async def search_page_content(self, keyword: str) -> List[Dict]:
        """
        Search for keyword in page content and return matching elements
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching elements with text and position info
        """
        results = await self.page.evaluate(f'''
            () => {{
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                const matches = [];
                const keyword = "{keyword}";
                let node;
                
                while (node = walker.nextNode()) {{
                    if (node.textContent.toLowerCase().includes(keyword.toLowerCase())) {{
                        const element = node.parentElement;
                        const rect = element.getBoundingClientRect();
                        matches.push({{
                            text: node.textContent.trim(),
                            tagName: element.tagName,
                            className: element.className,
                            id: element.id,
                            href: element.href || null,
                            position: {{
                                top: rect.top,
                                left: rect.left,
                                width: rect.width,
                                height: rect.height
                            }}
                        }});
                    }}
                }}
                
                return matches.slice(0, 20);  // Limit results
            }}
        ''')
        return results
    
    async def focus_on_element(self, element_info: Dict):
        """
        Focus on and highlight an element
        
        Args:
            element_info: Dict with element information
        """
        # Scroll to element
        if element_info.get('position'):
            pos = element_info['position']
            await self.page.evaluate(f'''
                window.scrollTo({{top: {pos['top']} - 200, behavior: 'smooth'}});
            ''')
            await asyncio.sleep(0.5)
        
        # Highlight the element
        if element_info.get('id'):
            await self.page.evaluate(f'''
                const el = document.getElementById("{element_info['id']}");
                if (el) {{
                    el.style.outline = "4px solid red";
                    el.style.outlineOffset = "2px";
                    el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                }}
            ''')
        elif element_info.get('className'):
            classes = element_info['className'].split()[0] if element_info['className'] else ''
            if classes:
                await self.page.evaluate(f'''
                    const els = document.querySelectorAll(".{classes}");
                    for (let el of els) {{
                        if (el.innerText.includes("{element_info['text'][:30]}")) {{
                            el.style.outline = "4px solid red";
                            el.style.outlineOffset = "2px";
                            el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                            break;
                        }}
                    }}
                ''')
    
    async def click_by_text(self, text: str, exact: bool = False):
        """Click element by text content"""
        if exact:
            locator = self.page.get_by_text(text, exact=True)
        else:
            locator = self.page.get_by_text(text)
        await locator.click()
        await asyncio.sleep(0.5)
    
    async def scroll_page(self, times: int = 3):
        """Scroll page to load lazy content"""
        for _ in range(times):
            await self.page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(0.5)
    
    async def wait_for_selector(self, selector: str, timeout: int = 5000):
        """Wait for an element to appear"""
        await self.page.wait_for_selector(selector, timeout=timeout)
        
    async def click(self, selector: str):
        """Click on an element"""
        await self.page.click(selector)
        await asyncio.sleep(0.5)
        
    async def fill_form(self, selector: str, value: str):
        """Fill a form field"""
        await self.page.fill(selector, value)
        
    async def screenshot(self, path: str, full_page: bool = True):
        """Take a screenshot"""
        await self.page.screenshot(path=path, full_page=full_page)
        
    async def close(self):
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    def get_captured_api_calls(self) -> List[Dict]:
        """Get all captured XHR/Fetch API calls with JSON responses"""
        return [
            {
                "url": r.url,
                "status": r.status,
                "body": r.body
            }
            for r in self.captured_responses
            if r.resource_type in ['xhr', 'fetch'] and r.body is not None
        ]
    
    async def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url


# Synchronous wrapper for easier use
class SyncBrowserAgent:
    """Synchronous wrapper for BrowserAgent"""
    
    def __init__(self, headless: bool = False):
        self._agent = BrowserAgent(headless=headless)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        
    def _run(self, coro):
        return self._loop.run_until_complete(coro)
        
    def get_page_content(self, url: str) -> Dict[str, Any]:
        return self._run(self._agent.get_page_content(url))
        
    def navigate(self, url: str):
        return self._run(self._agent.navigate(url))
        
    def hook_network_responses(self, handler: Callable):
        self._agent.hook_network_responses(handler)
        
    def filter_responses(self, **kwargs) -> List[NetworkResponse]:
        return self._agent.filter_responses(**kwargs)
        
    def get_captured_api_calls(self) -> List[Dict]:
        return self._agent.get_captured_api_calls()
    
    def find_links_by_text(self, text_pattern: str) -> List[Dict]:
        return self._run(self._agent.find_links_by_text(text_pattern))
    
    def find_link_and_click(self, text_pattern: str):
        return self._run(self._agent.find_link_and_click(text_pattern))
    
    def search_page_content(self, keyword: str) -> List[Dict]:
        return self._run(self._agent.search_page_content(keyword))
    
    def focus_on_element(self, element_info: Dict):
        return self._run(self._agent.focus_on_element(element_info))
    
    def click_by_text(self, text: str, exact: bool = False):
        return self._run(self._agent.click_by_text(text, exact))
    
    def scroll_page(self, times: int = 3):
        return self._run(self._agent.scroll_page(times))
        
    def close(self):
        self._run(self._agent.close())
        self._loop.close()
    
    def get_current_url(self) -> str:
        return self._run(self._agent.get_current_url())


# CLI interface for OpenClaw integration
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Playwright Browser Agent")
    parser.add_argument("url", help="URL to navigate")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--output", "-o", help="Output file for content")
    parser.add_argument("--hook-api", action="store_true", help="Hook and capture API calls")
    parser.add_argument("--screenshot", "-s", help="Save screenshot to path")
    parser.add_argument("--search", help="Search for keyword in page")
    parser.add_argument("--find-link", help="Find and click link by text pattern")
    
    args = parser.parse_args()
    
    agent = SyncBrowserAgent(headless=args.headless)
    
    try:
        print(f"Navigating to: {args.url}")
        
        if args.hook_api:
            def print_api(response):
                if response.resource_type in ['xhr', 'fetch']:
                    print(f"\n[API] {response.url[:100]}...")
                    if isinstance(response.body, dict):
                        print(f"      JSON: {json.dumps(response.body, indent=2)[:500]}")
                        
            agent.hook_network_responses(print_api)
            
        content = agent.get_page_content(args.url)
        
        result = {
            "success": True,
            "url": args.url,
            "title": content.get("title"),
            "content": content.get("text", "")[:5000],  # Limit text
            "links_count": len(content.get("links", [])),
            "api_calls": agent.get_captured_api_calls()
        }
        
        # Search for keyword if specified
        if args.search:
            print(f"\nSearching for: {args.search}")
            search_results = agent.search_page_content(args.search)
            result["search_results"] = search_results
            print(f"Found {len(search_results)} matches")
            
        # Find and click link if specified
        if args.find_link:
            print(f"\nLooking for link: {args.find_link}")
            clicked = agent.find_link_and_click(args.find_link)
            result["link_clicked"] = clicked
            result["current_url"] = agent.get_current_url()
            print(f"Link clicked: {clicked}")
        
        if args.screenshot:
            agent._run(agent._agent.screenshot(args.screenshot))
            result["screenshot"] = args.screenshot
            print(f"Screenshot saved to: {args.screenshot}")
            
        output = json.dumps(result, indent=2, ensure_ascii=False, default=str)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Output saved to: {args.output}")
        else:
            print("\n" + "="*50)
            print("RESULT:")
            print("="*50)
            print(output)
            
    finally:
        agent.close()
