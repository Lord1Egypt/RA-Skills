# Heartbeat-Memory

🧠 Heartbeat 自动记忆保存 - 支持 **Heartbeat 自动触发** 和 **手动触发** 两种方式。自动检查新 sessions，生成 Daily 笔记，并定期提炼 MEMORY.md。

**特点：**
- ✅ 双模式支持 - Heartbeat 自动触发 + 主 Agent 中手动调用
- ✅ 文件系统扫描 - 支持备份已删除的 sessions
- ✅ 智能日期检测 - 自动检测最早 session 日期
- ✅ 配置自动同步 - HEARTBEAT.md 自动更新（仅配置变更时）
- ✅ 代码模块化 - 4 个 utils 模块职责清晰
- ✅ 渐进式披露 - references/ 文档按需加载
- ✅ 多工作区支持 - workspace-<NAME> 通配符
- ✅ 增量更新支持 - 检测活跃 session 的新内容并生成增量摘要
- ✅ 错误处理稳定性 - 模块加载失败时优雅退出
- ✅ Subagent 智能过滤 - 自动过滤自身产生的 session，避免重复处理

<!-- Badge Row 1: Core Info -->
[![ClawHub](https://img.shields.io/badge/ClawHub-heartbeat--memory-E75C46?logo=clawhub)](https://clawhub.ai/JustZeroX/heartbeat-memory)
[![GitHub](https://img.shields.io/badge/GitHub-JustZeroX-181717?logo=github)](https://github.com/JustZeroX/skill-heartbeat-memory)
[![Version](https://img.shields.io/badge/version-0.0.7-orange)](https://github.com/JustZeroX/skill-heartbeat-memory)

<!-- Badge Row 2: Platforms -->
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://openclaw.ai) 
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGgzOXYzOUgweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik00OSAwaDM5djM5SDQ5eiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDQ5aDM5djM5SDB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQ5IDQ5aDM5djM5SDQ5eiIvPjwvc3ZnPg==)](https://openclaw.ai) 
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://openclaw.ai)

<!-- Badge Row 3: License -->
[![License](https://img.shields.io/badge/License-MIT-BD2D2D)](LICENSE)

---

### 中文 | [English](#english-version)

---

## 目录

- [🚀 快速开始](#-快速开始)
- [✨ 核心功能](#-核心功能)
- [📦 项目结构](#-项目结构)
- [🔧 安装](#-安装)
- [📖 使用指南](#-使用指南)
- [⚙️ 配置说明](#️-配置说明)
- [📍 路径说明](#-路径说明)
- [🌍 多工作区支持](#-多工作区支持)
- [🔍 渐进式披露](#-渐进式披露)
- [📊 处理策略](#-处理策略)
- [❓ 常见问题](#-常见问题)
- [🔧 故障排查](#-故障排查)
- [📄 许可证](#-许可证)

---

## 🚀 快速开始

### 步骤 1：安装

**方式 1：Via ClawHub（推荐 ⭐⭐⭐）**

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

**⚠️ 重要：Heartbeat 默认是关闭的！**

```bash
# 查看当前配置
openclaw config get agents.defaults.heartbeat

# 如未启用，编辑 openclaw.json 添加：
# "agents": { "defaults": { "heartbeat": { "every": "30m" } } }

# 重启 Gateway
openclaw gateway restart
```

---

### 步骤 3：使用

**方式 1：自动触发（推荐 ⭐）**

安装并启用 Heartbeat 后，Skill 会每 30 分钟自动执行，无需手动干预。

**方式 2：手动触发**

在聊天中直接发送：
```
执行 heartbeat-memory
```

AI 会在主会话中直接执行，无需额外配置。

---

## ✨ 核心功能

- **🤖 自动检查新 sessions** - 每次 Heartbeat 触发时自动扫描
- **🔄 增量更新支持** - 检测活跃 session 的新内容并生成增量摘要
- **📝 Daily 笔记生成** - 自动生成格式化的每日聊天记录
- **🧠 MEMORY.md 提炼** - 定期提炼长期记忆（默认每周日 20:00）
- **📊 智能分批处理** - 根据任务量自动选择处理策略
- **📈 状态追踪** - 记录每个 session 的最后处理位置，避免重复处理
- **🔔 完成通知** - 处理后自动发送通知
- **🚀 无需配置 LLM** - 自动使用 OpenClaw 主配置的 LLM
- **📅 智能日期检测** - 自动检测最早 session 日期或 workspace 创建日期
- **⚙️ 配置自动同步** - HEARTBEAT.md 自动更新（仅配置变更时）
- **🧩 代码模块化** - 4 个 utils 模块，职责清晰
- **🌍 多工作区支持** - workspace-<NAME> 通配符
- **🔒 Subagent 智能过滤** - 自动过滤自身产生的 session，保留最近 200 个追踪记录
- **💪 错误处理稳定性** - 模块加载失败时优雅退出，防止程序崩溃

---

## 📦 项目结构

```
heartbeat-memory/
├── SKILL.md                       # Skill 核心文档
├── index.js                       # 主入口文件（包含 Subagent 过滤、状态追踪）
├── README.md                      # 项目文档
├── references/                    # 渐进式披露文档
│   ├── config.md                  # 配置详解
│   ├── troubleshooting.md         # 故障排查
│   └── api.md                     # API 参考
├── utils/                         # 工具模块
│   ├── config-sync.js             # HEARTBEAT.md 同步 + 配置 hash
│   ├── date-detector.js           # 日期自动检测
│   ├── session-filters.js         # Session 过滤逻辑
│   └── memory-refiner.js          # MEMORY.md 提炼 + 增量更新
├── assets/                        # 资源文件
│   ├── config.example.json        # 配置示例
│   └── daily-note-sample.md       # Daily 笔记示例
└── scripts/
    └── post-install.js            # 安装后脚本
```

---

## 🔧 安装

### 方式 1：Via ClawHub（推荐 ⭐）

若未安装 clawhub，请先安装：
```bash
npm install -g clawhub
```

已安装 clawhub 后，执行：
```bash
clawhub install heartbeat-memory

# 启用 Heartbeat（编辑 openclaw.json 添加 "agents.defaults.heartbeat": {"every": "30m"}）
openclaw gateway restart
```

**优点：**
- ✅ 一键安装，自动下载到全局目录
- ✅ 所有工作区共享
- ✅ 支持后续更新

### 方式 2：Manual / Git

```bash
git clone https://github.com/JustZeroX/skill-heartbeat-memory.git ~/.openclaw/skills/heartbeat-memory

# 启用 Heartbeat（编辑 openclaw.json 添加 "agents.defaults.heartbeat": {"every": "30m"}）
openclaw gateway restart
```

**适用场景：**
- ✅ 想要自定义代码
- ✅ 参与贡献开发
- ✅ ClawHub 不可用时

### 验证安装

```bash
# 检查文件是否存在
ls ~/.openclaw/skills/heartbeat-memory/SKILL.md

# 检查语法
node --check ~/.openclaw/skills/heartbeat-memory/index.js
node --check ~/.openclaw/skills/heartbeat-memory/utils/*.js
```

---

## 📖 使用指南

### 执行方式

**方式 1：Heartbeat 自动触发（推荐）**
```
Heartbeat 每 30 分钟触发 → 自动执行 heartbeat-memory
```

**方式 2：手动触发**
```
在聊天中发送："执行 heartbeat-memory"
```

### 查看结果

**运行时路径（相对路径，Skill 内部使用）：**
```bash
# 查看 Daily 笔记
cat ./memory/daily/YYYY-MM-DD.md

# 查看长期记忆
cat ./MEMORY.md

# 查看配置
cat ./memory/heartbeat-memory-config.json

# 查看状态
cat ./memory/heartbeat-state.json
```

**外部访问路径（绝对路径，从终端访问）：**
```bash
# 查看当前工作区
echo $OPENCLAW_WORKSPACE

# 查看 Daily 笔记
cat ~/.openclaw/workspace/memory/daily/YYYY-MM-DD.md

# 查看长期记忆
cat ~/.openclaw/workspace/MEMORY.md

# 查看配置
cat ~/.openclaw/workspace/memory/heartbeat-memory-config.json

# 查看状态
cat ~/.openclaw/workspace/memory/heartbeat-state.json
```

### 修改配置

```bash
vim ~/.openclaw/workspace/memory/heartbeat-memory-config.json
```

---

## 🔄 增量更新说明

**问题背景：**
- 之前的设计只检测**新 sessions**，忽略已有 session 的内容增长
- 用户在长期 session 中持续对话时，新内容不会被记录

**解决方案：**
- ✅ **活跃 session 检测** - 比较 `lastMessageCount` 判断是否有新消息
- ✅ **增量摘要生成** - 只处理新增的消息，不重复处理旧内容
- ✅ **状态追踪** - 记录每个 session 的 `lastMessageCount` 和 `lastMessageTime`
- ✅ **Daily 笔记更新** - 在已有笔记中追加/更新对应 session 的内容
- ✅ **智能消息处理** - 动态调整处理数量（8-20 条），优先用户消息（70%）
- ✅ **消息数动态获取** - 从 session 对象获取实际消息数，非硬编码

**状态文件结构：**
```json
{
  "processedSessions": {
    "session-xxx": {
      "lastMessageTime": "2026-03-27T10:00:00Z",
      "lastMessageCount": 50,  // 动态获取实际消息数，非硬编码
      "status": "active"
    }
  }
}
```

**技术细节：**
- **消息数获取**：优先从 `session.messageCount` 获取，降级到 `session.lastMessageIndex`（使用 ?? 操作符）
- **动态处理数量**：根据消息长度自动调整（短消息 20 条，长消息 8 条）
- **消息优先级**：70% 用户消息 + 30% AI 回复，确保关键信息不遗漏
- **Prompt 优化**：完整上下文 + 严格 JSON 格式 + 12 个推荐标签
- **Subagent 过滤**：自动过滤自身产生的 session，保留最近 200 个追踪记录，避免重复处理

**Daily 笔记格式：**
```markdown
### 📋 会话标题
**标签：** ✅ | #话题 | 🔄 已更新
**时间：** 10:00-11:00（14:00 更新）
**摘要：** ...（包含新内容的增量摘要）
**新增内容：** 14:00 后讨论了 XXX...
```

---

## ⚙️ 配置说明

### 核心配置

编辑 `<工作区>/memory/heartbeat-memory-config.json`：

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| `enabled` | 是否启用 | `true` | `true` |
| `batchSize` | 每批处理数 | `5` | `5-10` |
| `timeoutSeconds` | LLM 超时（秒） | `1000` | `600-1500` |
| `maxSessionsPerRun` | 单次最多处理数 | `50` | `20-50` |
| `processSessionsAfter` | 只处理此日期后 | **自动检测** | ISO 日期 |

**完整配置说明：** 详见 [references/config.md](references/config.md)

### 配置示例

**基础配置（默认）：**
```json
{
  "memorySave": {
    "enabled": true
  }
}
```

**首次运行（避免大量历史）：**
```json
{
  "memorySave": {
    "enabled": true,
    "processSessionsAfter": "2026-03-01T00:00:00Z",
    "maxSessionsPerRun": 20
  }
}
```

**大量 sessions（分批处理）：**
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

---

## 📍 路径说明

### OpenClaw 自动切换 CWD 机制

OpenClaw 在执行 Skill 时会自动切换当前工作目录（CWD）到当前工作区。这意味着：

**Skill 内部（运行时）：**
- ✅ 使用**相对路径** `./memory/`
- ✅ 自动指向当前工作区的 `memory/` 目录
- ✅ 无需关心工作区的绝对路径

**外部访问（终端/文件管理器）：**
- ✅ 使用**绝对路径** `~/.openclaw/workspace/memory/`
- ✅ 可以直接通过终端或文件管理器访问
- ✅ 多工作区时路径会变化

### 路径对照表

| 场景 | 路径类型 | 示例 |
|------|----------|------|
| **Skill 内部读取/写入** | 相对路径 | `./memory/heartbeat-memory-config.json` |
| **终端访问（单工作区）** | 绝对路径 | `~/.openclaw/workspace/memory/heartbeat-memory-config.json` |
| **终端访问（多工作区）** | 绝对路径 | `~/.openclaw/workspace/workspace-<NAME>/memory/...` |
| **配置文件引用** | 相对路径 | `[references/config.md](references/config.md)` |

### 为什么使用相对路径？

1. **多工作区兼容** - 当使用 `workspace-<NAME>` 时，绝对路径会变化
2. **代码可移植** - Skill 可以在任何工作区运行
3. **简化配置** - 无需硬编码绝对路径
4. **符合 OpenClaw 设计** - 利用自动 CWD 切换机制

### 多工作区路径示例

```bash
# 默认工作区
~/.openclaw/workspace/memory/

# 命名工作区
~/.openclaw/workspace/workspace-projectA/memory/
~/.openclaw/workspace/workspace-personal/memory/

# Skill 内部统一使用
./memory/  # 自动解析到当前工作区
```

---

## 🌍 多工作区支持

### 工作区通配符

当配置多个工作区时，使用 `workspace-<NAME>` 通配符：

```bash
# 创建工作区
openclaw workspace create workspace-projectA
openclaw workspace create workspace-personal

# 切换工作区
openclaw workspace switch workspace-projectA

# 查看当前工作区
echo $OPENCLAW_WORKSPACE
```

### 配置隔离

每个工作区有独立的配置：

```
~/.openclaw/workspace/
├── memory/
│   ├── heartbeat-memory-config.json    # 默认工作区配置
│   └── heartbeat-state.json
├── workspace-projectA/
│   └── memory/
│       ├── heartbeat-memory-config.json    # ProjectA 独立配置
│       └── heartbeat-state.json
└── workspace-personal/
    └── memory/
        ├── heartbeat-memory-config.json    # Personal 独立配置
        └── heartbeat-state.json
```

### 跨工作区使用

Skill 会自动检测当前工作区，并使用对应的配置和存储路径。无需额外配置。

---

## 🔍 渐进式披露

本 Skill 采用**渐进式披露**设计原则，优化上下文加载：

```
Metadata (描述) → SKILL.md (319 行) → references/ (按需加载)
```

**文档层次：**

| 层级 | 内容 | 加载时机 | 行数 |
|------|------|----------|------|
| **Metadata** | name + description | 始终在上下文 | ~100 词 |
| **SKILL.md** | 快速开始 + 核心功能 + 常见问题 | Skill 触发时 | 319 行 |
| **references/** | 配置详解 + 故障排查 + API 参考 | 按需加载 | 1,043 行 |

**优势：**
- ✅ 减少首次加载 token 59%（821 行 → 319 行）
- ✅ 保持完整文档可访问性
- ✅ 按需加载，不浪费上下文

**参考文档：**
- [references/config.md](references/config.md) - 完整配置说明
- [references/troubleshooting.md](references/troubleshooting.md) - 故障排查指南
- [references/api.md](references/api.md) - API 字段详解

---

## 📊 处理策略

| sessions 数量 | 策略 | 预计耗时 |
|--------------|------|----------|
| <5 个 | 直接处理 | <2 分钟 |
| 5-10 个 | 分批处理 | 2-5 分钟 |
| >10 个 | 启动 subagent | 5-10 分钟 |

**处理流程：**
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
    "dayOfWeek": "monday",
    "time": "09:00"
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

### Q: 相对路径和绝对路径有什么区别？

A: 
- **相对路径**（`./memory/`）：Skill 内部使用，自动解析到当前工作区
- **绝对路径**（`~/.openclaw/workspace/memory/`）：终端访问使用，多工作区时路径会变化

详见 [📍 路径说明](#-路径说明)

**更多问题：** 详见 [references/troubleshooting.md](references/troubleshooting.md)

---

## 🔧 故障排查

### Skill 不执行

```bash
# 1. 检查 Heartbeat 配置
openclaw config get agents.defaults.heartbeat
# 输出 {"every": "30m"} 表示已启用

# 2. 如未启用，编辑 openclaw.json 添加：
# "agents": { "defaults": { "heartbeat": { "every": "30m" } } }

# 3. 重启 Gateway
openclaw gateway restart

# 4. 重建配置文件
rm ~/.openclaw/workspace/memory/heartbeat-memory-config.json
# 下次执行时会自动重建
```

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

### 路径相关问题

```bash
# 确认当前工作区
echo $OPENCLAW_WORKSPACE

# 检查 memory 目录是否存在
ls -la ~/.openclaw/workspace/memory/

# 多工作区检查
ls -la ~/.openclaw/workspace/workspace-*/memory/
```

**完整故障排查：** 详见 [references/troubleshooting.md](references/troubleshooting.md)

---

## 🌍 跨平台支持

- ✅ **macOS** - 完全支持
- ✅ **Linux** - 完全支持
- ✅ **Windows** - 完全支持（PowerShell/CMD）

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## English Version

### 🚀 Quick Start

**Step 1: Install**
```bash
npm install -g clawhub
clawhub install heartbeat-memory

# Enable Heartbeat (edit openclaw.json add "agents.defaults.heartbeat": {"every": "30m"})
openclaw gateway restart
```

**Step 2: Use**
- Auto: Heartbeat triggers every 30 minutes
- Manual: Send "执行 heartbeat-memory" in chat

### ✨ Core Features

- 🤖 Auto session scanning
- 🔄 Incremental updates - Detects new content in active sessions
- 🧠 Smart message processing - Dynamic batch size (8-20), 70% user messages priority
- 📝 Daily note generation
- 🧠 MEMORY.md refinement
- 📊 Smart batching
- 🔔 Completion notifications
- 📅 Auto date detection
- ⚙️ Config auto-sync
- 🌍 Multi-workspace support with workspace-<NAME> wildcard
- 🔒 Subagent smart filtering - Auto-filters own subagent sessions, keeps last 200 tracking records
- 💪 Error handling stability - Graceful exit on module load failure, prevents crashes

### 📦 Project Structure

```
heartbeat-memory/
├── SKILL.md
├── index.js                       # Main entry with Subagent filtering, state tracking
├── references/
│   ├── config.md
│   ├── troubleshooting.md
│   └── api.md
├── utils/
│   ├── config-sync.js             # HEARTBEAT.md sync + config hash
│   ├── date-detector.js           # Auto date detection
│   ├── session-filters.js         # Session filtering logic
│   └── memory-refiner.js          # MEMORY.md refinement + incremental updates
└── assets/
```

### 📍 Path Explanation

**OpenClaw Auto CWD Switching:**

OpenClaw automatically switches the current working directory (CWD) to the current workspace when executing skills. This means:

**Inside Skill (Runtime):**
- ✅ Use **relative paths** `./memory/`
- ✅ Automatically points to current workspace's `memory/` directory
- ✅ No need to worry about absolute workspace paths

**External Access (Terminal/File Manager):**
- ✅ Use **absolute paths** `~/.openclaw/workspace/memory/`
- ✅ Direct access via terminal or file manager
- ✅ Paths change with multi-workspace

**Path Comparison:**

| Scenario | Path Type | Example |
|----------|-----------|---------|
| **Skill internal read/write** | Relative | `./memory/heartbeat-memory-config.json` |
| **Terminal access (single workspace)** | Absolute | `~/.openclaw/workspace/memory/heartbeat-memory-config.json` |
| **Terminal access (multi-workspace)** | Absolute | `~/.openclaw/workspace/workspace-<NAME>/memory/...` |
| **Config file references** | Relative | `[references/config.md](references/config.md)` |

### 🌍 Multi-Workspace Support

**Workspace Wildcard:**

When configuring multiple workspaces, use `workspace-<NAME>` wildcard:

```bash
# Create workspaces
openclaw workspace create workspace-projectA
openclaw workspace create workspace-personal

# Switch workspace
openclaw workspace switch workspace-projectA

# Check current workspace
echo $OPENCLAW_WORKSPACE
```

**Configuration Isolation:**

Each workspace has independent configuration:

```
~/.openclaw/workspace/
├── memory/
│   ├── heartbeat-memory-config.json    # Default workspace config
│   └── heartbeat-state.json
├── workspace-projectA/
│   └── memory/
│       ├── heartbeat-memory-config.json    # ProjectA independent config
│       └── heartbeat-state.json
└── workspace-personal/
    └── memory/
        ├── heartbeat-memory-config.json    # Personal independent config
        └── heartbeat-state.json
```

### ⚙️ Configuration

**Basic:**
```json
{
  "memorySave": {
    "enabled": true
  }
}
```

**First Run:**
```json
{
  "memorySave": {
    "processSessionsAfter": "2026-03-01T00:00:00Z",
    "maxSessionsPerRun": 20
  }
}
```

**Large sessions (batch processing):**
```json
{
  "memorySave": {
    "maxSessionsPerRun": 30,
    "timeoutSeconds": 1500,
    "batchSize": 5
  }
}
```

### 🔍 Progressive Disclosure

This skill uses **progressive disclosure** design:
- SKILL.md: 319 lines (core content)
- references/: 1,043 lines (detailed docs, loaded on demand)
- Reduces initial token load by 59%

### ❓ FAQ

**Q: How to manually trigger?**
A: Send in chat: "执行 heartbeat-memory"

**Q: Why can't I use require()?**
A: `run()` requires tool injection, only available in Heartbeat or main Agent context.

**Q: What's the difference between relative and absolute paths?**
A: 
- **Relative paths** (`./memory/`): Used inside skill, automatically resolves to current workspace
- **Absolute paths** (`~/.openclaw/workspace/memory/`): Used for terminal access, changes with multi-workspace

See [📍 Path Explanation](#-path-explanation)

**More:** See [references/troubleshooting.md](references/troubleshooting.md)

---

_最后更新：2026-03-27_
