---
name: mama-crawler
description: 妈妈网育儿知识爬虫（PC端）。爬取妈妈网（www.mama.cn）育儿文章，输出 Markdown 格式并存入御知库（~/.yuzhi/crawls/mama_cn/）。默认使用PC端User-Agent，按分类或关键词搜索爬取。帝说"爬取妈妈网"、"/爬虫"或需要采集育儿知识时触发。
---

# 妈妈网育儿知识爬虫（PC端）

## 命令

### `python3 scripts/mama_crawler.py --category <分类> --max-pages <页数> --max-articles <数量>`
按分类爬取妈妈网文章（PC端）。

分类选项：
- `baby` — 亲子
- `yingyang` — 营养
- `disease` — 疾病
- `lady` — 女性
- `yongpin` — 用品
- `life` — 生活

### `python3 scripts/mama_crawler.py --search <关键词> --max-articles <数量>`
通过PC端搜索爬取相关文章。

### `python3 scripts/mama_crawler.py --all --max-pages 3 --max-articles 30`
爬取所有分类（慎用，会花较长时间）。

## 输出

文章保存到 `~/.yuzhi/crawls/mama_cn/<分类名>/` 目录下，每个文章一个 `.md` 文件，包含标题、来源、日期和正文。

## 反爬机制

- 每次请求间隔 2-5 秒随机延迟
- 使用桌面浏览器 User-Agent
- 不验证 SSL 证书

## 技术说明

- 默认 PC 端（www.mama.cn），结构稳定
- 文章 URL 格式：`https://www.mama.cn/z/art/<id>/`
- PC 端分类页面文章较少，建议使用 `--search` 关键词搜索模式获取更多内容
