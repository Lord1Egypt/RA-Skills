from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def insect_recognition(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别昆虫或其他节肢动物名称（或所属目, 科, 属, 种）。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826131900672010", "insect_recognition", arguments)

def insect_recognition_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别昆虫或其他节肢动物名称（或所属目, 科, 属, 种）。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826131900672010", "insect_recognition_for_data_base64", arguments)

