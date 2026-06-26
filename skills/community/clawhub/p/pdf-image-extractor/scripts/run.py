"""
PDF图片提取器 - 统一入口
支持三种模式，选择即可运行
"""

import os
import sys

def show_menu():
    """显示菜单"""
    print("=" * 50)
    print("📦 PDF图片提取器 - 小杰出品")
    print("=" * 50)
    print("")
    print("请选择模式：")
    print("")
    print("  1️⃣  原始高清模式")
    print("      ├─ 保持PDF原始分辨率")
    print("      ├─ 适合：印刷、高质量用途")
    print("      └─ 输出：原尺寸图片（5MB+）")
    print("")
    print("  2️⃣  标准尺寸模式")
    print("      ├─ 统一800x800正方形")
    print("      ├─ 适合：网站产品图、电商")
    print("      └─ 输出：约100KB JPG")
    print("")
    print("  3️⃣  压缩优化模式")
    print("      ├─ 400px内，50KB以内")
    print("      ├─ 适合：微信、抖音、小红书")
    print("      └─ 输出：约30KB JPG")
    print("")
    print("=" * 50)

def main():
    show_menu()
    
    choice = input("请输入选项 (1/2/3): ").strip()
    
    if choice == '1':
        print("\n🚀 启动原始高清模式...")
        import extract_original
        extract_original.main()
        
    elif choice == '2':
        print("\n🚀 启动标准尺寸模式...")
        import extract_standard
        extract_standard.main()
        
    elif choice == '3':
        print("\n🚀 启动压缩优化模式...")
        import extract_compress
        extract_compress.main()
        
    else:
        print("\n❌ 无效选项，请输入 1、2 或 3")
        print("或者直接运行单个脚本：")
        print("  python extract_original.py  # 原始高清")
        print("  python extract_standard.py  # 标准尺寸")
        print("  python extract_compress.py  # 压缩优化")
        return
    
    print("\n✅ 处理完成！")
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
