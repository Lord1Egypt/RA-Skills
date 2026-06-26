---
name: heartbeat-memory

description: 自动记忆保存 Skill。支持 Heartbeat 自动触发和主 Agent 中手动调用两种方式。自动检查新 sessions，生成 Daily 笔记，定期提炼 MEMORY.md，支持备份已删除的 sessions。

---

# heartbeat-memory

> 🌐 **ClawHub:​** [clawhub.ai/JustZeroX/heartbeat-memory](https://clawhub.ai/JustZeroX/heartbeat-memory)  

> 💻 **GitHub:​** [github.com/JustZeroX/skill-heartbeat-memory](https://github.com/JustZeroX/skill-heartbeat-memory.git)

Heartbeat 自动记忆保存 - 支持 **Heartbeat 自动触发** 和 **手动触发** 两种方式。自动检查新 sessions，使用 OpenClaw 主 LLM 生成/更新 daily 笔记，并定期提炼 MEMORY.md。

**特点：​**

- ✅ 双模式支持 - Heartbeat 自动触发 + 主 Agent 中手动调用

- ✅ 文件系统扫描 - 支持备份已删除的 sessions

- ✅ 智能日期检测 - 自动检测最早 session 日期

- ✅ 配置自动同步 - HEARTBEAT.md 自动更新

**推荐安装位置：​** `~/.openclaw/skills/heartbeat-memory/`（全局目录，所有工作区共享）

> 💡 **路径说明：​** Skill 安装路径是全局的。运行时所有文件操作都相对于当前工作区根目录（`./`）。OpenClaw 在唤醒 Agent 时会自动将当前目录切换到该 Agent 的专属工作区，因此 `./` 始终指向正确的工作区。

---

## 🚀 快速开始

### 步骤 1：安装

**方式 1：Via ClawHub（推荐 ⭐）​**

```bash
# 1. 安装 ClawHub（如未安装）
npm install -g clawhub

# 2. 安装 heartbeat-memory
clawhub install heartbeat-memory
```

**方式 2：Via GitHub**

```bash
git clone https://github.com/JustZeroX/skill-heartbeat-memory.git ~/.openclaw/skills/heartbeat-memory
```

---

### 步骤 2：配置 Heartbeat

**​⚠️ 重要：Heartbeat 默认是关闭的！​**

**方式 1：使用 CLI 命令（推荐）​**

```bash
# 查看当前配置
openclaw config get agents.defaults.heartbeat

# 如未启用，编辑 openclaw.json 添加："agents": { "defaults": { "heartbeat": { "every": "30m" } } }

# 重启 Gateway
openclaw gateway restart
```

**方式 2：手动编辑 openclaw.json**

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m"
      }
    }
  }
}
```

**验证是否生效：​**

```bash
openclaw config get agents.defaults.heartbeat
# 输出：{"every": "30m"} 表示已启用
```

---

### 步骤 3：使用

**方式 1：自动触发（推荐 ⭐）​**

安装并启用 Heartbeat 后，Skill 会每 30 分钟自动执行，无需手动干预。

**方式 2：手动触发**

在聊天中直接发送：

```
执行 heartbeat-memory
```

AI 会在主会话中直接执行，无需额外配置。

---

## ✨ 核心功能

### 1. 自动记忆保存

- **Heartbeat 触发**：每 30 分钟自动执行

- **智能扫描**：检测新的 sessions + 活跃 sessions（有新内容的已处理 session）

- **增量更新**：对活跃 session 生成增量摘要，避免重复处理
- **智能消息处理**：动态调整处理数量（8-20 条），优先用户消息（70%）

- **LLM 提炼**：生成结构化 Daily 笔记

- **状态追踪**：记录每个 session 的最后处理位置，避免重复处理

### 2. Daily 笔记生成

**输出位置：​** `./memory/daily/YYYY-MM-DD.md`

> 💡 **路径说明：​** 所有路径都是相对于当前工作区的根目录（`./`）。OpenClaw 运行时会自动切换 CWD 到当前 Agent 的工作区，因此无需手动指定工作区路径。

**内容包含：​**

- 当日总结（会话数、活跃度）

- 会话详情（标题、摘要、标签）

- 关键决策/发现

### 3. MEMORY.md 定期提炼

- **默认频率**：每周日 20:00

- **自动提炼**：从 Daily 笔记提取长期记忆

- **可配置**：支持自定义频率和时间

### 4. 自动初始化

首次运行时会自动：

1. ✅ 创建配置文件

2. ✅ 初始化状态文件

3. ✅ 创建必要目录

4. ✅ **自动检测** `processSessionsAfter` 日期

5. ✅ **自动同步** `HEARTBEAT.md` 配置状态

---

## 📝 HEARTBEAT.md 自动同步

**Skill 会自动维护 `HEARTBEAT.md` 中的"记忆自动保存"部分：​**

- ✅ **自动检测配置变更**（通过 hash 对比）

- ✅ **仅配置变更时更新**（避免重复写入）

- ✅ **动态路径展示**（自动适配多 workspace）

- ✅ **保留用户自定义内容**（天气检查等不受影响）

**示例：​**

```markdown
# HEARTBEAT.md - 心跳任务

