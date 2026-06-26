# Good-Memory Changelog

## v2.0.1 (2026-03-28)

### 核心修复：自动重置检测失效问题

**问题**：v2.0.0 仅识别显式重置（session 被重命名为 `.reset.` 后缀），但系统自动会话轮换/重启时不会打 reset 标记，导致恢复机制不触发。

**修复内容**：
- ✅ 新增**隐式会话切换检测**：支持系统自动轮换会话的场景，无需 reset 标记也能触发恢复
- ✅ 双重检测逻辑：同时支持显式重置（.reset 后缀）和隐式切换（UUID 变化）
- ✅ 修复潜在的跨用户会话污染问题
- ✅ 恢复记录从30条提升到50条，保留更完整上下文

#### 技术细节
- `maintenance.sh detect` 新增隐式切换识别，当新旧 UUID 不同但无 reset 文件时也标记为重置
- `autorecover.py` 新增额外检查逻辑，确保会话切换时总能找到上一个会话
- 兼容所有重置场景：手动执行 /reset、系统自动重置、后台服务重启

---

## v2.0.0 (2026-03-28)

### 重大更新：去掉中间文件机制
同 v1.3.0 升级，完全移除所有中间文件，直接基于 tracker JSON + session JSONL 工作。

---

## v1.3.0 (2026-03-27)

### 重大架构调整：完全去掉中间文件

**核心变化**：detect 不再写任何中间文件，Agent 直接读 tracker JSON + session JSONL。

#### 主要变化

- **完全移除中间文件机制**：不再写 `.gm-context-*.txt`、`.gm-history-*.txt`、`.gm-ended-*.txt`
- **detect 只更新 tracker**：写入 `last_history.file` + `last_history.ended_at`，不产生任何文件
- **Agent 自己读 tracker JSON**：从 `agents.{agent}.{chat_id}.last_history` 获取旧 session 路径
- **Agent 直接读 session JSONL**：解析最后 20-30 条记录（含 tool 操作），还原完整对话场景
- **恢复消息格式不变**：`已自动恢复 3月27日 16:45 之后说的话 📜 如果想要回忆更早的请对我说`

#### 文件变更

- `maintenance.sh`：移除 `get-history` 命令；detect 移除所有写文件逻辑
- `AGENTS.md`：更新指令流程，agent 自行解析 tracker + JSONL
- `SKILL.md`：重写文档，v1.3.0

#### 设计优势

- **零额外文件**：session JSONL 是唯一的数据源，无缓存、无中间状态
- **完整历史**：直接读取 JSONL，包含所有 tool_calls/tool_results，比摘要更丰富
- **更可靠**：没有中间文件就没有同步问题，tracker 就是唯一的真相来源

---

## v1.2.0 (2026-03-27)

### 重大架构调整

**不再使用中间文件存储上下文**。改为直接读取 session JSONL 文件，获得完整的对话历史（包括 tool_calls 等操作记录）。

#### 主要变化

- **新增 `get-history` 命令**：从 `last_history.file` 直接读取 session JSONL，解析并格式化最后 30 条记录，写入 `.gm-history-{chat_id}.txt`
- **detect 不再写上下文文件**：仅更新 tracker + 写入 `.gm-ended-{chat_id}.txt`（时间戳）
- **恢复消息格式简化**：首条回复改为 `已自动恢复 3月27日 16:45 之后说的话 📜 如果想要回忆更早的请对我说`（只有时间，无详细摘要）
- **读取内容更丰富**：直接解析 session JSONL，包含 user/assistant 消息和 tool 操作，比纯文本更完整

#### 技术细节

- `detect` 输出 `last_history:` + `last_session_created:`
- `get-history` 读取 `last_history.file`，格式化后写入 `.gm-history-{chat_id}.txt` 和 `.gm-ended-{chat_id}.txt`
- Agent 启动时依次执行 detect → get-history → 读取两个生成的文件

#### 文件变更

- `maintenance.sh`：移除 `format_history_jsonl`；新增 `get-history` 命令；detect 移除写上下文文件逻辑
- `AGENTS.md`：更新启动指令流程
- `SKILL.md`：重写文档，移除"context 文件"描述，改为"历史记录文件"

---

## v1.1.3 (2026-03-27)

### Bug 修复
- **Agent 路由错误**：修复 install.sh 中 tracker 的 agent 名称获取逻辑。之前错误地使用 session 文件存储目录（都是 "main"），现在正确从 `sessions.json` 的 `deliveryContext.accountId` 字段获取实际路由目标 Agent

### 技术细节
- 从 `sessions.json` 的 `deliveryContext.accountId` 字段获取实际路由 Agent，而不是用 session 文件的存储目录名
- 确保 tracker 中每个 session 正确映射到对应的 Agent（tuwen/guwen/xiangmu/main）

---

## v1.1.0 (2026-03-27)

### 新增
- **UUID 前缀比对**：tracker 新增 `active_uuid` 字段，verify 时优先比对 UUID 前缀（UUID 全局唯一，更可靠）
- **verify 输出新增 `last_history` 字段**：当检测到重置时，直接输出最近一次被重置的 session 文件路径

### 比对逻辑（双重验证）
1. **UUID 前缀比对**（主要）— UUID 全局唯一，前缀改变 = 一定是新 session
2. **Birth Time 比对**（辅助）— UUID 相同时，用 birth time 辅助确认

### 工作流程
```
每次收到消息：
  maintenance.sh update <agent> <chat_id>

Session 重置后恢复：
  1. maintenance.sh verify <agent> <chat_id>
  2. 如果 RESET_DETECTED，从 last_history 获取文件路径
  3. recovery.sh read-file <last_history> --lines 100
```

---

## v1.01 (2026-03-27)

### 核心改进
- **Tracker 文件 + Birth Time 验证机制**：解决系统自动重置后的上下文恢复问题
- **active_created_at 字段**：记录当前 session 文件的创建时间，用于验证 session 是否被重置
- **history[].created_at**：记录历史 session 文件的创建时间

### 文件变更
- `SKILL.md`：更新文档，添加 Tracker 结构说明和验证流程
- `recovery.sh`：新增 `read-file` 命令，支持读取指定文件路径
- `maintenance.sh`：新增 `verify` 命令，基于 birth time 验证 session 状态

### 工作流程
```
每次收到消息：
  maintenance.sh update <agent> <chat_id>

Session 重置后恢复：
  1. maintenance.sh verify <agent> <chat_id>
  2. 如果 RESET_DETECTED，从输出获取 last_session_file
  3. recovery.sh read-file <file> --lines 100
```

---

## v1.00 (更早版本)
- 基于 grep 扫描 session 文件前 20 行匹配 chat_id
- 使用 sessions_list 获取 transcriptPath
- scan/read/list 命令直接操作 session 文件
