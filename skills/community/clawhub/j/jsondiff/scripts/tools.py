from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def jsonDiff(
    expectKey: str,
    actualKey: str
) -> Dict[str, Any]:
    """
    执行json对比
    
    Args:
        expectKey: null
        actualKey: null
    
    Returns:
        
    """
    arguments = {
        "expectKey": expectKey,
        "actualKey": actualKey
    }
    
    return call_api("1777419071902723", "jsonDiff", arguments)

