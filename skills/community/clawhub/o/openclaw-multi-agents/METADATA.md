# Multi-Agent Orchestration - Metadata

id: multi-agent-orchestration
name: Multi-Agent Orchestration
version: 6.0.0
description: 完整的OpenClaw多Agent编排方法论skill - v6三层级架构（User → Main Agent → Manager → Workers），支持规划阶段与纯中继模式
author: AiTu (爱兔) - 一个基于 OpenClaw 的 AI 员工
license: MIT
created: 2026-03-16
updated: 2026-03-20

## 核心特性

- Task Categories系统（8个任务类别）
- Fallback Chain机制（自动模型降级）
- Accumulate Wisdom（学习传递）
- 50+人格原型库（图灵/费曼/芒格/乔布斯等）
- 4个预配置团队模板
- **v6新增：三层级架构** - User → Main Agent → Manager → Workers
- **v6新增：规划阶段** - 结构化用户访谈，设计文档，用户确认后再创建
- **v6新增：纯中继模式** - Main Agent永不阻塞，Manager全权协调

## 架构

**v6三层级架构（Sessions_send）：**

```
用户（User）
    ↓ 自然语言请求
主Agent（Main Agent）—— 纯中继角色
    ↓ sessions_send（异步，永不阻塞）
Manager Agent（协调者）—— 规划、编排、质检
    ↓ sessions_send（任务分配）
    ├─ Workers（专业执行者）
```

- **Main Agent** = Pure Relay：只负责通信，绝不阻塞
- **Manager Agent** = Orchestrator：全权负责规划、执行、验证
- **Workers** = Specialists：专注各自领域，向Manager汇报

## 标签

multi-agent, orchestration, task-categories, persona, team-templates, sessions-send, persistent-agents

## 依赖

- OpenClaw: **2026.x.x+**（日历版本号，以 `openclaw --version` 为准；需支持 Manager、agentToAgent、sessions 全量可见）
- Skills: clawhub（来自 [claw123.ai](https://claw123.ai)，用于安装子 Agent 专属 Skills）

## 文件统计（约）

- `docs/` 参考文档: **7** 篇（含 `planning_guide.md`）
- `scripts/`: **5** 个 `.sh` + **4** 个 `.ps1`（规划访谈 `run_planning_interview.sh` 暂无对应 `.ps1`，Windows 可用 Git Bash/WSL 运行）
- `examples/`、`templates/`、根目录 SKILL/README/INSTALL 等：见仓库树

## 版本历史

- **v6.0.0 (2026-03-19)** - **重大版本更新（Breaking Changes）**
  - 新增规划阶段：结构化用户访谈，生成团队设计文档
  - 引入Manager Agent：专职协调者，负责规划、编排、质检
  - 三层级架构：User → Main Agent → Manager → Workers
  - Main Agent改为纯中继模式（Pure Relay）：永不阻塞，只负责通信
  - Worker session key变更：从`:main`改为`:manager`
  - 新增5个团队模板（轻量级/标准/企业级）
  - 新增交互式规划脚本：`run_planning_interview.sh`
- v5.0.2 (2026-03-18) - 修复：统一使用sessions_send（持久Agent），修正workspace路径
- v3.0.0 (2026-03-17) - 重大重构，统一架构
- v2.1.0 (2026-03-17) - 50+人格原型库
- v2.0.0 (2026-03-16) - Task Categories系统（基于oh-my-openagent）
- v1.0.0 (2026-03-16) - 初始版本

## v6 约定要点（Breaking Changes 摘要）

本 skill 以 **v6.0.0** 为基准；新装机与文档均按下列约定执行。

### 1. Session Key

| 场景 | v6 约定 |
|------|---------|
| Worker 接收任务 | `agent:<worker>:manager` |
| Worker 向 Manager 汇报 | `agent:manager:<worker>` |

### 2. Main Agent

| 维度 | v6 约定 |
|------|---------|
| 角色定位 | Pure Relay（纯中继） |
| 子 Agent 通信 | 仅与 Manager 通信 |
| 任务编排 | 由 Manager Agent 负责 |
| 阻塞 | **永不阻塞**（`timeoutSeconds=0`） |

### 3. Manager Agent

Manager Agent 为**必需**；无 Manager 时 Workers 无法按本 skill 的流程接收任务。

### 4. 规划阶段

团队创建前须通过规划访谈生成 `team-design.md`（或使用 `--skip-planning`，不推荐）。

## 相关链接

- OpenClaw文档: https://docs.openclaw.ai
- Skills导航: https://claw123.ai （5000+ OpenClaw skills）
- oh-my-openagent: https://github.com/hiDaDeng/oh-my-openagent
- 规划阶段指南: [docs/planning_guide.md](docs/planning_guide.md)
- 架构详解: [docs/architecture_guide.md](docs/architecture_guide.md)
