from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_driver_license(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别驾驶证主页（证号、姓名、性别、国籍、住址、出生日期、准驾车型、初次领证日期、有效期限）和副页（档案编号）。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285518490634", "ocr_driver_license", arguments)

def ocr_driver_license_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别驾驶证主页（证号、姓名、性别、国籍、住址、出生日期、准驾车型、初次领证日期、有效期限）和副页（档案编号）。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285518490634", "ocr_driver_license_for_data_base64", arguments)

