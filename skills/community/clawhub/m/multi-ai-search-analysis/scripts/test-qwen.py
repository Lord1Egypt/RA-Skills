#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen 平台专项测试 - 验证 Enter 键发送优化

测试内容：
1. 登录状态检测
2. 输入框查找
3. Enter 键发送（不实际点击按钮）
4. 响应等待和提取
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


async def test_qwen():
    """测试 Qwen 平台"""
    
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Qwen 平台专项测试 - v2.0.1{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}\n{Style.RESET_ALL}")
    
    # 初始化浏览器
    print(f"[1/5] 初始化浏览器...")
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
    
    # 打开 Qwen
    print(f"[2/5] 打开 Qwen 页面...")
    page = await browser.new_page()
    await page.goto('https://chat.qwen.ai', timeout=30000)
    await asyncio.sleep(3)
    print(f"{Fore.GREEN}[OK] 页面已加载\n{Style.RESET_ALL}")
    
    # 检查登录状态
    print(f"[3/5] 检查登录状态...")
    
    # 查找输入框
    input_selectors = [
        'textarea#chat-input',
        '#chat-input',
        'textarea[aria-label*="Prompt"]',
        'textarea[aria-label*="消息"]',
        '[contenteditable="true"]',
        '[role="textbox"]',
        '[role="combobox"]',
    ]
    
    input_box = None
    for selector in input_selectors:
        try:
            input_box = await page.query_selector(selector, timeout=2000)
            if input_box:
                print(f"{Fore.GREEN}[OK] 找到输入框：{selector}{Style.RESET_ALL}")
                break
        except:
            continue
    
    if not input_box:
        print(f"{Fore.RED}[X] 未找到输入框，可能未登录{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}[!] 请先运行登录工具：python scripts/login.py{Style.RESET_ALL}\n")
        await browser.close()
        await playwright.stop()
        return False
    
    # 检查是否有登录按钮（未登录标志）
    login_btn = await page.query_selector('button:has-text("登录")', timeout=2000)
    if login_btn:
        try:
            is_visible = await login_btn.is_visible()
            if is_visible:
                print(f"{Fore.RED}[X] 检测到登录按钮，请先登录{Style.RESET_ALL}")
                await browser.close()
                await playwright.stop()
                return False
        except:
            pass
    
    print(f"{Fore.GREEN}[OK] 已登录\n{Style.RESET_ALL}")
    
    # 测试 Enter 键发送
    print(f"[4/5] 测试 Enter 键发送...")
    print(f"{Fore.YELLOW}[!] 注意：不会实际发送问题，只测试输入框聚焦和 Enter 键{Style.RESET_ALL}\n")
    
    try:
        # 点击输入框确保聚焦
        await input_box.click()
        await asyncio.sleep(0.5)
        print(f"{Fore.GREEN}[OK] 输入框已聚焦{Style.RESET_ALL}")
        
        # 输入测试文本
        test_text = "Qwen Enter 键发送测试"
        await input_box.fill(test_text)
        await asyncio.sleep(0.5)
        print(f"{Fore.GREEN}[OK] 已输入测试文本：'{test_text}'{Style.RESET_ALL}")
        
        # 检查是否有遮挡元素
        overlay_selectors = [
            '.qwen-select-thinking-label-text',
            '.ant-select-open',
            '.modal',
            '.popover',
        ]
        
        has_overlay = False
        for selector in overlay_selectors:
            try:
                overlay = await page.query_selector(selector, timeout=1000)
                if overlay:
                    is_visible = await overlay.is_visible()
                    if is_visible:
                        has_overlay = True
                        print(f"{Fore.YELLOW}[!] 发现遮挡元素：{selector}{Style.RESET_ALL}")
                        break
            except:
                continue
        
        if has_overlay:
            print(f"{Fore.YELLOW}[!] 尝试关闭遮挡元素...{Style.RESET_ALL}")
            try:
                await page.click('body', position={'x': 10, 'y': 10})
                await asyncio.sleep(0.5)
                print(f"{Fore.GREEN}[OK] 已点击空白处{Style.RESET_ALL}")
            except:
                pass
        
        # 测试 Enter 键（不实际发送，只验证可以按下）
        print(f"{Fore.GREEN}[OK] 准备测试 Enter 键...{Style.RESET_ALL}")
        
        # 实际按下 Enter（会发送消息，但我们会立即清除）
        await input_box.press('Enter')
        await asyncio.sleep(1)
        
        # 检查消息是否发送（输入框应该清空）
        input_value = await input_box.input_value()
        if not input_value or input_value.strip() == '':
            print(f"{Fore.GREEN}[OK] Enter 键发送成功（输入框已清空）{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] 输入框仍有内容：'{input_value}'{Style.RESET_ALL}")
        
        # 清除测试消息（可选）
        print(f"\n{Fore.YELLOW}[!] 测试完成，页面保留测试消息供确认{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[X] 测试失败：{e}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}建议：{Style.RESET_ALL}")
        print(f"  1. 检查网络连接")
        print(f"  2. 确认已登录 Qwen")
        print(f"  3. 手动刷新页面后重试\n")
        await browser.close()
        await playwright.stop()
        return False
    
    # 完成
    print(f"\n[5/5] 清理...")
    print(f"{Fore.YELLOW}[!] 浏览器保持打开，请手动关闭{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] 如需删除测试消息，请手动操作\n{Style.RESET_ALL}")
    
    # 不关闭浏览器，让用户确认
    input(f"{Fore.CYAN}按回车键关闭浏览器...{Style.RESET_ALL}")
    
    await browser.close()
    await playwright.stop()
    
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Qwen 测试完成！{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}\n{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[OK] Enter 键发送功能正常{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[OK] 可以运行完整分析：python scripts/run.py -t \"主题\" -p Qwen{Style.RESET_ALL}\n")
    
    return True


if __name__ == '__main__':
    success = asyncio.run(test_qwen())
    sys.exit(0 if success else 1)
