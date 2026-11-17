from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def plate_recognition(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别车牌号、车牌颜色、单/双层车牌、位置框。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826132090352650", "plate_recognition", arguments)

def plate_recognition_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别车牌号、车牌颜色、单/双层车牌、位置框。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826132090352650", "plate_recognition_for_data_base64", arguments)

