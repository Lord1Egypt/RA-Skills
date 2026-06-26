---
name: persistent-browser
version: 1.0.0
description: 用 Playwright 持久化上下文（main-identity）抓取需要登录态的网站（YouTube、GitHub、HuggingFace、Reddit、Kaggle、X/Twitter）。当用户要求外网搜索或指定这些网站时自动触发。
user-invocable: true
---

# Persistent Browser Scraper

用 Playwright `launch_persistent_context` 读写 `main-identity` 配置文件的技能。

## 核心原理

```
user_data_dir = /home/kncao/.openclaw/browser-profiles/main-identity
headless = False（必须，否则 X/Twitter 会返回空白）
```

每次抓取前先删 SingletonLock：
```bash
rm -f /home/kncao/.openclaw/browser-profiles/main-identity/SingletonLock
```

## 标准模板

```python
import asyncio
from playwright.async_api import async_playwright

USER_DATA_DIR = '/home/kncao/.openclaw/browser-profiles/main-identity'

async def scrape(url: str, selector: str = 'body', wait_ms: int = 8000):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=[
                "--password-store=basic",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ],
            viewport={'width': 1280, 'height': 800},
            java_script_enabled=True
        )
        try:
            page = await context.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(wait_ms)  # SPA hydration
            text = await page.inner_text(selector)
            await context.close()
            return text
        except Exception as e:
            await context.close()
            raise e
```

## 各网站等待时间

| 网站 | wait_ms | 备注 |
|------|---------|------|
| X/Twitter | 8000 | React SPA，需等 JS 渲染 |
| YouTube | 6000 | JS 懒加载 |
| GitHub | 3000 | SSR为主 |
| HuggingFace | 5000 | React |
| Reddit | 6000 | SSR+JS混合 |
| Kaggle | 8000 | React SPA |

## 触发条件

- 用户要求「搜索外网」「搜一下」
- 用户指定以下网站：YouTube、GitHub、HuggingFace、Reddit、Kaggle、X/Twitter
- 任何需要登录态才能访问的内容抓取

## 注意事项

- 必须用 `headless=False`，X/Twitter 在 headless=True 下会返回空白页面
- 每次调用前清理 SingletonLock，否则报 `ProcessSingleton` 错误
- SPA 页面（如 X）必须等 8 秒让前端 hydrate，否则正文为空
- 优先提取纯文本，不依赖截图
