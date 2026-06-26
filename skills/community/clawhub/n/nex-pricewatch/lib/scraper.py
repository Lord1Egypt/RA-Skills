"""
Nex PriceWatch Scraper Module
Price extraction and webpage scraping
Copyright 2026 Nex AI (Kevin Blancaflor)
MIT-0 License
"""

import re
import hashlib
import time
from decimal import Decimal
from typing import Dict, Any, Optional, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from .config import (
    USER_AGENT, MAX_RETRIES, REQUEST_TIMEOUT, CONNECT_TIMEOUT,
    SELECTOR_CSS, SELECTOR_XPATH, SELECTOR_REGEX, SELECTOR_TEXT,
    PRICE_PATTERNS, SNAPSHOTS_DIR, DATA_DIR
)
from .storage import get_target_by_id, save_price


def scrape_price(url: str, selector_type: str, selector: str) -> Dict[str, Any]:
    """
    Fetch page and extract price.
    Returns: {"raw_text": str, "price": Decimal, "currency": str, "success": bool, "error": str}
    """
    try:
        html = _fetch_page(url)
        if not html:
            return {
                'raw_text': '',
                'price': None,
                'currency': None,
                'success': False,
                'error': 'Failed to fetch page'
            }

        # Extract based on selector type
        if selector_type == SELECTOR_CSS:
            raw_text = _extract_by_css(html, selector)
        elif selector_type == SELECTOR_REGEX:
            raw_text = _extract_by_regex(html, selector)
        elif selector_type == SELECTOR_TEXT:
            raw_text = _extract_by_text(html, selector)
        elif selector_type == SELECTOR_XPATH:
            # Basic XPATH support (limited without lxml)
            raw_text = _extract_by_xpath_simple(html, selector)
        else:
            return {
                'raw_text': '',
                'price': None,
                'currency': None,
                'success': False,
                'error': f'Unknown selector type: {selector_type}'
            }

        if not raw_text:
            return {
                'raw_text': '',
                'price': None,
                'currency': None,
                'success': False,
                'error': f'No match found for selector: {selector}'
            }

        # Parse price
        price, currency = _parse_price(raw_text)

        if price is None:
            return {
                'raw_text': raw_text,
                'price': None,
                'currency': currency,
                'success': False,
                'error': f'Could not parse price from: {raw_text}'
            }

        return {
            'raw_text': raw_text,
            'price': float(price),
            'currency': currency or 'EUR',
            'success': True,
            'error': None
        }

    except Exception as e:
        return {
            'raw_text': '',
            'price': None,
            'currency': None,
            'success': False,
            'error': str(e)
        }


def _fetch_page(url: str) -> Optional[str]:
    """HTTP GET with urllib, proper headers, timeout, retry."""
    for attempt in range(MAX_RETRIES):
        try:
            req = Request(url, headers={'User-Agent': USER_AGENT})
            with urlopen(req, timeout=REQUEST_TIMEOUT) as response:
                html = response.read().decode('utf-8', errors='ignore')
                return html
        except (URLError, HTTPError, TimeoutError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return None
        except Exception as e:
            return None

    return None


def _extract_by_css(html: str, selector: str) -> str:
    """Simple CSS selector matching using regex."""
    # Handle basic selectors like .class, #id, tag, tag.class, tag#id
    selector = selector.strip()

    # Extract class name
    class_match = re.search(r'\.([a-zA-Z0-9_-]+)', selector)
    if class_match:
        class_name = class_match.group(1)
        pattern = rf'class=["\']([^"\']*{re.escape(class_name)}[^"\']*)["\'].*?>(.*?)<'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0][1].strip()

    # Extract ID
    id_match = re.search(r'#([a-zA-Z0-9_-]+)', selector)
    if id_match:
        id_name = id_match.group(1)
        pattern = rf'id=["\']?{re.escape(id_name)}["\']?[^>]*>(.*?)<'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0].strip()

    # Extract tag name
    tag_match = re.match(r'([a-zA-Z0-9-]+)', selector)
    if tag_match:
        tag_name = tag_match.group(1)
        pattern = rf'<{tag_name}[^>]*>(.*?)</{tag_name}>'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        if matches:
            # Return first non-empty match
            for match in matches:
                text = match.strip()
                if text and _looks_like_price(text):
                    return text

    return ''


def _extract_by_regex(html: str, pattern: str) -> str:
    """Custom regex extraction."""
    try:
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        if matches:
            if isinstance(matches[0], tuple):
                # Multiple groups - return first non-empty
                for group in matches[0]:
                    if group:
                        return group
            else:
                return matches[0]
    except re.error:
        pass

    return ''


def _extract_by_text(html: str, pattern: str) -> str:
    """Find text near a label (e.g., 'Prijs:' followed by amount)."""
    # Pattern: look for label text followed by price
    pattern_escaped = re.escape(pattern)
    regex = rf'{pattern_escaped}\s*:?\s*([€$\d.,\s\w]+)'
    matches = re.findall(regex, html, re.IGNORECASE)

    if matches:
        return matches[0].strip()

    return ''


