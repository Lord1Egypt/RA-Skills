from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_passport(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别护照号码、中文姓名、英文姓名、性别、国籍、出生日期、签发日期、有效期至、签发地点等信息，支持MRZ机读码解析。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285520541706", "ocr_passport", arguments)

def ocr_passport_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别护照号码、中文姓名、英文姓名、性别、国籍、出生日期、签发日期、有效期至、签发地点等信息，支持MRZ机读码解析。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285520541706", "ocr_passport_for_data_base64", arguments)

