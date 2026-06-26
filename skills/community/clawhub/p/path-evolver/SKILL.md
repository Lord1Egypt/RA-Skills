---
name: path-evolver
description: 记录 skill 使用成功率，主动发现更优工具，提示用户选择。Use when tracking skill success rates or discovering better tools.
license: MIT
compatibility: Creates cache file at ~/.openclaw/workspace/.path-evolver/workflow-cache.json
metadata:
  author: doudoulaodou
  version: "1.1.1"
  keywords: "optimization, learning, tracking, discovery"
  config:
    cachePath: ~/.openclaw/workspace/.path-evolver/workflow-cache.json
  network:
    required: true
    endpoints:
      - https://clawhub.ai
      - https://api.github.com
  security:
    dataStorage: "Local JSON cache only, no external uploads"
    sensitiveData: "Cache may contain task parameters; user should review cache contents"
    networkUsage: "Search queries only send task TYPE (e.g., 'web-search'), NOT task parameters or user data"
    dataSanitization: "Before searching ClawHub/GitHub, strip all user-provided content, keep only task category"
---

# Path Evolver

> Track skill success rates, discover better tools, prompt user to choose.

记录 skill 使用成功率，主动发现更优工具，提示用户选择。

---

## 🌐 Language / 语言

- [English](#english) (Below)
- [中文](#中文) (下方)

---

<a name="english"></a>
## English

### What is Path Evolver?

A lightweight skill that:
- **Tracks Success Rates** - Record how often each skill succeeds
- **Discovers Better Tools** - Search ClawHub/GitHub for alternatives
- **Prompts User** - Suggest better options when found

### What It Does NOT Do

- ❌ Auto-update OpenClaw priority config
- ❌ Intercept or replace skills automatically
- ❌ Force any changes without user confirmation

### Workflow

```
User uses skills (normal flow)
    ↓
Path Evolver records success/failure (background)
    ↓
Periodically analyze + search ClawHub
    ↓
Found better tool? → Prompt user:
    "Found [new-skill] with higher success rate. Switch?"
    ↓
User decides → Manual config update
```

### When to Use

| Trigger | Action |
|---------|--------|
| After skill execution | Record success/failure |
| New task type | Search ClawHub for relevant skills |
| Tool failure | Search for alternatives |
| User request | Analyze and recommend |

### Example

```
User: Search for OpenClaw tutorial

AI uses: web_search (success)
Path Evolver: records web_search successCount: 1

User: Search for AIOps best practices

AI uses: multi-search-engine (success, better results)
Path Evolver: records multi-search-engine successCount: 1

After 10 searches:
Path Evolver analysis:
- web_search: 3 uses, 67% success
- multi-search-engine: 4 uses, 100% success
- tavily-search: 3 uses, 100% success

Prompt user:
"tavily-search has 100% success rate. Consider using it for search tasks."
```

### Configuration

```json
{
  "cachePath": "~/.openclaw/workspace/.path-evolver/workflow-cache.json",
  "searchTriggers": {
    "newTaskType": true,
    "toolFailure": true,
    "userRequest": true
  }
}
```

### Installation

```bash
clawhub install path-evolver
```

---

<a name="中文"></a>
## 中文

### 什么是 Path Evolver？

一个轻量级技能：
- **追踪成功率** - 记录每个 skill 的成功次数
- **发现更优工具** - 搜索 ClawHub/GitHub 寻找替代方案
- **提示用户** - 发现更好选择时建议用户

### 不做什么

- ❌ 自动更新 OpenClaw 优先级配置
- ❌ 拦截或自动替换 skills
- ❌ 未经用户确认强制更改

### 工作流程

```
用户使用 skills（正常流程）
    ↓
Path Evolver 记录成功/失败（后台）
    ↓
定期分析 + 搜索 ClawHub
    ↓
发现更优工具？→ 提示用户：
    "发现 [new-skill] 成功率更高，是否切换？"
    ↓
用户决定 → 手动更新配置
```

### 使用时机

| 触发条件 | 行为 |
|----------|------|
| skill 执行后 | 记录成功/失败 |
| 新任务类型 | 搜索 ClawHub 相关 skills |
| 工具失败 | 搜索替代方案 |
| 用户请求 | 分析并推荐 |

### 示例

```
用户：搜索 OpenClaw 教程

AI 使用：web_search（成功）
Path Evolver：记录 web_search successCount: 1

用户：搜索 AIOps 最佳实践

AI 使用：multi-search-engine（成功，结果更好）
Path Evolver：记录 multi-search-engine successCount: 1

10 次搜索后：
Path Evolver 分析：
- web_search: 3 次，成功率 67%
- multi-search-engine: 4 次，成功率 100%
- tavily-search: 3 次，成功率 100%

提示用户：
"tavily-search 成功率 100%，建议用于搜索任务。"
```

### 安装

```bash
clawhub install path-evolver
```

---

## 🔒 数据隐私说明

### 数据流向

| 数据 | 存储位置 | 是否发送到外部 |
|------|----------|---------------|
| 任务类型 | 本地缓存 | ✅ 是（仅类型，如 "web-search"） |
| 任务参数 | 本地缓存 | ❌ 否 |
| 用户数据 | 无 | ❌ 否 |

### 搜索行为

当搜索 ClawHub/GitHub 时：
- ✅ 发送：任务类型（如 "web-search", "image-gen"）
- ❌ 不发送：用户输入、任务参数、敏感数据

### 示例

```
用户任务：搜索 OpenClaw 教程

本地缓存记录：
{
  "taskType": "web-search",
  "tool": "tavily-search",
  "success": true
}

搜索 ClawHub 时发送：
query: "web-search tools"  // 仅任务类型，不含用户输入
```

---

## 与 OpenClaw 原生机制的关系

| OpenClaw Priority | Path Evolver |
|-------------------|--------------|
| 静态配置 | 动态学习 |
| 手动设置 | 自动记录 |
| 不追踪成功率 | 追踪成功率 |
| 不发现新工具 | 主动发现 |

**互补关系：** Path Evolver 提供数据，用户手动更新 Priority

---

## 文件结构

```
path-evolver/
├── SKILL.md              # 本文件
├── README.md             # 说明文档
├── assets/
│   └── workflow-cache-template.json
└── references/
    └── design-decisions.md
```

---

## License

MIT License
