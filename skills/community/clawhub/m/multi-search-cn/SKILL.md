---
name: multi-search-cn
description: 聚合国内常用搜索引擎：默认用 DuckDuckGo HTML（cn-zh）零 API Key 抓取可解析结果，并输出必应中国、百度、搜狗、360 的直达搜索链接。当用户需要中文网页检索、国内信息、政策/舆情、对比多个搜索引擎、或 Brave/Google 不可用时使用。依赖 Python 3 标准库与 scripts/search_cn.py。
---

# Multi-Search-CN（国内多搜索引擎）

## 依赖

- **Python 3.8+**（macOS / Ubuntu / WSL 通常已有）
- 本 Skill 内脚本：`scripts/search_cn.py`（无 pip 依赖）

## 快速使用

在项目根或任意目录：

```bash
python3 .cursor/skills/multi-search-cn/scripts/search_cn.py "深圳 天气"
```

仅打印各引擎**搜索页链接**（不联网解析）：

```bash
python3 .cursor/skills/multi-search-cn/scripts/search_cn.py "关键词" --urls-only
```

机器可读 JSON：

```bash
python3 .cursor/skills/multi-search-cn/scripts/search_cn.py "OpenClaw" --json
```

## Agent 行为约定

1. **默认**先跑 `search_cn.py`（不带 `--urls-only`），把 DDG 解析结果 + 各引擎直达链接一并交给用户。
2. 若解析失败或无结果：**明确说明**，并给出 `--urls-only` 的链接列表，建议用户浏览器打开百度/必应。
3. **不要**假装已「爬遍」百度/必应正文；纯 curl 常被风控，本 Skill 不以解析百度 HTML 为承诺。
4. 高频请求前提醒用户注意频率与合规。

## 与 Brave / Baidu Search 等 Skill 的关系

- 有 **Brave API Key** 时优先用官方 Brave Search Skill。
- 无 Key 或需**国内结果**时，用本 Skill 的 DDG（cn-zh）+ 国内引擎直达链接。

## 更多

- 排错与 OpenClaw 说明见 [reference.md](reference.md)。
