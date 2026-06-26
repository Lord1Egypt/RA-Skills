#!/usr/bin/env python3
"""
camera_helper.py - Node 摄像头辅助工具

用法:
    python camera_helper.py --download "http://192.168.1.100:18790/images/capture_123.jpg" -o image.jpg
    python camera_helper.py --analyze frame.json
    python camera_helper.py --decode-frame frame.txt --output image.jpg  (兼容旧 base64 格式)
"""

import argparse
import base64
import json
import sys
import urllib.request
from pathlib import Path


def download_image(url: str, output_path: str):
    """从 Node 设备的 HTTP 服务器下载图片"""
    try:
        urllib.request.urlretrieve(url, output_path)
        size_kb = Path(output_path).stat().st_size / 1024
        print(f"图像已下载: {output_path} ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def decode_base64_frame(frame_data: str, output_path: str):
    """解码 Base64 图像帧并保存（兼容旧格式）"""
    try:
        if "," in frame_data:
            frame_data = frame_data.split(",")[1]

        image_bytes = base64.b64decode(frame_data)
        Path(output_path).write_bytes(image_bytes)
        print(f"图像已保存: {output_path}")
        return True
    except Exception as e:
        print(f"解码失败: {e}")
        return False


def analyze_frame_info(frame_json: str):
    """分析帧信息（支持 imageUrl 和旧 base64 格式）"""
    try:
        data = json.loads(frame_json)
        print("帧信息:")

        image_url = data.get('imageUrl', '')
        if image_url:
            print(f"  图片 URL: {image_url}")
            return True

        # 兼容旧 base64 格式
        frame_data = data.get('image', '')
        if frame_data:
            size_bytes = len(frame_data) * 3 / 4
            size_kb = size_bytes / 1024
            print(f"  图像大小 (base64): ~{size_kb:.1f} KB")
            return True

        print("  未找到 imageUrl 或 image 字段")
        return False
    except Exception as e:
        print(f"解析失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Node Camera 辅助工具')
    parser.add_argument('--download', help='从 Node HTTP 服务器下载图片 (URL)')
    parser.add_argument('--decode-frame', help='Base64 帧数据文件路径（兼容旧格式）')
    parser.add_argument('--output', '-o', default='output.jpg', help='输出图像路径')
    parser.add_argument('--analyze', help='分析帧 JSON 文件')
    args = parser.parse_args()

    if args.download:
        success = download_image(args.download, args.output)
        sys.exit(0 if success else 1)

    elif args.decode_frame:
        frame_data = Path(args.decode_frame).read_text().strip()
        success = decode_base64_frame(frame_data, args.output)
        sys.exit(0 if success else 1)

    elif args.analyze:
        frame_json = Path(args.analyze).read_text()
        success = analyze_frame_info(frame_json)
        sys.exit(0 if success else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
