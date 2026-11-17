from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_id_card(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别身份证正面（姓名、性别、民族、出生日期、住址、身份证号）和背面（签发机关、有效期限），自动判断正反面并校验身份证号有效性。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285519177738", "ocr_id_card", arguments)

def ocr_id_card_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别身份证正面（姓名、性别、民族、出生日期、住址、身份证号）和背面（签发机关、有效期限），自动判断正反面并校验身份证号有效性。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285519177738", "ocr_id_card_for_data_base64", arguments)

