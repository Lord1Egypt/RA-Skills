#!/usr/bin/env python3
"""
img.scdn.io 图片上传工具
用法: python upload.py <图片路径> [cdn_domain]
"""
import requests
import sys
import os

API_URL = "https://img.scdn.io/api/v1.php"


def upload_image(image_path, cdn_domain=None):
    """
    上传图片到 img.scdn.io
    
    参数:
        image_path: 图片文件路径
        cdn_domain: 可选的 CDN 域名
    
    返回:
        dict: 包含图片 URL 和其他信息
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {}
        if cdn_domain:
            data['cdn_domain'] = cdn_domain
        
        response = requests.post(API_URL, files=files, data=data)
    
    result = response.json()
    
    if result.get('success'):
        return {
            "success": True,
            "url": result.get('url'),
            "delete_url": result.get('delete_url'),
            "full_response": result
        }
    else:
        error_msg = result.get('error', '未知错误')
        raise Exception(f"上传失败: {error_msg}")


def main():
    if len(sys.argv) < 2:
        print("用法: python upload.py <图片路径> [cdn_domain]")
        print("示例: python upload.py /path/to/image.jpg")
        print("      python upload.py /path/to/image.jpg img.scdn.io")
        sys.exit(1)
    
    image_path = sys.argv[1]
    cdn_domain = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"正在上传: {image_path}")
    
    try:
        result = upload_image(image_path, cdn_domain)
        print(f"\n✅ 上传成功!")
        print(f"图片链接: {result['url']}")
        if result.get('delete_url'):
            print(f"删除链接: {result['delete_url']}")
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()