#!/usr/bin/env python3
"""
MLX Local AI 依赖检查脚本
"""

import sys
import subprocess

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 版本过低，需要 3.10+")
        return False
    print("✓ Python 版本符合要求")
    return True

def check_architecture():
    """检查系统架构"""
    import platform
    arch = platform.machine()
    print(f"系统架构: {arch}")
    if arch != "arm64":
        print("❌ 此脚本仅支持 Apple Silicon (arm64)")
        return False
    print("✓ 系统架构符合要求")
    return True

def check_package(package_name):
    """检查 Python 包是否安装"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {package_name} 未安装")
        return False

def check_mlx():
    """检查 MLX 是否可用"""
    try:
        import mlx.core as mx
        print(f"✓ MLX 版本: {mx.__version__}")
        
        # 检查 Metal
        if mx.metal.is_available():
            print("✓ Metal GPU 可用")
        else:
            print("⚠️ Metal GPU 不可用")
        return True
    except ImportError:
        print("❌ MLX 未安装")
        return False

def main():
    print("=" * 50)
    print("MLX Local AI 依赖检查")
    print("=" * 50)
    print()
    
    checks = [
        ("Python 版本", check_python_version),
        ("系统架构", check_architecture),
    ]
    
    packages = [
        "mlx",
        "mlx_lm",
        "sentence_transformers",
        "flask",
        "numpy",
        "requests",
    ]
    
    print("【系统检查】")
    for name, check in checks:
        check()
        print()
    
    print("【包检查】")
    for pkg in packages:
        check_package(pkg)
    
    print()
    print("【MLX 详细检查】")
    check_mlx()
    
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
