#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
捷帮文件处理工具 - 提供文本哈希计算、Base64编解码、URL编解码功能
API基础URL: https://www.jiebang.site
"""

import os
import json
from coze_workload_identity import requests


# API基础配置
BASE_URL = "https://www.jiebang.site"

# 占位skill_id，创建草稿后需替换
def get_admin_key():
    """从环境变量获取Admin Key"""
    admin_key = os.getenv("COZE_JIEBANG_ADMIN_KEY_7647547759297380390")
    if not admin_key:
        raise ValueError("缺少凭证配置，请检查环境变量 COZE_JIEBANG_ADMIN_KEY")
    return admin_key


def get_headers():
    """构建请求头，包含鉴权信息"""
    return {
        "Content-Type": "application/json",
        "X-Admin-Key": get_admin_key()
    }


def calc_hash(data: str, algorithm: str = "md5") -> dict:
    """
    计算文本哈希值
    
    Args:
        data: 要计算哈希的文本内容
        algorithm: 算法类型 (md5 / sha1 / sha256)
        
    Returns:
        包含哈希结果的字典
    """
    api_url = f"{BASE_URL}/api/hash"
    
    payload = {
        "data": data,
        "algorithm": algorithm
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def base64_convert(data: str, action: str = "encode") -> dict:
    """
    Base64编解码
    
    Args:
        data: 要处理的内容
        action: 操作 (encode / decode)
        
    Returns:
        处理结果
    """
    api_url = f"{BASE_URL}/api/base64"
    
    payload = {
        "data": data,
        "action": action
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def url_convert(data: str, action: str = "encode") -> dict:
    """
    URL编解码
    
    Args:
        data: 要处理的内容
        action: 操作 (encode / decode)
        
    Returns:
        处理结果
    """
    api_url = f"{BASE_URL}/api/url-encode"
    
    payload = {
        "data": data,
        "action": action
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=30
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def main():
    """主函数，处理命令行参数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="捷帮文件处理工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")
    
    # 哈希计算
    hash_parser = subparsers.add_parser("hash", help="计算文本哈希")
    hash_parser.add_argument("--data", required=True, help="文本内容")
    hash_parser.add_argument("--algorithm", default="md5", 
                            choices=["md5", "sha1", "sha256"],
                            help="算法类型")
    
    # Base64编解码
    base64_parser = subparsers.add_parser("base64", help="Base64编解码")
    base64_parser.add_argument("--data", required=True, help="内容")
    base64_parser.add_argument("--action", required=True, 
                              choices=["encode", "decode"],
                              help="操作类型")
    
    # URL编解码
    url_parser = subparsers.add_parser("url", help="URL编解码")
    url_parser.add_argument("--data", required=True, help="内容")
    url_parser.add_argument("--action", required=True,
                           choices=["encode", "decode"],
                           help="操作类型")
    
    args = parser.parse_args()
    
    if args.action == "hash":
        result = calc_hash(args.data, args.algorithm)
    elif args.action == "base64":
        result = base64_convert(args.data, args.action)
    elif args.action == "url":
        result = url_convert(args.data, args.action)
    else:
        print("请指定操作类型: hash / base64 / url")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
