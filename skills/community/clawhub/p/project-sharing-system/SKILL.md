---
name: project-sharing
slug: project-sharing-system
version: 1.0.0
description: 项目共享系统 — 多 Agent 项目状态协作与自动发现
author: openclaw
tags: [project-management, collaboration, multi-agent, automation]
---

# 📋 项目共享系统

多 Agent 项目状态共享与协作系统。让所有 Agent 实时了解当前项目状态，支持自动发现、状态同步和历史追溯。

## 安装

```bash
clawhub install project-sharing-system
```

## 使用

### 安装后自动配置
安装完成后，项目系统会自动：
- 创建 `projects_status.json` 和 `PROJECT_STATUS.md`
- 设置 `project` CLI 命令
- 配置自动备份

### CLI 命令

```bash
project list                    # 查看所有项目
project show <id>               # 查看项目详情
project add <id> --name "项目"  # 添加新项目
project update <id> --task "任务"  # 更新项目
project sync                    # 同步数据 + 备份
project snapshot                # 生成状态快照
project summary                 # 生成摘要报告
```

### Agent 自动发现

在会话启动时，Agent 可以读取 `projects_snapshot.md` 快速了解当前项目状态。

## 组件

| 文件 | 说明 |
|------|------|
| `projects_status.json` | 核心数据文件 |
| `PROJECT_STATUS.md` | Markdown 视图 |
| `scripts/project.js` | CLI 管理工具 |
| `scripts/project_snapshot.sh` | 快照生成器 |
| `scripts/auto_backup.sh` | 自动备份（保留30版本） |
| `assets/dashboard.html` | HTML 仪表板 |

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-23 | 初始版本：CLI + 快照 + 备份 + 仪表板 |
