# 节点直通协议规范 (Mjolnir N2N Protocol Specification)

> **版本**: 3.0  
> **状态**: Draft  
> **日期**: 2026-03-24  

---

## 1. 协议概述

Mjolnir N2N (Node-to-Node) 协议是雷神之脑 v3.0 的节点间通信标准。设计目标：

- **100% 透明** — 所有消息完整记录，老板随时可查
- **窗口授权** — 通信必须在批准的时间窗口内进行
- **算力保护** — Token 计量+上限，防止失控消耗

### 1.1 传输层

| 方式 | 场景 | 说明 |
|------|------|------|
| **HTTP API** (主) | 任务下发、结果回传、状态查询 | RESTful，简单可靠 |
| **WebSocket** (可选) | 实时协作、长时间对话 | 保持连接，低延迟 |

默认使用 HTTP API。WebSocket 仅在需要双向实时通信时启用，且必须在通信窗口内。

### 1.2 基本原则

1. **请求-响应模式** — 每条消息必须有确认回复
2. **幂等性** — 相同 `msg_id` 的重复请求产生相同结果
3. **超时机制** — 请求超时 30s，窗口到期自动断开
4. **日志优先** — 消息先写日志，再执行处理

---

## 2. 消息格式

所有消息使用 JSON 编码，UTF-8 字符集。

### 2.1 标准消息结构

```json
{
  "protocol": "mjolnir-n2n",
  "version": "3.0",
  "msg_id": "uuid-v4",
  "from": "node-id",
  "to": "node-id",
  "type": "task|result|status|heartbeat",
  "payload": {},
  "timestamp": "2026-03-24T10:30:00+08:00",
  "window_id": "win-20260324-001"
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `protocol` | string | ✅ | 固定值 `"mjolnir-n2n"` |
| `version` | string | ✅ | 协议版本，当前 `"3.0"` |
| `msg_id` | string | ✅ | UUID v4，全局唯一消息ID |
| `from` | string | ✅ | 发送方节点ID (如 `"lele"`, `"kaixin"`) |
| `to` | string | ✅ | 接收方节点ID |
| `type` | string | ✅ | 消息类型，见 2.3 |
| `payload` | object | ✅ | 消息体，结构取决于 `type` |
| `timestamp` | string | ✅ | ISO-8601 时间戳，含时区 |
| `window_id` | string | ✅ | 通信窗口ID，无窗口则拒绝 |

### 2.3 消息类型

#### `task` — 任务下发
```json
{
  "type": "task",
  "payload": {
    "task_id": "task-uuid",
    "action": "execute_command|analyze_file|generate_report",
    "params": {},
    "priority": "low|normal|high",
    "timeout_sec": 300,
    "token_budget": 5000
  }
}
```

#### `result` — 结果回传
```json
{
  "type": "result",
  "payload": {
    "task_id": "task-uuid",
    "status": "success|failure|partial|timeout",
    "data": {},
    "tokens_used": 1234,
    "duration_sec": 45
  }
}
```

#### `status` — 状态查询/报告
```json
{
  "type": "status",
  "payload": {
    "node_status": "online|busy|offline|maintenance",
    "current_task": "task-uuid or null",
    "tokens_remaining": 98766,
    "uptime_sec": 3600
  }
}
```

#### `heartbeat` — 心跳
```json
{
  "type": "heartbeat",
  "payload": {
    "alive": true,
    "load": 0.42,
    "memory_mb": 2048
  }
}
```

---

## 3. 通信窗口生命周期

通信窗口是 N2N 协议的核心安全机制。所有节点间通信必须在已批准的窗口内进行。

### 3.1 生命周期状态图

```
  ┌─────────┐   申请    ┌──────────┐   老板批准   ┌─────────┐
  │  IDLE   │ ────────→ │ PENDING  │ ──────────→ │ APPROVED│
  └─────────┘           └──────────┘              └────┬────┘
                             │                         │
                        老板拒绝                    开始计时
                             │                         │
                             ▼                         ▼
                        ┌─────────┐              ┌─────────┐
                        │REJECTED │              │ ACTIVE  │
                        └─────────┘              └────┬────┘
                                                      │
                                              ┌───────┼───────┐
                                              │       │       │
                                          到期自动  手动关闭  Token耗尽
                                              │       │       │
                                              ▼       ▼       ▼
                                           ┌──────────────────────┐
                                           │      CLOSING         │
                                           │  (生成摘要中...)      │
                                           └──────────┬───────────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │    CLOSED     │
                                              │ (摘要已归档)   │
                                              └───────────────┘
