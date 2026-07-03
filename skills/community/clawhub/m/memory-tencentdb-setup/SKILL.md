# memory-tencentdb 安装指南

## 概述

memory-tencentdb 是 OpenClaw 的四层记忆系统插件，支持自动捕获对话、结构化提取（L1）、场景分块（L2）和用户画像（L3）。

本指南涵盖插件安装、依赖配置、常见问题排查。

---

## 系统要求

| 项目 | 要求 |
|------|------|
| OpenClaw 版本 | >= 0.20.0 |
| Node.js 版本 | >= 18.x |
| 操作系统 | Windows / macOS / Linux |

---

## 安装步骤

### 1. 下载插件

```bash
# 从 ClawHub 安装
clawhub install memory-tencentdb

# 或手动下载到插件目录
# Windows: %APPDATA%\mx\openclaw-home\<account>\.openclaw\plugins\memory-tencentdb
# macOS/Linux: ~/.openclaw/plugins/memory-tencentdb
```

### 2. 安装依赖

**关键步骤**：插件依赖必须安装到 **Gateway 的 node_modules** 目录，而不是插件目录。

#### 方法 A：直接复制到 Gateway 目录（推荐）

```powershell
# Windows 示例
# 1. 先在插件目录安装依赖
cd "插件目录"
npm install --ignore-scripts

# 2. 复制到 Gateway node_modules
Copy-Item -Path "插件目录\node_modules\js-tiktoken" -Destination "Gateway目录\node_modules\js-tiktoken" -Recurse -Force
```

#### 方法 B：直接在 Gateway 目录安装

```powershell
# Windows 示例
cd "Gateway目录"
npm install js-tiktoken --ignore-scripts
```

### 3. 配置 openclaw.json

在 `openclaw.json` 中添加插件配置：

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["mx", "memory-tencentdb"],
    "load": {
      "paths": ["~/.openclaw/plugins/memory-tencentdb"]
    },
    "slots": {
      "memory": "memory-tencentdb"
    },
    "entries": {
      "memory-tencentdb": {
        "enabled": true,
        "config": {
          "pipeline": {
            "everyNConversations": 3,
            "enableWarmup": true,
            "l1IdleTimeoutSeconds": 10
          }
        }
      }
    }
  }
}
```

### 4. 重启 Gateway

**重要**：SIGUSR1 信号只重新加载配置，不会重新加载插件。必须完全重启 Gateway。

```bash
# 完全重启（推荐）
openclaw gateway stop
openclaw gateway start

# 或使用 mx 客户端重启
```

---

## 关键路径说明

### Windows 路径

| 项目 | 路径 |
|------|------|
| 插件目录 | `%APPDATA%\mx\openclaw-home\<account>\.openclaw\plugins\memory-tencentdb\` |
| Gateway 目录 | `%LOCALAPPDATA%\openclaw\mx\current\` |
| Gateway node_modules | `%LOCALAPPDATA%\openclaw\mx\current\node_modules\` |
| 配置文件 | `%APPDATA%\mx\openclaw-home\<account>\.openclaw\openclaw.json` |
| 记忆数据 | `%APPDATA%\mx\openclaw-home\<account>\.openclaw\memory-tdai\` |

### macOS/Linux 路径

| 项目 | 路径 |
|------|------|
| 插件目录 | `~/.openclaw/plugins/memory-tencentdb/` |
| Gateway 目录 | `~/.openclaw/gateway/` |
| 配置文件 | `~/.openclaw/openclaw.json` |
| 记忆数据 | `~/.openclaw/memory-tdai/` |

---

## 验证安装

### 1. 检查插件加载

```bash
# 查看日志，确认无报错
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep memory-tencentdb
```

正常输出应无 `Cannot find module` 错误。

### 2. 检查记忆数据

```bash
# 查看对话捕获
ls -la ~/.openclaw/memory-tdai/conversations/

# 查看 L1 记录
ls -la ~/.openclaw/memory-tdai/records/

# 查看向量数据库
ls -la ~/.openclaw/memory-tdai/vectors.db
```

### 3. 检查配置

```bash
# 使用 OpenClaw CLI 检查配置
openclaw config get | grep -A 20 "memory-tencentdb"
```

---

## 常见问题

### Q1: 插件加载失败，报错 `Cannot find module 'js-tiktoken'`

**原因**：依赖安装到了插件目录，但 Gateway 使用 jiti 加载插件时，从 Gateway 目录解析依赖。

**解决方案**：

```powershell
# 将 js-tiktoken 复制到 Gateway node_modules
Copy-Item -Path "插件目录\node_modules\js-tiktoken" -Destination "Gateway目录\node_modules\js-tiktoken" -Recurse -Force

# 完全重启 Gateway
openclaw gateway stop
openclaw gateway start
```

### Q2: SIGUSR1 重启后插件未生效

**原因**：SIGUSR1 信号只重新加载配置，不会重新加载插件。

**解决方案**：必须完全重启 Gateway（stop + start）。

### Q3: 如何确认 Gateway 使用的 node_modules 路径？

**诊断方法**：

```powershell
# Windows: 确认 Gateway 进程使用的 node 路径
(Get-Process -Id <PID>).Path

# 确认启动参数
(Get-WmiObject Win32_Process -Filter "ProcessId=<PID>").CommandLine
```

### Q4: L1 提取不触发

**检查项**：
1. 插件是否正常加载（查看日志）
2. `pipeline.everyNConversations` 配置是否合理（默认 3）
3. `pipeline.l1IdleTimeoutSeconds` 是否设置（默认 10 秒）
4. 是否有足够的对话积累

---

## 依赖列表

memory-tencentdb 需要以下核心依赖：

| 依赖 | 用途 |
|------|------|
| `js-tiktoken` | Token 计数，用于上下文管理 |
| `better-sqlite3` | 本地 SQLite 数据库（可选，用于向量存储） |

**注意**：所有依赖必须安装到 Gateway 的 node_modules 目录。

---

## 架构说明

memory-tencentdb 采用四层记忆架构：

| 层级 | 名称 | 功能 |
|------|------|------|
| L0 | 原始对话 | 自动捕获所有对话，存储为 JSONL |
| L1 | 结构化记录 | 从对话中提取关键信息（episodic/instruction/semantic） |
| L2 | 场景分块 | 按场景组织记忆，支持上下文召回 |
| L3 | 用户画像 | 长期学习用户偏好和行为模式 |

---

## 更新日志

### v0.3.8 (2026-06-15)
- 修复依赖解析问题
- 优化 L1 提取性能
- 增加向量数据库支持

### v0.3.7 (2026-06-08)
- 移除独立 LLM 代码，使用 Gateway 内置模型
- 优化 Pipeline 状态管理

---

## 相关链接

- ClawHub 页面: https://clawhub.ai/skills/memory-tencentdb
- OpenClaw 文档: https://docs.openclaw.ai
- 问题反馈: https://github.com/openclaw/openclaw/issues

---

## 许可证

MIT License
