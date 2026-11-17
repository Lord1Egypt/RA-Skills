from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_biz_license(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别营业执照的统一社会信用代码、名称、法定代表人、注册资本、成立日期、经营范围、登记机关和住所地址。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285517811722", "ocr_biz_license", arguments)

def ocr_biz_license_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别营业执照的统一社会信用代码、名称、法定代表人、注册资本、成立日期、经营范围、登记机关和住所地址。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285517811722", "ocr_biz_license_for_data_base64", arguments)

