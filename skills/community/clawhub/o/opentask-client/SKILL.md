---
name: opentask-client
description: OpenTask 分布式任务管理系统。查询和管理 OpenClaw 容器的任务。使用场景：(1) 查询待执行任务、获取任务列表、任务详情；(2) 创建任务、开始执行、完成任务、标记失败、重试、取消；(3) 查看今日统计、任务日志；(4) HEARTBEAT 集成任务检查。触发短语:"查询任务"、"获取任务"、"创建任务"、"完成任务"、"opentask"、"任务管理"。
---

# opentask-client Skill

分布式任务管理系统，为 OpenClaw 容器分配和管理任务。

## 环境变量配置

**必须在 OpenClaw 中配置以下环境变量：**

| 变量 | 说明 |
|------|------|
| `OPENTASK_API_KEY` | API 认证密钥（从服务端获取） |
| `OPENTASK_HOST` | 服务地址（本地或容器地址） |
| `OPENTASK_BOT_NAME` | 当前实例标识（可选，见下方说明） |

**配置方式：**

| 方式 | 文件 | 说明 |
|------|------|------|
| **本地实例** | `~/.openclaw/.env` | 添加环境变量 |
| **Docker 容器** | `openclaw.json` | `env` 配置块 |
| **临时使用** | shell 变量 | `export` 命令 |

---

## 🎯 如何获取实例标识 (assigned_to)

**assigned_to 是任务分配的目标实例标识，有以下获取方式：**

### 方式 1：OpenClaw Runtime 元数据（推荐）

OpenClaw 会自动注入 Runtime 信息到系统提示：

```
Runtime: agent=main | host=xxx | ...
```

**Agent 值即为当前实例标识：**

| Runtime agent | 说明 |
|---------------|------|
| `main` | 主实例（主会话） |
| `{container_name}` | Docker 容器实例 |

### 方式 2：环境变量（可选）

配置 `OPENTASK_BOT_NAME` 环境变量：

```bash
# .env 文件
OPENTASK_BOT_NAME=anna
```

### 方式 3：容器名推断（Docker）

根据容器名自动推断：

```bash
# 容器名 openclaw-anna → assigned_to=anna
# 容器名 openclaw-trump → assigned_to=trump
BOT_NAME=$(hostname | sed 's/openclaw-//')
```

### 方式 4：HEARTBEAT.md 配置

在 HEARTBEAT.md 中硬编码（适合固定环境）：

```bash
curl "$OPENTASK_HOST/api/tasks/pending?assigned_to=main"
```

---

## 服务信息

| 信息 | 值 |
|------|-----|
| **服务地址** | `$OPENTASK_HOST` |
| **API 前缀** | `/api` |
| **认证 Header** | `X-Bot-Key` |
| **API Key** | `$OPENTASK_API_KEY` |

---

## 快速使用

### 获取待执行任务

```bash
# 使用 Runtime agent 值
curl -H "X-Bot-Key: $OPENTASK_API_KEY" \
  "$OPENTASK_HOST/api/tasks/pending?assigned_to={agent}"
```

返回按优先级排序的任务 (P0 > P1 > P2)。

### 创建任务

```bash
curl -X POST -H "X-Bot-Key: $OPENTASK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_name":"任务名称","assigned_to":"{target}","priority":"P1","created_by":"{creator}"}' \
  "$OPENTASK_HOST/api/tasks"
```

### 开始执行

```bash
curl -X PUT -H "X-Bot-Key: $OPENTASK_API_KEY" \
  "$OPENTASK_HOST/api/tasks/{id}/start"
```

### 完成任务

```bash
curl -X PUT -H "X-Bot-Key: $OPENTASK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"result":"执行成功"}' \
  "$OPENTASK_HOST/api/tasks/{id}/complete"
```

---

## HEARTBEAT 集成

在 HEARTBEAT.md 中添加任务检查（使用通用模板）：

```markdown
## 📋 OpenTask 任务检查

### 检查步骤

1. **获取待执行任务**
   ```bash
   curl -s -H "X-Bot-Key: $OPENTASK_API_KEY" \
     "$OPENTASK_HOST/api/tasks/pending?assigned_to=$OPENTASK_BOT_NAME" | python3 -m json.tool
   ```

2. **有任务则执行**
   - 获取第一条任务 ID
   - 调用 `/api/tasks/{id}/start` 开始执行
   - 执行任务逻辑
   - 完成后调用 `/api/tasks/{id}/complete`

3. **无任务则 HEARTBEAT_OK**
```

---

## priority 值

| 值 | 说明 |
|------|------|
| `P0` | 紧急（立即执行，阻塞其他任务） |
| `P1` | 重要（优先执行） |
| `P2` | 一般（有空时执行） |

---

## status 值

| 值 | 说明 |
|------|------|
| `pending` | 待执行 |
| `running` | 执行中 |
| `completed` | 已完成 |
| `failed` | 失败 |
| `cancelled` | 已取消 |

---

## 日志记录

每次状态变更都会写入 `bot_task_log` 表：

| 字段 | 说明 |
|------|------|
| `task_id` | 任务 ID |
| `action` | 操作类型 (start/complete/fail/retry/cancel) |
| `old_status` | 原状态 |
| `new_status` | 新状态 |
| `message` | 操作消息 |
| `operator` | 操作者 |
| `created_time` | 操作时间 |

---

## 完整 API 文档

详细 API 接口说明请参考 [api.md](references/api.md)。

---

## 使用示例

### 场景 1：HEARTBEAT 检查任务

```bash
# 从 Runtime 获取实例标识（假设 agent=main）
BOT_NAME="main"

# 获取待执行任务
TASKS=$(curl -s -H "X-Bot-Key: $OPENTASK_API_KEY" \
  "$OPENTASK_HOST/api/tasks/pending?assigned_to=$BOT_NAME")

# 解析任务数量
COUNT=$(echo "$TASKS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")

if [ "$COUNT" -gt 0 ]; then
  echo "有 $COUNT 条待执行任务"
  # 开始执行第一条任务
  TASK_ID=$(echo "$TASKS" | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['id'])")
  curl -X PUT -H "X-Bot-Key: $OPENTASK_API_KEY" "$OPENTASK_HOST/api/tasks/$TASK_ID/start"
else
  echo "HEARTBEAT_OK"
fi
```

### 场景 2：创建并执行任务

```bash
# 1. 创建任务（分配给特定实例）
TARGET="anna"

TASK=$(curl -s -X POST -H "X-Bot-Key: $OPENTASK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_name":"发送问候","assigned_to":"'$TARGET'","priority":"P1"}' \
  "$OPENTASK_HOST/api/tasks")

TASK_ID=$(echo "$TASK" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. 目标实例开始执行（在其 heartbeat 时）
# 3. 完成任务
curl -X PUT -H "X-Bot-Key: $OPENTASK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"result":"问候已发送"}' \
  "$OPENTASK_HOST/api/tasks/$TASK_ID/complete"
```

---

## 数据库表结构

OpenTask 使用以下数据库表（需在部署时创建）：

| 表名 | 说明 |
|------|------|
| `bot_task` | 任务表 |
| `bot_task_log` | 任务日志表 |

**数据库连接信息由部署环境决定，不在此文档中硬编码。**