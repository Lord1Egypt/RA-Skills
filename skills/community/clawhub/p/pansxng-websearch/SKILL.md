---
name: pansxng-websearch
version: 1.0.0
description: |
  自包含的本地元搜索引擎技能。基于 SearXNG，零配置，开箱即用。
  触发词：搜索、搜一下、pansxng、联网搜索、私密搜索、searx、帮我搜、xxx是什么。
  使用场景：(1) 联网搜索 (2) 多引擎聚合 (3) 隐私搜索 (4) 指定引擎搜索
  无需任何前置条件——首次使用时自动安装全部依赖（Homebrew → Python 3.11 → Valkey → SearXNG）。
---

# PansXNG Websearch

基于 SearXNG 开源项目的**完全自包含**元搜索引擎。
**零手动配置**——首次使用时自动安装所有依赖，后续自动启动。

## 使用方式

直接说：
- "帮我搜 xxx"
- "搜索 xxx 是什么"
- "搜一下深圳天气"

## 自动安装链

```
首次搜索
  ├─ Homebrew 缺失？→ 自动安装
  ├─ Python 3.11 缺失？→ 自动安装
  ├─ Valkey 缺失？→ 自动安装
  └─ SearXNG 缺失？→ 自动克隆 + 安装依赖 + 配置
  → 启动 → 搜索 ✅
```

## 搜索脚本

路径：`scripts/search.py`

```bash
# 搜索
python3 scripts/search.py "关键词" [选项]

# 选项
--lang, -l     语言 (默认 zh-CN)
--count, -n    结果数量 (默认 10)
--json, -j     输出原始 JSON
--engines, -e  指定引擎 (逗号分隔，如 baidu,bing,sogou)
--categories, -c  分类: general, images, videos, news, it, science

# 管理
--status       查看完整状态
--install      手动触发安装
--start        手动启动
--stop         停止服务
```

## 回退机制

脚本返回 JSON 包含 `"fallback": true` 时，OpenClaw 自动回退到内置 `web_search` 工具。
确保任何情况下都有搜索结果。

## 国内可用引擎

- ✅ 百度 (baidu) — **推荐国内搜索**
- ✅ 搜狗 (sogou)
- ✅ 360搜索 (360search)
- ✅ Bing
- ⚠️ Google / DuckDuckGo — 国内可能超时

## 隐私

所有搜索请求通过本地 SearXNG 实例发出，无法追踪真实 IP。
