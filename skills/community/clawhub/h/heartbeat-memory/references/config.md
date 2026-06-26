# heartbeat-memory 配置详解

本文档提供 heartbeat-memory Skill 的完整配置说明。

---

## 📋 配置文件位置

> 💡 所有路径均相对于**当前活动 Agent 的工作区根目录**（`./`）。OpenClaw 在唤醒 Agent 时会自动将当前目录切换到该 Agent 的专属工作区，因此 `./` 始终指向正确的工作区。

**默认工作区（单 Agent 用户）：​**

```
./memory/heartbeat-memory-config.json
```

**多工作区场景（如需从外部访问）：​**

```
~/.openclaw/workspace-<NAME>/memory/heartbeat-memory-config.json
```

（`<NAME>` 替换为工作区标识符，如 `dev`、`test` 等）

每个工作区有**独立**的配置文件和状态文件。

---

## 🔧 完整配置项

### 核心配置

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| `memorySave.enabled` | 是否启用自动保存 | `true` | `true` |
| `memorySave.batchSize` | 每批处理 sessions 数 | `5` | `5-10` |
| `memorySave.timeoutSeconds` | LLM 超时时间（秒） | `1000` | `600-1500` |
| `memorySave.maxSessionsPerRun` | 单次最多处理 sessions 数 | `50` | `20-50` |
| `memorySave.processSessionsAfter` | 只处理此日期后的 sessions | **自动检测** | ISO 日期格式 |

### 高级配置

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| `memorySave.largeTaskThreshold` | 启动 subagent 的阈值 | `10` | `10-20` |
| `memorySave.continuousBatching` | 是否连续分批处理 | `true` | `true` |
| `memorySave.maxRetries` | LLM 失败重试次数 | `3` | `2-3` |
| `memorySave.scanFileSystem` | 是否扫描文件系统 | `true` | `true` |
| `memorySave.scanFileSystemDays` | 扫描最近 N 天的文件 | `30` | `30-60` |

### 通知配置

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| `notifyTarget` | 通知目标（user:xxx 或 chat:xxx） | 自动获取 | 根据渠道 |

### MEMORY.md 提炼配置

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| `refineSchedule.type` | 提炼频率类型 | `weekly` | `weekly`/`interval` |
| `refineSchedule.dayOfWeek` | 每周几提炼 | `sunday` | `monday-sunday` |
| `refineSchedule.time` | 每日时间 | `20:00` | `HH:mm` 格式 |
| `refineSchedule.days` | 每几天提炼（interval 模式） | `7` | `1-30` |

---

## 📝 配置示例

### 示例 1：基础配置（推荐新手）

```json
{
  "memorySave": {
    "enabled": true,
    "batchSize": 5,
    "timeoutSeconds": 1000,
    "maxSessionsPerRun": 50
  }
}
```

**适用场景：​** 日常使用，sessions 量适中

---

### 示例 2：首次运行（避免处理大量历史）

```json
{
  "memorySave": {
    "enabled": true,
    "processSessionsAfter": "2026-03-01T00:00:00Z",
    "maxSessionsPerRun": 20,
    "timeoutSeconds": 600
  }
}
```

**说明：​**

- `processSessionsAfter`：只处理 2026-03-01 之后的 sessions
- `maxSessionsPerRun`：每次最多 20 个，避免超时
- **提示：​** 首次运行后，Skill 会自动检测并设置此日期

---

### 示例 3：大量 sessions（分批处理）

```json
{
  "memorySave": {
    "enabled": true,
    "batchSize": 5,
    "largeTaskThreshold": 15,
    "maxSessionsPerRun": 30,
    "timeoutSeconds": 1500,
    "continuousBatching": true
  }
}
```

**说明：​**

- `batchSize: 5`：每批 5 个，避免内存溢出
- `largeTaskThreshold: 15`：超过 15 个启动 subagent
- `timeoutSeconds: 1500`：25 分钟超时，适合大量 sessions

---

### 示例 4：指定通知渠道

**飞书用户：​**

```json
{
  "notifyTarget": "feishu:ou_xxxxxxxxxxxxx",
  "memorySave": {
    "enabled": true,
    "batchSize": 5,
    "timeoutSeconds": 1000
  }
}
```

**飞书群聊：​**

```json
{
  "notifyTarget": "feishu:oc_xxxxxxxxxxxxx",
  "memorySave": {
    "enabled": true
  }
}
```

**通知渠道格式：​**

- 飞书用户：`feishu:ou_xxxxx`（用户 open_id）
- 飞书群聊：`feishu:oc_xxxxx`（群聊 ID）
- 微信：`wechat:xxxxx`
- Telegram：`telegram:xxxxx`

---

### 示例 5：自定义提炼频率

```json
{
  "memorySave": {
    "enabled": true,
    "refineSchedule": {
      "type": "weekly",
      "dayOfWeek": "monday",
      "time": "09:00"
    }
  }
}
```

**说明：​** 每周一早上 09:00 提炼 MEMORY.md，适合工作日开始整理上周记忆

---

### 示例 6：完整配置（生产环境）

```json
{
  "memorySave": {
    "enabled": true,
    "batchSize": 5,
    "largeTaskThreshold": 10,
    "continuousBatching": true,
    "timeoutSeconds": 1000,
    "maxRetries": 3,
    "processSessionsAfter": "2026-03-06T00:00:00Z",
    "maxSessionsPerRun": 20,
    "scanFileSystem": true,
    "scanFileSystemDays": 30,
    "refineSchedule": {
      "type": "weekly",
      "dayOfWeek": "sunday",
      "time": "20:00"
    }
  },
  "notifyTarget": "feishu:ou_xxxxxxxxxxxxx"
}
```

