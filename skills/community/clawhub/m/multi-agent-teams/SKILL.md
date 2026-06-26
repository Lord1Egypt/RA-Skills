---
name: multi-agent-teams
description: 交互式部署多 Agent 团队协作架构，支持自定义团队结构、预设模板和混合模式
homepage: https://github.com/MaybeMarvel/MyClaw/tree/main/skills/multi-agent-teams
metadata:
  {
    "openclaw":
      {
        "emoji": "🏢",
        "requires": { "bins": ["bash"] },
        "install": [],
      },
  }
---

# multi-agent-teams 技能

**版本：** v2.0  
**作者：** CXLight  
**描述：** 交互式部署多 Agent 团队协作架构

---

## 📋 功能

- **交互式配置** — 询问用户需求，创建合适的团队
- **预设模板** — 4 个标准团队快速部署
- **自定义团队** — 完全灵活的团队结构
- **混合模式** — 预设 + 自定义组合
- **自动生成** — SOUL.md/AGENTS.md 模板
- **配置验证** — 部署后自动验证

---

## 🚀 快速开始

### 安装

```bash
clawhub install multi-agent-teams
```

### 部署

```bash
cd ~/.openclaw/skills/multi-agent-teams
./scripts/deploy.sh
```

---

## 📖 使用方式

### 方式 1：交互式配置（推荐）

```bash
./scripts/deploy.sh
```

脚本会询问：
1. 配置模式（预设/自定义/混合）
2. 团队数量和名称
3. 每个团队的成员构成

### 方式 2：预设模板

```bash
./scripts/deploy.sh --preset
```

### 方式 3：帮助

```bash
./scripts/deploy.sh --help
```

---

## 🎯 配置模式

### 模式 1：预设模板

4 个标准团队：
- **code** (CTO) — 前端、后端、测试、产品、算法、审计
- **stock** (CIO) — 分析、风控、持仓、研究
- **social** (CMO) — 内容、排期、互动、数据分析
- **flow** (COO) — 工作流、定时、集成、监控

### 模式 2：自定义团队

创建任何你想要的团队：
- 客服团队
- 研究团队
- 设计团队
- 任何你需要的团队

### 模式 3：混合模式

预设 + 自定义组合

---

## 📁 目录结构

```
multi-agent-teams/
├── SKILL.md                 # 本文件
├── README.md                # 详细说明
├── templates/
│   ├── SOUL.md.tmpl         # SOUL.md 模板
│   └── AGENTS.md.tmpl       # AGENTS.md 模板
├── scripts/
│   ├── deploy.sh            # 部署脚本
│   └── verify.sh            # 验证脚本
└── generated/
    └── openclaw-snippet.json # 生成的配置
```

---

## 🧪 验证

```bash
./scripts/verify.sh
```

---

## ⚠️ 注意事项

1. **备份配置** — 部署前自动备份
2. **单一入口** — 所有请求通过 main-agent
3. **不要越级** — BOSS → main → 团队领导 → 成员
4. **重启生效** — 配置后需要 `openclaw gateway restart`

---

## 🐛 故障排查

### Agent 不识别

```bash
openclaw agents list
```

### sessions_spawn 失败

检查 subagents 配置是否包含目标成员。

---

## 📚 完整文档

技术文档：`/root/.openclaw/docs/multi-agent-team-architecture.md`

---

## 📝 更新日志

### v2.0 (2026-03-16)
- ✨ 新增交互式配置
- ✨ 支持自定义团队结构
- ✨ 混合模式（预设 + 自定义）

### v1.0 (2026-03-16)
- 初始版本
