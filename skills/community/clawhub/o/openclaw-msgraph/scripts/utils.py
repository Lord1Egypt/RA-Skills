"""
Utility functions for formatting and text processing.
"""

import re
from datetime import datetime
from typing import Optional


def format_datetime(dt_str: Optional[str]) -> str:
    """
    Format ISO datetime string for display.
    
    Args:
        dt_str: ISO datetime string (e.g., "2026-03-10T10:00:00.000Z")
        
    Returns:
        Formatted display string (e.g., "Tue Mar 10, 2026  10:00 AM EDT")
    """
    if not dt_str:
        return "?"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%a %b %d, %Y  %I:%M %p %Z").strip()
    except Exception:
        return dt_str


def parse_local_datetime(dt_str: str, tz: str = "America/New_York") -> dict:
    """
    Parse local datetime string and return Graph API compatible dict.
    
    Accepts multiple formats:
    - 'YYYY-MM-DDTHH:MM'
    - 'YYYY-MM-DD HH:MM'
    - 'YYYY-MM-DD' (defaults to 00:00)
    
    Args:
        dt_str: DateTime string
        tz: Timezone identifier
        
    Returns:
        Graph API dateTimeTimeZone dict
    """
    dt_str = dt_str.replace(" ", "T")
    if len(dt_str) == 10:
        dt_str += "T00:00:00"
    elif len(dt_str) == 16:
        dt_str += ":00"
    return {"dateTime": dt_str, "timeZone": tz}


def strip_html(html: str) -> str:
    """
    Strip HTML tags and clean up styling for readable plaintext.
    
    Args:
        html: HTML string
        
    Returns:
        Cleaned plaintext
    """
    # Remove style blocks
    text = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove all HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Clean up excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text
