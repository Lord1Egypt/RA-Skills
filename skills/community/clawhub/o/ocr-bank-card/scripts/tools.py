from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_bank_card(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别银行卡号、发卡银行和卡类型，使用 Luhn 算法校验卡号有效性。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285517101066", "ocr_bank_card", arguments)

def ocr_bank_card_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别银行卡号、发卡银行和卡类型，使用 Luhn 算法校验卡号有效性。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285517101066", "ocr_bank_card_for_data_base64", arguments)

