---
name: tech-news-digest
description: 自动生成科技新闻摘要。从多个来源（RSS、Twitter、GitHub、Web Search）抓取科技新闻，整合后生成摘要。
---

# Tech News Digest

自动科技新闻摘要生成器。

## 功能

- 从 6 个来源并行抓取新闻：RSS、Twitter、GitHub、Web Search 等
- 自动去重、评分、排序
- 支持 Discord、Email、PDF 模板输出

## 使用方法

### 配置

```bash
# 复制默认配置
mkdir -p workspace/config
cp config/defaults/sources.json workspace/config/
cp config/defaults/topics.json workspace/config/
```

### 环境变量（可选）

- `TWITTERAPI_IO_KEY` - Twitter API
- `X_BEARER_TOKEN` - X Twitter
- `TAVILY_API_KEY` - 搜索 API
- `BRAVE_API_KEY` - Brave Search
- `GITHUB_TOKEN` - GitHub

### 生成摘要

```bash
python3 scripts/run-pipeline.py \
  --defaults config/defaults \
  --config workspace/config \
  --hours 48 \
  --output /tmp/td-merged.json
```

## 注意

- 需要 Python 3
- 需要安装依赖：`pip install -r requirements.txt`
- 免费 API 额度有限