## 🧠 记忆自动保存

<!-- 此部分由 heartbeat-memory skill 自动维护，请勿手动修改 -->

- [x] 启用 heartbeat-memory Skill

- [x] 工作区：workspace（示例值，实际显示当前工作区名称）

- [x] 配置：处理 2026-03-06 之后的 sessions

- [x] 配置：每次最多处理 20 个 sessions

- [x] 配置：超时时间 1000 秒

**执行方式：​** Heartbeat 触发时自动执行 heartbeat-memory Skill

**配置文件：​** `./memory/heartbeat-memory-config.json`

**输出位置：​**

- Daily 笔记：`./memory/daily/YYYY-MM-DD.md`

- 长期记忆：`./MEMORY.md`

- 状态文件：`./memory/heartbeat-state.json`
```

---

## ⚙️ 核心配置

### 单工作区模式

编辑 `./memory/heartbeat-memory-config.json`：

### 多工作区模式

**每个工作区有独立的配置文件：​**

> 💡 **重要说明：​** 由于 OpenClaw 在运行时会自动将当前工作目录（CWD）切换到对应 Agent 的工作区，因此**所有工作区的配置文件路径写法完全相同**，均为 `./memory/heartbeat-memory-config.json`。Skill 会自动识别当前所属工作区，无需手动指定。

| 工作区 | 配置文件路径（运行时） | 实际物理路径（从外部访问） |
|--------|----------------------|--------------------------|
| 主工作区（workspace） | `./memory/heartbeat-memory-config.json` | `~/.openclaw/workspace/memory/heartbeat-memory-config.json` |
| 开发工作区（workspace-dev） | `./memory/heartbeat-memory-config.json` | `~/.openclaw/workspace-dev/memory/heartbeat-memory-config.json` |
| 测试工作区（workspace-test） | `./memory/heartbeat-memory-config.json` | `~/.openclaw/workspace-test/memory/heartbeat-memory-config.json` |

**自动检测：​** Skill 会自动识别当前所属工作区，无需手动指定。

**详见：​** [references/config.md](references/config.md#多工作区支持)

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| `enabled` | 是否启用 | `true` | `true` |
| `batchSize` | 每批处理数 | `5` | `5-10` |
| `timeoutSeconds` | LLM 超时（秒） | `1000` | `600-1500` |
| `maxSessionsPerRun` | 单次最多处理数 | `50` | `20-50` |
| `processSessionsAfter` | 只处理此日期后 | **自动检测** | ISO 日期 |

**完整配置说明：​** 详见 [references/config.md](references/config.md)

---

## 📋 配置示例

### 基础配置（默认）

```json
{
  "memorySave": {
    "enabled": true
  }
}
```

### 首次运行（避免大量历史）

> 💡 **提示：​** 首次运行时，Skill 会**自动检测**最早的 session 日期或 workspace 创建日期，并自动保存到配置文件。

```json
{
  "memorySave": {
    "enabled": true,
    "processSessionsAfter": "2026-03-01T00:00:00Z",
    "maxSessionsPerRun": 20
  }
}
```

### 大量 sessions（分批处理）

```json
{
  "memorySave": {
    "enabled": true,
    "maxSessionsPerRun": 30,
    "timeoutSeconds": 1500,
    "batchSize": 5
  }
}
```

**更多示例：​** 详见 [references/config.md](references/config.md)

---

## 📊 处理策略

| sessions 数量 | 策略 | 预计耗时 |
|--------------|------|----------|
| <5 个 | 直接处理 | <2 分钟 |
| 5-10 个 | 分批处理 | 2-5 分钟 |
| >10 个 | 启动 subagent | 5-10 分钟 |

**处理流程：​**

```
Heartbeat 触发
    ↓
