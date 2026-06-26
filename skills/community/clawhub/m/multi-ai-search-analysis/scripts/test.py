#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 快速验证安装和基本功能
"""

import asyncio
import sys
import os

# 设置 UTF-8 编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)
sys.path.insert(0, str(Path(__file__).parent.parent))

# 使用 ASCII 兼容符号
CHECK = '[OK]'
CROSS = '[FAIL]'

async def test_browser():
    """测试浏览器初始化"""
    print(f"\n{Fore.CYAN}[测试 1/3] 浏览器初始化...{Style.RESET_ALL}")
    
    try:
        from playwright.async_api import async_playwright
        
        playwright = await async_playwright().start()
        
        user_data_dir = str(Path(__file__).parent.parent / 'browser-profile-test')
        Path(user_data_dir).mkdir(exist_ok=True)
        
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            channel="msedge",
            args=['--disable-gpu', '--no-sandbox']
        )
        
        print(f"{Fore.GREEN}{CHECK} 浏览器初始化成功{Style.RESET_ALL}")
        
        # 打开测试页面
        page = await browser.new_page()
        await page.goto('https://www.bing.com', timeout=30000)
        await asyncio.sleep(2)
        
        print(f"{Fore.GREEN}{CHECK} 页面加载成功{Style.RESET_ALL}")
        
        await browser.close()
        print(f"{Fore.GREEN}{CHECK} 浏览器已关闭{Style.RESET_ALL}")
        
        # 清理测试目录
        import shutil
        try:
            shutil.rmtree(user_data_dir)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}{CROSS} 浏览器测试失败：{e}{Style.RESET_ALL}")
        return False

async def test_config():
    """测试配置文件"""
    print(f"\n{Fore.CYAN}[测试 2/3] 配置文件加载...{Style.RESET_ALL}")
    
    try:
        import json
        
        config_path = Path(__file__).parent.parent / 'config' / 'ai-platforms.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        platforms = config.get('platforms', [])
        print(f"{Fore.GREEN}{CHECK} 配置文件加载成功{Style.RESET_ALL}")
        print(f"  已配置平台：{len(platforms)}")
        for p in platforms:
            print(f"    - {p['name']}: {p['url']}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}{CROSS} 配置文件测试失败：{e}{Style.RESET_ALL}")
        return False

async def test_reporter():
    """测试报告生成器"""
    print(f"\n{Fore.CYAN}[测试 3/3] 报告生成器...{Style.RESET_ALL}")
    
    try:
        from reporter import generate_report
        
        test_results = [
            {
                'platform': 'DeepSeek',
                'content': '这是测试内容...',
                'success': True
            },
            {
                'platform': 'Qwen',
                'content': '这也是测试内容...',
                'success': True
            }
        ]
        
        output_path = generate_report(
            topic='测试主题',
            results=test_results,
            dimensions=['维度 1', '维度 2']
        )
        
        print(f"{Fore.GREEN}{CHECK} 报告生成成功：{output_path}{Style.RESET_ALL}")
        
        # 清理测试文件
        try:
            Path(output_path).unlink()
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}{CROSS} 报告生成器测试失败：{e}{Style.RESET_ALL}")
        return False

async def main():
    """主测试函数"""
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Multi-AI Search Analysis - 安装测试{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    
    results = []
    
    # 运行测试
    results.append(('浏览器', await test_browser()))
    results.append(('配置文件', await test_config()))
    results.append(('报告生成器', await test_reporter()))
    
    # 汇总结果
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  测试结果汇总{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    for name, success in results:
        if success:
            print(f"{Fore.GREEN}{CHECK} {name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{CROSS} {name}{Style.RESET_ALL}")
    
    success_count = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\n总计：{success_count}/{total} 通过")
    
    if success_count == total:
        print(f"\n{Fore.GREEN}所有测试通过！可以开始使用了{Style.RESET_ALL}")
        print(f"\n运行分析：{Fore.CYAN}python scripts/run.py -t '你的主题'{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}部分测试失败，请检查错误信息{Style.RESET_ALL}")
        print(f"运行安装：{Fore.CYAN}python scripts/install.py{Style.RESET_ALL}\n")

if __name__ == '__main__':
    asyncio.run(main())
