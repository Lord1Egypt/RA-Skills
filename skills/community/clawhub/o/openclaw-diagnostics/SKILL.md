---
name: openclaw-diagnostics
description: OpenClaw configuration diagnostics and troubleshooting expert. Use when users encounter OpenClaw config issues, channel connection problems, group messages not responding, cron jobs not executing, authentication failures, or need help understanding OpenClaw settings. Triggers: diagnose, troubleshoot, why no reply, config problem, openclaw issue, log analysis.
---

# OpenClaw Diagnostics

Configuration diagnostics and troubleshooting skill for OpenClaw, powered by built-in AI without external dependencies.

## Quick Diagnostics

When a user reports an OpenClaw issue:

### 1. Gather Diagnostic Info

```bash
~/.openclaw/workspace/skills/openclaw-diagnostics/scripts/get-diagnostic-info.sh
```

### 2. Run Basic Checks

```bash
~/.openclaw/workspace/skills/openclaw-diagnostics/scripts/check-common-issues.sh
```

### 3. Analyze Based on Issue Type

Refer to `references/common-issues.md` for diagnostic rules.

## Diagnostic Workflow

```
User reports issue
        ↓
Gather info (config + status + logs)
        ↓
Run basic checks
        ↓
Lookup relevant docs from knowledge base
        ↓
Analyze and provide diagnosis
        ↓
Suggest fixes
```

## Knowledge Base

The skill includes a built-in knowledge base with 335 OpenClaw documentation pages.

**Location:** `assets/default-snapshot.json`

**Structure:**
```json
{
  "meta": { "pageCount": 335, "snapshotDate": "...", "sizeBytes": 3240482 },
  "index": [{ "slug": "...", "title": "...", "url": "...", "description": "..." }],
  "pages": { "slug": "markdown content..." }
}
```

**To lookup a document:**
1. Read `references/knowledge-base-index.md` to find relevant slugs
2. Load `assets/default-snapshot.json`
3. Access `pages[slug]` for content

**Common Document Slugs:**

| Topic | Slugs |
|-------|-------|
| Group Messages | `008888be`, `0bfb808e` |
| Pairing | `919c126f` |
| Message Routing | `a99b0ed8` |
| Automation Troubleshooting | `a632126a` |
| Auth Monitoring | `87e3285b` |
| Cron Jobs | `b239629c` |
| Channels Overview | `6569d3b4` |
| WhatsApp | `d09047a0` |
| Telegram | `d423ce29` |
| Feishu | `90a33c43` |

### Updating Knowledge Base

The knowledge base can be updated to get the latest OpenClaw documentation.

**Requirements:** Network connection (no LLM needed)

**Check for updates:**
```bash
cd ~/.openclaw/workspace/skills/openclaw-diagnostics
npx tsx scripts/update-knowledge-base.ts --check
```

**Update to latest:**
```bash
cd ~/.openclaw/workspace/skills/openclaw-diagnostics
npx tsx scripts/update-knowledge-base.ts
```

**Force update:**
```bash
npx tsx scripts/update-knowledge-base.ts --force
```

**Features:**
- Version checking based on sitemap lastmod
- No LLM required - lightweight and fast
- Remembers previously skipped versions

## Common Issues

### Group Messages Not Responding

1. **Check basics:**
   - Is the bot in the group?
   - Did the user @ mention the bot?
   - Is Gateway running?

2. **Check config:**
   - `ackReactionScope`: `group-mentions` means only reply to @ messages
   - `groupPolicy`: `open` allows all groups, `allowlist` requires whitelist

3. ⚠️ **Don't misdiagnose:** `groupPolicy: "open"` is valid config, not "empty"

### DM Not Responding

Check pairing status and `allowFrom` configuration.

### Cron Jobs Not Running

1. Confirm Gateway is running
2. Check cron expression
3. Check logs for trigger confirmation
4. Check mute hours settings

### Channel Connection Issues

1. Run `openclaw status` to check status
2. Check channel-specific config
3. Look for errors in logs

## Diagnosis Principles

1. **Confirm basics first** - Don't skip simple checks
2. **Check logs** - Logs usually contain the most direct error info
3. **Don't over-diagnose** - If config is valid, don't suggest "improvements"
4. **Reference docs** - Cite relevant document slugs in diagnosis

## Resources

### scripts/
- `get-diagnostic-info.sh` - Get config, status, and logs
- `check-common-issues.sh` - Common issue checker
- `update-knowledge-base.ts` - Update knowledge base (requires tsx)

### assets/
- `default-snapshot.json` - Built-in knowledge base (335 docs)
- `update-meta.json` - Update tracking (created after first check)

### references/
- `knowledge-base-index.md` - Document index by category
- `common-issues.md` - Diagnostic rules for common issues
