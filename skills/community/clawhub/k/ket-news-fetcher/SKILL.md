---
name: ket-news-fetcher
description: 抓取BBC News并生成Daily English News PDF，包含完整文章、全文翻译和80个词汇
author:
  name: Maosi English Team
  github: https://github.com/effecE
homepage: https://clawhub.com
license: Apache-2.0
metadata:
  {
    "openclaw":
      {
        "version": "6.8.0",
        "emoji": "📰",
        "tags": ["english", "news", "BBC", "learning", "education", "pdf"],
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "requests-html",
              "label": "Install requests-html (for JavaScript rendering)",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "beautifulsoup4",
              "label": "Install beautifulsoup4",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "fpdf2",
              "label": "Install fpdf2 (for PDF generation with Chinese support)",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "reportlab",
              "label": "Install reportlab (fallback PDF generation)",
            },
          ],
      },
  }
---

# Daily English News - BBC新闻PDF生成器

抓取BBC News RSS，生成每日英语新闻PDF，包含完整文章、全文中文翻译和80个核心词汇。

## 使用方法

```bash
cd /root/.openclaw/workspace/skills/ket-news-fetcher
python3 ket_news_pdf.py
```

## 输出

- PDF文件：`/root/.openclaw/workspace-explodegao/english-audio/Miaosi Daily English News YYYY-MM-DD.pdf`
- 包含4篇BBC News文章

## PDF内容

每个PDF包含：
- 标题：Daily English News
- 副标题：Miaosi English Team
- 日期：YYYY-MM-DD
- 4篇BBC News完整文章
- 每篇文章：英文原文 + 中文翻译 + 80个词汇（附中文翻译）

## 技术实现

- requests-html: JavaScript渲染（抓取动态页面）
- BeautifulSoup: HTML解析
- fpdf2: PDF生成（支持中日韩文字体）
- Google翻译API: 实时翻译

## 文章来源

- BBC News RSS: https://feeds.bbci.co.uk/news/rss.xml
- 每次抓取最新的4篇文章

## 更新日志

### v6.8.0 (2026-03-27)
- 修复特殊字符导致PDF编码错误
- 添加clean_text函数处理en-dash、em-dash、smart quotes等

### v6.7 (2026-03-26)
- 文件名更新为 "Miaosi Daily English News YYYY-MM-DD.pdf"

### v6.6 (2026-03-26)
- 添加"Miaosi English Team"副标题

### v6.5 (2026-03-25)
- 修复文件名格式

### v6.4 (2026-03-24)
- 每篇文章80个词汇（不再只是KET词汇）
- 移除全文翻译部分

### v6.3 (2026-03-23)
- 添加全文中文翻译
- 添加全部词汇表

## License
Apache License 2.0
