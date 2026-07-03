from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_best_logo_url(
    url: str
) -> Dict[str, Any]:
    """
    从网站提取并返回最佳Logo的URL地址，适用于只需要获取最佳Logo URL的场景
    
    Args:
        url: 要分析的网站URL
    
    Returns:
        
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777316659872771", "get_best_logo_url", arguments)

def analyze_logo(
    url: str,
    onlyBestUrl: Optional[bool] = False
) -> Dict[str, Any]:
    """
    分析Logo的基本信息（尺寸、格式、质量等），支持onlyBestUrl参数只返回最佳Logo的URL
    
    Args:
        url: 要分析的网站URL
        onlyBestUrl: 是否只返回最佳Logo的URL，默认为false
    
    Returns:
        
    """
    arguments = {
        "url": url,
        "onlyBestUrl": onlyBestUrl
    }
    
    return call_api("1777316659872771", "analyze_logo", arguments)

