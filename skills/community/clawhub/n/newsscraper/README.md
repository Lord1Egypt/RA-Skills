# 新闻热点爬取 Skill (News Hot Scraper)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Skill Status](https://img.shields.io/badge/status-beta-orange.svg)]()

自动爬取国内热点新闻信息,支持多种平台,能够生成新闻摘要并注明出处。

## ✨ 功能特性

### 1. 多平台支持
- 微博热搜
- 知乎热榜
- B站热门
- 抖音热点
- 今日头条
- 腾讯新闻
- 澎湃新闻

### 2. 两种数据获取方式
- **API 方式**: 使用免费的热榜聚合 API,快速获取多平台热点
- **直接爬取**: 使用 requests + BeautifulSoup 直接从新闻网站爬取

### 3. 两种摘要生成方案
- **提取式摘要**: 基于关键词提取关键句,快速简洁
- **生成式摘要**: 使用 HuggingFace 的中文摘要模型,生成更自然的摘要

### 4. 完整的出处标注
- 标题
- 来源平台
- 发布时间
- 原文链接
- 摘要内容

## 📦 安装

### 方式 1: 使用 pip 安装

```bash
# 基础安装(仅支持提取式摘要)
pip install news-hot-scraper

# 安装生成式摘要依赖
pip install news-hot-scraper[abstractive]
```

### 方式 2: 从源码安装

```bash
# 克隆仓库
git clone https://clawhub.com/workbuddy/news-hot-scraper.git
cd news-hot-scraper

# 安装基础依赖
pip install -r requirements.txt

# 安装生成式摘要依赖(可选)
pip install transformers torch
```

## 🚀 快速开始

### 1. 使用 API 方式获取多平台热点

```bash
# 获取微博和知乎的热点
python scripts/news_scraper.py --mode api --platforms weibo,zhihu --limit 20 --output news_data.json

# 生成提取式摘要
python scripts/news_summarizer.py --method extractive --input news_data.json --output summary.json --report summary.md
```

### 2. 直接爬取特定平台

```bash
# 爬取微博热搜
python scripts/news_scraper.py --mode scrape --platform weibo --limit 10 --output news_data.json

# 生成生成式摘要(质量更好)
python scripts/news_summarizer.py --method abstractive --input news_data.json --output summary.json --report summary.md
```

### 3. 根据主题爬取新闻

```bash
# 爬取关于"人工智能"的新闻
python scripts/news_scraper.py --mode scrape --keyword "人工智能" --platforms weibo,zhihu --limit 15 --output news_data.json
```

## 输出格式

### JSON 格式
```json
[
  {
    "title": "新闻标题",
    "platform": "weibo",
    "url": "https://...",
    "hot": 1234567,
    "rank": 1,
    "timestamp": "2026-03-21T13:00:00",
    "summary": "新闻摘要内容..."
  }
]
```

### Markdown 报告格式
```markdown
# 新闻热点摘要报告

生成时间: 2026-03-21T13:00:00
总计: 20 条新闻

## 微博热搜

### 1. 热搜标题

**摘要**: 摘要内容...

**热度**: 1234567

**来源**: [微博热搜](https://...)

**时间**: 2026-03-21T13:00:00

---
```

## 使用场景

- "帮我搜集关于[主题]的国内热点新闻"
- "爬取微博热搜、知乎热榜的今日热点"
- "获取科技领域的最新新闻并生成摘要"
- "监控特定主题的新闻动态"
- "整理多个平台的热点话题"

## 技术栈

### 爬虫技术
- **requests**: HTTP 请求
- **BeautifulSoup4**: HTML 解析
- **API 接口**: 全网热榜聚合 API(uapis.cn)

### 摘要生成
- **提取式**: jieba(分词)、textrank(句子重要性排序)
- **生成式**: transformers + HuggingFace 模型

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

## 文档说明

- **SKILL.md**: Skill 的主要使用文档
- **references/platforms.md**: 各平台爬取策略和 API 文档
- **references/summarization_methods.md**: 摘要生成方法详解
- **scripts/news_scraper.py**: 新闻数据爬取脚本
- **scripts/news_summarizer.py**: 新闻摘要生成脚本

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

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献代码!请遵循以下步骤:

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📧 联系方式

- 项目主页: [https://clawhub.com/workbuddy/news-hot-scraper](https://clawhub.com/workbuddy/news-hot-scraper)
- 问题反馈: [Issues](https://clawhub.com/workbuddy/news-hot-scraper/issues)

## ⚠️ 免责声明

本 Skill 仅供学习和研究使用。请遵守各平台的使用条款和相关法律法规。使用本工具爬取的数据不得用于商业目的,请尊重数据来源的版权。

## 🙏 致谢

- [jieba](https://github.com/fxsjy/jieba) - 中文分词
- [transformers](https://github.com/huggingface/transformers) - HuggingFace Transformers
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析

---

**Made with ❤️ by WorkBuddy AI**
