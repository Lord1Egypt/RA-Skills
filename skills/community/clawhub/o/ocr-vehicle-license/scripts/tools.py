from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def ocr_vehicle_license(
    dataUrl: str
) -> Dict[str, Any]:
    """
    识别机动车行驶证的号牌号码、车辆类型、所有人、住址、品牌型号、发动机号码、车辆识别代号等信息，支持自动方向检测和主副页过滤。 需要输入图片文件链接。
    
    Args:
        dataUrl: 图片文件链接地址
    
    Returns:
        
    """
    arguments = {
        "dataUrl": dataUrl
    }
    
    return call_api("1826285521913866", "ocr_vehicle_license", arguments)

def ocr_vehicle_license_for_data_base64(
    dataBase64: str
) -> Dict[str, Any]:
    """
    识别机动车行驶证的号牌号码、车辆类型、所有人、住址、品牌型号、发动机号码、车辆识别代号等信息，支持自动方向检测和主副页过滤。 需要输入图片文件的BASE64编码。
    
    Args:
        dataBase64: base64 encoded data of image file
    
    Returns:
        
    """
    arguments = {
        "dataBase64": dataBase64
    }
    
    return call_api("1826285521913866", "ocr_vehicle_license_for_data_base64", arguments)

