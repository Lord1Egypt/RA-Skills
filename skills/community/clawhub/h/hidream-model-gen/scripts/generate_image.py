#!/usr/bin/env python3
"""
生成图片并保存到本地 - 自动发送结果版本
"""
import os
import sys
import argparse

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from vivago_client import create_client


def main():
    parser = argparse.ArgumentParser(description='Generate image using Vivago AI')
    parser.add_argument('prompt', help='Image description')
    parser.add_argument('--port', default='kling-image', help='Model port (kling-image, hidream-txt2img, nano-banana)')
    parser.add_argument('--ratio', default='16:9', help='Aspect ratio (1:1, 4:3, 3:4, 16:9, 9:16)')
    parser.add_argument('--batch-size', type=int, default=1, help='Number of images to generate (1-4)')
    
    args = parser.parse_args()
    
    print(f"🎨 正在生成图片...")
    print(f"   Prompt: {args.prompt}")
    print(f"   模型: {args.port}")
    print(f"   比例: {args.ratio}")
    print()
    
    try:
        client = create_client()
        
        # 生成图片
        results = client.text_to_image(
            prompt=args.prompt,
            port=args.port,
            wh_ratio=args.ratio,
            batch_size=args.batch_size
        )
        
        if not results:
            print("❌ 生成失败")
            return 1
        
        # 下载并保存每张图片
        saved_files = []
        for i, result in enumerate(results):
            image_id = result.get('image')
            if not image_id:
                continue
            
            print(f"📥 正在下载图片 {i+1}/{len(results)}...")
            
            # 尝试下载
            output_path = f"/tmp/{image_id}.jpg"
            downloaded_path = client.download_image(image_id, output_path)
            
            if downloaded_path and os.path.exists(downloaded_path):
                file_size = os.path.getsize(downloaded_path)
                print(f"   ✅ 已保存: {downloaded_path} ({file_size/1024:.1f} KB)")
                saved_files.append(downloaded_path)
            else:
                print(f"   ❌ 下载失败")
        
        print()
        print("=" * 60)
        
        if saved_files:
            print(f"✅ 成功生成并下载 {len(saved_files)} 张图片")
            # 输出文件路径供外部工具读取
            with open('/tmp/vivago_output_files.txt', 'w') as f:
                for path in saved_files:
                    f.write(path + '\n')
            return 0
        else:
            print("❌ 图片下载失败")
            return 1
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
