# Database Module

## 概述

数据库模块提供 Agent 配置的持久化存储和动态管理功能。

## 文件结构

```
db/
├── init.js              # 数据库初始化
├── agent-manager.js     # Agent 管理模块
├── config-sync.js       # 配置同步模块
├── session-validator.js # 会话验证模块
└── agents.db            # SQLite 数据库文件（自动生成）
```

## 功能模块

### 1. init.js - 数据库初始化

```javascript
const { initDatabase, initDefaultAgents } = require('./db/init');

// 初始化数据库
const db = await initDatabase();

// 初始化默认 Agent
await initDefaultAgents(db);
```

### 2. agent-manager.js - Agent 管理

```javascript
const { 
  getAllAgents, 
  getAgentByName, 
  updateAgentAddress,
  upsertAgent,
  toggleAgentStatus,
  logMessage,
  validateAgentAddress
} = require('./db/agent-manager');

// 获取所有 Agent
const agents = await getAllAgents();

// 获取特定 Agent
const agent = await getAgentByName('coder-agent');

// 更新 Agent 地址
await updateAgentAddress('coder-agent', 'qqbot:c2c:NEW_ID');

// 验证地址格式
const isValid = validateAgentAddress('qqbot:c2c:12345');
```

### 3. config-sync.js - 配置同步

```javascript
const { 
  loadFromDatabase, 
  saveToDatabase, 
  syncToCode,
  validateAndUpdate 
} = require('./db/config-sync');

// 从数据库加载配置
const config = await loadFromDatabase();

// 同步配置到代码文件
await syncToCode();

// 验证并更新配置
await validateAndUpdate();
```

### 4. session-validator.js - 会话验证

```javascript
const { 
  validateSessionConfig,
  getAvailableAgents,
  logSessionActivity,
  checkConfigUpdateNeeded
} = require('./db/session-validator');

// 会话开始时验证配置
const result = await validateSessionConfig();

// 获取可用 Agent
const available = await getAvailableAgents();

// 记录会话活动
await logSessionActivity('coder-agent', 'task-completed', { task: '实现登录功能' });
```

## 数据库表结构

### agents 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | Agent 名称（唯一） |
| role | TEXT | Agent 角色 |
| target | TEXT | QQ 地址 |
| description | TEXT | 描述 |
| capabilities | TEXT | 能力列表（JSON） |
| is_active | INTEGER | 是否激活 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### agent_configs 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| agent_name | TEXT | Agent 名称 |
| config_key | TEXT | 配置键 |
| config_value | TEXT | 配置值 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### message_logs 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| from_agent | TEXT | 发送方 |
| to_agent | TEXT | 接收方 |
| message | TEXT | 消息内容 |
| status | TEXT | 状态 |
| created_at | DATETIME | 创建时间 |

## 使用示例

### 初始化数据库

```bash
npm run db:init
```

### 查看 Agent 列表

```bash
npm run db:list
```

### 更新 Agent 地址

```bash
npm run db:update update coder-agent qqbot:c2c:NEW_ID
```

### 同步配置

```bash
npm run db:sync
```

### 验证配置

```bash
npm run db:validate
```

## 错误处理

所有数据库操作都包含错误处理：

```javascript
try {
  const result = await updateAgentAddress('coder-agent', 'qqbot:c2c:NEW_ID');
  console.log('✅ 更新成功:', result);
} catch (error) {
  console.error('❌ 更新失败:', error.message);
}
```

## 性能优化

- 使用 SQLite 提供快速的数据访问
- 支持批量操作
- 自动连接池管理
- 事务支持（未来扩展）

## 安全注意事项

1. 数据库文件存储在项目根目录
2. 建议将数据库文件加入 .gitignore
3. 生产环境建议使用外部数据库服务
4. 定期备份数据库文件

## 扩展功能

未来可能添加的功能：

- [ ] 支持 PostgreSQL/MySQL
- [ ] 配置加密存储
- [ ] 版本控制
- [ ] 审计日志
- [ ] 多租户支持