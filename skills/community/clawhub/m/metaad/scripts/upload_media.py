#!/usr/bin/env python3
"""
上传图片/视频素材到 Meta
"""

import requests
from pathlib import Path
from meta_api import get_ad_account_id, get_access_token, get_api_version, BASE_URL


def upload_image(image_path, name=None):
    """
    上传图片到 Meta Ad Library
    
    Args:
        image_path: 本地图片路径
        name: 素材名称（可选）
    
    Returns:
        dict: 包含 hash 和 url 的字典
    """
    account_id = get_ad_account_id()
    url = f"{BASE_URL}/{get_api_version()}/{account_id}/adimages"
    
    # 读取图片文件
    image_file = Path(image_path)
    if not image_file.exists():
        raise FileNotFoundError(f"图片不存在: {image_path}")
    
    # 构建 multipart 请求
    files = {
        'file': (image_file.name, open(image_path, 'rb'), f'image/{image_file.suffix[1:]}')
    }
    data = {
        'access_token': get_access_token()
    }
    if name:
        data['name'] = name
    
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    result = response.json()
    
    if 'images' in result:
        image_hash = list(result['images'].keys())[0]
        image_url = result['images'][image_hash]['url']
        return {
            'hash': image_hash,
            'url': image_url,
            'name': image_file.name
        }
    else:
        raise Exception(f"上传失败: {result}")


def upload_video(video_path, name=None, description=None):
    """
    上传视频到 Meta
    
    Args:
        video_path: 本地视频路径
        name: 视频名称
        description: 视频描述
    
    Returns:
        dict: 包含 video_id 的字典
    """
    account_id = get_ad_account_id()
    url = f"{BASE_URL}/{get_api_version()}/{account_id}/advideos"
    
    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"视频不存在: {video_path}")
    
    files = {
        'file': (video_file.name, open(video_path, 'rb'), 'video/mp4')
    }
    data = {
        'access_token': get_access_token()
    }
    if name:
        data['name'] = name
    if description:
        data['description'] = description
    
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    result = response.json()
    
    return {
        'video_id': result.get('id'),
        'name': video_file.name
    }


def upload_images_batch(image_paths):
    """
    批量上传图片
    
    Args:
        image_paths: 图片路径列表
    
    Returns:
        list: 上传结果列表
    """
    results = []
    for path in image_paths:
        try:
            result = upload_image(path)
            results.append(result)
            print(f"✅ 上传成功: {path} -> Hash: {result['hash']}")
        except Exception as e:
            print(f"❌ 上传失败: {path} -> {e}")
            results.append(None)
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python upload_media.py <图片路径1> [图片路径2] ...")
        print("示例: python upload_media.py image1.jpg image2.png")
        exit(1)
    
    image_paths = sys.argv[1:]
    print(f"=== 批量上传 {len(image_paths)} 个文件 ===\n")
    
    results = upload_images_batch(image_paths)
    
    print("\n=== 上传结果 ===")
    for i, result in enumerate(results):
        if result:
            print(f"{i+1}. ✅ {result['name']}")
            print(f"   Hash: {result['hash']}")
            print(f"   URL: {result['url']}")
        else:
            print(f"{i+1}. ❌ {image_paths[i]} (失败)")
