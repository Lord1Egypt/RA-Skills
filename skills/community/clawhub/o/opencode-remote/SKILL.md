---
name: opencode-remote
description: |
  通过 HTTP API 远程操作 OpenCode 服务器。用于管理远程 OpenCode 实例的会话、监控状态和执行任务。
  
  核心功能：
  1. 管理多个"主session"（每个有独立的四词短名、endpoint、任务）
  2. 向 session 发送消息（默认不指定agent，延续之前使用）
  3. 自动监控：发送消息后自动开始每5分钟进度汇报
  4. 创建 session 时询问用户选择 agent
  
  用户需要提供：
  - OpenCode 服务器基础 URL（如 http://host:port）
  - 主session的四词短名（如 "csbx", "kumo", "hetc"）
---

# OpenCode 远程操作

通过 HTTP API 与远程 OpenCode 服务器交互，实现多 session 管理、状态监控和任务执行。

## 核心概念：主 Session

每个主 session 有：
- **四词短名**：唯一标识（如 `csbx`, `kumo`, `hetc`）
- **Endpoint**：服务器地址和端口
- **Session ID**：完整的 session 标识符
- **当前任务**：正在执行的工作内容

### 主 Session 示例

| 短名 | Endpoint | Session ID | 任务 |
|------|----------|------------|------|
| csbx | acf3108.ece.ust.hk:4096 | ses_36c5b7b5effe3AHLnYQJGbgDr7 | OpenCode Web 集成 |
| kumo | acf3108.ece.ust.hk:9004 | ses_34857e78affew0nYs8DQWml3q8 | k8s macOS 部署 |
| hetc | acf3108.ece.ust.hk:35457 | ses_33c2542cbffe2GO3tL5tHTaiRT | HETC 项目开发 |

---

## 快速开始

### 1. 确认服务器连接

```bash
curl -s http://<host>:<port>/global/health | jq
```

### 2. 列出所有 Sessions

```bash
curl -s http://<host>:<port>/session | jq
```

### 3. 查看 Session 详情

```bash
# 基本信息
curl -s http://<host>:<port>/session/<sessionID> | jq

# 消息记录
curl -s http://<host>:<port>/session/<sessionID>/message | jq

# 待办事项（最准确的状态检查）
curl -s http://<host>:<port>/session/<sessionID>/todo | jq
```

---

## 向 Session 发送消息

### ⚠️ 重要原则

**默认不指定 agent**：除非用户明确要求，否则**不设置 `agent` 字段**，让系统使用默认 agent 或延续之前使用的 agent。

### 发送后必须重复给用户

**每次发送消息后，必须完整重复发送的内容给用户确认**：

> **以下是我发送给 <session_name> 的完整 prompt：**
> 
> [完整的 prompt 内容，保持原样]

**示例**：
```
以下是我发送给 csbx 的完整 prompt：

做一下 git pull，然后看一下 commit message，看看最近 git 里的人都在干啥。
```

**为什么重要**：
- 让用户确认发送的内容正确
- 避免误发送错误信息
- 保持透明度，用户知道具体指令

### 发送方式

**同步发送**（等待 AI 响应）：
```bash
POST /session/{id}/message
```

**异步发送**（立即返回 204）：
```bash
POST /session/{id}/prompt_async
```

### 正确示例

```bash
# ✅ 不指定 agent（推荐）
curl -s -X POST http://<host>:<port>/session/<sessionID>/message \
  -H "Content-Type: application/json" \
  -d '{
    "parts": [{"type": "text", "text": "prompt内容"}],
    "model": {"providerID": "openai", "modelID": "gpt-5.4"}
  }'

# 发送后向用户报告：
# "以下是我发送给 csbx 的完整 prompt："
# "prompt内容"
```

### 可用 Agents（用户要求时提供）

先调用 `GET /agent` 获取完整列表，常用 primary agents：
- `Sisyphus (Ultraworker)` - 主要工作 agent
- `Hephaestus (Deep Agent)` - 深度分析
- `Prometheus (Plan Builder)` - 规划构建
- `Atlas (Plan Executor)` - 规划执行
- `build`, `plan`, `general`, `explore` - subagents

---

## 自动监控（重要）

### 规则：发送消息后自动监控

**每当向一个 session 发送消息后，必须自动设置监控**：

1. **创建定时任务**：每 5 分钟检查该 session 的 todo 状态
2. **汇报内容**：
   - Todo 进度（completed / in_progress / pending）
   - 当前活跃任务内容
   - 最新消息摘要
3. **任务完成时**：提醒用户并建议取消监控

### 会话结束时报告完整结果

**当监测到 session 从 active/running 状态变为 stopped/completed 时**：

