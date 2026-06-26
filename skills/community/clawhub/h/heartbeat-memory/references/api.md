# heartbeat-memory API 参考

本文档提供 heartbeat-memory Skill 的字段详解和数据结构说明。

---

## 📋 配置文件结构

### heartbeat-memory-config.json

```json
{
  "memorySave": {
    "enabled": "boolean",
    "batchSize": "number",
    "largeTaskThreshold": "number",
    "continuousBatching": "boolean",
    "timeoutSeconds": "number",
    "maxRetries": "number",
    "processSessionsAfter": "string (ISO 日期)",
    "maxSessionsPerRun": "number",
    "scanFileSystem": "boolean",
    "scanFileSystemDays": "number",
    "refineSchedule": {
      "type": "string",
      "dayOfWeek": "string",
      "time": "string",
      "days": "number"
    }
  },
  "notifyTarget": "string"
}
```

---

## 🔍 字段详解

### memorySave 配置

#### enabled

- **类型：** `boolean`
- **默认值：** `true`
- **说明：** 是否启用自动记忆保存
- **示例：**
  ```json
  {
    "memorySave": {
      "enabled": true
    }
  }
  ```

---

#### batchSize

- **类型：** `number`
- **默认值：** `5`
- **范围：** `1-10`
- **说明：** 每批处理的 sessions 数量
- **建议：**
  - 少量 sessions (<20)：`5`
  - 大量 sessions (>50)：`3-5`
- **示例：**
  ```json
  {
    "memorySave": {
      "batchSize": 5
    }
  }
  ```

---

#### timeoutSeconds

- **类型：** `number`
- **默认值：** `1000`
- **范围：** `300-3600`（5 分钟 -60 分钟）
- **说明：** LLM 提炼的超时时间（秒）
- **建议：**
  - 少量 sessions：<10 个 → `300-600`
  - 中量 sessions：10-30 个 → `600-1000`
  - 大量 sessions：>30 个 → `1000-1500`
- **示例：**
  ```json
  {
    "memorySave": {
      "timeoutSeconds": 1000
    }
  }
  ```

---

#### maxSessionsPerRun

- **类型：** `number`
- **默认值：** `50`
- **范围：** `10-200`
- **说明：** 单次执行最多处理的 sessions 数量
- **建议：**
  - 日常使用：`50`
  - 首次运行：`20`
  - 大量 sessions：`30`
- **示例：**
  ```json
  {
    "memorySave": {
      "maxSessionsPerRun": 50
    }
  }
  ```

---

#### processSessionsAfter

- **类型：** `string` (ISO 8601 日期)
- **默认值：** `null`（自动检测）
- **说明：** 只处理此日期后的 sessions
- **格式：** `"YYYY-MM-DDTHH:mm:ssZ"`
- **示例：**
  ```json
  {
    "memorySave": {
      "processSessionsAfter": "2026-03-01T00:00:00Z"
    }
  }
  ```

---

#### scanFileSystem

- **类型：** `boolean`
- **默认值：** `true`
- **说明：** 是否扫描文件系统获取已删除的 sessions
- **示例：**
  ```json
  {
    "memorySave": {
      "scanFileSystem": true
    }
  }
  ```

---

#### scanFileSystemDays

- **类型：** `number`
- **默认值：** `30`
- **范围：** `0-365`（0=不限制）
- **说明：** 只扫描最近 N 天的文件
- **示例：**
  ```json
  {
    "memorySave": {
      "scanFileSystemDays": 30
    }
  }
  ```

---

### refineSchedule 配置

#### type

- **类型：** `string`
- **默认值：** `"weekly"`
- **可选值：** `"weekly"`, `"interval"`
- **说明：** 提炼频率类型
  - `weekly`：每周固定时间
  - `interval`：每隔 N 天
- **示例：**
  ```json
  {
    "refineSchedule": {
      "type": "weekly"
    }
  }
  ```

---

#### dayOfWeek

- **类型：** `string`
- **默认值：** `"sunday"`
- **可选值：** `"monday"`, `"tuesday"`, ..., `"sunday"`
- **说明：** 每周几进行提炼（仅 weekly 模式）
- **示例：**
  ```json
  {
    "refineSchedule": {
      "type": "weekly",
      "dayOfWeek": "sunday"
    }
  }
  ```

