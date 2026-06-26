# Playwright 浏览器自动化技能

## 📋 技能概述

Playwright 是微软开发的现代化浏览器自动化库，比 Selenium 更快、更可靠。

## 🆚 Playwright vs Selenium

| 特性 | Playwright | Selenium |
|------|-----------|----------|
| 速度 | ⚡ 快 | 🐢 较慢 |
| 自动等待 | ✅ 内置 | ❌ 需要手动 |
| 多浏览器 | ✅ Chromium/Firefox/WebKit | ✅ 所有主流浏览器 |
| 网络拦截 | ✅ 支持 | ❌ 有限 |
| 截图 | ✅ 全页截图 | ❌ 仅视口 |
| API 设计 | ✅ 现代化 | ⚠️ 传统 |

## 🛠️ 安装

```bash
# 安装 Python 库
pip3 install playwright --break-system-packages

# 安装浏览器
python3 -m playwright install chromium
```

## 🚀 快速开始

### 基础示例

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 访问网页
    page.goto('https://www.baidu.com')
    
    # 截图
    page.screenshot(path='example.png')
    
    browser.close()
```

### 搜索示例

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 直接访问搜索 URL
    page.goto('https://www.baidu.com/s?wd=Python', wait_until='networkidle')
    
    # 获取搜索结果
    results = page.query_selector_all('.result h3')
    for i, r in enumerate(results[:5], 1):
        print(f"{i}. {r.inner_text()}")
    
    browser.close()
```

### 高级功能

#### 1. 全页截图

```python
page.screenshot(path='full.png', full_page=True)
```

#### 2. 网络拦截

```python
# 阻止图片加载
def block_images(route):
    if route.request.resource_type == "image":
        route.abort()
    else:
        route.continue_()

page.route("**/*", block_images)
page.goto("https://example.com")
```

#### 3. 等待元素

```python
# 自动等待元素可见
page.wait_for_selector('#my-element')

# 等待特定状态
page.wait_for_selector('.loaded', state='visible')
```

#### 4. 表单操作

```python
# 填写表单
page.fill('#username', 'user123')
page.fill('#password', 'pass456')
page.click('#login-btn')

# 等待跳转
page.wait_for_url('**/dashboard')
```

#### 5. 多标签页

```python
# 创建新标签
page = browser.new_page()

# 切换标签
pages = browser.pages
pages[0].bring_to_front()
```

## 📚 常用 API

### 页面导航

```python
page.goto('https://example.com')
page.reload()
page.go_back()
page.go_forward()
```

### 元素操作

```python
# 点击
page.click('#button')

# 输入
page.fill('#input', 'text')
page.type('#input', 'text', delay=100)  # 模拟键盘

# 选择
page.select_option('#select', 'value')
page.check('#checkbox')
page.uncheck('#checkbox')
```

### 获取内容

```python
# 文本
text = page.inner_text('#element')
html = page.inner_html('#element')

# 属性
href = page.get_attribute('a', 'href')
value = page.input_value('#input')

# 数量
count = page.count('.items')
```

### 截图和 PDF

```python
# 截图
page.screenshot(path='page.png')
page.screenshot(path='full.png', full_page=True)

# PDF (仅 Chromium)
page.pdf(path='page.pdf')
```

## ⚠️ 常见问题

### 问题 1: 元素不可见

**解决**: 使用 `wait_for_selector`

```python
page.wait_for_selector('#element', state='visible')
page.click('#element')
```

### 问题 2: 页面加载慢

**解决**: 使用 `networkidle`

```python
page.goto('https://example.com', wait_until='networkidle')
```

### 问题 3: 反爬虫

**解决**: 设置 User-Agent 和隐藏自动化特征

```python
browser = p.chromium.launch(
    headless=True,
    args=['--disable-blink-features=AutomationControlled']
)
page.set_extra_http_headers({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...'
})
```

## 🎯 最佳实践

1. **使用 `with` 语句**: 自动清理资源
2. **启用 headless 模式**: 节省资源
3. **使用 `networkidle`**: 确保页面完全加载
4. **合理等待**: 避免固定 `sleep`
5. **错误处理**: 使用 `try-except`

## 📦 依赖

```txt
playwright>=1.40.0
```

## 🔗 相关资源

- [Playwright 官网](https://playwright.dev/)
- [Python API 文档](https://playwright.dev/python/docs/intro)
- [GitHub 仓库](https://github.com/microsoft/playwright)

## 🔄 从 Selenium 迁移

如果你之前使用 Selenium，迁移非常简单：

```python
# Selenium 代码
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://example.com')
element = driver.find_element(By.ID, 'my-element')

# Playwright 等价代码
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    element = page.locator('#my-element')
```

**主要差异**:
- Playwright 使用 `page` 而不是 `driver`
- 自动等待，不需要 `WebDriverWait`
- 选择器更强大 (支持 CSS/XPath/text)
- `locator` 替代 `find_element`

---

**版本**: v1.1  
**创建时间**: 2026-03-14 02:00 AM  
**更新**: 2026-03-14 08:07 AM (添加迁移指南)  
**作者**: Han's AI Assistant
