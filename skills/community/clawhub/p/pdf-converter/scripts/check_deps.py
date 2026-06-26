#!/usr/bin/env python3
"""
检查 PDF 转换器依赖是否已安装
"""

import sys
import subprocess

def check_package(package_name, import_name=None):
    """检查包是否已安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def check_poppler():
    """检查 poppler 是否已安装"""
    try:
        result = subprocess.run(['which', 'pdfinfo'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    print("🔍 检查 PDF 转换器依赖...\n")
    
    packages = [
        ("pdf2image", "pdf2image", "PDF 渲染"),
        ("python-pptx", "pptx", "PowerPoint 生成"),
        ("pdf2docx", "pdf2docx", "Word 生成"),
        ("Pillow", "PIL", "图片处理"),
    ]
    
    all_ok = True
    
    for package_name, import_name, description in packages:
        installed = check_package(package_name, import_name)
        status = "✅" if installed else "❌"
        print(f"{status} {package_name:20s} - {description}")
        if not installed:
            all_ok = False
    
    # 检查 poppler
    poppler_ok = check_poppler()
    status = "✅" if poppler_ok else "❌"
    print(f"{status} poppler-utils       - PDF 渲染引擎")
    if not poppler_ok:
        all_ok = False
    
    print()
    
    if all_ok:
        print("✅ 所有依赖已安装，可以开始使用！")
        print("\n使用示例:")
        print("  python3 skills/pdf-converter/scripts/convert.py file.pdf")
    else:
        print("❌ 缺少依赖，请安装:")
        print("\n1. 安装 Python 库:")
        print("   pip3 install --break-system-packages pdf2image python-pptx pdf2docx Pillow")
        print("\n2. 安装 poppler:")
        print("   macOS:  brew install poppler")
        print("   Ubuntu: sudo apt-get install poppler-utils")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
