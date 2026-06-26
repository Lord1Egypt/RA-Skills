---
name: news-hot-hub
description: 新闻热点数据聚合器——整合知乎、今日头条、AIBase三大平台热搜数据。支持单独获取任一平台热榜，也支持一次性获取所有平台数据并汇总输出。当用户提到"热搜聚合"、"全平台热点"、"各平台热门话题"、"热榜整合"、"热点数据采集"、"我要看全网热点"、"刷一下各平台热榜"、"一键获取热榜"、"知乎头条热榜"、"全网热点"、"多平台热搜"时使用此技能。也可以单独触发某个平台：提到"知乎热搜/知乎热门/知乎数据"触发知乎，提到"头条热榜/今日头条"触发头条，提到"AIBase/AI基地/AI新闻/AI日报"触发AIBase。
---

# news Hot Hub — 中文热点数据聚合器

## 概述

整合知乎、今日头条、AIBase三大中文平台的热搜/热门数据。采用「调度器 + 独立脚本」插件式架构，每个平台一个独立 Python 脚本，由统一的 `hub.py` 调度。

## 目录结构

```
news-hot-hub/
├── SKILL.md                 # 本文件 — AI Agent 技能指令
├── requirements.txt         # Python 依赖
├── scripts/                 # 可执行脚本
│   ├── hub.py               # 统一调度入口 ★
│   ├── zhihu.py             # 知乎（已实现）
│   ├── toutiao.py           # 今日头条（已实现）
│   └── aibase.py            # AIBase（已实现）
└── references/              # 参考文档
    ├── architecture.md      # 架构设计
    ├── data-schema.md       # 数据格式规范
    └── platform-guide.md    # 平台接入指南
```

## 安装

```bash
pip install -r ${SKILL_DIR}/requirements.txt
```

核心依赖：`requests`, `beautifulsoup4`, `lxml`

## CLI 使用

统一入口：`${SKILL_DIR}/scripts/hub.py`

```bash
python ${SKILL_DIR}/scripts/hub.py <command> [options]
```

### 平台标识

| 全称 | 缩写 | 中文 |
|---|---|---|
| `zhihu` | `zh` | 知乎 |
| `toutiao` | `tt` | 今日头条 |
| `aibase` | `ab` | AIBase |

### 命令一览

| 命令 | 说明 | 选项 |
|---|---|---|
| `fetch <platform>` | 获取指定平台热榜 | `--limit N` |
| `all` | 并行获取全部平台 | `--limit N` |
| `compare` | 跨平台热点词频对比 | `--limit N` |
| `status` | 检查各平台脚本可用性 | — |

### 使用示例

```bash
# 单平台获取
python ${SKILL_DIR}/scripts/hub.py fetch zhihu
python ${SKILL_DIR}/scripts/hub.py fetch toutiao --limit 20
python ${SKILL_DIR}/scripts/hub.py fetch aibase
python ${SKILL_DIR}/scripts/hub.py fetch aibase daily

# 多平台
python ${SKILL_DIR}/scripts/hub.py fetch zhihu,toutiao

# 全部平台
python ${SKILL_DIR}/scripts/hub.py all

# 跨平台对比
python ${SKILL_DIR}/scripts/hub.py compare

# 检查可用性
python ${SKILL_DIR}/scripts/hub.py status
```

## 触发逻辑

Agent 加载本 skill 后，根据用户意图判断调用方式：

1. **只提单一平台** → `fetch <platform>`
2. **提到多个平台** → `fetch <p1>,<p2>` 逗号分隔
3. **“全部”/“所有”/“一键”/“全平台”** → `all`
4. **“对比”/“比较”/“交叉分析”** → `compare`
5. **不明确** → 询问用户需要哪个/哪些平台

### AIBase子命令映射

| 用户意图 | 子命令 |
|---|---|
| AI新闻 | `fetch aibase`（默认 hot-search → news）|
| AI日报 | `fetch aibase daily` |
| AI新闻+日报 | `fetch aibase all` |

## 输出格式

### fetch / all

JSON Lines（每行一个平台结果）：

```json
{"platform": "知乎", "success": true, "data": {"type": "hot_search", "count": 25, "data": [...]}}
```

### compare

跨平台词频分析 JSON，包含 `top_keywords` 和 `per_platform` 字段。

> 详细数据格式见 `references/data-schema.md`

## 环境变量

| 变量 | 说明 |
|---|---|
| `HOT_HUB_LIMIT` | 全局默认 limit，CLI `--limit` 可覆盖 |

## 参考文档

需要深入了解时，按需读取 `references/` 目录下的文档：

- **架构设计** → `references/architecture.md`：系统架构、数据流、扩展机制
- **数据格式** → `references/data-schema.md`：各平台 JSON 输出字段详细定义
- **接入指南** → `references/platform-guide.md`：新平台接入步骤、脚本模板、认证说明

## 快速参考

| 需求 | 命令 |
|---|---|
| 知乎热搜 | `fetch zhihu` |
| 头条热榜 | `fetch toutiao` |
| AIBase新闻 | `fetch aibase` |
| AI日报 | `fetch aibase daily` |
| 全部平台 | `all` |
| 词频对比 | `compare` |
| 可用性检查 | `status` |
