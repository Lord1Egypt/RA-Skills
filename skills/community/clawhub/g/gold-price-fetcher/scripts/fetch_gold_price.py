#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时金价获取脚本
通过京东金融 API 获取实时金价
"""

import requests
import json
import os
from datetime import datetime

# API 配置
API_URL = "https://ms.jr.jd.com/gw2/generic/CreatorSer/newh5/m/getFirstRelatedProductInfo"
PARAMS = {
    "circleId": "13245",
    "invokeSource": "5",
    "productId": "21001001000001"
}

# 缓存文件路径
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "last_price.json")


def load_cache():
    """加载缓存数据"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None


def save_cache(price, timestamp):
    """保存缓存数据"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    data = {
        "price": price,
        "timestamp": timestamp,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_gold_price():
    """获取实时金价"""
    try:
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 解析金价（嵌套结构：resultData -> data -> minimumPriceValue）
        price = None
        if 'resultData' in data and 'data' in data['resultData']:
            price = data['resultData']['data'].get('minimumPriceValue')
        
        if price is None:
            return {"success": False, "error": "未找到金价数据"}
        
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 保存缓存
        save_cache(price, current_time)
        
        # 格式化输出
        result = f"{current_time} 金价：{price} 元/克"
        
        return {
            "success": True,
            "price": price,
            "timestamp": current_time,
            "formatted": result
        }
        
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络请求失败：{str(e)}"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON 解析失败：{str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"未知错误：{str(e)}"}


if __name__ == "__main__":
    import sys
    # Windows 控制台编码处理
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    result = fetch_gold_price()
    
    if result.get("success"):
        print(result["formatted"])
    else:
        print(f"获取失败：{result.get('error')}")
