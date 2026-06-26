# Scripts - 统一脚本使用说明

## 📋 概述

本目录包含所有管理脚本，用于数据库初始化、配置管理、Agent 更新、任务管理等操作。

## 🚀 快速开始

### 1. 初始化数据库

```bash
# 使用 npm 脚本（推荐）
npm run db:init

# 或使用自定义数据库路径
DB_PATH=/path/to/custom.db npm run db:init

# 或直接运行
node scripts/init-db.js
```

### 2. 查看配置状态

```bash
# 使用配置管理 CLI
npm run config status

# 或直接运行
node scripts/config-cli.js status
```

### 3. 列出所有 Agent

```bash
# 使用 npm 脚本
npm run db:list

# 或使用配置管理 CLI
npm run config list

# 或直接运行
node scripts/update-agent.js list
```

### 4. 更新 Agent 地址

```bash
# 使用配置管理 CLI（推荐）
npm run config update coder-agent qqbot:c2c:NEW_ID

# 或直接运行
node scripts/config-cli.js update coder-agent qqbot:c2c:NEW_ID
```

### 5. 管理任务

```bash
# 列出所有任务
npm run config task:list

# 查看任务详情
npm run config task:show task-001

# 分配任务给 Agent
npm run config task:assign task-001 coder-agent

# 完成任务
npm run config task:complete task-001 coder-agent
```

## 📝 脚本列表

### init-db.js - 数据库初始化

初始化 SQLite 数据库，包含 Agent 和任务管理表。

**用法:**
```bash
node scripts/init-db.js [db_path]
```

**功能:**
- 创建数据库文件（默认：`db/agents.db`）
- 创建表结构（agents, agent_configs, message_logs, tasks, task_assignments, task_history）
- 初始化默认 Agent

**输出示例:**
```
🚀 开始初始化数据库...

✅ 数据库已打开：/workspace/github-collab-git/db/agents.db
✅ agents 表已创建
✅ agent_configs 表已创建
✅ message_logs 表已创建
✅ tasks 表已创建
✅ task_assignments 表已创建
✅ task_history 表已创建
✅ 已初始化 4 个默认 Agent

✅ 数据库初始化完成！
```

### config-cli.js - 统一配置管理 CLI

完整的配置管理命令行工具，支持 Agent 和任务管理。

**用法:**
```bash
node scripts/config-cli.js <command> [options]
```

**Agent 命令:**
- `status` - 显示配置状态
- `list` - 列出所有 Agent
- `update <name> <address>` - 更新 Agent 地址
- `backup` - 备份数据库
- `restore <path>` - 恢复数据库
- `export <path>` - 导出配置
- `import <path>` - 导入配置
- `cleanup [days]` - 清理过期日志
- `summary` - 显示配置摘要

**任务命令:**
- `task:list` - 列出所有任务
- `task:show <id>` - 查看任务详情
- `task:assign <id> <agent>` - 分配任务给 Agent
- `task:complete <id> <agent>` - 完成任务
- `task:stats` - 显示任务统计

**示例:**
```bash
# Agent 管理
node scripts/config-cli.js status
node scripts/config-cli.js list
node scripts/config-cli.js update coder-agent qqbot:c2c:NEW_ID
node scripts/config-cli.js backup
node scripts/config-cli.js export /tmp/config.json
node scripts/config-cli.js summary

# 任务管理
node scripts/config-cli.js task:list
node scripts/config-cli.js task:show task-001
node scripts/config-cli.js task:assign task-001 coder-agent
node scripts/config-cli.js task:complete task-001 coder-agent
```

## 🔄 工作流程

### 初始化流程

```bash
# 1. 初始化数据库
npm run db:init

# 2. 查看默认 Agent
npm run config list

# 3. 更新 Agent 地址
npm run config update coder-agent qqbot:c2c:YOUR_ID

# 4. 验证配置
npm run config status

# 5. 同步配置到代码
npm run db:sync
```

### 任务管理流程

```bash
# 1. 创建任务（通过代码或 API）
# 2. 查看任务列表
npm run config task:list

# 3. 分配任务给 Agent
npm run config task:assign task-001 coder-agent

# 4. 查看任务详情
npm run config task:show task-001

# 5. 完成任务
npm run config task:complete task-001 coder-agent

# 6. 查看任务统计
npm run config task:stats
```

### 配置迁移流程

```bash
# 1. 导出配置（包含 Agent 和任务）
npm run config export /tmp/config-backup.json

# 2. 在新环境初始化数据库
npm run db:init

# 3. 导入配置
npm run config import /tmp/config-backup.json

# 4. 验证配置
npm run config status
```

### 日常维护流程

```bash
# 1. 查看配置状态
npm run config status

# 2. 备份数据库
npm run config backup

# 3. 更新 Agent 地址（如需要）
npm run config update agent-name new-address

# 4. 清理旧日志
npm run config cleanup 30

# 5. 查看配置摘要
npm run config summary
```

## 📊 数据库架构

### 统一数据库表结构

```
agents.db
├── agents              # Agent 配置
├── agent_configs       # Agent 详细配置
├── message_logs        # 消息日志
├── tasks              # 任务信息
├── task_assignments    # 任务分配历史
└── task_history        # 任务变更历史
```

### 表说明

**agents 表**
- 存储 Agent 基本信息（名称、角色、地址、描述、能力）

**agent_configs 表**
- 存储 Agent 额外配置（键值对形式）

**message_logs 表**
- 记录 Agent 间消息往来

**tasks 表**
- 存储任务信息（标题、描述、状态、优先级、分配情况）

**task_assignments 表**
- 记录任务分配历史（哪个 Agent 在何时被分配了什么任务）

**task_history 表**
- 记录任务变更历史（状态变化、分配变化等）

## ⚠️ 注意事项

1. **地址格式**: 必须使用 `qqbot:c2c:USER_ID` 或 `qqbot:group:GROUP_ID` 格式
2. **自定义数据库路径**: 通过环境变量 `DB_PATH` 指定
3. **自动同步**: 每次更新数据库后，配置会自动同步到代码文件
4. **会话校验**: 每次对话开始时会自动校验配置
5. **错误处理**: 配置错误时会有降级机制
6. **备份**: 定期备份数据库文件以防数据丢失
7. **任务 ID**: 任务 ID 必须唯一，建议使用 `task-UUID` 格式

## 🆘 故障排除

### 问题：数据库文件不存在

**解决:**
```bash
npm run db:init
```

### 问题：配置不同步

**解决:**
```bash
npm run db:sync
```

### 问题：地址格式错误

**解决:**
确保地址格式为 `qqbot:c2c:USER_ID` 或 `qqbot:group:GROUP_ID`

### 问题：Agent 未找到

**解决:**
```bash
npm run config list  # 查看已配置的 Agent
```

### 问题：任务未找到

**解决:**
```bash
npm run config task:list  # 查看已创建的任务
```

## 📞 技术支持

如有问题，请联系：
- 技术支持：OpenClaw Team
- 文档：https://openclaw.ai/docs
- 社区：https://community.openclaw.ai