---
name: news-search
description: 专门用于查询各大搜索网站的新闻结果。支持百度新闻、今日头条、Bing新闻、Google新闻和新浪新闻。可以同时聚合多个来源的结果，并进行去重处理。
---

# 新闻查询技能 (News Search Skill)

该技能使用 Playwright 无头浏览器访问各大搜索引擎的新闻频道，提取最新的新闻标题、链接、来源和发布时间。

## 支持的新闻源

- **百度新闻 (baidu)**: `https://www.baidu.com/s?tn=news&word={keyword}`
- **今日头条 (toutiao)**: `https://so.toutiao.com/search?keyword={keyword}&pd=news`
- **Bing 新闻 (bing)**: `https://www.bing.com/news/search?q={keyword}`
- **Google 新闻 (google)**: `https://news.google.com/search?q={keyword}`
- **新浪新闻 (sina)**: `https://search.sina.com.cn/?q={keyword}&c=news`

## 使用方法

进入脚本目录并运行 `news-search.js`：

```bash
cd /Users/wuwei/.openclaw/workspace/skills/news-search/scripts
node news-search.js <keyword> [options]
```

### 参数说明

- `keyword`: 搜索关键词（必填）。

### 选项说明

- `--engine=NAME`: 指定新闻引擎。可选值：`baidu`, `toutiao`, `bing`, `google`, `sina`, `all` (默认)。
- `--max=N`: 每个引擎返回的最大结果数（默认 10）。
- `--format=md|json`: 输出格式（默认 md）。

### 示例

```bash
# 搜索所有来源的关于 "人工智能" 的新闻
node news-search.js "人工智能"

# 仅使用百度新闻搜索 "特斯拉财报"
node news-search.js "特斯拉财报" --engine=baidu

# 获取 JSON 格式的结果并限制数量
node news-search.js "A股今日走势" --engine=toutiao --max=5 --format=json
```

## 输出示例 (Markdown)

```
============================================================
🔍 "人工智能" 新闻搜索结果（共 15 条）
============================================================

1. 2025年人工智能十大趋势发布
   🔗 https://news.example.com/article1
   📌 来源: 新华网 | 渠道: 百度新闻 | 时间: 2小时前

2. OpenAI 发布最新大模型预览版
   🔗 https://tech.example.com/article2
   📌 来源: 腾讯科技 | 渠道: 今日头条新闻 + Bing News
...
```

## 依赖项

- `playwright`: 浏览器自动化工具。
- `playwright-extra`: Playwright 扩展，支持插件。
- `puppeteer-extra-plugin-stealth`: 增强反爬虫绕过能力。

## 安装

```bash
cd /Users/wuwei/.openclaw/workspace/skills/news-search/scripts
npm install
```