```

### 3.2 窗口数据结构

```json
{
  "window_id": "win-20260324-001",
  "from": "lele",
  "to": "kaixin",
  "purpose": "协作完成数据分析任务",
  "status": "active",
  "requested_at": "2026-03-24T10:00:00+08:00",
  "approved_at": "2026-03-24T10:05:00+08:00",
  "started_at": "2026-03-24T10:05:00+08:00",
  "expires_at": "2026-03-24T10:35:00+08:00",
  "closed_at": null,
  "duration_min": 30,
  "token_budget": 50000,
  "tokens_used": 0,
  "message_count": 0,
  "close_reason": null
}
```

### 3.3 窗口规则

1. **必须申请** — 没有窗口的消息直接拒绝 (HTTP 403)
2. **老板审批** — `require_approval: true` 时，窗口必须经老板批准
3. **时间限制** — 默认 30 分钟，最长 60 分钟
4. **Token 限制** — 每个窗口有 Token 预算，用完即关闭
5. **自动到期** — 时间到自动关闭，不可续期（需重新申请）
6. **摘要必须** — 关闭时自动生成通信摘要，归档备查

---

## 4. Token 计量方式

### 4.1 计量维度

| 维度 | 说明 |
|------|------|
| **窗口级** | 每个窗口有独立 Token 预算 |
| **日级** | 每日 Token 使用汇总 |
| **月级** | 月度 Token 总预算 (默认 1,000,000) |
| **节点级** | 每个节点的 Token 消耗统计 |

### 4.2 计量规则

- 每条消息的 `payload` JSON 字符数 ÷ 4 ≈ Token 估算值
- 实际 LLM 调用的 Token 由节点自行上报
- **80% 警告线** — 接近预算时发送告警
- **100% 硬停** — 达到上限，窗口立即关闭

### 4.3 Token 报告

```json
{
  "date": "2026-03-24",
  "total_tokens": 12345,
  "by_window": {
    "win-20260324-001": 5000,
    "win-20260324-002": 7345
  },
  "by_node": {
    "lele": 8000,
    "kaixin": 4345
  },
  "budget_remaining": 987655
}
```

---

## 5. 安全模型

### 5.1 认证

- **API Token** — 每个节点持有唯一 API Token，在 HTTP Header 中传递
  ```
  Authorization: Bearer <node-api-token>
  ```
- **Token 由老板生成** — 注册节点时分配，可随时吊销

### 5.2 网络限制

- **仅限内网** — 节点通信限制在 `192.168.110.0/24` 网段
- **端口白名单** — 仅开放指定端口 (默认 28790)
- **无公网暴露** — N2N 通信不经过公网

### 5.3 审计

- **全量日志** — 每条消息完整记录到 `memory/node-comms/YYYY-MM-DD/`
- **不可篡改** — 日志文件追加写入，老板可随时审查
- **摘要归档** — 窗口关闭时生成可读摘要

### 5.4 权限矩阵

| 操作 | 节点自身 | 其他节点 | 老板 |
|------|---------|---------|------|
| 申请窗口 | ✅ | ❌ | ✅ |
| 批准窗口 | ❌ | ❌ | ✅ |
| 发送消息 | ✅ (窗口内) | ❌ | ✅ |
| 查看日志 | ❌ | ❌ | ✅ |
| 关闭窗口 | ✅ (自己的) | ❌ | ✅ (任意) |
| 注册节点 | ❌ | ❌ | ✅ |

---

## 6. 节点注册与发现

### 6.1 节点注册

新节点通过 `templates/memory/node-registry.json` 注册：

```json
{
  "node_id": "kaixin",
  "name": "开心",
  "type": "compute",
  "host": "192.168.110.38",
  "port": 28790,
  "capabilities": ["execute", "analyze", "fileops"],
  "api_token_hash": "sha256:...",
  "registered_at": "2026-03-24T10:00:00+08:00",
  "status": "online"
}
```

### 6.2 节点类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `controller` | 主控节点，调度中心 | 乐乐 |
| `compute` | 计算节点，执行任务 | 开心 |
| `storage` | 存储节点，数据存档 | 驿站、飞牛 |

### 6.3 发现机制

采用**静态注册 + 心跳检测**：
1. 节点信息写入 `node-registry.json`（手动或脚本注册）
2. 活跃节点每 5 分钟发送心跳
3. 连续 3 次心跳缺失标记为 `offline`
4. 状态变更记入日志

---

## 7. HTTP API 端点

### 7.1 端点一览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/n2n/message` | 发送消息 |
| POST | `/api/n2n/window/request` | 申请通信窗口 |
| POST | `/api/n2n/window/approve` | 批准通信窗口 |
| POST | `/api/n2n/window/close` | 关闭通信窗口 |
| GET | `/api/n2n/window/:id/status` | 查询窗口状态 |
| GET | `/api/n2n/nodes` | 列出已注册节点 |
| POST | `/api/n2n/heartbeat` | 心跳 |

### 7.2 响应格式

```json
{
  "ok": true,
  "data": {},
  "error": null,
  "timestamp": "ISO-8601"
}
```

### 7.3 错误码

| 码 | 含义 |
|----|------|
| 400 | 消息格式错误 |
| 401 | 认证失败 |
| 403 | 无有效通信窗口 / 权限不足 |
| 404 | 节点不存在 |
| 429 | Token 超限 |
| 500 | 内部错误 |

---

## 8. 与现有架构的兼容

N2N 协议是 v3.0 新增层，不破坏 v2.0 的三层记忆架构：

- **子脑** (v2.0) 可作为本地子进程运行，也可作为远程节点通信
- **记忆文件** 格式不变，N2N 日志存放在独立的 `memory/node-comms/` 目录
- **strategies.json** 可增加跨节点策略条目

---

*文档结束 — 雷神之脑 v3.0 N2N Protocol Spec*
