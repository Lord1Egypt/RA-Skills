---
name: goto-codedev-manager
version: 1.0.0
description: 多 IDE / 多 AI 编程 Agent 统一调度 Skill，连接 Codex/Claude Code/QoerCN(Lingma 兼容)/Trae/VS Code/Cursor/Qoder 完成代码开发、Git Diff 分析、EF Core 实体识别、Migration 生成、数据库变更交接单产出、测试构建与开发报告生成
author: GotoPlan Team
license: MIT

trigger_keywords:
  - 代码开发
  - 开发任务
  - 写代码
  - Codex
  - Claude Code
  - Cursor
  - 通义灵码
  - Lingma
  - QoerCN
  - Qoer
  - Trae
  - Qoder
  - VS Code
  - Git Diff
  - 代码变更
  - 实体识别
  - EF Core
  - Migration
  - 数据库变更
  - 建表草案
  - 开发同步
  - 跑测试
  - 开发报告

capabilities:
  - list_adapters              # 列出可用的编程 Agent/IDE 适配器
  - open_workspace             # 打开工作区
  - read_project               # 读取项目结构、识别技术栈
  - detect_stack               # 返回语言/框架/迁移工具
  - read_project_context       # 当前分支、改动文件、技术栈
  - get_task_progress          # 读取所选 Agent 的任务状态
  - analyze_git_diff           # git diff → 结构化变更（Agent 无关）
  - detect_entities            # 解析新增/修改的 EF Core 实体字段
  - detect_database_changes    # 判断是否需要数据库结构变更
  - run_tests                  # dotnet test
  - run_build                  # dotnet build
  - generate_schema_contract   # 生成 .db-contract/ 交接单
  - generate_report            # 生成中文开发同步报告
  - assign_coding_task         # 经所选适配器执行开发任务（需确认）
  - generate_migration         # dotnet ef migrations add（需确认）
  - apply_migration_local      # 仅对本地/测试库 dotnet ef database update（需确认）
  - git_commit                 # 生成提交说明并提交（需确认）

supported_agents:
  - codex                # Codex CLI（priority 1）
  - claude_code          # Claude Code CLI（priority 2）
  - qoer                 # QoerCN CLI（priority 3，Lingma 升级后正式入口）
  - lingma               # Lingma 兼容入口，实际走 Qoer CLI（priority 4）
  - trae                 # Trae CLI（priority 5）
  - vscode               # VS Code CLI（priority 6）
  - cursor               # Cursor CLI（priority 7）
  - qoder                # Qoder CLI（priority 8）
  - generic              # 通用 CLI / 工作区兜底

supported_stacks:
  - dotnet               # .NET / EF Core（MVP）
  # node / python / java 预留扩展位

entry_point: core/dispatcher.py
config_dir: config/

# OpenClaw 在 /skill install 时自动安装以下依赖
dependencies:
  python: ">=3.11"
  packages:
    - pyyaml>=6.0.1
    - python-dotenv>=1.0.0
    - pydantic>=2.5.0
    - jinja2>=3.1.2
    - structlog>=23.0.0

requires_confirmation:
  - assign_coding_task
  - generate_migration
  - apply_migration_local
  - git_commit

forbidden_actions:
  - apply_migration_prod       # 直连生产库执行 Migration
  - force_push                 # git push --force
  - drop_migration_history     # 删除/重置 Migration 历史
  - reset_hard                 # git reset --hard
  - delete_branch

example_prompts:
  - "用 Codex 在 GotoPlan 后台开发计划模板中心接口，并识别需要新增的数据库表"
  - "分析当前工作区的 Git Diff，看看有没有新增实体需要建表"
  - "为 gotoplan-backend 生成 Customer 表的数据库变更交接单"
  - "生成 AddPlanTemplates 这个 EF Core Migration 并在测试库验证"
  - "列出当前可用的编程工具适配器"
---

# goto-codedev-manager

GotoPlan / OpenClaw 生态中的**多 IDE / 多 AI 编程 Agent 统一调度能力层**——不绑死任何单一 IDE，
统一连接 Codex、Claude Code、QoerCN（Lingma 兼容）、Trae、VS Code、Cursor、Qoder 等编程工具，对本地项目完成开发任务分派、
Git Diff 分析、数据库变更识别、Migration 生成、测试构建，并产出「数据库变更交接单」(Schema Contract)，
交给 goto-devops-orchestrator → goto-cloudserver-manager 安全落库。**绝不直连生产数据库。**

## 两条正交适配轴

- **编程 Agent / IDE 轴**（`adapters/`）：谁来改代码、怎么下任务。Codex/Claude Code/QoerCN/Trae/VS Code/Cursor/Qoder 均通过 CLI 控制。
- **后端技术栈轴**（`stacks/`）：怎么识别实体、怎么生成 Migration。MVP = dotnet/efcore。

> 核心原则：**谁修改了代码不重要**，所有 Agent 都作用在同一项目工作区；codedev-manager 始终通过
> 「项目结构 + Git Diff + 测试/构建命令」理解开发进度，因此变更分析与建表识别是 Agent 无关的。

## 三级权限

- 只读（读代码、分析 Diff、生成 Migration 草案/交接单、跑测试）自动执行；
- 写操作（下开发任务、生成 Migration、测试库落库、提交）先给计划再确认；
- 危险操作（直连生产库、强推、重置历史）直接拒绝。

## 快速使用

```
# 列出可用编程工具
列出当前可用的编程工具适配器

# 让 Codex 开发并识别数据库变更
用 Codex 在 gotoplan-backend 开发"计划模板中心"接口，并生成数据库变更交接单

# 仅基于已写代码生成交接单
分析 gotoplan-backend 的改动，为新增实体生成建表交接单
```

更多配置（`config/workspaces.yaml`、`config/adapters.yaml`）和与 goto-devops-orchestrator /
goto-cloudserver-manager 的协同说明见 [README.md](README.md)。
