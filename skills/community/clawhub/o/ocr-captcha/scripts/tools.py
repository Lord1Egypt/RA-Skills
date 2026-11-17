from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_captcha(
    dataUrl: str
) -> Dict[str, Any]:
    """
    输入常见验证码图片，返回验证码文本内容。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1825936344787978", "ocr_captcha", arguments)

def ocr_captcha_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    输入常见验证码图片，返回验证码文本内容。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1825936344787978", "ocr_captcha_for_data_base64", arguments)

