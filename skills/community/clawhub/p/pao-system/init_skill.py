#!/usr/bin/env python3
"""
PAO 系统零配置初始化脚本
实现零配置启动，自动检测和配置所需环境
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


# 默认配置
DEFAULT_PORT = 8765
DEFAULT_HOST = "127.0.0.1"
DEFAULT_LOG_LEVEL = "INFO"


def detect_python_version():
    """检测 Python 版本"""
    version = sys.version_info
    print(f"[DETECT] Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[WARN] 建议使用 Python 3.8+")
        return False
    return True


def detect_dependencies():
    """检测依赖是否已安装"""
    required = [
        "websockets",
        "cryptography",
        "pydantic",
        "loguru",
        "psutil",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package} 已安装")
        except ImportError:
            print(f"[MISSING] {package} 未安装")
            missing.append(package)
    
    return missing


def install_dependencies(missing):
    """安装缺失的依赖"""
    if not missing:
        print("[INFO] 所有依赖已安装")
        return True
    
    print(f"[INFO] 开始安装缺失依赖: {missing}")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + missing,
            check=True,
        )
        print("[SUCCESS] 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 依赖安装失败: {e}")
        return False


def create_config():
    """创建初始配置文件"""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    config_path = config_dir / "pao_config.json"
    
    # 如果配置文件已存在，跳过
    if config_path.exists():
        print(f"[INFO] 配置文件已存在: {config_path}")
        return config_path
    
    config = {
        "server": {
            "host": DEFAULT_HOST,
            "port": DEFAULT_PORT,
        },
        "logging": {
            "level": DEFAULT_LOG_LEVEL,
            "file": "logs/pao.log",
        },
        "workers": {
            "enabled": True,
            "config_file": "workers.json",
        },
    }
    
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[SUCCESS] 配置文件已创建: {config_path}")
    
    return config_path


def create_log_directory():
    """创建日志目录"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    print(f"[INFO] 日志目录已创建: {log_dir}")
    return log_dir


def detect_port_available(port):
    """检测端口是否可用"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            print(f"[OK] 端口 {port} 可用")
            return True
    except OSError as e:
        print(f"[WARN] 端口 {port} 被占用: {e}")
        return False


def find_available_port(start_port=8765, max_attempts=20):
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        if detect_port_available(port):
            return port
    print(f"[ERROR] 未找到可用端口")
    return None


def init_skill():
    """初始化技能"""
    print("=" * 60)
    print("PAO 系统零配置初始化")
    print("=" * 60)
    print(f"[TIME] 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 步骤1: 检测 Python 版本
    print("[STEP 1/6] 检测 Python 版本...")
    if not detect_python_version():
        print("[ERROR] Python 版本不支持")
        return False
    print()
    
    # 步骤2: 检测依赖
    print("[STEP 2/6] 检测依赖...")
    missing = detect_dependencies()
    if missing:
        print(f"[INFO] 发现 {len(missing)} 个缺失依赖")
        answer = input("是否现在安装? [Y/n]: ").strip().lower()
        if answer in ("", "y", "yes"):
            if not install_dependencies(missing):
                print("[ERROR] 依赖安装失败")
                return False
        else:
            print("[INFO] 跳过依赖安装")
    print()
    
    # 步骤3: 创建配置
    print("[STEP 3/6] 创建配置文件...")
    config_path = create_config()
    print()
    
    # 步骤4: 创建日志目录
    print("[STEP 4/6] 创建日志目录...")
    create_log_directory()
    print()
    
    # 步骤5: 检测端口
    print("[STEP 5/6] 检测端口...")
    port = DEFAULT_PORT
    if not detect_port_available(port):
        print("[INFO] 尝试查找可用端口...")
        port = find_available_port()
        if port:
            print(f"[INFO] 将使用端口: {port}")
            # 更新配置
            config = json.loads(config_path.read_text(encoding='utf-8'))
            config["server"]["port"] = port
            config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f"[INFO] 配置已更新")
    print()
    
    # 步骤6: 生成启动脚本
    print("[STEP 6/6] 生成启动脚本...")
    create_start_script(port)
    print()
    
    # 完成
    print("=" * 60)
    print("[SUCCESS] 初始化完成!")
    print("=" * 60)
    print()
    print("下一步:")
    print(f"  1. 运行 python pao.py 启动 PAO 系统")
    print(f"  2. 或运行 start.bat 快速启动")
    print()
    
    return True


def create_start_script(port):
    """创建启动脚本"""
    # 创建 Windows 启动脚本
    bat_content = """@echo off
echo Starting PAO System...
python pao.py
pause
"""
    
    bat_path = Path("start.bat")
    bat_path.write_text(bat_content, encoding='utf-8')
    print(f"[SUCCESS] 启动脚本已创建: {bat_path}")
    
    # 创建 Unix 启动脚本
    sh_content = """#!/bin/bash
echo "Starting PAO System..."
python pao.py
"""
    
    sh_path = Path("start.sh")
    sh_path.write_text(sh_content, encoding='utf-8')
    print(f"[SUCCESS] 启动脚本已创建: {sh_path}")


if __name__ == "__main__":
    # 切换到脚本所在目录
    os.chdir(Path(__file__).parent)
    
    success = init_skill()
    
    sys.exit(0 if success else 1)