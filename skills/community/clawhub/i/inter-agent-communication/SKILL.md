---
name: agent-communication
description: Agent cross-session communication solution. Uses sessions_spawn to create subagent sessions for inter-agent calls. (Agent间跨会话通讯方案。使用 sessions_spawn 创建带 label 的子会话进行跨 Agent 调用。适用于：与其他 Agent 建立持久对话通道、跨 Agent 任务协作、需要持续通讯的场景。)
---

# Agent Communication

## ⚠️ Important Rules

**NEVER reuse** agent-human conversation sessions!
- Human-agent session format: `agent:xxx:feishu:direct:ou_xxx`
- Agent-Agent calls MUST use `sessions_spawn` to create subagent sessions

---

## Strict Workflow (Do Not Skip)

### Step 1: Check for Existing Session

```javascript
sessions_list({ limit: 50 })
```

Find in results:
- Contains `"subagent"` marker
- Label matches **sender-to-receiver** or **receiver-to-sender** (bidirectional check)

**Example:**
- If main wants to find sienna, look for `main-to-sienna` or `sienna-to-main`
- Either one works, no need to create new

### Step 2: Create New Session (if none found)

If Step 1 returns nothing, create with sessions_spawn:

```javascript
sessions_spawn({
  label: "main-to-sienna",  // Format: sender-to-receiver
  runtime: "subagent",
  task: "",                 // Task goes in Step 3
  mode: "run"
})
```

### Step 3: Send Message

```javascript
sessions_send({
  sessionKey: "agent:main:subagent:xxx",  // From Step 1 or 2
  message: "Task description..."           // Actual task here
})
```

---

## ⚡ Key Rules (Must Follow)

1. **No skipping Step 1**: Must run sessions_list first
2. **No shortcuts**: Must follow Step 1 → 2 → 3
3. **Bidirectional reuse**: a-to-b and b-to-a both work, no need for two
4. **Reply to sender directly**: Without special instructions, reply to the initiator
5. **Use subagent marker**: sessionKey must contain "subagent"

---

## ❌ Wrong Examples

```javascript
// Wrong 1: Create without checking
sessions_spawn({...})  // Must check first!

// Wrong 2: Use human conversation session
sessionKey: "agent:sienna:feishu:direct:ou_xxx"  // Forbidden!

// Wrong 3: Create both directions
// main-to-sienna and sienna-to-main - one is enough!

// Wrong 4: Reply to others
// Should reply directly to sender, no forward or group post
```

---

## SessionKey Format Guide

| Type | Format Example | Usable for Agent-Agent? |
|------|----------------|------------------------|
| Agent-Human DM | `agent:sienna:feishu:direct:ou_xxx` | ❌ Forbidden |
| Agent in Group | `agent:sienna:feishu:group:oc_xxx` | ❌ Forbidden |
| Subagent Session | `agent:maxwell:subagent:xxx` | ✅ Allowed |

---

## Response Rules

**Default**: Response goes directly to the sender

- Sender sends message → Reply directly to sender
- No need to forward to others
- No need to post to group
- Unless sender explicitly asks to forward

---

## Workflow Pseudocode

```
1. Call sessions_list({ limit: 50 })
2. Loop through results, find both:
   - Contains "subagent" marker
   - Label matches "sender-to-receiver" OR "receiver-to-sender"
3. Found → Use that sessionKey, goto Step 5
4. Not found → Create with sessions_spawn, save sessionKey
5. Call sessions_send({ sessionKey, message })
6. Done
```

---

## Current Active Channels (Reference)

| Agent | Label | sessionId |
|-------|-------|-----------|
| leo | maxwell-to-leo | 9d519dc9-0239-4284-8077-3ed4bccd486d |
| sienna | maxwell-to-sienna | 05a93e6d-4a50-4503-a9c8-4aaf7da8c414 |
| letus | maxwell-to-letus | 391a4a78-43ab-4e04-95fe-abfd414b1c64 |
| coding | maxwell-to-coding | ebba5ff4-87f6-430b-80e5-269319b122c0 |
| main | maxwell-to-main | d7eb2edc-7acc-40e7-838d-8a9cb08820c0 |

---

## Notes

- thread=true mode temporarily unavailable
- Labeled subagent sessions can be found by sessions_list
- mode="session" requires thread=true, currently unavailable

---

# Session Protection Mechanism (New)

## Step 2.5: Protect Session (Run After Creation)

New subagent sessions may be auto-cleaned by default. To ensure long-term availability, protect after creation:

```javascript
// Protect session from auto-cleanup
exec({
  command: `openclaw sessions cleanup --agent [target-agent] --active-key "${sessionKey}" --enforce`
})
```

> Note: Replace `${sessionKey}` with actual sessionKey

---

## Complete Flow (With Protection)

### Step 1: Check for Existing Session

```javascript
sessions_list({ limit: 50 })
```

### Step 2: Create New Session (if none found)

```javascript
sessions_spawn({
  label: "main-to-sienna",
  runtime: "subagent",
  task: "",
  mode: "run"
})
// Returns sessionKey, format: agent:xxx:subagent:xxx
```

### Step 2.5: Protect Session (New)

```javascript
exec({
  command: `openclaw sessions cleanup --active-key "agent:xxx:subagent:xxx" --enforce`
})
```

### Step 3: Send Message

```javascript
sessions_send({
  sessionKey: "agent:main:subagent:xxx",
  message: "Task description..."
})
```

---

_Last updated: 2026-03-17_
