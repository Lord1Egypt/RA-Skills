#!/usr/bin/env python3
"""
生成图片并通过飞书发送 - Feishu专用版本
"""
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from vivago_client import create_client


def generate_and_send(prompt: str, port: str = 'kling-image', wh_ratio: str = '16:9'):
    """
    生成图片并保存到本地，返回文件路径供飞书发送
    
    Returns:
        tuple: (success: bool, file_paths: list, message: str)
    """
    try:
        client = create_client()
        
        # 生成图片
        results = client.text_to_image(
            prompt=prompt,
            port=port,
            wh_ratio=wh_ratio,
            batch_size=1
        )
        
        if not results:
            return False, [], "生成失败"
        
        # 下载图片
        saved_files = []
        for result in results:
            image_id = result.get('image')
            if not image_id:
                continue
            
            output_path = f"/tmp/{image_id}.jpg"
            downloaded_path = client.download_image(image_id, output_path)
            
            if downloaded_path and os.path.exists(downloaded_path):
                saved_files.append(downloaded_path)
        
        if saved_files:
            return True, saved_files, f"成功生成 {len(saved_files)} 张图片"
        else:
            return False, [], "图片下载失败"
            
    except Exception as e:
        return False, [], f"错误: {str(e)}"


if __name__ == '__main__':
    # 命令行调用，输出文件路径
    if len(sys.argv) < 2:
        print("Usage: python generate_for_feishu.py <prompt> [port] [ratio]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 'kling-image'
    ratio = sys.argv[3] if len(sys.argv) > 3 else '16:9'
    
    success, files, message = generate_and_send(prompt, port, ratio)
    
    # 输出文件路径到 stdout，供外部读取
    if success and files:
        for f in files:
            print(f)
    else:
        print(f"ERROR: {message}", file=sys.stderr)
        sys.exit(1)
