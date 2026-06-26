---
name: miaoda-web-fetch
description: "Use when user needs to crawl or fetch a specific URL to extract/summarize its content. Provides necessary command usage instructions for fetching known URLs. 触发词：网页抓取, 抓取网页, 提取网页内容, web crawl, 爬取, fetch url, 总结网页, 抓取 URL, 读取网页"
override-tools:
  - web_fetch
---

# Web Fetch

通过 `miaoda-studio-cli web-crawl` 抓取指定网页内容，由 AI 自动总结/提取。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--url` | 网页 URL | 是 | - |
| `--output, -o` | 输出格式: text/json | 否 | text |

## 命令选择决策树

```
用户想获取互联网信息
├─ 有具体 URL → miaoda-studio-cli web-crawl
├─ 无具体 URL，需搜索 → miaoda-studio-cli search-summary（见 miaoda-web-search skill）
└─ 先搜索再深入 → search-summary 获取 URL（见 miaoda-web-search skill）→ web-crawl 提取详情
```

## 使用示例

```bash
# 抓取指定 URL 并提取信息
miaoda-studio-cli web-crawl --url https://example.com/pricing

# 搜索 → 深入抓取：先搜索找到目标 URL，再抓取提取详细信息
miaoda-studio-cli search-summary --query "ByteDance 开源项目" --output json
miaoda-studio-cli web-crawl --url <搜索结果中的URL>
```

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 无具体 URL 时用 `miaoda-studio-cli web-crawl` | 无 URL 用 `miaoda-studio-cli search-summary`（见 miaoda-web-search skill） |
| 需要后续程序处理结果但未加 `--output json` | 需要解析结果时始终加 `--output json` |
| 命令失败后不检查退出码 | 退出码 `1` 表示失败，检查参数和网络后重试 |
