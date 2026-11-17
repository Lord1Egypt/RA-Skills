#!/usr/bin/env python3
"""
GTC 2026 产业趋势卡片生成器 - Playwright版本
确保精确1080x1350像素截图
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# 配置
OUTPUT_DIR = Path("/root/.openclaw/workspace/output/gtc_industry_cards")
TEMPLATE_DIR = Path("/root/.openclaw/workspace/skills/knowledge-card-designer/assets/templates")

async def generate_card(page, name, width, height):
    """生成单张卡片"""
    html_file = TEMPLATE_DIR / f"{name}.html"
    output_file = OUTPUT_DIR / f"{name}.png"
    
    if not html_file.exists():
        print(f"⚠️ 模板不存在: {html_file}")
        return False
    
    try:
        # 设置视口大小
        await page.set_viewport_size({"width": width, "height": height})
        
        # 加载HTML文件
        await page.goto(f"file://{html_file}")
        
        # 等待页面加载完成
        await page.wait_for_load_state("networkidle")
        
        # 截取精确尺寸的截图
        await page.screenshot(
            path=str(output_file),
            clip={"x": 0, "y": 0, "width": width, "height": height}
        )
        
        file_size = output_file.stat().st_size
        print(f"✅ 生成成功: {name}.png ({file_size/1024:.1f}KB) - {width}x{height}")
        return True
        
    except Exception as e:
        print(f"❌ 生成失败 {name}: {e}")
        return False

async def generate_all():
    """批量生成所有卡片"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    cards = [
        ("cover", 900, 383),
        ("trend1", 1080, 1350),
        ("trend2", 1080, 1350),
        ("trend3", 1080, 1350),
        ("trend4", 1080, 1350),
        ("trend5", 1080, 1350),
        ("trend6", 1080, 1350),
        ("trend7", 1080, 1350),
        ("trend8", 1080, 1350),
        ("action", 1080, 1350),
    ]
    
    print("=" * 60)
    print("GTC 2026 产业趋势卡片生成器 (Playwright)")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        for name, width, height in cards:
            await generate_card(page, name, width, height)
        
        await browser.close()
    
    print("=" * 60)
    print("生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(generate_all())
