#!/usr/bin/env python3
"""
Test script: Navigate sina.com -> Military section -> Find Iran-related news -> Focus on first match
"""

import asyncio
import json
import time
from playwright.async_api import async_playwright


async def main():
    print("=" * 60)
    print("🚀 启动浏览器...")
    print("=" * 60)

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,
        slow_mo=100,
        channel="chrome",
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
        ]
    )
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = await context.new_page()

    # Capture network responses
    api_responses = []
    async def on_response(response):
        try:
            ct = response.headers.get('content-type', '')
            if response.request.resource_type in ['xhr', 'fetch'] and 'json' in ct:
                body = await response.json()
                api_responses.append({
                    "url": response.url[:120],
                    "status": response.status,
                    "body_preview": str(body)[:200]
                })
        except:
            pass
    page.on("response", on_response)

    # ========== Step 1: Navigate to sina.com ==========
    print("\n📌 Step 1: 访问 www.sina.com ...")
    await page.goto("https://www.sina.com.cn", wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(2)
    title = await page.title()
    print(f"   页面标题: {title}")
    print(f"   当前 URL: {page.url}")

    # ========== Step 2: Find military section ==========
    print("\n📌 Step 2: 查找军事板块链接...")

    # Find all links that contain 军事
    mil_links = await page.evaluate('''
        () => {
            return Array.from(document.querySelectorAll('a'))
                .filter(a => {
                    const text = a.innerText.trim();
                    return text.includes('军事') && text.length < 20;
                })
                .map(a => ({
                    text: a.innerText.trim(),
                    href: a.href
                }))
                .slice(0, 10);
        }
    ''')

    if mil_links:
        print(f"   找到 {len(mil_links)} 个军事相关链接:")
        for link in mil_links[:5]:
            print(f"     - {link['text']} -> {link['href']}")

        # Click the first military link
        target = mil_links[0]
        print(f"\n   ➡️  点击: {target['text']} ({target['href']})")

        # Navigate to military section
        await page.goto(target['href'], wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        print(f"   当前 URL: {page.url}")
        print(f"   页面标题: {await page.title()}")
    else:
        # Fallback: try direct URL
        print("   未找到军事链接，直接访问 mil.news.sina.com.cn ...")
        await page.goto("https://mil.news.sina.com.cn/", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        print(f"   当前 URL: {page.url}")
        print(f"   页面标题: {await page.title()}")

    # ========== Step 3: Scroll to load more content ==========
    print("\n📌 Step 3: 滚动页面加载更多内容...")
    for i in range(3):
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        await asyncio.sleep(0.8)
    # Scroll back to top
    await page.evaluate('window.scrollTo(0, 0)')
    await asyncio.sleep(0.5)

    # ========== Step 4: Search for Iran-related content ==========
    print("\n📌 Step 4: 搜索'伊朗'相关内容...")

    iran_results = await page.evaluate('''
        () => {
            const keyword = "伊朗";
            const results = [];

            // Search in all links (most news items are links)
            const links = document.querySelectorAll('a');
            for (const a of links) {
                const text = a.innerText.trim();
                if (text.includes(keyword) && text.length > 5 && text.length < 200) {
                    const rect = a.getBoundingClientRect();
                    // Build a unique CSS selector
                    let selector = '';
                    if (a.id) {
                        selector = '#' + a.id;
                    } else if (a.className) {
                        const cls = a.className.split(/\\s+/).filter(c => c && !c.includes(':')).slice(0, 2).join('.');
                        if (cls) selector = 'a.' + cls;
                    }
                    results.push({
                        text: text.substring(0, 100),
                        href: a.href,
                        tagName: a.tagName,
                        selector: selector,
                        position: {
                            top: rect.top + window.scrollY,
                            left: rect.left,
                            width: rect.width,
                            height: rect.height
                        }
                    });
                }
            }

            // Also search in text nodes (headings, paragraphs, etc.)
            const textEls = document.querySelectorAll('h1, h2, h3, h4, h5, p, span, li, div');
            for (const el of textEls) {
                // Only direct text content (avoid duplicating parent text)
                const directText = Array.from(el.childNodes)
                    .filter(n => n.nodeType === 3)
                    .map(n => n.textContent.trim())
                    .join('');
                if (directText.includes(keyword) && directText.length > 5) {
                    const rect = el.getBoundingClientRect();
                    let selector = '';
                    if (el.id) {
                        selector = '#' + el.id;
                    } else if (el.className) {
                        const cls = el.className.split(/\\s+/).filter(c => c && !c.includes(':')).slice(0, 2).join('.');
                        if (cls) selector = el.tagName.toLowerCase() + '.' + cls;
                    }
                    results.push({
                        text: directText.substring(0, 100),
                        href: el.closest('a')?.href || null,
                        tagName: el.tagName,
                        selector: selector,
                        position: {
                            top: rect.top + window.scrollY,
                            left: rect.left,
                            width: rect.width,
                            height: rect.height
                        }
                    });
                }
            }

            // Deduplicate by text
            const seen = new Set();
            return results.filter(r => {
                if (seen.has(r.text)) return false;
                seen.add(r.text);
                return true;
            }).slice(0, 20);
        }
    ''')

    if iran_results:
        print(f"   ✅ 找到 {len(iran_results)} 条伊朗相关内容:")
        for i, r in enumerate(iran_results[:10]):
            marker = "👉" if i == 0 else "  "
            print(f"   {marker} [{i+1}] {r['text']}")
            if r.get('href'):
                print(f"        链接: {r['href'][:80]}")
    else:
        print("   ⚠️  当前页面未找到'伊朗'相关内容")
        print("   尝试搜索更宽泛的关键词...")

    # ========== Step 5: Focus on first Iran-related news ==========
    if iran_results:
        first = iran_results[0]
        print(f"\n📌 Step 5: 将焦点切到第一条伊朗相关新闻...")
        print(f"   🎯 目标: {first['text']}")

        # Scroll to element and highlight it
        await page.evaluate('''
            (targetInfo) => {
                // First, scroll to the element position
                const targetY = targetInfo.position.top - 200;  // 200px offset from top
                window.scrollTo({top: targetY, behavior: 'smooth'});

                // Try to find and highlight the element
                const allLinks = document.querySelectorAll('a');
                for (const a of allLinks) {
                    if (a.innerText.trim().includes(targetInfo.text.substring(0, 20))) {
                        // Highlight with red border and yellow background
                        a.style.outline = '4px solid red';
                        a.style.outlineOffset = '4px';
                        a.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
                        a.style.transition = 'all 0.3s ease';

                        // Also add a floating label
                        const label = document.createElement('div');
                        label.style.cssText = `
                            position: absolute;
                            top: ${a.getBoundingClientRect().top + window.scrollY - 35}px;
                            left: ${a.getBoundingClientRect().left}px;
                            background: red;
                            color: white;
                            padding: 4px 12px;
                            border-radius: 4px;
                            font-size: 14px;
                            font-weight: bold;
                            z-index: 99999;
                            pointer-events: none;
                        `;
                        label.textContent = '👉 第一条伊朗相关新闻';
                        document.body.appendChild(label);

                        // Scroll into view with smooth behavior
                        a.scrollIntoView({behavior: 'smooth', block: 'center'});
                        return true;
                    }
                }

                // If not found in links, try all elements
                const allEls = document.querySelectorAll('h1, h2, h3, h4, h5, p, span, div');
                for (const el of allEls) {
                    if (el.innerText.trim().includes(targetInfo.text.substring(0, 20))) {
                        el.style.outline = '4px solid red';
                        el.style.outlineOffset = '4px';
                        el.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
                        el.scrollIntoView({behavior: 'smooth', block: 'center'});
                        return true;
                    }
                }
                return false;
            }
        ''', first)

        await asyncio.sleep(1)

        # Take a screenshot to show the result
        screenshot_path = "C:/Users/elijahxb/.openclaw/workspace/skills/playwright-browser/sina_iran_result.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"\n   📸 截图已保存: {screenshot_path}")

        print(f"\n{'=' * 60}")
        print(f"✅ 任务完成！")
        print(f"   - 已访问新浪军事板块")
        print(f"   - 找到 {len(iran_results)} 条伊朗相关内容")
        print(f"   - 屏幕焦点已切到第一条: {first['text']}")
        if first.get('href'):
            print(f"   - 新闻链接: {first['href']}")
        print(f"{'=' * 60}")
    else:
        print("\n⚠️  未能找到伊朗相关新闻内容")
        screenshot_path = "C:/Users/elijahxb/.openclaw/workspace/skills/playwright-browser/sina_mil_page.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"   📸 当前页面截图: {screenshot_path}")

    # Print captured API calls summary
    if api_responses:
        print(f"\n📡 捕获到 {len(api_responses)} 个 API 请求:")
        for api in api_responses[:5]:
            print(f"   - [{api['status']}] {api['url']}")

    # Keep browser open for 15 seconds so user can see the result
    print("\n⏳ 浏览器将保持打开 15 秒供查看...")
    await asyncio.sleep(15)

    # Cleanup
    await browser.close()
    await pw.stop()
    print("\n🔒 浏览器已关闭")


if __name__ == "__main__":
    asyncio.run(main())
