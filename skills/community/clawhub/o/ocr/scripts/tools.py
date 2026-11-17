from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr(
    dataUrl: str
) -> Dict[str, Any]:
    """
    兼顾速度与精度的文字识别。输入包含文本的图像，自动检测并识别内容。适用于各类文档、广告牌、屏幕截图等场景。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1825936339966986", "ocr", arguments)

def ocr_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    兼顾速度与精度的文字识别。输入包含文本的图像，自动检测并识别内容。适用于各类文档、广告牌、屏幕截图等场景。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1825936339966986", "ocr_for_data_base64", arguments)

