#!/usr/bin/env python3
"""
杰峰 OpenAPI 加密工具

包含：
- 签名算法
- 时间戳生成
"""

import hashlib
import time


def get_counter() -> str:
    """
    获取计数器（7 位，不足补 0）
    
    Returns:
        7 位计数字符串
    """
    counter = 1
    if counter < 10:
        return '000000' + str(counter)
    elif counter < 100:
        return '00000' + str(counter)
    elif counter < 1000:
        return '0000' + str(counter)
    elif counter < 10000:
        return '000' + str(counter)
    elif counter < 100000:
        return '00' + str(counter)
    elif counter < 1000000:
        return '0' + str(counter)
    else:
        return str(counter)


def get_time_millis() -> str:
    """
    获取组合时间戳（counter 7 位 + timeMillis 13 位）
    
    Returns:
        20 位时间戳字符串
    """
    counter = get_counter()
    time_millis = str(int(time.time() * 1000))
    return counter + time_millis


def str_to_bytes(s: str) -> list:
    """
    字符串转字节数组（处理 UTF-8 多字节字符）
    
    Args:
        s: 输入字符串
        
    Returns:
        字节数组
    """
    bytes_arr = []
    for char in s:
        code = ord(char)
        if code >= 0x010000 and code <= 0x10FFFF:
            bytes_arr.append(((code >> 18) & 0x07) | 0xF0)
            bytes_arr.append(((code >> 12) & 0x3F) | 0x80)
            bytes_arr.append(((code >> 6) & 0x3F) | 0x80)
            bytes_arr.append((code & 0x3F) | 0x80)
        elif code >= 0x000800 and code <= 0x00FFFF:
            bytes_arr.append(((code >> 12) & 0x0F) | 0xE0)
            bytes_arr.append(((code >> 6) & 0x3F) | 0x80)
            bytes_arr.append((code & 0x3F) | 0x80)
        elif code >= 0x000080 and code <= 0x0007FF:
            bytes_arr.append(((code >> 6) & 0x1F) | 0xC0)
            bytes_arr.append((code & 0x3F) | 0x80)
        else:
            bytes_arr.append(code & 0xFF)
    return bytes_arr


def change(encrypt_str: str, move_card: int) -> list:
    """
    简单移位算法（严格按照 Java 版本实现）
    
    Args:
        encrypt_str: 输入字符串
        move_card: 移动卡标识
        
    Returns:
        移位后的字节数组
    """
    try:
        encrypt_byte = list(encrypt_str.encode('iso-8859-1'))
    except UnicodeEncodeError:
        encrypt_byte = str_to_bytes(encrypt_str)
    
    encrypt_length = len(encrypt_byte)
    
    for i in range(encrypt_length):
        if (i % move_card) > ((encrypt_length - i) % move_card):
            temp = encrypt_byte[i]
        else:
            temp = encrypt_byte[encrypt_length - (i + 1)]
        
        encrypt_byte[i] = encrypt_byte[encrypt_length - (i + 1)]
        encrypt_byte[encrypt_length - (i + 1)] = temp
    
    return encrypt_byte


def merge_byte(encrypt_byte: list, change_byte: list) -> list:
    """
    合并字节数组
    
    Args:
        encrypt_byte: 原字节数组
        change_byte: 移位后的字节数组
        
    Returns:
        合并后的字节数组
    """
    encrypt_length = len(encrypt_byte)
    encrypt_length2 = encrypt_length * 2
    temp = [0] * encrypt_length2
    
    for i in range(encrypt_length):
        temp[i] = encrypt_byte[i]
        temp[encrypt_length2 - 1 - i] = change_byte[i]
    
    return temp


def generate_signature(uuid: str, app_key: str, app_secret: str, 
                       time_millis: str, move_card: int) -> str:
    """
    生成杰峰 OpenAPI 签名
    
    算法步骤：
    1. 将 uuid, appKey, appSecret, timeMillis 依次拼接
    2. 获取拼接后字符串的二进制数组
    3. 二进制数组进行简单移位算法
    4. 原二进制数组与移位后的二进制数组合并
    5. 将合并的二进制数组 md5 加密一次生成密钥
    
    Args:
        uuid: 客户唯一标识
        app_key: 应用 key
        app_secret: 应用密钥
        time_millis: 时间戳
        move_card: 移动取模基数
        
    Returns:
        32 位十六进制签名字符串
    """
    encrypt_str = uuid + app_key + app_secret + time_millis
    
    try:
        encrypt_byte = list(encrypt_str.encode('iso-8859-1'))
    except UnicodeEncodeError:
        encrypt_byte = str_to_bytes(encrypt_str)
    
    change_byte = change(encrypt_str, move_card)
    merge = merge_byte(encrypt_byte, change_byte)
    signature = hashlib.md5(bytes(merge)).hexdigest()
    
    return signature


# 测试
if __name__ == "__main__":
    uuid = "uuidxxxx"
    app_key = "appkeyxxxx"
    app_secret = "90f8bc17be2a425db6068c749dee4f5d"
    time_millis = "00000011645153792342"
    move_card = 2
    
    signature = generate_signature(uuid, app_key, app_secret, time_millis, move_card)
    
    print(f"Signature: {signature}")
    print(f"注意：签名算法需与杰峰服务器验证逻辑一致")
