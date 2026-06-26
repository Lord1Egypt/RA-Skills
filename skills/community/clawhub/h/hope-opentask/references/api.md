# OpenTask API Reference

## 服务信息

| 信息 | 值 |
|------|-----|
| **服务地址** | http://127.0.0.1:8090 |
| **API 前缀** | /api |
| **认证方式** | X-Bot-Key Header |
| **API Key** | hope-bot-apikey-2026-0424 |

---

## 认证

所有 API 请求需要携带 `X-Bot-Key` 请求头：

```bash
curl -H "X-Bot-Key: hope-bot-apikey-2026-0424" "http://127.0.0.1:8090/api/tasks"
```

---

## API 接口

### 任务列表

```
GET /api/tasks
```

**参数：**
- `assigned_to` (可选): 指定 bot (anna/trump/cc/session_agent)
- `status` (可选): 状态筛选 (pending/running/completed/failed/cancelled)
- `priority` (可选): 优先级筛选 (P0/P1/P2)

**示例：**
```bash
curl -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks?assigned_to=anna&status=pending"
```

---

### 待执行任务

```
GET /api/tasks/pending
```

**参数：**
- `assigned_to` (必填): 指定 bot

**示例：**
```bash
curl -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/pending?assigned_to=anna"
```

**返回：** 按优先级排序的任务列表 (P0 > P1 > P2)

---

### 获取任务详情

```
GET /api/tasks/{id}
```

**示例：**
```bash
curl -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/1"
```

---

### 创建任务

```
POST /api/tasks
```

**Body：**
```json
{
  "task_name": "任务名称",
  "task_description": "任务描述",
  "task_params": "{\"key\":\"value\"}",
  "assigned_to": "anna",
  "priority": "P1",
  "created_by": "hope"
}
```

**示例：**
```bash
curl -X POST -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  -H "Content-Type: application/json" \
  -d '{"task_name":"发送消息","assigned_to":"anna","priority":"P1","created_by":"hope"}' \
  "http://127.0.0.1:8090/api/tasks"
```

---

### 开始执行

```
PUT /api/tasks/{id}/start
```

**示例：**
```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/1/start"
```

---

### 完成任务

```
PUT /api/tasks/{id}/complete
```

**Body：**
```json
{
  "result": "执行结果描述"
}
```

**示例：**
```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  -H "Content-Type: application/json" \
  -d '{"result":"任务完成"}' \
  "http://127.0.0.1:8090/api/tasks/1/complete"
```

---

### 标记失败

```
PUT /api/tasks/{id}/fail
```

**Body：**
```json
{
  "error_message": "错误原因描述"
}
```

**示例：**
```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  -H "Content-Type: application/json" \
  -d '{"error_message":"网络超时"}' \
  "http://127.0.0.1:8090/api/tasks/1/fail"
```

---

### 重试任务

```
PUT /api/tasks/{id}/retry
```

**说明：** 将失败任务重置为 pending，重试计数 +1（最大 3 次）

**示例：**
```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/1/retry"
```

---

### 取消任务

```
PUT /api/tasks/{id}/cancel
```

**示例：**
```bash
curl -X PUT -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/tasks/1/cancel"
```

---

### 今日统计

```
GET /api/stats/today
```

**返回：**
```json
{
  "anna": {"total": 5, "pending": 2, "running": 1, "completed": 2, "failed": 0},
  "trump": {"total": 3, "pending": 1, "running": 0, "completed": 2, "failed": 0}
}
```

---

### 任务日志

```
GET /api/logs/{task_id}
```

**示例：**
```bash
curl -H "X-Bot-Key: hope-bot-apikey-2026-0424" \
  "http://127.0.0.1:8090/api/logs/1"
```

---

## 任务状态流转

```
pending → running → completed
                  ↘ failed → pending (retry)
                  
pending/running → cancelled
```

---

## assigned_to 值

| 值 | 说明 |
|------|------|
| **anna** | Anna 容器 |
| **trump** | Trump 容器 |
| **cc** | Claude Code 容器 |
| **session_agent** | Session Agent |

---

## priority 值

| 值 | 说明 | 排序权重 |
|------|------|----------|
| **P0** | 紧急 | 最高优先 |
| **P1** | 重要 | 次优先 |
| **P2** | 一般 | 最后处理 |

---

## task_params 格式

JSON 字符串，灵活存储任务参数、步骤、输入输出：

```json
{
  "telegram_id": "5520269161",
  "message": "老板早上好！",
  "steps": ["检查连接", "发送消息", "确认成功"]
}
```