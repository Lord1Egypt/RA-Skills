---
name: miaoda-web-search
description: "ALWAYS use this skill FIRST when you need to find, look up, or verify ANY information from the internet — do NOT guess URLs and fetch them directly. Provides necessary command usage instructions for keyword-based web search with AI-generated summaries. 触发词：搜索, 网页搜索, 搜一下, 查一下, 查询, 了解, 找一下, 帮我看看, web search, look up, find out, search, 搜索摘要, 查资料, 搜索引擎, 最新信息, 最近动态"
override-tools:
  - web_search
---

# Web Search

通过 `miaoda-studio-cli search-summary` 按关键词搜索互联网信息，由 AI 自动总结。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--query` | 搜索关键词（1-500 字符） | 是 | - |
| `--output, -o` | 输出格式: text/json | 否 | text |

## 命令选择决策树

```
用户想获取互联网信息
├─ 有具体 URL → miaoda-studio-cli web-crawl（见 miaoda-web-fetch skill）
├─ 无具体 URL，需搜索 → miaoda-studio-cli search-summary
└─ 先搜索再深入 → search-summary 获取 URL → web-crawl 提取详情（见 miaoda-web-fetch skill）
```

## 使用示例

```bash
# 按关键词搜索
miaoda-studio-cli search-summary --query "React 19 新特性"

# 搜索并获取 JSON 输出
miaoda-studio-cli search-summary --query "ByteDance 开源项目" --output json
```

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 无具体 URL 时用 `miaoda-studio-cli web-crawl` | 无 URL 用 `miaoda-studio-cli search-summary`，有 URL 用 `miaoda-studio-cli web-crawl`（见 miaoda-web-fetch skill） |
| 搜索关键词超过 500 字符 | 提炼核心关键词，保持精简 |
| 需要后续程序处理结果但未加 `--output json` | 需要解析结果时始终加 `--output json` |
| 命令失败后不检查退出码 | 退出码 `1` 表示失败，检查参数和网络后重试 |