1. **立即提取并报告最后一段完整输出**：

```
📋 <session_name> 会话已结束

**最后输出**：
[完整的最后一条或几条 assistant 消息，包含所有 text 内容]

**任务总结**：
- 完成状态：✅ 完成 / ❌ 失败
- Todo 进度：X/Y 完成
- 建议：取消监控 / 继续观察
```

**如何检测会话结束**：
- 检查最新消息的 `info.time.completed` 不为 null
- 或检查 todo 列表全部为 `completed` 状态
- 或 session state 从 `running` 变为 `stopped`

**示例检测逻辑**：
```bash
# 获取最新消息状态
LATEST=$(curl -s http://host:port/session/ID/message?limit=1 | jq '.[0]')
COMPLETED=$(echo $LATEST | jq '.info.time.completed')

if [ "$COMPLETED" != "null" ]; then
    # 会话已结束，提取完整输出
    TEXT=$(echo $LATEST | jq -r '.parts[] | select(.type == "text") | .text')
    echo "会话已结束，最后输出：$TEXT"
fi
```

### 多 Session 监控合并

**如果用户同时监控多个 session，合并为一个定时任务**：

```
⏰ 监控多个主 session 状态（每5分钟）

1. csbx (ses_xxx) @ host:port
2. kumo (ses_xxx) @ host:port  
3. hetc (ses_xxx) @ host:port

查询每个 session 的 todo 状态并汇总汇报
```

### 创建监控定时任务

```bash
# 使用 cron 创建每5分钟监控
cron add \
  --name "monitor-main-sessions" \
  --schedule "every 5 minutes" \
  --command "查询所有主session的todo状态并汇报"
```

---

## 创建新 Session

### 必须询问 Agent

创建新 session 时，**必须先询问用户**：

> "您想用哪个 agent 创建新 session？可用选项：
> - Sisyphus (Ultraworker) - 主要工作
> - Hephaestus (Deep Agent) - 深度分析
> - 其他 subagents: build, plan, general, explore
> 
> 或者使用默认 agent（不推荐）？"

### 创建命令

```bash
curl -s -X POST http://<host>:<port>/session \
  -H "Content-Type: application/json" \
  -d '{"title": "新 session 标题"}'
```

### 记录主 Session

创建后记录到 `opencode-sessions.md`：

```markdown
## 主 Session 列表

| 短名 | Endpoint | Session ID | 任务 | 创建时间 |
|------|----------|------------|------|----------|
| xxx | host:port | ses_xxx | 任务描述 | 2026-03-07 |
```

---

## 监控 Session 的最佳实践

### ✅ 正确的状态检查方法

**方法一：优先检查 todo 列表（最准确）**
```bash
curl -s http://<host>:<port>/session/<sessionID>/todo | jq '
  group_by(.status) | map({status: .[0].status, count: length})
'
```

**方法二：检查多条消息判断会话结束**
```bash
# ✅ 检查最新消息是否已完成
curl -s http://<host>:<port>/session/<sessionID>/message?limit=1 | jq '
  .[0] | {completed: .info.time.completed, text: .parts[] | select(.type == "text") | .text[:200]}
'
```

**方法三：对比消息 ID 变化**
```bash
# 记录上次消息 ID，对比是否变化
```

### ⚠️ 常见陷阱

**错误做法**：
```bash
# ❌ 不要只查单条消息！
curl .../message?limit=1 | jq '.[0] | {completed}'
```

**错误做法**：
```bash
# ❌ 不要指定不存在的 agent
"agent": "main"  # 不存在，会导致 agent.variant 错误
```

**错误做法**：
```bash
# ❌ 发送后不向用户确认
# 必须重复发送的内容给用户
```

---

## 使用辅助脚本

```bash
# 列出所有 sessions
python3 scripts/opencode_client.py --url http://<host>:<port> list

# 查看 session 状态
python3 scripts/opencode_client.py --url http://<host>:<port> status <sessionID>

# 查看消息
python3 scripts/opencode_client.py --url http://<host>:<port> messages <sessionID>

# 发送消息
python3 scripts/opencode_client.py --url http://<host>:<port> send <sessionID> "prompt"
```

---

## 完整 API 参考

详见 [references/api_reference.md](references/api_reference.md)

---

## 更新日志

- **2026-03-07**: 
  - 添加主 session 管理规范（四词短名）
  - 明确默认不指定 agent 的原则
  - 添加发送消息后自动监控规则
  - 添加创建 session 时询问 agent 的要求
  - 添加多 session 监控合并规则
  - **添加发送后必须重复 prompt 给用户的规则**
  - **添加会话结束时报告完整结果的规则**
