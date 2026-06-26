---
name: huo15-memory-evolution
description: 火一五记忆进化技能 - 完全自主实现，提供四类记忆分类、Dream Agent 日志提炼、Team Memory 共享、Auto Capture 自动捕获、Session State 管理器、任务进度追踪器。自主实现 Claude Code 的 Auto Memory 和 Compaction 保护机制。触发词：记忆系统、记忆进化、记忆重构。
dependencies:
  required: []
---

# 🧠 火一五记忆进化技能

> 完全自主实现的 OpenClaw 记忆系统，对标 Claude Code 源码

[![版本](https://img.shields.io/badge/version-v3.4.5-blue)](https://clawhub.ai/jobzhao15/huo15-memory-evolution)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📖 目录

- [特性](#-特性)
- [快速开始](#-快速开始)
- [核心概念](#-核心概念)
- [脚本清单](#-脚本清单)
- [开发计划](#-开发计划)
- [版本历史](#-版本历史)
- [相关链接](#-相关链接)

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| 🗂️ **四类记忆分类** | user / feedback / project / reference |
| 🔒 **Agent 记忆隔离** | 每个企微用户/群聊独立记忆空间 |
| 🌙 **Dream Agent** | 每日自动日志提炼，LLM 驱动 |
| ✅ **Auto Capture** | 实时捕获高光时刻，不依赖定时 |
| 👥 **Team Memory** | 群聊 agent 之间共享部分记忆 |
| 🔄 **Session State** | Compaction 保护，防止上下文丢失 |
| 🌊 **Drift 校验** | 自动检测过时记忆 |
| 🚀 **批量安装** | 一键为所有动态 agent 安装 |

---

## ⚡ 快速开始

### 前置要求

- OpenClaw 已安装
- 企微插件已安装（必须先安装）

### 安装

```bash
# 1. 安装技能
clawhub install huo15-memory-evolution

# 2. 初始化
cd ~/.openclaw/workspace/skills/huo15-memory-evolution
./scripts/install.sh

# 3. 批量安装到所有动态 Agent
./scripts/batch-install.sh

# 4. 验证
./scripts/verify.sh
```

### 使用

```bash
# 保存记忆
./scripts/auto-capture.sh "用户喜欢简洁回答" user

# 查看记忆
cat ~/.openclaw/workspace/MEMORY.md

# 运行 Dream Agent
./scripts/dream.sh

# 检查 drift
./scripts/check-drift.sh
```

---

## 📚 核心概念

### 记忆分类体系

| 类型 | 说明 | 示例 |
|------|------|------|
| **user** | 用户画像、偏好、习惯 | Sir 喜欢简洁回答 |
| **feedback** | 纠正反馈、确认偏好 | 不要用 touser 发图片 |
| **project** | 项目上下文、决策、进展 | 软著申请已开始 |
| **reference** | 外部系统指针 | Odoo 系统地址 |

### 记忆文件格式

```yaml
---
name: wecom-media-send-rule
type: feedback
description: 企微群聊发图片必须用 chatid，不是 touser
created: 2026-03-31
---

## 规则
企微群聊发图片必须用 chatid，不是 touser

**Why:** 之前用 touser 发送图片失败，报错 86008

**How to apply:** 在企微群聊场景下，媒体发送一律使用 chatid 参数
```

### 禁止写入的内容

- ❌ 代码模式、约定、架构 — 可从代码推导
- ❌ Git 历史 — `git log` 权威
- ❌ 调试方案 — 修复在代码中
- ❌ 实际凭证值 — 只记录位置
- ❌ 临时任务详情 — 写在 HEARTBEAT.md

### Agent 隔离架构

```
~/.openclaw/
├── workspace/                          # 主 Agent (ZhaoBo)
│   └── memory/                        # 主记忆
├── workspace-wecom-default-dm-xun/    # Xun 的独立空间
│   └── memory/                        # 独立记忆（完全隔离）
└── workspace-wecom-default-group-xxx/ # 群聊 Agent
    └── memory/
```

---

## 🔧 脚本清单

| 脚本 | 功能 | 频率 |
|------|------|------|
| `dream.sh` | 每日日志提炼（4阶段） | 每天 09:00 |
| `auto-capture.sh` | **自动捕获高光时刻** | **实时** |
| `session-memory.sh` | 当前会话笔记 | 实时 |
| `session-state.sh` | Session State 管理器 | HEARTBEAT |
| `task-progress.sh` | 任务进度追踪 | 按需 |
| `memory-recall.sh` | 记忆检索 | 按需 |
| `memory-extract.sh` | 后台记忆提取 | 实时 |
| `memory-freshness.sh` | 新鲜度检查 | 按需 |
| `dream-lock.sh` | Consolidation Lock | dream 时 |
| `context-suggest.sh` | Context 建议生成器 | HEARTBEAT |
| `team-memory-sync.sh` | Team Memory 同步 | 按需 |
| `check-drift.sh` | Drift 校验 | 每 6 小时 |
| `save-memory.sh` | 主动记忆写入 | 按需 |
| `team-memory.sh` | Team Memory 共享 | 按需 |
| `install.sh` | 从零安装 | 首次安装 |
| `batch-install.sh` | 批量安装 | 首次安装 |
| `verify.sh` | 验证安装 | 按需 |

---

## 📋 开发计划

> 截止日期：2026-04-30

### 进行中

- [x] **findRelevantMemories** - ✅ LLM 智能选择记忆 (v3.5.0)
  - 使用 LLM 从记忆中智能选择最相关的 5 个返回
  - 参考：`src/memdir/findRelevantMemories.ts`

- [ ] **CLAUDE.md 发现注入** - 项目级自动发现和注入
  - 在工作目录查找 CLAUDE.md 并注入上下文
  - 参考：OpenHarness 实现

- [ ] **Manifest pre-inject** - 提取前注入记忆列表
  - 让 LLM 知道已有记忆，避免重复

- [ ] **Forked extraction** - 后台 subagent 提取
  - 使用 sessions_spawn 后台运行，不阻塞主对话

- [ ] **Throttle N turns** - 每 N 轮提取一次
  - 与 HEARTBEAT 集成

- [ ] **Skip if main wrote** - 主 agent 已写则跳过
  - 完整实现并测试

---

## 📜 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| **v3.5.0** | 2026-04-06 | LLM 智能检索 memory-recall v3.0 + Session State v2.0（追踪摘要边界）+ 任务指令自动捕获|
| **v3.4.5** | 2026-04-07 | 新增异步任务追踪（add_pending_task/update_pending_task/list_pending_tasks）+ session-state.sh 集成 |
| **v3.4.3** | 2026-04-06 | 修复 memory-recall.sh 缺少 sys 导入 + inject 72小时超时检查 + 清理 activity 目录 |
| **v3.4.0** | 2026-04-05 | 新增 context-suggest.sh + team-memory-sync.sh + Dream Gates |
| **v3.3.0** | 2026-04-05 | 新增 memory-recall.sh + memory-extract.sh + memory-freshness.sh + dream-lock.sh |
| **v3.2.0** | 2026-04-05 | 新增去重检查 + 更新/删除机制 + Session Memory + Before recommending |
| **v3.1.0** | 2026-04-05 | 完全自主实现：移除 fluid-memory 等第三方依赖 |
| **v3.0.0** | 2026-04-05 | 新增 Auto Capture + 统一存储路由 + 批量安装 |
| **v2.0.0** | 2026-04-04 | Dream Agent + Drift 校验 |
| **v1.0.0** | 2026-04-03 | 初始版本 |

---

## 🔗 相关链接

- **ClawHub**: https://clawhub.ai/jobzhao15/huo15-memory-evolution
- **源码仓库**: https://cnb.cool/huo15/openclaw-workspace
- **Claude Code 源码**: https://github.com/modelcontextprotocol/servers

---

## 📄 License

MIT License - 火一五信息科技有限公司出品
