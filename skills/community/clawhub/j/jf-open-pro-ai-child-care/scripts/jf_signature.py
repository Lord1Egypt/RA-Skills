#!/usr/bin/env python3
"""
杰峰签名工具类
基于 Java 源码 TimeMillisUtil 和 SignatureUtil 实现

TimeMillisUtil:
  - getCounter(): 生成 7 位计数器（0000001-9999999，循环）
  - getTimMillis(): 返回 counter(7 位) + timestamp(13 位) = 20 位

SignatureUtil:
  - getEncryptStr(): 签名 = MD5(mergeByte(encryptByte, changeByte))
  - change(): 简单移位算法
  - mergeByte(): 合并字节数组
"""

import hashlib
import time
import threading

# 全局计数器（模拟 Java 静态变量）
_counter = 0
_counter_lock = threading.Lock()


def get_counter():
    """
    模拟 TimeMillisUtil.getCounter()
    生成 7 位计数器，范围 0000001-9999999，超过后重置为 1
    """
    global _counter
    with _counter_lock:
        _counter += 1
        if _counter >= 10000000:
            _counter = 1
        
        if _counter < 10:
            return "000000" + str(_counter)
        elif _counter < 100:
            return "00000" + str(_counter)
        elif _counter < 1000:
            return "0000" + str(_counter)
        elif _counter < 10000:
            return "000" + str(_counter)
        elif _counter < 100000:
            return "00" + str(_counter)
        elif _counter < 1000000:
            return "0" + str(_counter)
        else:
            return str(_counter)


def get_time_millis():
    """
    模拟 TimeMillisUtil.getTimMillis()
    返回 20 位时间戳：counter(7 位) + timestamp(13 位毫秒)
    """
    tim_millis = int(time.time() * 1000)
    return get_counter() + str(tim_millis)


def change(encrypt_str, move_card):
    """
    模拟 SignatureUtil.change() - 简单移位算法
    
    Args:
        encrypt_str: 待加密字符串
        move_card: 移动卡标识（取模基数）
    
    Returns:
        移位后的字节数组
    """
    encrypt_byte = bytearray(encrypt_str.encode('iso-8859-1'))
    encrypt_length = len(encrypt_byte)
    
    for i in range(encrypt_length):
        if (i % move_card) > ((encrypt_length - i) % move_card):
            temp = encrypt_byte[i]
        else:
            temp = encrypt_byte[encrypt_length - (i + 1)]
        
        encrypt_byte[i], encrypt_byte[encrypt_length - (i + 1)] = \
            encrypt_byte[encrypt_length - (i + 1)], temp
    
    return bytes(encrypt_byte)


def merge_byte(encrypt_byte, change_byte):
    """
    模拟 SignatureUtil.mergeByte() - 合并字节数组
    
    Args:
        encrypt_byte: 原始字节数组
        change_byte: 移位后的字节数组
    
    Returns:
        合并后的字节数组（长度为原始 2 倍）
    """
    encrypt_length = len(encrypt_byte)
    encrypt_length2 = encrypt_length * 2
    
    temp = bytearray(encrypt_length2)
    for i in range(encrypt_length):
        temp[i] = encrypt_byte[i]
        temp[encrypt_length2 - 1 - i] = change_byte[i]
    
    return bytes(temp)


def get_encrypt_str(uuid, app_key, app_secret, time_millis, move_card):
    """
    模拟 SignatureUtil.getEncryptStr() - 获取签名字符串
    
    Args:
        uuid: 客户唯一标识
        app_key: 应用 key
        app_secret: 应用密钥
        time_millis: 20 位时间戳（counter + timestamp）
        move_card: 移动卡标识
    
    Returns:
        MD5 签名字符串
    """
    encrypt_str = uuid + app_key + app_secret + time_millis
    
    encrypt_byte = encrypt_str.encode('iso-8859-1')
    change_byte = change(encrypt_str, move_card)
    merge_byte_result = merge_byte(encrypt_byte, change_byte)
    
    return hashlib.md5(merge_byte_result).hexdigest()


def generate_signature(uuid, app_key, app_secret, move_card):
    """
    便捷方法：生成完整的签名参数
    
    Args:
        uuid: 客户唯一标识
        app_key: 应用 key
        app_secret: 应用密钥
        move_card: 移动卡标识
    
    Returns:
        tuple: (time_millis, signature)
    """
    time_millis = get_time_millis()
    signature = get_encrypt_str(uuid, app_key, app_secret, time_millis, move_card)
    return time_millis, signature


if __name__ == "__main__":
    # 测试
    uuid = "69b7611b61763c001e79b4b6"
    app_key = "830f42c5735d4309d4ccd56596ee3337"
    app_secret = "0d8118f2398547ea818449b22fcaa9f9"
    move_card = 7
    
    time_millis, signature = generate_signature(uuid, app_key, app_secret, move_card)
    
    print(f"timeMillis: {time_millis}")
    print(f"signature:  {signature}")
