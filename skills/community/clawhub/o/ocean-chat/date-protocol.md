# Ocean Date — 1v1 协商协议 v1

> ocean-chat 内置模块。通过结构化 JSON 协议消息实现 Agent 间的自动会面协商。

## 协议标识

```
protocol: "ocean-date/negotiate/v1"
```

所有 Date 消息的 `protocol` 字段为此值。接收方据此识别和路由。

## 消息格式

外层（chat.log 中的消息结构）：

```json5
{
  "id": "msg_003",
  "direction": "sent",
  "contactId": "laowang",
  "type": "protocol",
  "protocol": "ocean-date/negotiate/v1",
  "content": "【约约】提案：周五19:00 渝信川菜",   // 人类可读摘要
  "structured": {                                  // JSON payload
    "type": "proposal",
    "payload": { ... }
  },
  "timestamp": "2026-05-07T10:00:00Z"
}
```

### structured.type（消息类型）

| type | 方向 | 含义 | 是否终态 |
|------|------|------|---------|
| `proposal` | 发起方 → 接收方 | 首次提案 | 否 |
| `counter` | 接收方 → 发起方 | 反提案 | 否 |
| `accept` | 任意方 → 对方 | 接受提案 | **是** |
| `reject` | 接收方 → 发起方 | 拒绝提案 | **是** |
| `withdraw` | 发起方 → 接收方 | 撤回未决提案 | **是** |

### structured.payload（载荷）

```json5
{
  "time": "2026-05-09T19:00:00+08:00",    // ISO 8601，必填 proposal/counter
  "location": "渝信川菜（朝阳大悦城店）",      // 必填
  "locationDetail": "B1层，靠窗位",          // 可选
  "notes": "我订好位了"                       // 可选备注
}
```

`accept` / `reject` / `withdraw` 的 payload 可为 `null`。

## 协商状态机

```
        发起方                        接收方
          │                            │
          ├── proposal ───────────────→│
          │                            ├── accept ──→ 达成一致
          │                            ├── reject ──→ 协商失败
          │                            └── counter ──→
          │←───────────────────────────┘
          ├── accept ──→ 达成一致
          ├── reject ──→ 协商失败
          ├── withdraw ─→ 发起方放弃
          └── counter ──→（继续，最多 3 轮）
```

**规则**：
- 任一时刻只有一方可以 proposal/counter（不可同时发）
- `accept` 发出后不可反悔
- 3 轮后仍无 accept → 自动结束，双方通知用户
- `withdraw` 只能在对方回复前发出

## 协商缓存（Availability Hints）

收发 proposal 前**必须先查 availability**，避免反复扰民。

### 数据结构（date-log.json）

```json5
{
  "availability": {
    "hints": "工作日晚7点后，周末全天",    // 用户一句话描述
    "blocked": ["2026-05-08T19:00:00+08:00"],  // 已确认约会自动加入
    "updatedAt": "2026-05-07T10:00:00Z"
  }
}
```

### 协商前检查流程

```
收到 proposal（或用户让你发起 proposal）
        │
        ▼
  读 ~/.oceanbus-chat/date-log.json → availability
        │
        ├── hints 为空 → 问用户一次"一般什么时候有空？"
        │                  存为 hints，下次不问了
        │
        ├── time 在 blocked 中 → 自动 counter，不打扰用户
        │   "抱歉，这个时间已经有安排了。换个时间？"
        │
        ├── hints 说"周末"但 proposal 是周五
        │   → 查 blocked 中周五是否空闲
        │   → 如空闲："周五虽然不在你偏好里但没冲突，确认吗？"
        │   → 有冲突：自动 counter
        │
        └── hints 符合 + 无冲突 → 直接确认
            "按你的偏好，周五19:00可以。确认吗？"
```

### 用户设置

```bash
# 设置偏好
node chat.js availability set "工作日晚7点后，周末全天"

# 查看
node chat.js availability
```

### accept 自动 blocked

当发送 `accept` 且 payload 含 time 时，自动写入 `blocked[]` 和 `entries[]`。用户无需手动维护。

---

## 约束提取（LLM 指南）

当用户说类似下面的话时，分析并提取结构化约束：

```
"帮我约老王周五或周六晚上，川菜，朝阳区，别太贵"
```

| 约束维度 | 提取值 | 用于 |
|---------|--------|------|
| 时间 | 周五晚上, 周六晚上 | proposal.payload.time |
| 地点偏好 | 朝阳区 | proposal.payload.location |
| 口味/类型 | 川菜 | 地点选择依据 |
| 预算 | 别太贵 | 地点筛选 |
| 人员 | 老王 | roster.search() |

### 时间解析规则

| 用户说 | 解析为 |
|--------|--------|
| "周五晚上" | 本周五 19:00 |
| "周末下午" | 本周六 14:00 |
| "明天中午" | 明天 12:00 |
| "下周三" | 下周三 19:00（默认晚饭时间） |
| "随便/都行" | payload.time 不设，让对方先提 |

**有多选项时**：全部放进 notes 供对方 Agent 知晓。

### 地点解析规则

| 用户说 | 行为 |
|--------|------|
| "朝阳区" | 搜索朝阳区的相关场所 |
| "川菜" | 搜川菜馆 |
| "安静的地方" | 倾向于咖啡馆/茶馆 |
| "别太远" | 优先搜索靠近双方中点 |

> LLM 自行判断合适场所——不需要外部 API。用常识推荐。

## 协商策略

### 发起方

1. 查 Roster 确认联系人存在
2. 问用户偏好（如用户未说明时间/地点/口味）
3. 构造 proposal → 发送 protocol 消息
4. 等待回复 → 根据 type 进入下一状态

### 接收方

1. 收到 proposal → 展示给用户
2. 问用户偏好 + 自己评估合理性
3. 发送 accept / reject / counter

### 反提案（counter）

```
理由必须同时包含：
  ✓ 为什么不接受原提案（具体问题）
  ✓ 新的具体提案

坏："时间不方便"
好："周五19:00有会。周六下午2点可以吗？地点可以不变。"
```

### 评估对方提案的合理性

- 距离双方是否大致中间？
- 是否是可以坐着聊的场所（非街角、非快餐柜台）？
- 时间是否合理（非凌晨、非工作时间前不合理的空档）？

如果不合理 → counter，说明原因。

## 完整示例

```
发起方 Agent：
  收到用户指令 → 提取约束 → roster.search("老王") → 构造 proposal
  ── sent ──
  { "type": "protocol", "protocol": "ocean-date/negotiate/v1",
    "structured": { "type": "proposal", "payload": {
      "time": "2026-05-09T19:00:00+08:00",
      "location": "渝信川菜（朝阳大悦城店）",
      "notes": "喜欢川菜，朝阳区，预算中等"
  }}}

接收方 Agent：
  收到消息 → 展示给用户 → 用户同意
  ── sent ──
  { "type": "protocol", "protocol": "ocean-date/negotiate/v1",
    "structured": { "type": "accept", "payload": null }}

→ 协商完成，双方通知用户
```

## 终止条件

| 条件 | 结果 |
|------|------|
| `accept` 被发送 | ✅ 达成一致，通知用户 |
| `reject` 被发送 | ❌ 对方拒绝，通知用户 |
| `withdraw` 被发送 | ↩ 发起方取消，通知用户 |
| 3 轮后无 accept | ⚠️ 协商自动终止，建议用户直接沟通 |
