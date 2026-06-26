#!/usr/bin/env python3
"""
批量上传图片到微信公众号素材库
"""

import requests
import json
import os
import sys

# 加载配置
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

APP_ID = config.get('appId')
APP_SECRET = config.get('appSecret')

def get_access_token():
    """获取 access token"""
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}'
    resp = requests.get(url, verify=False)
    data = resp.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"获取 token 失败：{data}")
        sys.exit(1)

def upload_image(token, image_path):
    """上传单张图片"""
    url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'
    
    with open(image_path, 'rb') as f:
        files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
        resp = requests.post(url, files=files, verify=False)
    
    data = resp.json()
    if 'url' in data:
        return data['url']
    else:
        print(f"上传失败 {os.path.basename(image_path)}: {data}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法：python3 upload_images.py <图片文件夹>")
        sys.exit(1)
    
    image_folder = sys.argv[1]
    
    if not os.path.exists(image_folder):
        print(f"文件夹不存在：{image_folder}")
        sys.exit(1)
    
    # 获取 token
    print("获取 access token...")
    token = get_access_token()
    
    # 上传图片
    image_urls = {}
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.webp'):
            image_path = os.path.join(image_folder, filename)
            print(f"上传 {filename}...")
            url = upload_image(token, image_path)
            if url:
                image_urls[filename] = url
                print(f"  ✅ {url[:60]}...")
    
    # 保存结果
    output_path = os.path.join(image_folder, 'image_urls.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(image_urls, f, ensure_ascii=False, indent=2)
    
    print(f"\n共上传 {len(image_urls)} 张图片")
    print(f"URL 已保存到：{output_path}")

if __name__ == '__main__':
    main()
