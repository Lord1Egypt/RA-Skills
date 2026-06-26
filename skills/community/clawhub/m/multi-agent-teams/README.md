# 多 Agent 团队协作架构

**交互式部署工具**

---

## 🎯 概述

本技能帮助你**交互式地**在 OpenClaw 中部署多 Agent 团队协作系统。

**核心特性：**
- 🤖 **交互式配置** — 回答几个问题，自动创建团队
- 📦 **预设模板** — 4 个标准团队一键部署
- 🎨 **完全自定义** — 创建任何你想要的团队
- 🔧 **自动生成** — 配置片段、SOUL.md 模板

---

## 📋 前置要求

- OpenClaw v2026.1.6+
- 已配置模型访问权限
- Bash shell

---

## 🚀 快速部署

### 3 步完成部署

```bash
# 1. 运行交互式配置
cd /root/.openclaw/skills/multi-agent-teams
./scripts/deploy.sh

# 2. 合并生成的配置
# (脚本会提示你如何操作)

# 3. 重启 Gateway
openclaw gateway restart
```

---

## 🎯 配置模式

### 模式对比

| 模式 | 适合场景 | 耗时 |
|------|---------|------|
| 预设模板 | 标准需求 | 1 分钟 |
| 自定义 | 特殊需求 | 5 分钟 |
| 混合 | 部分标准 + 部分特殊 | 3 分钟 |

---

## 📖 使用示例

### 示例 1：快速部署标准团队

```bash
./scripts/deploy.sh --preset
```

**结果：** 4 个团队 18 个成员

```
code (CTO) → frontend, backend, test, product, algorithm, audit
stock (CIO) → analysis, risk, portfolio, research
social (CMO) → content, scheduling, engagement, analytics
flow (COO) → workflow, cron, integration, monitor
```

---

### 示例 2：创建客服团队

```bash
./scripts/deploy.sh

# 选择：2) 自定义团队
# 输入：
要创建几个团队？[1-10]: 1

配置第 1 个团队
团队 ID (英文，如 code/stock): support
团队名称 (中文，如 代码开发团队): 客户服务团队
团队领导角色 (如 CTO/CIO): 客服总监
团队成员 (逗号分隔): pre_sale,after_sale,technical,complaint
```

**结果：** 1 个团队 4 个成员

```
support (客服总监) → pre_sale, after_sale, technical, complaint
```

---

### 示例 3：创建研究团队

```bash
./scripts/deploy.sh

# 选择：2) 自定义团队
# 输入：

要创建几个团队？[1-10]: 1

配置第 1 个团队
团队 ID: research
团队名称：市场研究团队
团队领导角色：研究主管
团队成员：industry,competitor,data,trend
```

**结果：**

```
research (研究主管) → industry, competitor, data, trend
```

---

### 示例 4：混合部署

```bash
./scripts/deploy.sh

# 选择：3) 混合模式

# 选择预设团队：1 3 (code 和 social)
# 是否添加自定义团队？y

# 自定义：
团队 ID: research
团队名称：市场研究团队
团队领导：研究主管
成员：industry,competitor,data
```

**结果：** 3 个团队

```
code (CTO) → 6 个成员 (预设)
social (CMO) → 4 个成员 (预设)
research (研究主管) → 4 个成员 (自定义)
```

---

## 📁 部署内容

### 目录结构

```
/root/.openclaw/agents/teams/
├── {team1}/
│   ├── workspace/        # 团队领导工作区
│   ├── agent/            # 认证配置
│   ├── sessions/         # 会话历史
│   └── {member1}/        # 成员 1
│       ├── workspace/
│       ├── agent/
│       └── sessions/
└── {team2}/
    └── ...
```

### 配置文件

- `openclaw.json` — agents.list 配置片段
- `auth-profiles.json` — 认证配置（自动复制）
- `models.json` — 模型配置（自动复制）

### 人格文件模板

部署后需要为每个 Agent 创建：
- `SOUL.md` — 人格定义
- `AGENTS.md` — 行为规范

模板位置：`templates/` 目录

---

## 🔧 配置说明

### 团队 ID 命名规则

- 使用英文小写
- 可以包含连字符 `-`
- 示例：`code`, `stock`, `customer-support`

### 团队成员命名规则

- 使用英文小写
- 多个单词用下划线 `_` 或连字符 `-`
- 示例：`frontend`, `pre_sale`, `data-analysis`

### 模型推荐

| 团队类型 | 推荐模型 |
|---------|---------|
| 代码开发 | qwen3-coder-plus |
| 投资分析 | qwen3-max-2026-01-23 |
| 内容运营 | kimi-k2.5 |
| 客服支持 | qwen3.5-plus |
| 研究分析 | qwen3.5-plus |

---

## 🧪 验证

### 验证脚本

```bash
./scripts/verify.sh
```

### 手动验证

```bash
# 列出所有 Agent
openclaw agents list

# 查看绑定规则
openclaw agents list --bindings

# 检查 Gateway 状态
openclaw gateway status
```

---

## 📚 模板使用

### SOUL.md 模板

```bash
cat templates/SOUL.md.tmpl
```

### AGENTS.md 模板

```bash
cat templates/AGENTS.md.tmpl
```

---

## ⚠️ 注意事项

1. **备份** — 部署前自动备份配置
2. **单一入口** — 所有外部请求通过 main-agent
3. **不要越级指挥** — BOSS → main → 团队领导 → 成员
4. **重启生效** — 配置后需要 `openclaw gateway restart`

---

## 🐛 常见问题

### Q: 如何添加新成员到现有团队？

A: 编辑 `openclaw.json`，在对应团队领导的 `subagents.allowAgents` 中添加成员 ID，然后创建成员的目录和配置文件。

### Q: 如何删除团队？

A: 从 `openclaw.json` 的 `agents.list` 中移除相关 Agent 配置，然后删除对应目录。

### Q: sessions_spawn 调用失败？

A: 检查：
1. `subagents.allowAgents` 是否包含目标成员
2. 成员目录和配置文件是否存在
3. Gateway 是否已重启

---

## 📞 支持

- 技术文档：`/root/.openclaw/docs/multi-agent-team-architecture.md`
- 验证脚本：`./scripts/verify.sh`
- 模板文件：`templates/` 目录

---

**版本：** v2.0  
**最后更新：** 2026-03-16  
**作者：** CXLight
