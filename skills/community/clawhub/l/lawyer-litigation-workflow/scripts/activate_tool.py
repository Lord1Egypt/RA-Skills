#!/usr/bin/env python3
"""
激活工具 v1.0
用户购买专业版后，使用此工具输入激活码升级许可。

用法：
  python activate_tool.py --key YOUR_ACTIVATION_KEY

激活码获取方式：
  联系开发者（马律）提供设备ID后获取一对一激活码。
  设备ID可通过 --show-device 查看。
"""

import hashlib
import hmac
import json
import sys
from pathlib import Path
from license_manager import LicenseManager


def show_device_info():
    """显示设备信息，供用户提供给开发者生成激活码"""
    lm = LicenseManager()
    print(f"设备ID: {lm.data.get('device_id', '未初始化')}")
    print(f"当前许可: {lm.status()['tier']}")
    print(f"已用次数: {lm.status()['used']}")
    print()
    print("请将设备ID发送给开发者以获取激活码。")
    print("联系方式: 马律 | wx: fanshu0530 | email: mxl@dongrun-law.com")


def show_pricing():
    """显示价格信息"""
    print("""
价格方案:
  专业版（月付）  299元/月
  专业版（年付）  2999元/年（省589元）
  企业版          企业专属部署，联系定制报价

联系: 马律（山东东润律师事务所）
微信: fanshu0530
邮箱: mxl@dongrun-law.com
""")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="律师工作流激活工具")
    parser.add_argument("--key", type=str, help="激活码（从开发者处获取）")
    parser.add_argument("--show-device", action="store_true", help="显示设备ID（发给开发者以获取激活码）")
    parser.add_argument("--pricing", action="store_true", help="显示价格方案")
    args = parser.parse_args()

    if args.show_device:
        show_device_info()
    elif args.pricing:
        show_pricing()
    elif args.key:
        lm = LicenseManager()
        ok, msg = lm.activate(args.key)
        print(msg)
        if ok:
            print()
            s = lm.status()
            print(f"版本: {s['tier']}")
            print(f"剩余次数: {s['remaining']}")
            print("您现在可以使用全部功能。")
        sys.exit(0 if ok else 1)
    else:
        parser.print_help()
        print()
        show_pricing()
