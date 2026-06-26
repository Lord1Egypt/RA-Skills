# Playwright 使用指南

## ✅ 安装状态

- **Python 包**：✅ 已安装
- **浏览器**：✅ 已下载（使用系统 Chrome）
- **CLI 命令**：⚠️ 不在 PATH（不影响使用）

---

## 🚀 快速开始

### 方式 1：使用 htmlPrototype 技能（推荐）

```bash
cd ~/.openclaw/skills/htmlPrototype

# 从需求文档生成
python3 main.py --doc requirements.md

# 从文本描述生成
python3 main.py "创建一个产品列表页"

# 交互模式
python3 main.py "创建一个产品列表页" -i
```

---

### 方式 2：直接使用截图脚本

```bash
# 截图 HTML 文件
python3 ~/.openclaw/workspace/scripts/screenshot_system_chrome.py \
    prototype.html \
    --output output.png

# 自定义尺寸
python3 ~/.openclaw/workspace/scripts/screenshot_system_chrome.py \
    prototype.html \
    --output output.png \
    --width 1920 \
    --height 1080
```

---

### 方式 3：编写自己的脚本

```python
from playwright.sync_api import sync_playwright

# 使用系统 Chrome
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(
        executable_path=chrome_path,
        headless=True  # 无头模式（后台运行）
    )
    
    # 创建页面
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    
    # 打开网页
    page.goto("https://example.com")
    
    # 等待加载
    page.wait_for_load_state('networkidle')
    
    # 截图
    page.screenshot(path="screenshot.png", full_page=True)
    
    # 关闭浏览器
    browser.close()

print("✅ 截图完成！")
```

---

## 📋 常用功能示例

### 1. 截图网页

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 打开网页
    page.goto("https://www.apple.com")
    
    # 截图全屏
    page.screenshot(path="apple_full.png", full_page=True)
    
    # 截图可见区域
    page.screenshot(path="apple_visible.png")
    
    browser.close()
```

---

### 2. 截图本地 HTML 文件

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

html_file = Path.home() / "Desktop/prototype.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    
    # 打开本地文件
    page.goto(f"file://{html_file}")
    page.wait_for_load_state('networkidle')
    
    # 截图
    page.screenshot(path="prototype.png", full_page=True)
    
    browser.close()
```

---

### 3. 执行 JavaScript

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    
    # 执行 JS 获取标题
    title = page.evaluate("document.title")
    print(f"页面标题：{title}")
    
    # 获取元素文本
    text = page.inner_text("h1")
    print(f"H1 内容：{text}")
    
    browser.close()
```

---

### 4. 点击和输入

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    
    # 点击元素
    page.click("button#submit")
    
    # 输入文本
    page.fill("input#username", "testuser")
    page.fill("input#password", "password123")
    
    # 选择下拉框
    page.select_option("select#country", "US")
    
    # 勾选复选框
    page.check("input#agree")
    
    browser.close()
```

---

### 5. 等待元素

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    
    # 等待元素出现
    page.wait_for_selector(".content")
    
    # 等待元素可见
    page.wait_for_selector(".button", state="visible")
    
    # 等待特定时间（毫秒）
    page.wait_for_timeout(2000)
    
    browser.close()
```

---

### 6. 多页面/标签页

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 创建多个页面
    page1 = browser.new_page()
    page1.goto("https://example1.com")
    
    page2 = browser.new_page()
    page2.goto("https://example2.com")
    
    # 切换页面
    page1.bring_to_front()
    
    browser.close()
```

---

### 7. 录制视频

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 创建页面并录制
    context = browser.new_context(record_video_dir="videos/", record_video_size={"width": 1280, "height": 720})
    page = context.new_page()
    page.goto("https://example.com")
    
    # ... 执行操作 ...
    
    # 关闭并保存视频
    context.close()
    browser.close()
    
    print("✅ 视频已保存：videos/")
```

---

### 8. 下载文件

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    # 设置下载路径
    page.set_content("""
        <a href="file.pdf" download>下载</a>
    """)
    
    # 等待下载
    with page.expect_download() as download_info:
        page.click("a")
    download = download_info.value
    
    # 保存文件
    download.save_as("downloads/file.pdf")
    
    browser.close()
```

---

## 🎯 htmlPrototype 技能中的使用

### 截图函数

```python
# ~/.openclaw/skills/htmlPrototype/screenshot/capture.py

from playwright.sync_api import sync_playwright

def screenshot(html_path: str, output_path: str, width: int = 1440, height: int = 900) -> bool:
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=True
        )
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(f'file://{html_path}')
        page.wait_for_load_state('networkidle')
        page.screenshot(path=str(output_path), full_page=True)
        browser.close()
    
    return True
```

---

## 📊 性能优化

### 1. 复用浏览器实例

```python
from playwright.sync_api import sync_playwright

# 启动一次浏览器
with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 复用多个页面
    for url in urls:
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=f"{url}.png")
        page.close()
    
    browser.close()
```

### 2. 使用无头模式

```python
# 无头模式（更快，不显示界面）
browser = p.chromium.launch(headless=True)

# 有头模式（可以看到操作过程）
browser = p.chromium.launch(headless=False)
```

### 3. 调整 viewport

```python
# 小尺寸（更快）
page = browser.new_page(viewport={'width': 1280, 'height': 720})

# 大尺寸（更清晰）
page = browser.new_page(viewport={'width': 1920, 'height': 1080})
```

---

## 🐛 故障排查

### 问题 1：找不到 Chrome

```python
# 检查 Chrome 路径
import subprocess
result = subprocess.run(["ls", "/Applications/Google Chrome.app"], capture_output=True)
if result.returncode != 0:
    print("❌ Chrome 未安装")
```

### 问题 2：截图空白

```python
# 增加等待时间
page.goto(url)
page.wait_for_load_state('networkidle')  # 等待网络空闲
page.wait_for_timeout(1000)  # 额外等待 1 秒
```

### 问题 3：内存泄漏

```python
# 确保关闭浏览器
try:
    browser = p.chromium.launch()
    page = browser.new_page()
    # ... 操作 ...
finally:
    browser.close()
```

---

## 📚 学习资源

- **官方文档**：https://playwright.dev/python/
- **API 参考**：https://playwright.dev/python/docs/api/class-playwright
- **示例代码**：https://github.com/microsoft/playwright-python

---

## 🎓 最佳实践

### 1. 使用上下文管理器

```python
with sync_playwright() as p:
    with p.chromium.launch() as browser:
        page = browser.new_page()
        # ... 操作 ...
```

### 2. 错误处理

```python
try:
    page.goto(url)
    page.screenshot(path="output.png")
except Exception as e:
    print(f"❌ 失败：{e}")
finally:
    browser.close()
```

### 3. 日志记录

```python
import logging
logging.basicConfig(level=logging.INFO)

def screenshot_with_log(url, output):
    logging.info(f"正在截图：{url}")
    try:
        # ... 截图代码 ...
        logging.info(f"✅ 成功：{output}")
    except Exception as e:
        logging.error(f"❌ 失败：{e}")
```

---

## 💡 实际应用

### 批量截图

```python
urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    for i, url in enumerate(urls):
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=f"screenshot_{i}.png")
        page.close()
    
    browser.close()
```

### 生成 PDF

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    
    # 生成 PDF
    page.pdf(path="page.pdf", format="A4")
    
    browser.close()
```

---

**Playwright 已就绪，开始使用吧！** 🚀
