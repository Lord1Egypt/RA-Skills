#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA Cookie 自动获取脚本（Playwright自动化）

此脚本尝试使用Playwright自动化获取IMA Cookie。

注意：由于IMA需要微信扫码登录，可能需要用户手动授权。

使用方法：
    python get_ima_cookie_playwright.py
    
Cookie获取后会自动保存到 ~/.hermes/.env
"""

import asyncio
import re
import os
import sys
from pathlib import Path

# 尝试导入playwright
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ 未安装 playwright，请先安装：")
    print("   pip install playwright")
    print("   playwright install chromium")
    sys.exit(1)


class IMACookieFetcher:
    """IMA Cookie 获取器"""
    
    IMA_URL = "https://ima.qq.com"
    ENV_FILE = Path.home() / ".hermes" / ".env"
    
    def __init__(self):
        self.cookie_str = None
        self.browser = None
        self.context = None
        self.page = None
        
    async def run(self):
        """运行获取流程"""
        print("=" * 70)
        print("IMA Cookie 自动获取工具 (Playwright)")
        print("=" * 70)
        
        async with async_playwright() as p:
            # 启动浏览器
            print("\n📂 启动 Chromium 浏览器...")
            self.browser = await p.chromium.launch(
                headless=False,  # 需要可见以便扫码
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox'
                ]
            )
            
            # 创建上下文（模拟真实浏览器）
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # 添加额外的浏览器特征
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            self.page = await self.context.new_page()
            
            print(f"\n🌐 打开 IMA: {self.IMA_URL}")
            await self.page.goto(self.IMA_URL, wait_until='networkidle', timeout=60000)
            
            # 检查是否需要登录
            print("\n⏳ 等待用户登录...")
            print("   请在浏览器窗口中使用微信扫码登录")
            
            # 等待登录成功 - 检查URL变化或页面内容
            max_wait = 180  # 最多等3分钟
            waited = 0
            
            while waited < max_wait:
                await asyncio.sleep(5)
                waited += 5
                
                # 检查当前URL
                current_url = self.page.url
                print(f"   [{waited}s] 当前URL: {current_url[:60]}...")
                
                # 如果URL包含wikis，说明已登录
                if 'wikis' in current_url or 'ima.qq.com' in current_url:
                    # 尝试获取Cookie
                    cookies = await self.context.cookies()
                    cookie_dict = {c['name']: c['value'] for c in cookies}
                    
                    if 'IMA-TOKEN' in cookie_dict:
                        print("\n✅ 检测到登录成功！")
                        break
                
                # 检查页面是否包含登录后的元素
                try:
                    title = await self.page.title()
                    if 'IMA' in title or '知识' in title:
                        break
                except:
                    pass
            
            # 获取Cookie
            print("\n📋 提取 Cookie...")
            cookies = await self.context.cookies()
            
            # 构建Cookie字符串
            cookie_parts = []
            for c in cookies:
                cookie_parts.append(f"{c['name']}={c['value']}")
            self.cookie_str = "; ".join(cookie_parts)
            
            # 检查关键Cookie
            if 'IMA-TOKEN=' not in self.cookie_str:
                print("\n⚠️  未检测到 IMA-TOKEN，可能登录未完成或需要更多操作")
                print("   请确保扫码登录成功后再试")
                return False
            
            print(f"\n✅ 成功获取 Cookie！")
            print(f"   Cookie长度: {len(self.cookie_str)} 字符")
            print(f"   IMA-TOKEN: {self.cookie_str[:50]}...")
            
            # 保存到.env
            self.save_to_env()
            
            await self.browser.close()
            return True
    
    def save_to_env(self):
        """保存Cookie到.env文件"""
        print(f"\n💾 保存到 {self.ENV_FILE}...")
        
        # 读取现有.env
        env_content = ""
        if self.ENV_FILE.exists():
            with open(self.ENV_FILE, 'r') as f:
                env_content = f.read()
        
        # 检查是否已有IMA_COOKIE
        if 'IMA_COOKIE=' in env_content:
            # 替换现有值
            env_content = re.sub(
                r'IMA_COOKIE=.*?(?:\n|$)',
                f'IMA_COOKIE="{self.cookie_str}"\n',
                env_content
            )
        else:
            # 添加新行
            env_content += f'\nIMA_COOKIE="{self.cookie_str}"\n'
        
        # 写入文件
        with open(self.ENV_FILE, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Cookie 已保存到 IMA_COOKIE")


async def main():
    fetcher = IMACookieFetcher()
    success = await fetcher.run()
    
    if success:
        print("\n" + "=" * 70)
        print("🎉 Cookie 获取成功！")
        print("=" * 70)
        print("\n下一步：")
        print("   python ./skills/ima_knowledge_base/test_knowledge_base.py \"$IMA_COOKIE\"")
        print("\n或运行完整测试：")
        print("   python ./skills/ima_knowledge_base/get_ima_cookie_guide.py \"$IMA_COOKIE\"")
    else:
        print("\n❌ Cookie 获取失败")
        print("\n备选方案：请手动获取Cookie：")
        print("   1. 打开 https://ima.qq.com")
        print("   2. 登录后按 F12 打开开发者工具")
        print("   3. Network -> 刷新页面 -> 点击任意请求 -> 复制 Cookie")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
