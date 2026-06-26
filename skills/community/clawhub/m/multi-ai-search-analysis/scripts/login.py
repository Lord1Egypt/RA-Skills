#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录工具 - 打开所有 AI 平台供用户手动登录
"""

import asyncio
import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)
sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.async_api import async_playwright


async def login_all():
    """打开所有平台供用户登录"""
    
    platforms = [
        {"name": "DeepSeek", "url": "https://chat.deepseek.com"},
        {"name": "Qwen", "url": "https://chat.qwen.ai"},
        {"name": "豆包", "url": "https://www.doubao.com"},
        {"name": "Kimi", "url": "https://kimi.moonshot.cn"},
        {"name": "Gemini", "url": "https://gemini.google.com"},
    ]
    
    print(f"\n{Fore.GREEN}========================================{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Multi-AI 登录工具{Style.RESET_ALL}")
    print(f"{Fore.GREEN}========================================{Style.RESET_ALL}\n")
    
    playwright = await async_playwright().start()
    
    # 使用持久化上下文保存登录状态
    user_data_dir = str(Path(__file__).parent.parent / 'browser-profile')
    Path(user_data_dir).mkdir(exist_ok=True)
    
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=['--disable-gpu', '--no-sandbox']
    )
    
    print(f"{Fore.CYAN}正在打开各平台登录页面...{Style.RESET_ALL}\n")
    
    # 为每个平台打开一个标签页
    pages = []
    for i, platform in enumerate(platforms):
        if i == 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
        
        await page.goto(platform['url'], timeout=30000)
        pages.append((platform['name'], page))
        
        print(f"{Fore.GREEN}✓ [{platform['name']}] 已打开{Style.RESET_ALL}")
        await asyncio.sleep(1)
    
    print(f"\n{Fore.YELLOW}========================================{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}请在每个标签页中完成登录{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}========================================{Style.RESET_ALL}\n")
    
    print("登录方式：")
    print("  - DeepSeek: 微信扫码或手机号")
    print("  - Qwen: GitHub/Google/Apple 账号")
    print("  - 豆包：手机号 + 验证码")
    print("  - Kimi: 手机号 + 验证码")
    print("  - Gemini: Google 账号（需要网络环境支持）")
    print()
    
    input(f"{Fore.CYAN}完成后按回车键关闭浏览器...{Style.RESET_ALL}")
    
    await browser.close()
    
    print(f"\n{Fore.GREEN}✓ 登录状态已保存{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ 可以运行分析脚本了{Style.RESET_ALL}\n")
    print(f"  命令：python scripts/run.py --topic \"你的主题\"{Style.RESET_ALL}\n")


if __name__ == '__main__':
    asyncio.run(login_all())
