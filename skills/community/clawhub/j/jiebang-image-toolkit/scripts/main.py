#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
捷帮图片工具 - 提供图片格式转换和二维码生成功能
API基础URL: https://www.jiebang.site
"""

import os
import json
from coze_workload_identity import requests


# API基础配置
BASE_URL = "https://www.jiebang.site"


def get_admin_key():
    """从环境变量获取Admin Key"""
    admin_key = os.getenv("COZE_JIEBANG_ADMIN_KEY_7647549465691209778")
    if not admin_key:
        raise ValueError("缺少凭证配置，请检查环境变量 COZE_JIEBANG_ADMIN_KEY")
    return admin_key


def get_headers():
    """构建请求头，包含鉴权信息"""
    return {
        "Content-Type": "application/json",
        "X-Admin-Key": get_admin_key()
    }


def image_convert(image: str, from_format: str, to_format: str, quality: int = 85) -> dict:
    """
    图片格式转换
    
    Args:
        image: 图片URL或Base64编码
        from_format: 源格式 (png/jpeg/webp/bmp/svg)
        to_format: 目标格式 (png/jpeg/webp/bmp/svg)
        quality: 输出质量 (1-100)
        
    Returns:
        包含转换结果的字典
    """
    api_url = f"{BASE_URL}/api/image-convert"
    
    payload = {
        "image": image,
        "from": from_format,
        "to": to_format,
        "quality": quality
    }
    
    try:
        response = requests.post(
            api_url,
            headers=get_headers(),
            json=payload,
            timeout=60
        )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def generate_qrcode(text: str, size: int = 300, error_level: str = "M") -> dict:
    """
    生成二维码
    
    Args:
        text: 二维码内容
        size: 二维码尺寸
        error_level: 纠错级别 L/M/Q/H
        
    Returns:
        包含二维码结果的字典
    """
    api_url = f"{BASE_URL}/api/qrcode"
    
    try:
        # 尝试GET请求
        params = {"text": text, "size": size, "error_level": error_level}
        response = requests.get(
            api_url,
            headers=get_headers(),
            params=params,
            timeout=30
        )
        
        if response.status_code >= 400:
            # 尝试POST请求
            response = requests.post(
                api_url,
                headers=get_headers(),
                json={"text": text, "size": size, "error_level": error_level},
                timeout=30
            )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def main():
    """主函数，处理命令行参数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="捷帮图片工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")
    
    # 图片转换子命令
    convert_parser = subparsers.add_parser("convert", help="图片格式转换")
    convert_parser.add_argument("--image", required=True, help="图片URL或Base64")
    convert_parser.add_argument("--from-format", required=True, help="源格式")
    convert_parser.add_argument("--to-format", required=True, help="目标格式")
    convert_parser.add_argument("--quality", type=int, default=85, help="输出质量")
    
    # 二维码子命令
    qrcode_parser = subparsers.add_parser("qrcode", help="生成二维码")
    qrcode_parser.add_argument("--text", required=True, help="二维码内容")
    qrcode_parser.add_argument("--size", type=int, default=300, help="尺寸")
    qrcode_parser.add_argument("--error-level", default="M", help="纠错级别")
    
    args = parser.parse_args()
    
    if args.action == "convert":
        result = image_convert(args.image, args.from_format, args.to_format, args.quality)
    elif args.action == "qrcode":
        result = generate_qrcode(args.text, args.size, args.error_level)
    else:
        print("请指定操作类型: convert 或 qrcode")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
