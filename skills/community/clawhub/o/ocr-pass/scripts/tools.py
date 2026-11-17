from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_pass(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别港澳通行证、台湾通行证的通行证号码、姓名、性别、出生日期、有效期、签发地点等信息，支持MRZ机读码解析。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285519862794", "ocr_pass", arguments)

def ocr_pass_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别港澳通行证、台湾通行证的通行证号码、姓名、性别、出生日期、有效期、签发地点等信息，支持MRZ机读码解析。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285519862794", "ocr_pass_for_data_base64", arguments)

