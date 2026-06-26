#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖安装诊断工具
帮助诊断和解决依赖安装问题
"""

import sys
import os
from pathlib import Path

def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def check_python_version():
    """检查 Python 版本"""
    print_header("Python 版本信息")
    version = sys.version_info
    print(f"Python 版本：{sys.version}")
    print(f"主版本号：{version.major}.{version.minor}.{version.micro}")
    print(f"平台：{sys.platform}")
    
    # 构建版本标识符（如 cp313）
    version_tag = f"cp{version.major}{version.minor}"
    print(f"\nWheel 文件版本标识应为：{version_tag}")
    return version_tag

def check_dependencies_dir():
    """检查 dependencies 目录"""
    print_header("Dependencies 目录检查")
    
    script_dir = Path(__file__).parent
    deps_dir = script_dir / "dependencies"
    
    print(f"技能目录：{script_dir.absolute()}")
    print(f"依赖目录：{deps_dir.absolute()}")
    
    if not deps_dir.exists():
        print(f"\n❌ 错误：dependencies 目录不存在！")
        return []
    
    whl_files = list(deps_dir.glob("*.whl"))
    
    if not whl_files:
        print(f"\n❌ 错误：dependencies 目录中没有 .whl 文件！")
        return []
    
    print(f"\n✓ 找到 {len(whl_files)} 个 wheel 文件:")
    for whl in sorted(whl_files):
        size_mb = whl.stat().st_size / (1024 * 1024)
        print(f"  - {whl.name} ({size_mb:.1f} MB)")
    
    return whl_files

def check_wheel_compatibility(whl_files, expected_version_tag):
    """检查 wheel 文件与 Python 版本的兼容性"""
    print_header("Wheel 文件兼容性检查")
    
    compatible_count = 0
    incompatible_count = 0
    
    for whl in whl_files:
        filename = whl.name
        
        # 提取版本标签（如 cp313）
        parts = filename.split("-")
        if len(parts) >= 3:
            version_part = parts[-2]  # 例如 cp313-cp313-win_amd64
            file_version = version_part.split("-")[0]  # cp313
            
            is_compatible = file_version == expected_version_tag or "none" in file_version
            
            if is_compatible:
                print(f"  ✓ {filename[:50]}... ({file_version}) - 兼容")
                compatible_count += 1
            else:
                print(f"  ❌ {filename[:50]}... ({file_version}) - 不兼容，需要 {expected_version_tag}")
                incompatible_count += 1
    
    print(f"\n总计：{compatible_count} 个兼容，{incompatible_count} 个不兼容")
    return incompatible_count == 0

def check_pip():
    """检查 pip 状态"""
    print_header("Pip 状态检查")
    
    import subprocess
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ Pip 版本：{result.stdout.strip()}")
        else:
            print(f"❌ Pip 检查失败：{result.stderr.strip()}")
    except Exception as e:
        print(f"❌ 无法执行 pip：{e}")

def check_installed_packages():
    """检查已安装的包"""
    print_header("已安装的依赖包")
    
    required_packages = [
        'psycopg2-binary', 'psycopg2',
        'pandas', 'openpyxl', 'numpy', 
        'python-dateutil', 'tzdata', 'et_xmlfile'
    ]
    
    import subprocess
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            installed_lines = result.stdout.strip().split('\n')[2:]  # 跳过表头
            installed_names = [line.split()[0].lower() for line in installed_lines if line.strip()]
            
            for pkg in required_packages:
                pkg_name = pkg.lower().replace('-', '_').replace('binary', '')
                found = any(pkg_name in name for name in installed_names)
                
                if found:
                    print(f"  ✓ {pkg} - 已安装")
                else:
                    print(f"  ❌ {pkg} - 未安装")
        else:
            print(f"❌ 无法获取已安装包列表")
    except Exception as e:
        print(f"❌ 检查失败：{e}")

def provide_solution(all_compatible):
    """提供解决方案"""
    print_header("建议的解决方案")
    
    if all_compatible:
        print("""
✅ 所有检查通过！如果安装仍然失败，请尝试：

1. 使用绝对路径重新安装：
   cd <技能目录>/scripts
   pip install --no-index --find-links=<完整路径>/scripts/dependencies -r scripts/requirements.txt

2. 查看详细错误日志：
   pip install --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt -v

3. 尝试在线安装（如果可以访问网络）：
   pip install psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile
""")
    else:
        print("""
❌ 发现 wheel 文件与 Python 版本不匹配！

解决方案：

1. 下载与当前 Python 版本匹配的 wheel 文件：
   
   在有网络的机器上执行：
   pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d scripts/dependencies
   
2. 将下载的 wheel 文件复制到内网机器的 scripts/dependencies 目录

3. 重新运行安装脚本：
   Windows: .\\scripts\\install-dependencies.bat
   Linux/Mac: ./scripts/install-dependencies.sh

4. 或者使用在线安装（如果可以访问网络）：
   pip install psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile
""")

def main():
    """主函数"""
    print_header("PostgreSQL Tool 依赖安装诊断工具")
    
    # 1. 检查 Python 版本
    version_tag = check_python_version()
    
    # 2. 检查 dependencies 目录
    whl_files = check_dependencies_dir()
    
    if not whl_files:
        print("\n请确保 wheel 文件已下载到 dependencies 目录")
        return 1
    
    # 3. 检查兼容性
    all_compatible = check_wheel_compatibility(whl_files, version_tag)
    
    # 4. 检查 pip
    check_pip()
    
    # 5. 检查已安装的包
    check_installed_packages()
    
    # 6. 提供解决方案
    provide_solution(all_compatible)
    
    print_header("诊断完成")
    return 0 if all_compatible else 1

if __name__ == "__main__":
    sys.exit(main())
