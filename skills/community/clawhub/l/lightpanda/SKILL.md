---
name: lightpanda
description: Lightpanda is a lightweight headless browser written in Zig. 9x faster and 16x less memory than Chrome. Perfect for web scraping, content extraction, and automation. 安装: curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux && chmod a+x lightpanda | 轻量级无头浏览器，比Chrome快9倍，省内存16倍，适合网页抓取和内容提取
version: 1.0.0
---

# Lightpanda / 轻量级无头浏览器

## 简介 / Introduction

Lightpanda 是用 Zig 编写的轻量级无头浏览器，非 Chromium 分支。

**性能对比：**
| 指标 | Lightpanda | Headless Chrome | 差距 |
|------|------------|-----------------|------|
| 内存 (100页) | 123MB | 2GB | **16x 更省** |
| 速度 (100页) | 5s | 46s | **9x 更快** |

## 安装 / Installation

```bash
# Linux
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux && \
chmod a+x ./lightpanda

# macOS
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos && \
chmod a+x ./lightpanda
```

## 使用方法 / Usage

### 基本命令 / Basic Commands

```bash
# 查看版本
./lightpanda version

# 抓取网页为 HTML
./lightpanda fetch --obey-robots --dump html --log-format pretty --log-level info <URL>

# 抓取网页为 Markdown（推荐）
./lightpanda fetch --obey-robots --dump markdown --log-format pretty --log-level info <URL>

# 等待加载后再抓取
./lightpanda fetch --obey-robots --dump markdown --wait-ms 3000 <URL>

# 等待特定元素
./lightpanda fetch --obey-robots --dump markdown --wait-selector ".content" <URL>
```

### Python 调用 / Python Integration

```python
import subprocess
import re

def fetch_url(url, format="markdown", wait_ms=2000):
    """使用 Lightpanda 抓取网页"""
    output_format = "markdown" if format == "markdown" else "html"
    cmd = [
        "./lightpanda", "fetch",
        "--obey-robots",
        "--dump", output_format,
        "--wait-ms", str(wait_ms),
        "--log-format", "pretty",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# 使用示例
content = fetch_url("https://example.com", "markdown")
print(content)
```

## 适用场景 / Use Cases

| 场景 | 说明 |
|------|------|
| 🌐 网页抓取 | 轻量快速，适合批量抓取 |
| 📄 内容提取 | 转 Markdown，方便后续处理 |
| 🔍 竞品分析 | 定期抓取页面内容 |
| 📰 新闻聚合 | 抓取文章内容 |
| 📊 数据监控 | 监控网页变化 |

## 注意事项 / Notes

- **无需 Chrome**：独立二进制，不依赖系统浏览器
- **CDP 协议**：支持 Puppeteer/Playwright 连接（高级用法）
- **遵守 robots.txt**：默认 `--obey-robots`
- **输出格式**：推荐使用 `--dump markdown` 便于后续处理

## Docker 部署 / Docker Deployment

```bash
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

## 示例 / Examples

### 抓取网页并保存

```bash
./lightpanda fetch --obey-robots --dump markdown --log-format pretty --log-level info https://news.ycombinator.com > output.md
```

### 批量抓取

```python
import subprocess
import time

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

for url in urls:
    print(f"Fetching: {url}")
    result = subprocess.run(
        ["./lightpanda", "fetch", "--obey-robots", "--dump", "markdown", "--wait-ms", "2000", url],
        capture_output=True,
        text=True
    )
    # 处理 result.stdout
    time.sleep(1)  # 礼貌性延迟
```

### 与 LangChain/文档处理结合

```python
import subprocess

def scrape_for_rag(url):
    """抓取网页用于 RAG 处理"""
    result = subprocess.run(
        ["./lightpanda", "fetch", "--obey-robots", "--dump", "markdown", "--wait-ms", "3000", url],
        capture_output=True,
        text=True
    )
    return result.stdout
```
