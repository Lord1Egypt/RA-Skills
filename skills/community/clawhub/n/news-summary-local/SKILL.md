---
name: news-summary
version: "1.0.0"
description: |
  本地新闻摘要 Skill。读取工作区内的 RSS/XML 文件，提取标题并生成简洁列表。
maintainer:
  name: 王可以
  email: you@example.com
---

# News Summary

## Usage

```bash
# 在工作区根目录或任意路径运行
./summarize.sh news.rss   # 参数为 RSS 文件路径，默认使用 workdir 下的 news.rss
```

## 实现细节
- `extract.sh` 使用 `grep`/`sed` 提取 `<title>` 标签内的文本。
- `summarize.sh` 调用 `extract.sh` 并输出前 10 条标题。
