---
name: "hn-crawler"
description: "爬取 https://hn.aimaker.dev/ 网站资讯，执行爬取->提取->整理->总结完整流程。Invoke when user wants to crawl news from hn.aimaker.dev or process web content through the full pipeline."
---

# HN 资讯爬虫 Skill

本 Skill 用于爬取 https://hn.aimaker.dev/ 网站的资讯内容，并通过完整的处理流程将原始数据转化为结构化的总结报告。

## 工作流程

整个处理流程分为四个阶段：

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
│  Crawl  │ -> │ Extract  │ -> │ Organize │ -> │ Summarize │
│  爬取   │    │  提取    │    │  整理    │    │  总结     │
└─────────┘    └──────────┘    └──────────┘    └───────────┘
```

### 1. Crawl（爬取）
- **脚本**: `scripts/crawl.py`
- **功能**: 使用 HTTP 请求获取网页原始 HTML 内容
- **输出**: `data/raw/hn_aimaker_<timestamp>.html`

### 2. Extract（提取）
- **脚本**: `scripts/extract.py`
- **功能**: 解析 HTML，提取文章标题、链接、摘要、发布时间等信息
- **输出**: `data/extracted/articles_<timestamp>.json`

### 3. Organize（整理）
- **脚本**: `scripts/organize.py`
- **功能**: 对提取的数据进行清洗、去重、分类和格式化
- **输出**: `data/organized/articles_organized_<timestamp>.json`

### 4. Summarize（总结）
- **脚本**: `scripts/summarize.py`
- **功能**: 生成摘要报告，包括热点话题统计、趋势分析等
- **输出**: `data/summary/summary_<timestamp>.md`

## 快速开始

### 安装依赖

```bash
cd .trae/skills/hn-crawler/scripts
pip install -r requirements.txt
```

### 运行完整流程

```bash
# 方法1：逐个执行
python scripts/crawl.py
python scripts/extract.py
python scripts/organize.py
python scripts/summarize.py

# 方法2：一键执行完整流程
python scripts/run_pipeline.py
```

## 目录结构

```
.trae/skills/hn-crawler/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── requirements.txt        # Python 依赖
│   ├── crawl.py               # 爬取脚本
│   ├── extract.py             # 提取脚本
│   ├── organize.py            # 整理脚本
│   ├── summarize.py           # 总结脚本
│   └── run_pipeline.py        # 一键运行完整流程
└── data/                      # 数据输出目录（自动创建）
    ├── raw/                   # 原始 HTML
    ├── extracted/             # 提取的 JSON 数据
    ├── organized/             # 整理后的数据
    └── summary/               # 总结报告
```

## 数据格式

### 提取后的文章格式 (JSON)

```json
{
  "articles": [
    {
      "title": "文章标题",
      "url": "https://example.com/article",
      "summary": "文章摘要",
      "published_at": "2024-01-15T10:30:00",
      "source": "hn.aimaker.dev",
      "category": "AI",
      "score": 150
    }
  ],
  "metadata": {
    "crawled_at": "2024-01-15T12:00:00",
    "total_count": 30
  }
}
```

## 配置选项

各脚本支持以下环境变量或命令行参数：

- `TARGET_URL`: 目标 URL（默认: https://hn.aimaker.dev/）
- `OUTPUT_DIR`: 输出目录（默认: data/）
- `TIMEOUT`: 请求超时时间（默认: 30秒）

## 注意事项

1. 请遵守网站的 robots.txt 和爬虫协议
2. 建议设置适当的请求间隔，避免对服务器造成压力
3. 爬取的数据仅供个人学习研究使用