sessions_list 获取会话列表
    ↓
sessions_history 获取消息内容
    ↓
sessions_spawn 启动 subagent 进行 LLM 提炼
    ↓
写入 Daily 笔记
    ↓
检查是否需要提炼 MEMORY.md
    ↓
发送完成通知
```

---

## ❓ 常见问题

### Q: 如何手动触发？

A: 在聊天中发送："执行 heartbeat-memory"

### Q: 为什么不能用 require 调用？

A: `run()` 依赖工具注入（`sessions_list` 等），只有 Heartbeat 自动触发或主 Agent 会话中工具才可用。

### Q: 可以修改提炼频率吗？

A: 可以，编辑配置文件：

```json
{
  "refineSchedule": {
    "type": "weekly",
    "dayOfWeek": "sunday",
    "time": "20:00"
  }
}
```

### Q: 如何处理大量 sessions？

A: 自动分批处理，每次最多 50 个，剩余下次继续。也可手动限制：

```json
{
  "maxSessionsPerRun": 20
}
```

### Q: 通知未发送怎么办？

A: 检查 `notifyTarget` 配置，或删除该字段让 Skill 自动获取当前用户。

**更多问题：​** 详见 [references/troubleshooting.md](references/troubleshooting.md)

---

## 🔧 故障排查速查

### Skill 不执行

```bash
# 1. 检查 Heartbeat 配置
openclaw config get agents.defaults.heartbeat
# 输出 {"every": "30m"} 表示已启用

# 2. 如未启用，编辑 openclaw.json 添加：
# "agents": { "defaults": { "heartbeat": { "every": "30m" } } }

# 3. 重启 Gateway
openclaw gateway restart

# 4. 重建配置文件（相对于当前工作区）
rm ./memory/heartbeat-memory-config.json
```

> 💡 **路径说明：​** 故障排查命令中的路径都是相对于当前工作区（`./`）。在工作区目录下执行即可，无需指定完整路径。

### HEARTBEAT.md 未更新

```bash
# 删除 configHash（强制重新同步）
# 编辑 heartbeat-state.json，删除 "configHash" 字段
```

### 处理速度慢

```json
{
  "memorySave": {
    "maxSessionsPerRun": 20,
    "timeoutSeconds": 1500
  }
}
```

**完整故障排查：​** 详见 [references/troubleshooting.md](references/troubleshooting.md)

---

## 📖 参考文档

| 文档 | 说明 |
|------|------|
| [references/config.md](references/config.md) | 完整配置说明和示例 |
| [references/troubleshooting.md](references/troubleshooting.md) | 故障排查指南 |
| [references/api.md](references/api.md) | API 字段详解 |

---

## 🎯 最佳实践

### 首次运行

1. 不设置 `processSessionsAfter`（自动检测）
2. 设置 `maxSessionsPerRun: 20`
3. 观察执行日志

### 日常使用

1. 保持默认配置
2. 定期查看 Daily 笔记
3. 根据需要调整提炼频率

### 性能优化

- 大量 sessions：`maxSessionsPerRun: 30`, `timeoutSeconds: 1500`
- 频繁触发：禁用 OK 通知（在 openclaw.json 中配置）
- 内存优化：`batchSize: 3`, `maxSessionsPerRun: 10`

---

_最后更新：2026-03-27_