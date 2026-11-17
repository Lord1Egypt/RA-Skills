# Shared Stealth Browser Configuration

This file contains the shared browser configuration used across all browser-based booking platforms. Import this in any Playwright script to ensure consistent stealth behavior.

## Usage

```python
from playwright.sync_api import sync_playwright
from stealth_config import create_stealth_browser

with sync_playwright() as p:
    browser, context = create_stealth_browser(p)
    page = context.new_page()
    # ... your booking automation ...
    browser.close()
```

## Configuration

```python
"""
Shared stealth browser configuration for all Spot booking scripts.
Import and use this to ensure consistent anti-detection behavior.
"""
from playwright.sync_api import Browser, BrowserContext

# Realistic user agents (rotate per request)
USER_AGENTS = [
    # Chrome on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    # Chrome on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    # Firefox on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0',
    # Safari on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
    # Chrome on Linux
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
]

# Viewport sizes (rotate per session)
VIEWPORTS = [
    {'width': 1920, 'height': 1080},  # Desktop HD
    {'width': 1440, 'height': 900},   # MacBook Pro 15"
    {'width': 1536, 'height': 864},   # Windows laptop
    {'width': 1280, 'height': 800},   # MacBook Air
]

# Launch arguments for stealth
LAUNCH_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-blink-features=AutomationControlled',
    '--disable-infobars',
    '--window-size=1920,1080',
    '--start-maximized',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-plugins-discovery',
    '--disable-component-extensions-with-background-pages',
    '--disable-default-apps',
    '--disable-features=TranslateUI',
    '--disable-ipc-flooding-protection',
    '--metrics-recording-only',
    '--mute-audio',
    '--no-pings',
    '--password-store=basic',
    '--use-mock-keychain',
]

# Stealth init scripts
STEALTH_SCRIPTS = [
    # Remove webdriver flag
    'Object.defineProperty(navigator, "webdriver", {get: () => undefined})',
    
    # Override plugins
    '''Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
    })''',
    
    # Override languages
    '''Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en'],
    })''',
    
    # Override platform
    '''Object.defineProperty(navigator, 'platform', {
        get: () => 'MacIntel',
    })''',
    
    # Chrome runtime
    '''window.chrome = { runtime: {} }''',
    
    # Permissions
    '''const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    )''',
]


def create_stealth_browser(playwright, user_agent=None, viewport=None, proxy=None):
    """
    Create a stealth browser instance with anti-detection measures.
    
    Args:
        playwright: Playwright instance
        user_agent: Custom user agent (optional, rotates if not provided)
        viewport: Custom viewport (optional, rotates if not provided)
        proxy: Proxy server URL (optional, for VPN routing)
    
    Returns:
        (browser, context) tuple
    """
    import random
    
    ua = user_agent or random.choice(USER_AGENTS)
    vp = viewport or random.choice(VIEWPORTS)
    
    browser = playwright.chromium.launch(
        headless=True,
        args=LAUNCH_ARGS,
    )
    
    context_context = {
        'viewport': vp,
        'user_agent': ua,
        'locale': 'en-US',
        'timezone_id': 'America/Los_Angeles',
        'permissions': ['geolocation'],
        'color_scheme': 'light',
    }
    
    if proxy:
        context_context['proxy'] = {'server': proxy}
    
    context = browser.new_context(**context_context)
    
    # Add stealth init scripts
    for script in STEALTH_SCRIPTS:
        context.add_init_script(script)
    
    return browser, context


def human_delay(min_ms=500, max_ms=2000):
    """Random delay to mimic human interaction timing."""
    import random
    import time
    delay = random.randint(min_ms, max_ms) / 1000
    time.sleep(delay)


def human_type(page, selector, text, min_delay=50, max_delay=150):
    """Type text with human-like delays between keystrokes."""
    import random
    import time
    
    page.click(selector)
    for char in text:
        page.keyboard.type(char, delay=random.randint(min_delay, max_delay))
    time.sleep(random.randint(200, 500) / 1000)


def human_click(page, selector):
    """Click with human-like delay before and after."""
    human_delay(200, 800)
    page.click(selector)
    human_delay(500, 1500)


def detect_bot_block(page, timeout=10):
    """
    Detect if the page is showing a bot block / CAPTCHA.
    
    Returns:
        dict with 'blocked' (bool) and 'type' (str) keys
    """
    block_indicators = [
        # Cloudflare
        'text=Checking your browser',
        'text=Verify you are human',
        'text=Ray ID',
        # reCAPTCHA
        'iframe[src*="recaptcha"]',
        'iframe[src*="google.com/recaptcha"]',
        # hCaptcha
        'iframe[src*="hcaptcha"]',
        # CF Turnstile
        'iframe[src*="challenges.cloudflare.com']',
        # DataDome
        'text=Please verify',
        'text=Access denied',
        # PerimeterX
        'text=Please verify you are human',
        'text=Bot detected',
        # Generic
        'text=403 Forbidden',
        'text=429 Too Many Requests',
    ]
    
    for indicator in block_indicators:
        try:
            element = page.locator(indicator).first
            if element.is_visible(timeout=timeout * 1000):
                return {'blocked': True, 'type': indicator}
        except:
            continue
    
    return {'blocked': False, 'type': None}