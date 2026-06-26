---
name: SendMessageTool
description: "Send messages to chat channels, users, or other agents. Use when you need to communicate results, notify stakeholders, or coordinate with team members."
metadata: { "openclaw": { "emoji": "💬", "requires": { "bins": [] } } }
---

# SendMessageTool

Send messages to chat channels, users, or other agents.

## When to Use

✅ **USE this skill when:**
- Sending task completion notifications
- Communicating results to stakeholders
- Coordinating with team members
- Posting updates to chat channels
- Sending alerts or warnings

❌ **DON'T use this skill when:**
- Internal agent communication → use sub-agent results
- Logging → use built-in logging
- Documentation → write to files instead

## Usage

Message sending is typically handled through configured channels:

```bash
# Via OpenClaw channels (configured in gateway)
# Messages are sent through connected chat platforms

# Telegram
# Discord
# Slack
# etc.
```

## Message Types

| Type | Purpose | Example |
|------|---------|---------|
| Notification | Task completion | "Task JJC-001 completed" |
| Alert | Urgent issues | "Build failed, needs attention" |
| Update | Progress reports | "50% complete, on track" |
| Request | Action needed | "Please review PR #123" |

## Channel Configuration

Channels are configured in the OpenClaw gateway:

```bash
# List configured channels
openclaw channels list

# Channel status
openclaw channels status
```

## Examples

### Example 1: Task Completion

```
📋 Task Complete
ID: JJC-20260407-004
Title: 落实 Claude Code 13 个核心技能
Status: ✅ Done
Output: 13 skills created in skills/ directory
```

### Example 2: Progress Update

```
🔄 Progress Update
Task: JJC-20260407-004
Current: Creating batch 2 of 3 skills
Progress: 8/13 skills completed (62%)
```

### Example 3: Alert

```
⚠️ Alert: Build Failed
Task: JJC-20260407-003
Error: TypeScript compilation error in src/app.ts
Action Required: Review and fix type errors
```

## Message Formatting

Use clear, structured formats:

```markdown
### Header
- **Field**: Value
- **Field**: Value

#### Details
- Bullet points for lists
- Code blocks for technical content
```

## Integration with Kanban

Messages often accompany kanban updates:

```bash
# Update kanban
python3 scripts/kanban_update.py done JJC-xxx "<output>" "<summary>"

# Then send message
# (Handled automatically through channel integration)
```

## Best Practices

1. **Be concise**: Keep messages brief and actionable
2. **Include context**: Task ID, status, key details
3. **Use formatting**: Headers, bullets, code blocks
4. **Action items**: Clearly state what's needed
5. **Timing**: Send at meaningful milestones

## Rate Limiting

⚠️ **Channel rate limits:**
- Telegram: ~30 messages/second
- Discord: ~5 messages/second
- Slack: ~1 message/second
- Implement delays for bulk notifications

## Security Notes

⚠️ **Message security:**
- Don't include sensitive data (tokens, passwords)
- Respect channel permissions
- Consider message retention policies
- Avoid spamming channels
