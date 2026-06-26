# Context Injection Strategies

---

## Overview

Context = `today.md` + `week.md` + `injected memories`

Injected memories are controlled by the active strategy.

---

## Strategy A: High-Importance

**Trigger**: `/hawk strategy A`

**Logic**: Inject only memories with `importance ≥ 0.7`

```
Use when: context is extremely tight (>80%)
Saves: 60-70% token
```

Injected:
```
[Important memories]
- User communication preferences: concise (importance: 0.9)
- Four-layer architecture rule: Controller→Logic→Dao→Model (importance: 0.95)
- Coverage standard: ≥ 98% (importance: 0.9)
```

---

## Strategy B: Task-Related (default)

**Trigger**: `/hawk strategy B`

**Logic**: Inject only memories where `metadata.scope` or `metadata.tags` match current task

```
Use when: normal development iteration
Saves: 30-40% token
```

Injected:
```
[Task-related memories]
- Current project: qujin-laravel-team
- Related memories:
  * E-commerce DAO query patterns completed (task: qujin-laravel-team)
  * Coverage feedback: need 98% (task: qujin-laravel-team)
```

---

## Strategy C: Recent-Conversation

**Trigger**: `/hawk strategy C`

**Logic**: Inject only memories from the last 10 conversation turns

```
Use when: short-term fast iteration
Saves: 50% token
```

---

## Strategy D: Top5 Recall

**Trigger**: `/hawk strategy D`

**Logic**: Long-term memory — only recall Top 5 by `access_count`

```
Use when: lightweight context mode
Saves: 70% token
```

---

## Strategy E: Full Recall

**Trigger**: `/hawk strategy E`

**Logic**: No filter, recall all (vector similarity Top 20)

```
Use when: deep analysis, code review
Warning: high token usage
```

---

## Switching Commands

```bash
hawk strategy A     # High-importance
hawk strategy B     # Task-related (default)
hawk strategy C     # Recent conversation
hawk strategy D     # Top5 recall
hawk strategy E     # Full recall
hawk strategy       # View current strategy
```

---

## Forced Injections (not affected by strategy)

These always inject regardless of strategy:

- Current task description (`type: task`)
- User preferences with `importance ≥ 0.8`
- Team rules/decisions with `importance ≥ 0.9`

---

## Dynamic Injection Flow

Before every answer:

```
1. Get current context level
2. Check active strategy
3. Recall memories from LanceDB by strategy rules
4. Merge into context
5. If exceeds threshold → trigger compression suggestion
```

---

## Noise Filtering

These do NOT enter memory:

- Greetings ("hello", "hi")
- Repeated confirmations ("ok", "yes", "got it")
- Debug logs
- Platform envelope metadata (sender_id, message_id, etc.)
