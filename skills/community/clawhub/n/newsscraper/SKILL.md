---
name: news-hot-scraper
description: This skill should be used when users need to scrape hot news topics from Chinese platforms (微博、知乎、B站、抖音、今日头条、腾讯新闻、澎湃新闻), generate summaries, and cite sources. It supports both API-based and direct scraping methods, and offers both extractive and abstractive summarization techniques.
---

# News Hot Scraper

## Overview

自动爬取国内热点新闻信息,支持多种平台(微博、知乎、B站、抖音、今日头条、腾讯新闻、澎湃新闻),能够生成新闻摘要并注明出处。提供 API 和直接爬取两种数据获取方式,以及提取式和生成式两种摘要生成方案。

## 核心功能

### 1. 新闻数据获取
根据用户输入的主题或关键词,从支持的平台获取热点新闻数据。支持两种方式:

- **API 方式**: 使用免费的热榜聚合 API(如 uapis.cn)快速获取多平台热点数据
- **直接爬取**: 使用 requests + BeautifulSoup 等技术直接从新闻网站爬取数据

### 2. 新闻摘要生成
对获取的新闻内容进行智能摘要,支持两种技术方案:

- **提取式摘要**: 基于关键词和句子重要性提取关键句,快速简洁
- **生成式摘要**: 使用 HuggingFace 的中文摘要模型(如 `google/mt5-small-chinese`),生成更自然的摘要

### 3. 出处标注
为每条新闻清晰标注:
- 标题
- 来源平台
- 发布时间
- 原文链接
- 摘要内容

## 使用场景

当用户需要:
- "帮我搜集关于[主题]的国内热点新闻"
- "爬取微博热搜、知乎热榜的今日热点"
- "获取科技领域的最新新闻并生成摘要"
- "监控特定主题的新闻动态"
- "整理多个平台的热点话题"

## 工作流程

### 步骤 1: 确定数据源和获取方式

根据用户需求和实际情况选择:
- **快速获取**: 优先使用 API 方式(如全网热榜聚合 API)
- **详细内容**: 使用直接爬取方式获取更多内容

参考 `references/platforms.md` 了解各平台的爬取策略和注意事项。

### 步骤 2: 执行数据获取

使用 `scripts/news_scraper.py` 脚本进行数据爬取:

```bash
# 使用 API 方式获取多平台热点
python scripts/news_scraper.py --mode api --platforms weibo,zhihu --limit 20

# 直接爬取特定平台
python scripts/news_scraper.py --mode scrape --platform weibo --limit 10

# 根据主题爬取新闻
python scripts/news_scraper.py --mode scrape --keyword "人工智能" --platforms weibo,zhihu --limit 15
```

### 步骤 3: 生成新闻摘要

使用 `scripts/news_summarizer.py` 脚本生成摘要:

```bash
# 提取式摘要(快速)
python scripts/news_summarizer.py --method extractive --input news_data.json --output summary.json

# 生成式摘要(质量更好)
python scripts/news_summarizer.py --method abstractive --input news_data.json --output summary.json
```

参考 `references/summarization_methods.md` 了解不同摘要方法的原理和适用场景。

### 步骤 4: 整理和输出

将结果整理成结构化的格式(JSON/Markdown),包含:
- 新闻标题
- 来源平台
- 发布时间
- 摘要内容
- 原文链接
- 热度/排名(如适用)

## 技术栈

### 爬虫技术
- **requests**: HTTP 请求
- **BeautifulSoup4**: HTML 解析
- **newspaper3k**: 新闻内容提取(可选)
- **API 接口**: 全网热榜聚合 API(uapis.cn 等)

### 摘要生成
- **提取式**: jieba(分词)、textrank(句子重要性排序)
- **生成式**: transformers + HuggingFace 模型(`google/mt5-small-chinese`)

### 数据处理
- **JSON**: 数据存储和交换
- **Markdown**: 报告输出

## 注意事项

### 合规性
- 遵守网站的 robots.txt 规则
- 控制请求频率,避免对目标网站造成压力
- 尊重数据的使用条款和版权

### 反爬虫处理
- 使用合理的请求头(User-Agent)
- 添加适当的延时(建议 1-3 秒)
- 考虑使用代理 IP(如需要大量爬取)

### 数据质量
- 验证新闻来源的可靠性
- 过滤重复或低质量内容
- 记录数据获取的时间戳

## 资源

### scripts/
- **news_scraper.py**: 新闻数据爬取脚本,支持 API 和直接爬取两种方式
- **news_summarizer.py**: 新闻摘要生成脚本,支持提取式和生成式两种方法

### references/
- **platforms.md**: 各平台(微博、知乎、B站等)的爬取策略、API 文档和注意事项
- **summarization_methods.md**: 摘要生成方法的详细介绍,包括技术原理和实现代码示例

### assets/
- (暂无,可根据需要添加模板或示例数据)

## 常见问题

### Q: 优先使用 API 还是直接爬取?
A: 对于快速获取多平台热点,优先使用 API(如全网热榜聚合 API),它们通常已经处理了反爬虫问题。如果需要更详细的内容或特定平台的数据,再使用直接爬取。

### Q: 提取式摘要和生成式摘要哪个更好?
A: 提取式摘要速度快,但可能不够连贯;生成式摘要质量更高,但需要更长时间。根据使用场景选择:
- 实时监控/快速浏览: 提取式
- 深度分析/报告生成: 生成式

### Q: 如何处理反爬虫限制?
A: 参考 `references/platforms.md` 中的反爬虫处理建议,包括:
- 使用合理的请求头和延时
- 考虑使用代理 IP
- 遵守 robots.txt 规则
- 优先使用官方 API(如果可用)

## 扩展建议

未来可以考虑添加:
- 定时任务功能,定期自动爬取热点
- 数据可视化(词云、趋势图)
- 多语言支持
- 情感分析
- 主题聚类分析

## 依赖安装

### 基础依赖(必须安装)
```bash
pip install requests beautifulsoup4
```

### 提取式摘要依赖(推荐)
```bash
pip install jieba
```

### 生成式摘要依赖(可选)
```bash
pip install transformers torch
```

注意: ClawHub 不会自动安装依赖,用户需要根据上述说明手动安装所需的 Python 包。