def _extract_by_xpath_simple(html: str, xpath: str) -> str:
    """Simple XPATH-like extraction (limited without lxml)."""
    # Only support very basic XPath patterns
    # Example: //div[@class='price']/span or //span[@id='price']

    if '//' in xpath:
        # Extract tag and attribute patterns
        tag_match = re.search(r'//(\w+)', xpath)
        attr_match = re.search(r'\[@([a-z-]+)=["\']([^"\']+)["\']\]', xpath)

        if attr_match:
            attr_name = attr_match.group(1)
            attr_value = attr_match.group(2)

            if attr_name == 'class':
                return _extract_by_css(html, f'.{attr_value}')
            elif attr_name == 'id':
                return _extract_by_css(html, f'#{attr_value}')

    return ''


def _parse_price(text: str) -> Tuple[Optional[Decimal], Optional[str]]:
    """Parse price string into (Decimal, currency_code)."""
    text = text.strip()

    # Try each price pattern
    for pattern in PRICE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            price_str = match.group(0)
            result = _extract_numeric_price(price_str)
            if result[0] is not None:
                return result

    # Fallback: try to extract any number
    numbers = re.findall(r'[\d.,]+', text)
    if numbers:
        result = _extract_numeric_price(numbers[0])
        if result[0] is not None:
            return result

    return None, None


def _extract_numeric_price(price_str: str) -> Tuple[Optional[Decimal], Optional[str]]:
    """Extract numeric value and currency from price string."""
    # Detect currency
    currency = _detect_currency(price_str)

    # Remove currency symbols and some letters, but keep numbers, dots and commas
    cleaned = re.sub(r'[€$£¥₹₽₺₪\s]', '', price_str)
    # Remove letters except those that might be part of numbers
    cleaned = re.sub(r'[a-zA-Z]', '', cleaned)

    # Normalize: handle both comma and period as decimal separator
    # Format: 1.499,00 (EU) or 1,499.00 (US) or 1499
    cleaned = cleaned.strip()

    if not cleaned:
        return None, currency

    # Determine decimal separator
    # Logic: the LAST separator is the decimal separator
    # - If only one separator: it's decimal
    # - If multiple separators: the last one is decimal
    last_comma = cleaned.rfind(',')
    last_period = cleaned.rfind('.')

    if last_comma == -1 and last_period == -1:
        # No separator
        try:
            return Decimal(cleaned), currency
        except:
            return None, currency

    # The last separator is always the decimal separator
    if last_comma > last_period:
        # Last separator is comma: 1.499,00 (EU) or 1,50 (EU) or 1,500 (thousands)
        # If comma has 2 or fewer digits after: decimal separator
        # If comma has 3+ digits after: thousands separator
        remaining = cleaned[last_comma + 1:]
        if len(remaining) <= 2:
            # Decimal separator
            cleaned = cleaned.replace('.', '').replace(',', '.')
        else:
            # Thousands separator (unexpected, but handle it)
            cleaned = cleaned.replace('.', '').replace(',', '')
    else:
        # Last separator is period: 1,499.00 (US) or 99.99 (US)
        # Remove all commas (thousands) and keep period (decimal)
        cleaned = cleaned.replace(',', '')
        # Period stays as decimal separator

    try:
        return Decimal(cleaned), currency
    except:
        return None, currency


def _detect_currency(text: str) -> str:
    """Detect currency code from text."""
    text_upper = text.upper()

    currency_map = {
        '€': 'EUR',
        'EUR': 'EUR',
        'EURO': 'EUR',
        'EUROS': 'EUR',
        '$': 'USD',
        'USD': 'USD',
        'DOLLAR': 'USD',
        '£': 'GBP',
        'GBP': 'GBP',
        '¥': 'JPY',
        'JPY': 'JPY',
        '₹': 'INR',
        'INR': 'INR',
        '₽': 'RUB',
        'RUB': 'RUB',
        '₺': 'TRY',
        'TRY': 'TRY',
        '₪': 'ILS',
        'ILS': 'ILS',
    }

    # Check for currency symbols first
    for symbol, code in currency_map.items():
        if symbol in text:
            return code

    # Check for currency codes
    for code in ['EUR', 'USD', 'GBP', 'JPY', 'CNY', 'INR', 'BRL', 'RUB', 'TRY', 'ILS']:
        if code in text_upper:
            return code

    return 'EUR'  # Default


def _looks_like_price(text: str) -> bool:
    """Check if text looks like it contains a price."""
    return bool(re.search(r'[\d.,]', text)) and len(text) < 50


def take_snapshot(url: str, target_id: int) -> Optional[str]:
    """Save page HTML to snapshots dir and return hash."""
    html = _fetch_page(url)
    if not html:
        return None

    # Create hash of content
    content_hash = hashlib.sha256(html.encode()).hexdigest()[:12]

    # Save to snapshots
    snapshot_path = SNAPSHOTS_DIR / f"target_{target_id}_{content_hash}.html"
    try:
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return content_hash
    except:
        return None


def check_all_targets() -> list:
    """Run all enabled targets, save prices, return results."""
    from .storage import list_targets, save_price, detect_price_change

    targets = list_targets(enabled_only=True)
    results = []

    for target in targets:
        result = {
            'target_id': target['id'],
            'name': target['name'],
            'url': target['url'],
        }

        # Scrape price
        scrape_result = scrape_price(target['url'], target['selector_type'], target['selector'])
        result.update(scrape_result)

        if scrape_result['success']:
            # Save to database
            price = scrape_result['price']
            raw_text = scrape_result['raw_text']

            snapshot_hash = take_snapshot(target['url'], target['id'])
            save_price(target['id'], price, raw_text, snapshot_hash)

            # Detect change
            change_info = detect_price_change(target['id'], price)
            result['change_info'] = change_info

        results.append(result)

    return results
