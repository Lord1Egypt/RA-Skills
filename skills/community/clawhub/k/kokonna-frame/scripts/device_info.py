#!/usr/bin/env python3
"""
KoKonna 画框设备信息查询工具

用法：
    python3 device_info.py --device living_room
    python3 device_info.py --device all
    python3 device_info.py --list-devices
"""

import argparse
import json
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


def show_device_info(device_name: str):
    """显示设备信息"""
    print(f"\n=== {device_name} ===")
    
    try:
        frame = KoKonnaFrame(device=device_name)
        info = frame.get_device_info()
        
        if info:
            # 格式化输出
            print(f"状态: {'在线' if info.get('online') else '离线'}")
            print(f"电池: {info.get('batteryLevel', 'N/A')}%")
            print(f"充电中: {'是' if info.get('isCharging') else '否'}")
            print(f"固件: {info.get('firmware', 'N/A')}")
            print(f"昵称: {info.get('nickname', 'N/A')}")
            print(f"时区: {info.get('timezone', 'N/A')}")
            print(f"屏幕: {info.get('screenWidth', 'N/A')}x{info.get('screenHeight', 'N/A')} (旋转{info.get('screenRotate', 0)}°)")
            print(f"实际显示: {frame.width}x{frame.height}")
            
            if info.get('lastHeartbeat'):
                print(f"最后心跳: {info.get('lastHeartbeat')}")
        else:
            print("无法获取设备信息")
    except Exception as e:
        print(f"查询失败: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="KoKonna 画框设备信息查询",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --device living_room
  %(prog)s --device all
  %(prog)s --list-devices
        """
    )
    
    parser.add_argument(
        "-d", "--device",
        required=False,
        help="设备名称（在 config.yaml 中配置）或 'all' 查询所有设备"
    )
    
    parser.add_argument(
        "-l", "--list-devices",
        action="store_true",
        help="列出所有可用设备"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式"
    )
    
    args = parser.parse_args()
    
    # 列出设备
    if args.list_devices:
        list_available_devices()
        return
    
    # 检查必需参数
    if not args.device:
        parser.print_help()
        sys.exit(1)
    
    # 获取可用设备
    config = load_config()
    devices = config.get("devices", {})
    
    if not devices:
        print("错误: 未配置任何设备")
        print("请在 ~/.openclaw/skills/kokonna-frame/config.yaml 中添加设备配置。")
        sys.exit(1)
    
    # 查询
    if args.device == "all":
        # 查询所有设备
        for device_name in devices.keys():
            show_device_info(device_name)
    else:
        # 查询指定设备
        if args.device not in devices:
            print(f"错误: 未知设备 '{args.device}'")
            print(f"可用设备: {', '.join(devices.keys())}")
            sys.exit(1)
        
        show_device_info(args.device)


if __name__ == "__main__":
    main()
