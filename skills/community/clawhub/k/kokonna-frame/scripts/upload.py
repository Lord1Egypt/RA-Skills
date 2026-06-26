#!/usr/bin/env python3
"""
KoKonna 画框图片上传工具

用法：
    python3 upload.py --device living_room --image /path/to/image.jpg
    python3 upload.py --device living_room --image /path/to/image.jpg --name "画作名"
    python3 upload.py --device all --image /path/to/image.jpg
"""

import argparse
import sys
from pathlib import Path

# 添加父目录到路径以便导入 kokonna 模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from kokonna import KoKonnaFrame, load_config


def list_available_devices():
    """列出所有可用设备"""
    config = load_config()
    devices = config.get("devices", {})
    
    if not devices:
        print("未配置任何设备。")
        print("请在 ~/.openclaw/skills/kokonna-frame/config.yaml 中添加设备配置。")
        return []
    
    print("可用设备:")
    for device_name in devices.keys():
        print(f"  - {device_name}")
    
    return list(devices.keys())


def upload_to_device(device: str, image_path: str, name: str = None):
    """上传图片到指定设备"""
    print(f"正在上传到 {device}...")
    
    try:
        frame = KoKonnaFrame(device=device)
        result = frame.upload_image(image_path, name=name)
        print(f"✓ {device} 上传成功!")
        return True
    except Exception as e:
        print(f"✗ {device} 上传失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="上传图片到 KoKonna 画框",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --device living_room --image photo.jpg
  %(prog)s --device living_room --image photo.jpg --name "日落"
  %(prog)s --device all --image photo.jpg
  %(prog)s --list-devices
        """
    )
    
    parser.add_argument(
        "-d", "--device",
        required=False,
        help="设备名称（在 config.yaml 中配置）或 'all' 推送到所有设备"
    )
    
    parser.add_argument(
        "-i", "--image",
        help="图片文件路径"
    )
    
    parser.add_argument(
        "-n", "--name",
        help="图片名称（可选，显示在画框上）"
    )
    
    parser.add_argument(
        "-l", "--list-devices",
        action="store_true",
        help="列出所有可用设备"
    )
    
    args = parser.parse_args()
    
    # 列出设备
    if args.list_devices:
        list_available_devices()
        return
    
    # 检查必需参数
    if not args.device or not args.image:
        parser.print_help()
        sys.exit(1)
    
    # 检查图片文件
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"错误: 图片文件不存在: {args.image}")
        sys.exit(1)
    
    # 获取可用设备
    config = load_config()
    devices = config.get("devices", {})
    
    if not devices:
        print("错误: 未配置任何设备")
        print("请在 ~/.openclaw/skills/kokonna-frame/config.yaml 中添加设备配置。")
        sys.exit(1)
    
    # 上传
    if args.device == "all":
        # 推送到所有设备
        success_count = 0
        for device_name in devices.keys():
            if upload_to_device(device_name, args.image, args.name):
                success_count += 1
        
        print(f"\n完成: {success_count}/{len(devices)} 个设备上传成功")
    else:
        # 推送到指定设备
        if args.device not in devices:
            print(f"错误: 未知设备 '{args.device}'")
            print(f"可用设备: {', '.join(devices.keys())}")
            sys.exit(1)
        
        success = upload_to_device(args.device, args.image, args.name)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
