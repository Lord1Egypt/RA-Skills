# Feishu Group Delivery Setup

## Overview

The delivery model: Create a Feishu group → Add the Agent bot → Clients join and ask questions directly (no @ needed).

## No-@ Reply Configuration

By default, bots in Feishu groups require an @mention to respond. For consulting scenarios, this is friction — clients shouldn't have to remember to @ the bot.

### Method 1: Open Group Policy (Simplest)

In `~/.openclaw/openclaw.json`:
```json5
{
  channels: {
    feishu: {
      groupPolicy: "open",
      // When groupPolicy is "open", requireMention defaults to false
      // Bot responds to all messages in all groups without @
    }
  }
}
```

**Pros**: Zero config, works immediately for all groups.
**Cons**: Bot responds in ALL groups it's added to — no selective control.

### Method 2: Top-Level requireMention Override

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["oc_group1", "oc_group2"],
      requireMention: false,
      // Bot responds without @ in allowed groups only
    }
  }
}
```

**Pros**: Selective — only allowed groups, but no @ needed in those groups.
**Cons**: Must manually add each group ID to `groupAllowFrom`.

### Method 3: Per-Group Override

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      requireMention: true,  // Default: require @
      groupAllowFrom: ["oc_consulting_group"],
      groups: {
        oc_consulting_group: {
          requireMention: false,  // Override: no @ needed in this group
        }
      }
    }
  }
}
```

**Pros**: Maximum control — different behavior per group.
**Cons**: Most config to maintain.

### Recommendation

For most consulting scenarios, **Method 1 or 2** is sufficient. Use Method 3 only if you have groups where the bot should stay silent unless @mentioned.

## Delivery Workflow

### Setting Up

1. **Create the Feishu group** — Name it after the consulting topic (e.g., "抖音运营咨询群")
2. **Add the Agent bot** — Add your OpenClaw Agent's Feishu bot to the group
3. **Configure no-@ reply** — Apply one of the methods above
4. **Test** — Send a message in the group, verify the bot responds without @
5. **Send a few test questions** — Verify answers are accurate and within scope

### Client Onboarding

1. Client completes payment
2. Invite client to the Feishu group
3. Send a welcome message explaining how to use the service
4. Client starts asking questions — Agent responds automatically

### Operational Tips

- **Pin a welcome message** explaining what the Agent can help with and its limitations
- **Monitor periodically** — Check that the Agent isn't giving wrong answers
- **Set expectations** — Let clients know the Agent may search for information and that complex questions may take a moment
- **Have a human escalation path** — For questions the Agent can't handle, have a way for clients to reach you directly
