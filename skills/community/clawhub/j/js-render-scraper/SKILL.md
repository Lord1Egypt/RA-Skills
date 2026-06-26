---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3044022028523a0cb66b8d83293f741645ed990b8b53fbbcc4fdb5bfe1c3155c52a65ca602204f9d1cc18247d54fb3eee588805aad50197317528a5f99955b7bed7ff218faa1
    ReservedCode2: 3045022100b347e607d77b922f0aa9705ef58511fce84f7d231b705130af0cfe3c0eb28db3022043001c1760b6124edbda628200170db404f267f4ab49ff6965f1aaf1184c0587
description: 爬取需要 JavaScript 渲染的动态网页内容。当用户要求抓取 SPA、React/Vue 应用、无限滚动页面、需要登录的页面或任何依赖 JS 动态加载内容的网站时使用。支持使用 Playwright 进行浏览器自动化抓取。
name: js-render-scraper
---

# JS 渲染页面爬虫

使用 Playwright 浏览器自动化技术爬取 JavaScript 渲染的动态网页。

## 核心工作流程

### 1. 分析目标页面

在开始爬取前，分析页面特点：
- 识别页面是 SPA、SSR 还是客户端渲染
- 检查内容加载方式（滚动加载、点击加载、延迟加载等）
- 确定需要的交互操作（滚动、点击按钮、等待元素等）

### 2. 配置爬取参数

创建爬取配置：
```python
scraper_config = {
    "url": "目标URL",
    "wait_for_selector": "内容容器选择器",
    "scroll": True/False,           # 是否需要滚动加载
    "scroll_delay": 2000,            # 滚动间隔（毫秒）
    "max_scrolls": 10,               # 最大滚动次数
    "click_buttons": [],             # 需要点击的按钮选择器列表
    "wait_time": 3000,              # 初始等待时间
    "extract_method": "html"/"text"/"json"
}
```

### 3. 执行爬取

使用 Playwright 执行自动化爬取：

```python
from playwright.sync_api import sync_playwright

def scrape_js_page(config):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 访问页面
        page.goto(config["url"])

        # 等待页面加载
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(config.get("wait_time", 3000))

        # 处理滚动加载
        if config.get("scroll"):
            for _ in range(config.get("max_scrolls", 10)):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(config.get("scroll_delay", 2000))

        # 处理点击按钮
        for button_selector in config.get("click_buttons", []):
            try:
                page.click(button_selector)
                page.wait_for_timeout(1000)
            except:
                pass

        # 等待目标元素出现
        if config.get("wait_for_selector"):
            page.wait_for_selector(config["wait_for_selector"], timeout=10000)

        # 提取内容
        if config.get("extract_method") == "json":
            content = page.evaluate("() => JSON.stringify(window.__INITIAL_DATA__)")
        else:
            element = page.wait_for_selector(config["wait_for_selector"])
            content = element.inner_html() if config.get("extract_method") == "html" else element.inner_text()

        browser.close()
        return content
```

### 4. 内容解析与清洗

爬取原始 HTML 后，进行解析：

```python
from bs4 import BeautifulSoup

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # 移除脚本和样式
    for tag in soup(["script", "style"]):
        tag.decompose()

    # 提取需要的数据
    data = {
        "title": soup.find("title").text if soup.find("title") else "",
        "text": soup.get_text(separator="\n", strip=True),
        "links": [{"text": a.text, "href": a.get("href")} for a in soup.find_all("a", href=True)],
        "images": [img.get("src") for img in soup.find_all("img", src=True)]
    }

    return data
```

## 常见场景模板

### 场景 1：爬取无限滚动页面

```python
def scrape_infinite_scroll(url, item_selector):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)

        last_height = 0
        items = []

        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

            new_items = page.query_selector_all(item_selector)
            if len(new_items) == last_height:
                break
            last_height = len(new_items)

        # 提取所有项目数据
        for item in new_items:
            items.append({
                "text": item.inner_text(),
                "html": item.inner_html()
            })

        browser.close()
        return items
```

### 场景 2：爬取需要登录的页面

```python
def scrape_with_login(url, username, password, login_selectors):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 执行登录
        page.goto(login_selectors["login_url"])
        page.fill(login_selectors["username_input"], username)
        page.fill(login_selectors["password_input"], password)
        page.click(login_selectors["submit_button"])
        page.wait_for_load_state("networkidle")

        # 访问目标页面
        page.goto(url)
        page.wait_for_load_state("networkidle")

        content = page.content()
        browser.close()
        return content
```

### 场景 3：爬取 Shadow DOM 内容

```python
def scrape_shadow_dom(url, shadow_host_selector):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # 展开 Shadow DOM 并提取内容
        content = page.evaluate("""
            () => {
                const shadowHost = document.querySelector(arguments[0]);
                const shadowRoot = shadowHost.shadowRoot;
                return shadowRoot ? shadowRoot.innerHTML : '';
            }
        """, shadow_host_selector)

        browser.close()
        return content
```

## 反爬策略应对

| 策略 | 应对方法 |
|------|----------|
| User-Agent 检测 | 使用真实的浏览器 User-Agent |
| IP 封禁 | 添加延迟、使用代理池 |
| 验证码 | 使用打码平台或机器学习识别 |
| Selenium 检测 | 使用 `stealth` 插件伪装 |
| 请求频率限制 | 添加随机延迟 |

## 错误处理

```python
def safe_scrape(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return scrape_js_page({"url": url})
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"爬取失败 after {max_retries} attempts: {e}")
            time.sleep(5 * (attempt + 1))  # 指数退避
```

## 注意事项

1. **遵守 robots.txt**：爬取前检查目标站点的 robots.txt
2. **添加延迟**：避免对服务器造成过大压力
3. **设置合理的超时**：防止无限等待
4. **保存中间状态**：复杂爬取任务定期保存进度
5. **监控资源使用**：浏览器实例会占用内存，合理控制并发

## 输出格式

返回结构化数据：
```json
{
  "url": "爬取的URL",
  "timestamp": "爬取时间",
  "status": "success/error",
  "data": {
    "title": "页面标题",
    "content": "提取的内容",
    "links": [],
    "images": []
  },
  "error": "错误信息（如果失败）"
}
```
