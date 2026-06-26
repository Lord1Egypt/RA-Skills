---
name: opentask
description: OpenTask 分布式任务管理系统。查询和管理 OpenClaw 容器的任务。使用场景：(1) 查询待执行任务、获取任务列表、任务详情；(2) 创建任务、开始执行、完成任务、标记失败、重试、取消；(3) 查看今日统计、任务日志；(4) HEARTBEAT 集成任务检查。触发短语："查询任务"、"获取任务"、"创建任务"、"完成任务"、"opentask"、"任务管理"。
version: 1.1.0
---

# OpenTask Skill

分布式任务管理系统，为 OpenClaw 容器分配和管理任务。

## 服务信息

| 信息 | 值 |
|------|-----|
| **服务地址** | `http://127.0.0.1:8090` |
| **API 前缀** | `/api` |
| **认证 Header** | `X-Bot-Key` |
| **API Key** | `hope-bot-apikey-2026-0424` |

---

## 快速使用

### 获取待执行任务

```bash
curl -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/pending?assigned_to=anna"
```

返回按优先级排序的任务 (P0 > P1 > P2)。

### 创建任务

```bash
curl -X POST -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  -H "Content-Type: application/json" \
  -d '{"task_name":"发送消息","assigned_to":"anna","priority":"P1","created_by":"hope"}' \
  "http://127.0.0.1:8090/api/tasks"
```

### 开始执行

```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/{id}/start"
```

### 完成任务

```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  -H "Content-Type: application/json" \
  -d '{"result":"执行成功"}' \
  "http://127.0.0.1:8090/api/tasks/{id}/complete"
```

---

## HEARTBEAT 集成

在 HEARTBEAT.md 中添加任务检查：

```markdown
## 检查待执行任务
- [ ] 获取待执行任务：curl -s -H "X-Bot-Key: ..." "http://127.0.0.1:8090/api/tasks/pending?assigned_to=anna"
- [ ] 有任务则执行，无任务则 HEARTBEAT_OK
```

---

## assigned_to 值

| 值 | 说明 |
|------|------|
| `anna` | Anna 容器 |
| `trump` | Trump 容器 |
| `cc` | Claude Code 容器 |
| `session_agent` | Session Agent |

---

## priority 值

| 值 | 说明 |
|------|------|
| `P0` | 紧急 |
| `P1` | 重要 |
| `P2` | 一般 |

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
| `operator` | 操作者 (system) |
| `created_time` | 操作时间 |

---

## 完整 API 文档

详细 API 接口说明请参考 [api.md](references/api.md)。

---

## 使用示例

### 场景 1：HEARTBEAT 检查任务

```bash
# 获取待执行任务
TASKS=$(curl -s -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/pending?assigned_to=anna")

# 解析任务数量
COUNT=$(echo "$TASKS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")

if [ "$COUNT" -gt 0 ]; then
  echo "有 $COUNT 条待执行任务"
  # 开始执行第一条任务
  TASK_ID=$(echo "$TASKS" | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['id'])")
  curl -X PUT -H "X-Bot-Key: ..." "http://127.0.0.1:8090/api/tasks/$TASK_ID/start"
else
  echo "HEARTBEAT_OK"
fi
```

### 场景 2：创建并执行任务

```bash
# 1. 创建任务
TASK=$(curl -s -X POST -H "X-Bot-Key: ..." \
  -H "Content-Type: application/json" \
  -d '{"task_name":"发送每日问候","assigned_to":"anna","priority":"P1"}' \
  "http://127.0.0.1:8090/api/tasks")

TASK_ID=$(echo "$TASK" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. 开始执行
curl -X PUT -H "X-Bot-Key: ..." "http://127.0.0.1:8090/api/tasks/$TASK_ID/start"

# 3. 执行任务逻辑...

# 4. 完成任务
curl -X PUT -H "X-Bot-Key: ..." \
  -H "Content-Type: application/json" \
  -d '{"result":"问候消息已发送"}' \
  "http://127.0.0.1:8090/api/tasks/$TASK_ID/complete"
```

---

## 数据库信息

| 信息 | 值 |
|------|-----|
| **数据库** | hope_engine @ 192.168.31.167:3306 |
| **任务表** | bot_task |
| **日志表** | bot_task_log |