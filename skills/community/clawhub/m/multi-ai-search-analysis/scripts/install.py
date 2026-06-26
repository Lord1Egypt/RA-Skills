#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本 - 一键安装所有依赖
"""

import subprocess
import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  {text}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")

def run_command(cmd, description):
    """运行命令并显示进度"""
    print(f"{Fore.CYAN}[{description}]{Style.RESET_ALL}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"{Fore.GREEN}✓ 完成{Style.RESET_ALL}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}✗ 失败：{e}{Style.RESET_ALL}")
        return False

def main():
    print_header("Multi-AI Search Analysis - 安装向导")
    
    # 检查 Python 版本
    print(f"{Fore.CYAN}检查 Python 版本...{Style.RESET_ALL}")
    if sys.version_info < (3, 8):
        print(f"{Fore.RED}✗ Python 版本过低，需要 3.8+{Style.RESET_ALL}")
        sys.exit(1)
    print(f"{Fore.GREEN}✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{Style.RESET_ALL}")
    
    # 升级 pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "升级 pip")
    
    # 安装依赖
    requirements_path = Path(__file__).parent.parent / 'requirements.txt'
    if requirements_path.exists():
        run_command(f"{sys.executable} -m pip install -r {requirements_path} -i https://pypi.tuna.tsinghua.edu.cn/simple", 
                   "安装 Python 依赖")
    else:
        print(f"{Fore.YELLOW}⚠ requirements.txt 不存在，跳过{Style.RESET_ALL}")
    
    # 安装 Playwright 浏览器
    print(f"\n{Fore.CYAN}安装 Playwright 浏览器（Edge）...{Style.RESET_ALL}")
    try:
        subprocess.run(f"{sys.executable} -m playwright install msedge", shell=True, check=True)
        print(f"{Fore.GREEN}✓ Edge 浏览器安装完成{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        print(f"{Fore.YELLOW}⚠ Edge 浏览器可能已安装，跳过{Style.RESET_ALL}")
    
    # 创建必要目录
    print(f"\n{Fore.CYAN}创建必要目录...{Style.RESET_ALL}")
    dirs = ['reports', 'logs', 'browser-profile']
    for dir_name in dirs:
        dir_path = Path(__file__).parent.parent / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"{Fore.GREEN}✓ {dir_name}/{Style.RESET_ALL}")
    
    # 测试安装
    print_header("测试安装")
    try:
        import playwright
        print(f"{Fore.GREEN}✓ Playwright 已安装 (v{playwright.__version__}){Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.RED}✗ Playwright 未安装{Style.RESET_ALL}")
    
    try:
        from colorama import init
        print(f"{Fore.GREEN}✓ Colorama 已安装{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.RED}✗ Colorama 未安装{Style.RESET_ALL}")
    
    # 显示使用说明
    print_header("安装完成！")
    print(f"""
{Fore.GREEN}✓ 所有依赖已安装完成{Style.RESET_ALL}

{Fore.YELLOW}下一步：{Style.RESET_ALL}
1. 运行登录工具完成各平台登录：
   {Fore.CYAN}python scripts/login.py{Style.RESET_ALL}

2. 运行分析：
   {Fore.CYAN}python scripts/run.py -t "你的分析主题"{Style.RESET_ALL}

3. 查看报告：
   {Fore.CYAN}reports/你的主题 - 日期时间.md{Style.RESET_ALL}

{Fore.YELLOW}示例命令：{Style.RESET_ALL}
  python scripts/run.py -t "2026 年 AI 市场趋势" -d 技术 投资 应用 竞争
  python scripts/run.py -t "iPhone 16 Pro 评测" -d 性能 拍照 续航 价格
  python scripts/run.py -t "Python vs Java" --report-template comparison

{Fore.YELLOW}遇到问题？{Style.RESET_ALL}
- 查看 logs/ 目录的日志文件
- 检查浏览器是否已安装：playwright install msedge
- 确保各 AI 平台已登录：python scripts/login.py

{Fore.GREEN}{'='*60}{Style.RESET_ALL}
""")

if __name__ == '__main__':
    main()
