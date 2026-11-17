from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_handwriting(
    dataUrl: str
) -> Dict[str, Any]:
    """
    输入包含手写文本的图像，自动检测文本行并识别内容。适用于手写笔记、签名、手写表单等。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1825936342731786", "ocr_handwriting", arguments)

def ocr_handwriting_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    输入包含手写文本的图像，自动检测文本行并识别内容。适用于手写笔记、签名、手写表单等。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1825936342731786", "ocr_handwriting_for_data_base64", arguments)

