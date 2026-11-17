# Hook API 文档

## 概述

Hook Engine 提供事件驱动的拦截机制，允许在关键操作前后执行自定义检查和日志记录。

## 事件生命周期

```
PreExec → [命令执行] → PostExec
PreMessage → [消息发送] → PostMessage
Stop → [会话结束]
```

## 事件数据结构

### PreExec

```json
{
  "event": "PreExec",
  "command": "ls -la",
  "workdir": "/path/to/dir",
  "env": { "PATH": "...", "HOME": "..." }
}
```

### PostExec

```json
{
  "event": "PostExec",
  "command": "ls -la",
  "exitCode": 0,
  "stdout": "file1\nfile2\n",
  "stderr": "",
  "duration": 150
}
```

### PreMessage

```json
{
  "event": "PreMessage",
  "content": "消息内容",
  "channel": "mx",
  "target": "user-id"
}
```

### PostMessage

```json
{
  "event": "PostMessage",
  "content": "消息内容",
  "channel": "mx",
  "messageId": "msg-123",
  "status": "sent"
}
```

### Stop

```json
{
  "event": "Stop",
  "session": "session-id",
  "reason": "user-request",
  "summary": "完成了 XX 任务"
}
```

## Hook 脚本接口

### 输入

- Hook 脚本从 **stdin** 接收 JSON 格式的事件数据
- 脚本必须可执行（`chmod +x`）
- 脚本必须在 5 秒内返回结果

### 输出

脚本向 **stdout** 输出 JSON 格式结果：

```json
{
  "decision": "allow|warn|block",
  "message": "人类可读的说明文本",
  "matched_rules": ["rule-name-1", "rule-name-2"],
  "timestamp": "2026-06-26T22:00:00Z"
}
```

### Decision 语义

| decision | 行为 |
|----------|------|
| `allow` | 操作正常执行 |
| `warn` | 操作执行，但向用户显示警告 |
| `block` | 操作被阻止，向用户显示拒绝原因 |

## 规则文件格式

规则文件使用 Markdown + YAML frontmatter：

```markdown
---
name: rule-unique-name
enabled: true
event: PreExec
matcher: "regex pattern"
action: block
priority: 50
---

规则说明文本（Markdown body）。
当规则触发时，此文本作为提示信息展示给用户。
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✓ | 规则唯一标识 |
| enabled | boolean | ✓ | 是否启用 |
| event | string | ✓ | 绑定事件类型 |
| matcher | string | ✓ | 正则表达式匹配模式 |
| action | string | ✓ | allow/warn/block/log |
| priority | number | ✗ | 优先级（默认 50，越大越先评估） |

## 审计日志

所有 hook 触发记录写入 `memory/hook-audit.log`：

```
[2026-06-26T22:00:00Z] [PreExec] [block] [block-disk-format] cmd=format C: ...
[2026-06-26T22:00:01Z] [PostExec] [allow] [success] cmd=ls exit=0 duration=50ms
```

## 扩展方式

### 添加新事件类型

1. 在 `hooks/` 下创建对应的 hook 脚本
2. 命名规则：`{event-type}-{purpose}.sh`
3. 遵循 stdin→评估→stdout JSON 接口

### 添加新规则

1. 在 `rules/` 下创建或编辑 `.md` 文件
2. 按 frontmatter 格式定义规则元数据
3. body 部分定义提示信息

### 自定义 Hook

创建自定义 hook 脚本时，遵循以下接口：

```bash
#!/bin/bash
# 1. 读取 stdin
EVENT=$(cat)
# 2. 处理逻辑
# 3. 输出 JSON
echo '{"decision":"allow","message":"ok","matched_rules":[],"timestamp":"..."}'
```
