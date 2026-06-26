#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稳定性测试脚本 - 验证登录检测和选择器优化

测试内容：
1. 浏览器初始化
2. 各平台登录状态检测
3. 输入框选择器查找
4. 发送按钮选择器查找
5. 响应内容选择器查找
"""

import asyncio
import sys
import os
from pathlib import Path

# Windows 中文环境设置 UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

from colorama import init, Fore, Style

init(autoreset=True)
sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.async_api import async_playwright


# 导入配置
import json
config_path = Path(__file__).parent.parent / 'config' / 'ai-platforms.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)


class AIPlatform:
    """AI 平台配置"""
    def __init__(self, config: dict):
        self.name = config['name']
        self.url = config['url']
        self.selectors = config.get('selectors', {})


async def test_login_detection(platform: AIPlatform, page) -> bool:
    """测试登录状态检测"""
    try:
        await page.goto(platform.url, timeout=30000)
        await asyncio.sleep(2)
        
        # 检测输入框
        input_selectors = platform.selectors.get('input', 'textarea').split(', ')
        input_selectors.extend([
            '[role="textbox"]', '[role="combobox"]',
            '[contenteditable="true"]', 'textarea',
        ])
        
        has_input = False
        for selector in input_selectors:
            try:
                elem = await page.query_selector(selector, timeout=1000)
                if elem:
                    has_input = True
                    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} 找到输入框：{selector[:50]}")
                    break
            except:
                continue
        
        # 检测登录按钮
        login_selectors = [
            'button:has-text("登录")', 'button:has-text("Login")',
            'button:has-text("扫码")', '.login-btn',
        ]
        
        has_login_btn = False
        for selector in login_selectors:
            try:
                elem = await page.query_selector(selector, timeout=1000)
                if elem and await elem.is_visible():
                    has_login_btn = True
                    print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} 发现登录按钮：{selector[:50]}")
                    break
            except:
                continue
        
        if has_login_btn and not has_input:
            print(f"  {Fore.RED}[X]{Style.RESET_ALL} 未登录")
            return False
        elif has_input:
            print(f"  {Fore.GREEN}[OK]{Style.RESET_ALL} 已登录")
            return True
        else:
            print(f"  {Fore.YELLOW}[?]{Style.RESET_ALL} 状态不明")
            return True
            
    except Exception as e:
        print(f"  {Fore.RED}✗{Style.RESET_ALL} 检测失败：{e}")
        return False


async def test_selectors(platform: AIPlatform, page):
    """测试各元素选择器"""
    print(f"\n  {Fore.CYAN}选择器测试:{Style.RESET_ALL}")
    
    # 测试输入框选择器
    print(f"  - 输入框选择器...", end=' ')
    input_selectors = platform.selectors.get('input', 'textarea').split(', ')
    input_selectors.extend(['[role="textbox"]', '[contenteditable="true"]', 'textarea'])
    
    found_input = False
    for selector in input_selectors[:10]:  # 只测试前 10 个
        try:
            elem = await page.query_selector(selector, timeout=1000)
            if elem:
                found_input = True
                print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} (找到：{selector[:40]})")
                break
        except:
            continue
    
    if not found_input:
        print(f"{Fore.RED}[X]{Style.RESET_ALL} (未找到)")
    
    # 测试发送按钮选择器
    print(f"  - 发送按钮选择器...", end=' ')
    send_selectors = platform.selectors.get('send', 'button').split(', ')
    send_selectors.extend(['button[type="submit"]', '[aria-label*="发送"]'])
    
    found_send = False
    for selector in send_selectors[:10]:
        try:
            elem = await page.query_selector(selector, timeout=1000)
            if elem:
                found_send = True
                print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} (找到：{selector[:40]})")
                break
        except:
            continue
    
    if not found_send:
        print(f"{Fore.RED}[X]{Style.RESET_ALL} (未找到)")
    
    # 测试响应内容选择器（需要实际发送消息才能测试，这里只检查配置）
    response_selectors = platform.selectors.get('response', '.markdown-body').split(', ')
    print(f"  - 响应内容选择器：{Fore.GREEN}[OK]{Style.RESET_ALL} (配置了{len(response_selectors)}个)")


async def main():
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Multi-AI Search Analysis - 稳定性测试 v2.0{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    # 初始化浏览器
    print(f"{Fore.CYAN}[1/3] 初始化浏览器...{Style.RESET_ALL}")
    playwright = await async_playwright().start()
    
    user_data_dir = str(Path(__file__).parent.parent / 'browser-profile')
    Path(user_data_dir).mkdir(exist_ok=True)
    
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        channel="msedge",
        args=['--disable-gpu', '--no-sandbox']
    )
    print(f"{Fore.GREEN}[OK] 浏览器已就绪\n{Style.RESET_ALL}")
    
    # 测试各平台
    platforms = [AIPlatform(p) for p in config['platforms']]
    
    print(f"{Fore.CYAN}[2/3] 测试各平台登录状态和选择器...{Style.RESET_ALL}\n")
    
    results = []
    for platform in platforms:
        print(f"{Fore.YELLOW}测试：{platform.name}{Style.RESET_ALL}")
        
        try:
            page = await browser.new_page()
            is_logged = await test_login_detection(platform, page)
            
            if is_logged:
                await test_selectors(platform, page)
            
            await page.close()
            results.append((platform.name, is_logged))
            print()
            
        except Exception as e:
            print(f"  {Fore.RED}[X] 测试失败：{e}{Style.RESET_ALL}\n")
            results.append((platform.name, False))
    
    # 关闭浏览器
    print(f"{Fore.CYAN}[3/3] 清理...{Style.RESET_ALL}")
    await browser.close()
    await playwright.stop()
    
    # 汇总结果
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  测试结果汇总{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    for name, is_logged in results:
        if is_logged:
            status = f"{Fore.GREEN}[OK] 已登录{Style.RESET_ALL}"
        else:
            status = f"{Fore.RED}[X] 未登录{Style.RESET_ALL}"
        print(f"  {name}: {status}")
    
    logged_count = sum(1 for _, is_logged in results if is_logged)
    print(f"\n  总计：{logged_count}/{len(platforms)} 平台已登录")
    
    if logged_count == len(platforms):
        print(f"\n{Fore.GREEN}[OK] 所有平台已就绪，可以运行分析！{Style.RESET_ALL}")
        print(f"\n  运行命令：python scripts/run.py -t \"你的主题\"")
    else:
        print(f"\n{Fore.YELLOW}[!] 有平台未登录，请先运行登录工具：{Style.RESET_ALL}")
        print(f"  python scripts/login.py")
    
    print()


if __name__ == '__main__':
    asyncio.run(main())
