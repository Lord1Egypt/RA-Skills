#!/usr/bin/env python3
"""
演示功能 - 授权通过后才能执行
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_license import check_license


def main():
    # 第一步：检查授权
    valid, msg = check_license()
    if not valid:
        print(f"\n❌ 授权失败: {msg}", file=sys.stderr)
        print("\n购买授权请访问: https://your-website.com/buy", file=sys.stderr)
        sys.exit(1)
    
    # 第二步：授权通过，执行实际功能
    print("✅ 授权验证通过！")
    print("\n这是收费技能的演示功能：")
    print("-----------------------------------")
    print("📝 这里是付费才能使用的核心功能")
    print("💡 你可以替换成你的实际业务逻辑")
    print("🔑 当前授权有效，功能正常运行")
    print("-----------------------------------")


if __name__ == "__main__":
    main()
