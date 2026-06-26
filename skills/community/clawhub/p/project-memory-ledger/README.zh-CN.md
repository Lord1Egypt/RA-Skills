# Project Memory Ledger（OpenClaw Skill）

面向 AI/Agent 的工程项目总账：长效记忆 + 证据链（不变量/决策/变更）+ 回滚 + 可追溯。

**关键词：** 项目总账、工程总账、变更记录、决策记录、不变量、可追溯、回滚、证据链、长效记忆、LLM/Agent 记忆、OpenClaw、Google Drive、Markdown

## 它做什么

### 1）本地总账（永远写本地 Markdown）
总账一律写入本地 Markdown 文件：
- `<workspace>/ledgers/INVARIANTS.md`
- `<workspace>/ledgers/DECISIONS.md`
- `<workspace>/ledgers/CHANGES.md`
- `<workspace>/ledgers/PROJECTS.md`
- `<workspace>/ledgers/PRD_PATCHES.md`

### 2）立项脚手架（文档存储位置由 backend 决定）
`backend` 仅决定“项目文档资产”存放在哪里：
- `backend=local`：本地项目目录 + Markdown 文档
- `backend=drive`：Drive 项目目录 + GDoc/GSheet 文档（需要 `gws` 认证）

> 为避免双份文档带来一致性问题，本 skill **不做文档双写**；总账仍以本地为权威。

---

## 快速开始

### 0）选择 workspace
“workspace”就是你的 OpenClaw 工作目录（不一定叫 `workspace-nero`）。

### 1）创建配置文件
推荐路径：
- `<workspace>/config/project_memory_ledger.json`

最小配置（本地文档）：
```json
{
  "language": "zh",
  "backend": "local",
  "default_project": "project-memory-ledger",
  "local_dir": "./ledgers",
  "projects_root_dir": "./projects",
  "projects_root_folder_id": ""
}
```

Drive 文档配置：
```json
{
  "language": "zh",
  "backend": "drive",
  "default_project": "project-memory-ledger",
  "local_dir": "./ledgers",
  "projects_root_dir": "./projects",
  "projects_root_folder_id": "<用于创建项目目录的 Drive folder id>"
}
```

模板：
- `references/default_config.json`

### 2）初始化
```bash
python3 skills/project-memory-ledger/scripts/ledger.py init --config <workspace>/config/project_memory_ledger.json
```

### 3）写入总账条目
```bash
python3 skills/project-memory-ledger/scripts/ledger.py append \
  --config <workspace>/config/project_memory_ledger.json \
  --doc changes \
  --project "Keyword Engine" \
  --text "- **Interfaces**: hunter-system ↔ keyword-engine\n- **Change**: ...\n- **Why**: ...\n- **Evidence**: ...\n- **Rollback**: ...\n"
```

### 4）立项登记（自动生成目录结构与文档）
```bash
python3 skills/project-memory-ledger/scripts/ledger.py register-project \
  --config <workspace>/config/project_memory_ledger.json \
  --name "My New Project" \
  --purpose "为什么要做 + 验收标准" \
  --interfaces "hunter-system ↔ keyword-engine" \
  --notes "可选"
```

- `backend=local` → 创建 `<workspace>/projects/My New Project/...` + Markdown 文档
- `backend=drive` → 创建 Drive 目录 + GDoc/GSheet 文档

### 5）PRD 自动更新（propose-only）
```bash
python3 skills/project-memory-ledger/scripts/ledger.py update-prd \
  --config <workspace>/config/project_memory_ledger.json \
  --project "Keyword Engine" \
  --mode propose
```

---

## 约定

### Project 标记
Project 大小写不敏感，写入前会归一化成 slug。

推荐：
- `hunter-system`
- `keyword-engine`
- `common`（跨项目通用规则/方法论，但不进 AGENTS/MEMORY）

禁用 `shared`。跨项目勾稽必须显式写：
- `Interfaces: A ↔ B`

### 默认 Project
如果不传 `--project`，脚本会注入：
- `Project: project-memory-ledger`

---

## Drive backend options（说明）
Drive 模式是可插拔 backend：
- Option 1（v1 已实现）：`gws` CLI（安装并完成认证）
- Option 2：Google API / service account（适合服务器/CI）
- Option 3：第三方 Drive 工具

Drive 不可用时，使用 `backend=local`。