---

#### time

- **类型：** `string`
- **默认值：** `"20:00"`
- **格式：** `"HH:mm"`（24 小时制）
- **说明：** 每天几点进行提炼
- **示例：**
  ```json
  {
    "refineSchedule": {
      "time": "20:00"
    }
  }
  ```

---

#### days

- **类型：** `number`
- **默认值：** `7`
- **范围：** `1-30`
- **说明：** 每隔 N 天进行一次提炼（仅 interval 模式）
- **示例：**
  ```json
  {
    "refineSchedule": {
      "type": "interval",
      "days": 7
    }
  }
  ```

---

### 通知配置

#### notifyTarget

- **类型：** `string`
- **默认值：** `null`（自动获取当前用户）
- **格式：** `"channel:user_id"` 或 `"chat:chat_id"`
- **说明：** 通知发送目标
- **示例：**
  ```json
  {
    "notifyTarget": "feishu:ou_xxxxxxxxxxxxx"  // 替换为你的飞书用户 ID
  }
  ```

**渠道格式：**
- 飞书用户：`feishu:ou_xxxxx`（用户 open_id）
- 飞书群聊：`feishu:oc_xxxxx`（群聊 ID）
- 微信：`wechat:xxx`
- Telegram: `telegram:xxx`

---

## 📊 状态文件结构

### heartbeat-state.json

```json
{
  "processedSessions": ["session-id-1", "session-id-2"],
  "lastCheck": "2026-03-27T10:00:00.000Z",
  "lastRefine": "2026-03-27T10:00:00.000Z",
  "configHash": "abc123...",
  "memorySave": {
    "enabled": true
  }
}
```

---

### 状态字段详解

#### processedSessions

- **类型：** `Array<string>`
- **说明：** 已处理的 session IDs 列表
- **用途：** 避免重复处理

---

#### lastCheck

- **类型：** `string` (ISO 8601 日期)
- **说明：** 上次检查 sessions 的时间
- **格式：** `"YYYY-MM-DDTHH:mm:ss.sssZ"`

---

#### lastRefine

- **类型：** `string` (ISO 8601 日期)
- **说明：** 上次提炼 MEMORY.md 的时间
- **格式：** `"YYYY-MM-DDTHH:mm:ss.sssZ"`

---

#### configHash

- **类型：** `string`
- **说明：** 配置文件的 hash 值
- **用途：** 检测配置是否变更
- **算法：** MD5（fallback: Base64）

---

## 📝 Daily 笔记结构

### daily/YYYY-MM-DD.md

```markdown
# 2026-03-27 聊天记录

## 📊 当日总结

- 总会话数：6 个
- 活跃：6 | 删除：0 | 重置：0
- 主要话题：Heartbeat 配置，技能优化
- 关键决策：执行阶段 1 代码结构化

## 💬 会话详情

### 📋 会话标题

**标签：** ✅ | #Skill #优化
**时间：** 10:30
**摘要：** 讨论技能优化方案...

**关键决策/决策：**
- 决定执行代码结构化
- 创建 utils 模块

---
```

---

## 🔧 工具模块 API

### utils/config-sync.js

```javascript
const { syncHeartbeatMD, computeConfigHash } = require('./utils/config-sync');

// 同步 HEARTBEAT.md
syncHeartbeatMD(config, workspacePath);

// 计算配置 hash
const hash = computeConfigHash(config);
```

---

### utils/date-detector.js

```javascript
const { autoDetectProcessSessionsAfter } = require('./utils/date-detector');

// 自动检测日期
const date = autoDetectProcessSessionsAfter(workspacePath, sessions);
```

---

### utils/session-filters.js

```javascript
const { filterSessions, limitSessions } = require('./utils/session-filters');

// 过滤 sessions
const { validSessions, newSessions, skippedCount } = filterSessions(sessions, processedIds, config);

// 限制处理数量
const { limitedSessions, remainingCount } = limitSessions(newSessions, maxSessions);
```

---

## 📖 相关文档

- [配置详解](config.md) - 完整配置说明和示例
- [故障排查](troubleshooting.md) - 常见问题和解决方案
- [SKILL.md](../SKILL.md) - Skill 使用指南
