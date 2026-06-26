# GitHub Collaborator Agent - 配置说明

## 📋 配置概览

本项目使用统一的配置管理系统，支持环境变量、配置文件、数据库配置等多种配置方式。

## 🔧 环境变量配置

### .env 文件

```bash
# 数据库配置
DB_PATH=./src/db/github-collab.db
AGENTS_DB_PATH=./src/db/agents.db
CONFIG_DB_PATH=./src/db/config.db
TASKS_DB_PATH=./src/db/tasks.db

# 服务器配置
PORT=3000
HOST=localhost

# 日志配置
LOG_LEVEL=info
LOG_FILE=./logs/app.log

# Agent 配置
AGENT_HEARTBEAT_INTERVAL=30000
AGENT_TIMEOUT=60000

# 任务配置
TASK_AUTO_ASSIGN=true
TASK_PRIORITY_HIGH=1
TASK_PRIORITY_MEDIUM=2
TASK_PRIORITY_LOW=3

# 性能配置
CACHE_ENABLED=true
CACHE_TTL=3600
CACHE_MAX_SIZE=1000
```

### 配置加载顺序

1. **环境变量** (最高优先级)
2. **.env 文件**
3. **config/config.js**
4. **默认配置** (最低优先级)

## 🗂️ 配置文件

### config/config.js

```javascript
module.exports = {
  // 数据库配置
  database: {
    path: process.env.DB_PATH || './src/db/github-collab.db',
    agents: process.env.AGENTS_DB_PATH || './src/db/agents.db',
    config: process.env.CONFIG_DB_PATH || './src/db/config.db',
    tasks: process.env.TASKS_DB_PATH || './src/db/tasks.db'
  },
  
  // 服务器配置
  server: {
    port: parseInt(process.env.PORT) || 3000,
    host: process.env.HOST || 'localhost'
  },
  
  // 日志配置
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    file: process.env.LOG_FILE || './logs/app.log'
  },
  
  // Agent 配置
  agent: {
    heartbeatInterval: parseInt(process.env.AGENT_HEARTBEAT_INTERVAL) || 30000,
    timeout: parseInt(process.env.AGENT_TIMEOUT) || 60000
  },
  
  // 任务配置
  task: {
    autoAssign: process.env.TASK_AUTO_ASSIGN === 'true',
    priority: {
      high: parseInt(process.env.TASK_PRIORITY_HIGH) || 1,
      medium: parseInt(process.env.TASK_PRIORITY_MEDIUM) || 2,
      low: parseInt(process.env.TASK_PRIORITY_LOW) || 3
    }
  },
  
  // 性能配置
  performance: {
    cache: {
      enabled: process.env.CACHE_ENABLED === 'true',
      ttl: parseInt(process.env.CACHE_TTL) || 3600,
      maxSize: parseInt(process.env.CACHE_MAX_SIZE) || 1000
    }
  }
};
```

## 📊 数据库配置

### 数据库文件

| 数据库文件 | 用途 | 位置 |
|------------|------|------|
| `github-collab.db` | 主数据库 | `src/db/` |
| `agents.db` | Agent 数据库 | `src/db/` |
| `config.db` | 配置数据库 | `src/db/` |
| `tasks.db` | 任务数据库 | `src/db/` |

### 数据库表结构

#### users 表
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT DEFAULT 'user',
  status TEXT DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### tasks 表
```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  priority INTEGER DEFAULT 2,
  status TEXT DEFAULT 'pending',
  assignee_id INTEGER,
  project_id INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (assignee_id) REFERENCES users(id),
  FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

#### agents 表
```sql
CREATE TABLE agents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  status TEXT DEFAULT 'idle',
  current_task_id INTEGER,
  last_heartbeat DATETIME,
  ip_address TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (current_task_id) REFERENCES tasks(id)
);
```

#### projects 表
```sql
CREATE TABLE projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'active',
  progress INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 安全配置

### 密码加密

```javascript
const bcrypt = require('bcrypt');

// 加密密码
const hashedPassword = await bcrypt.hash(password, 10);

// 验证密码
const isValid = await bcrypt.compare(password, hashedPassword);
```

### 会话管理

```javascript
// 生成会话 ID
const sessionId = crypto.randomBytes(32).toString('hex');

// 设置会话过期时间
const sessionExpiry = Date.now() + 3600000; // 1 小时
```

## ⚡ 性能配置

### 缓存配置

```javascript
const cache = {
  enabled: true,
  ttl: 3600, // 1 小时
  maxSize: 1000, // 最大缓存项数
  evictionPolicy: 'LRU' // 最近最少使用
};
```

### 数据库优化

```javascript
// 启用 WAL 模式
db.exec('PRAGMA journal_mode = WAL');

// 启用同步
db.exec('PRAGMA synchronous = NORMAL');

// 设置缓存大小
db.exec('PRAGMA cache_size = -64000'); // 64MB
```

## 📝 日志配置

### 日志级别

- `error`: 错误日志
- `warn`: 警告日志
- `info`: 信息日志
- `debug`: 调试日志
- `trace`: 追踪日志

### 日志格式

```javascript
{
  timestamp: "2026-03-27T10:00:00.000Z",
  level: "info",
  message: "Task created successfully",
  data: {
    taskId: 1,
    title: "Test Task"
  }
}
```

## 🔄 配置同步

### 配置备份

```bash
node src/scripts/config-cli.js backup
```

### 配置恢复

```bash
node src/scripts/config-cli.js restore config_backup.json
```

### 配置同步

```bash
node src/scripts/sync-config.js
```

## 🚀 快速配置

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 编辑环境变量

```bash
# 编辑 .env 文件，设置必要的配置
vim .env
```

### 3. 初始化数据库

```bash
npm run db:init
```

### 4. 验证配置

```bash
node src/scripts/validate-config.js
```

## 📚 相关文档

- [README.md](README.md) - 项目说明
- [SKILL.md](SKILL.md) - Agent 技能说明
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构

---

**版本**: v2.0.0  
**更新时间**: 2026-03-27  
**作者**: OpenClaw Team  
**仓库**: https://github.com/openclaw/github-collab