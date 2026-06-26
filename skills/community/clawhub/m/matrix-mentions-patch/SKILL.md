---
name: matrix-mentions-patch
description: Fix OpenClaw Matrix plugin mention detection bug. Use when OpenClaw doesn't respond to @mentions in Matrix group rooms despite correct configuration. The bug is that buildMentionRegexes() is called without agentId, causing mention patterns to not be built correctly.
---

# Matrix Mentions Patch

## Problem

OpenClaw Matrix plugin doesn't respond to @mentions in group rooms even when:
- The room is configured with `requireMention: true`
- The user correctly @mentions the bot (e.g., `@runwheezy:matrix.biochao.cc`)

## Root Cause

In `/home/bot/.openclaw/extensions/matrix/src/matrix/monitor/index.ts`, the `buildMentionRegexes` function is called WITHOUT passing `agentId`:

```typescript
// BUG: Missing agentId parameter
const mentionRegexes = core.channel.mentions.buildMentionRegexes(cfg);
```

Without `agentId`, the function can't resolve agent-specific mention patterns from config, causing mentions to never be detected.

## Fix

Edit `/home/bot/.openclaw/extensions/matrix/src/matrix/monitor/index.ts`:

Find line ~298:
```typescript
const mentionRegexes = core.channel.mentions.buildMentionRegexes(cfg);
```

Change to:
```typescript
const mentionRegexes = core.channel.mentions.buildMentionRegexes(cfg, "main");
```

Replace "main" with your actual agent ID if different.

## Apply

1. Make the edit above
2. Restart OpenClaw gateway: `openclaw gateway restart`

The fix loads immediately - no rebuild needed since the extension is loaded dynamically.
