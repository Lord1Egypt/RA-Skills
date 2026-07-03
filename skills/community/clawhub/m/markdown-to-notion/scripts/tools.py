from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def markdown_to_notion(
    markdown: str
) -> Dict[str, Any]:
    """
    Convert markdown content to notion json page content
    
    Args:
        markdown: The markdown content to convert.
    
    Returns:
        
    """
    arguments = {
        "markdown": markdown
    }
    
    return call_api("1777316659401731", "markdown_to_notion", arguments)

