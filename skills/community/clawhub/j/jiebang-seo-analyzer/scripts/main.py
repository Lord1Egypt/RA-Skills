#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
捷帮SEO分析工具 - 提供网页元数据提取和SEO健康检查功能
API基础URL: https://www.jiebang.site
"""

import os
import json
from coze_workload_identity import requests


# API基础配置
BASE_URL = "https://www.jiebang.site"

# 获取凭证（Admin Key）
def get_admin_key():
    """从环境变量获取Admin Key"""
    admin_key = os.getenv("COZE_JIEBANG_ADMIN_KEY_7647549465691193394")
    if not admin_key:
        raise ValueError("缺少凭证配置，请检查环境变量 COZE_JIEBANG_ADMIN_KEY")
    return admin_key


def get_headers():
    """构建请求头，包含鉴权信息"""
    return {
        "Content-Type": "application/json",
        "X-Admin-Key": get_admin_key()
    }


def extract_meta(url: str) -> dict:
    """
    提取网页元数据
    
    Args:
        url: 网页URL
        
    Returns:
        包含元数据的字典
    """
    api_url = f"{BASE_URL}/api/meta-extract"
    
    try:
        # 尝试GET请求
        params = {"url": url}
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
                json={"url": url},
                timeout=30
            )
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: {response.status_code}, {response.text}")
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {str(e)}")


def seo_check(url: str) -> dict:
    """
    执行SEO健康检查
    
    Args:
        url: 网页URL
        
    Returns:
        包含SEO检查结果的字典
    """
    api_url = f"{BASE_URL}/api/seo-check"
    
    try:
        # 尝试GET请求
        params = {"url": url}
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
                json={"url": url},
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
    
    parser = argparse.ArgumentParser(description="捷帮SEO分析工具")
    parser.add_argument("--action", choices=["meta", "seo"], required=True, 
                        help="操作类型: meta(元数据提取) 或 seo(SEO检查)")
    parser.add_argument("--url", required=True, help="目标网页URL")
    
    args = parser.parse_args()
    
    if args.action == "meta":
        result = extract_meta(args.url)
    else:
        result = seo_check(args.url)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