---

## 🌍 多工作区支持

### 工作区检测逻辑

Skill 会自动检测当前所属的工作区：

1. **从 openclaw.json 读取**（最快）

```json
{
  "agents": {
    "list": [
      { "id": "main", "workspace": "./workspace" },
      { "id": "dev-agent", "workspace": "./workspace-dev" },
      { "id": "test-agent", "workspace": "./workspace-test" }
    ]
  }
}
```

2. **扫描 `./workspace*` 目录**
   - 自动发现 `workspace`、`workspace-dev`、`workspace-test` 等
   - 验证目录中有 `AGENTS.md` 或 `SOUL.md`

3. **从 session 路径推断**
   - 分析 session 的 `transcriptPath` 或 `sessionKey`
   - 提取 agent ID 并匹配工作区

### 多工作区记忆系统

**每个工作区独立运行，所有路径均相对于各自工作区的根目录（`./`）：​**

| 工作区 | 配置文件 | Daily 笔记 | MEMORY.md | 状态文件 |
|--------|----------|-----------|-----------|----------|
| `workspace`（默认） | `./memory/heartbeat-memory-config.json` | `./memory/daily/` | `./MEMORY.md` | `./memory/heartbeat-state.json` |
| `workspace-dev` | 同上（相对于该工作区的 `./`） | 同上 | 同上 | 同上 |
| `workspace-test` | 同上（相对于该工作区的 `./`） | 同上 | 同上 | 同上 |

> 💡 **说明：​** 由于 OpenClaw 在运行时会自动将 CWD 切换到当前 Agent 的工作区，因此所有工作区的配置文件路径写法完全相同，均为 `./memory/heartbeat-memory-config.json`，无需区分。

**优势：​**

- ✅ **数据隔离** - 每个工作区的记忆独立存储
- ✅ **配置独立** - 可以为不同工作区设置不同的提炼频率
- ✅ **自动检测** - 无需手动指定，Skill 自动识别
- ✅ **互不干扰** - 一个工作区的配置不影响其他工作区

### 配置示例（多工作区）

**主工作区（日常使用）：​**

```json
// 文件位置：./memory/heartbeat-memory-config.json（相对于 workspace）
{
  "memorySave": {
    "enabled": true,
    "refineSchedule": {
      "type": "weekly",
      "dayOfWeek": "sunday",
      "time": "20:00"
    }
  }
}
```

**创作工作区（高频提炼，每 3 天一次）：​**

```json
// 文件位置：./memory/heartbeat-memory-config.json（相对于 workspace-dev）
{
  "memorySave": {
    "enabled": true,
    "refineSchedule": {
      "type": "interval",
      "days": 3
    }
  }
}
```

**测试工作区（每周一提炼）：​**

```json
// 文件位置：./memory/heartbeat-memory-config.json（相对于 workspace-test）
{
  "memorySave": {
    "enabled": true,
    "refineSchedule": {
      "type": "weekly",
      "dayOfWeek": "monday",
      "time": "09:00"
    }
  }
}
```

---

## 🎯 配置调优建议

### timeoutSeconds 建议

| sessions 数量 | 建议值 | 说明 |
|--------------|--------|------|
| <10 个 | `300-600` | 5-10 分钟 |
| 10-30 个 | `600-1000` | 10-16 分钟 |
| 30-50 个 | `1000-1500` | 16-25 分钟 |
| >50 个 | `1500-3600` | 25-60 分钟 |

### maxSessionsPerRun 建议

| 场景 | 建议值 | 说明 |
|------|--------|------|
| 日常使用 | `50` | 默认值，适合大多数场景 |
| 首次运行 | `20` | 避免处理太多历史 |
| 大量 sessions | `30` | 分批处理，避免 OOM |
| 快速处理 | `10` | 快速完成，剩余下次处理 |

### processSessionsAfter 策略

| 策略 | 配置 | 说明 |
|------|------|------|
| **自动检测** | 不设置 | Skill 自动检测最早 session 日期 |
| **手动指定** | `"2026-03-01T00:00:00Z"` | 只处理指定日期后的 sessions |
| **处理所有** | `null` | 处理所有 sessions（不推荐） |

---

## 🔍 配置验证

### 检查配置是否生效

```bash
# 查看当前工作区配置（在工作区目录下执行）
cat ./memory/heartbeat-memory-config.json

# 查看状态文件（包含 configHash）
cat ./memory/heartbeat-state.json

# 从外部查看多工作区配置（将 <NAME> 替换为实际工作区名称）
ls -lh ~/.openclaw/workspace-<NAME>/memory/heartbeat-memory-config.json
# 示例：
# ls -lh ~/.openclaw/workspace-dev/memory/heartbeat-memory-config.json
# ls -lh ~/.openclaw/workspace-test/memory/heartbeat-memory-config.json
```

### 强制刷新配置

如果配置已变更但 HEARTBEAT.md 未更新：

```bash
# 删除 configHash（触发重新同步）
# 编辑 ./memory/heartbeat-state.json，删除 "configHash" 字段
```

---

## 📊 配置变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 2026.3.27 | 2026-03-27 | 新增多工作区支持说明 |
| 2026.3.27 | 2026-03-27 | 新增自动检测日期功能 |
| 2026.3.27 | 2026-03-27 | 新增 HEARTBEAT.md 自动同步 |
| 2026.3.20 | 2026-03-20 | 初始版本 |

---

## 📖 相关文档

- [故障排查](troubleshooting.md) - 常见问题和解决方案
- [API 参考](api.md) - 字段详解和数据结构
- [SKILL.md](../SKILL.md) - Skill 使用指南
```
