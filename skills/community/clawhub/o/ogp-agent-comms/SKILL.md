---
skill_name: ogp-agent-comms
version: 0.6.0
description: Interactive wizard to configure agent-to-agent communication policies (updated for multi-framework `--for` workflows, OGP 0.2.24+ peer identity, and 0.2.28+ multi-agent routing)
trigger: Use when the user wants to configure how their agent responds to incoming agent-comms messages from federated peers
---
## Prerequisites

The OGP daemon must be installed. If you see errors like 'ogp: command not found', install it first:

```bash
npm install -g @dp-pcs/ogp
ogp-install-skills
ogp setup
ogp agent-comms interview
ogp config show
```

Full documentation: https://github.com/dp-pcs/ogp



# OGP Agent-Comms Configuration

This skill is an interactive wizard for configuring how your agent handles incoming agent-comms messages from federated peers.

## When to Use

Use this skill when:
- User wants to set up agent-to-agent communication policies
- User wants to configure what topics their agent can discuss with peers
- User wants different policies for different peers
- User says things like "configure agent comms", "set up agent communication", "how should my agent respond to X"

## Overview

Agent-comms policies control HOW your agent responds to incoming messages (separate from scope grants which control WHETHER messages are allowed).

**Two layers:**
1. **Scope grants** (doorman) - Controls which intents/topics are ALLOWED
2. **Response policies** (this skill) - Controls HOW your agent RESPONDS
3. **Human delivery preferences** - Controls WHERE and WHEN your agent surfaces federated requests back to the human

**Important default:** when a federation request is approved, OGP auto-enables the `general` topic for that peer. Everything else still needs explicit policy if the user wants something more restrictive or more open.

**Multi-Agent Routing (v0.2.28+):**
When using `notifyTargets` in your OGP config, federation messages can be routed to specific agents based on the message context. Each agent can have its own agent-comms policies.

**Human delivery behavior (v0.4.2+):**
Use `humanDeliveryTarget` plus `inboundFederationPolicy.mode` to tell the agent whether it should forward everything, summarize, act autonomously, or wait for approval before replying.

OGP now evaluates delegated-authority rules—global defaults, per-peer overrides, message-class-specific rules (`agent-work`, `human-relay`, `approval-request`, `status-update`), and topic overrides—before finalizing delivery behavior. This determines whether the agent may reply directly or must escalate to the configured human session. On OpenClaw, `/hooks/agent` is the preferred delivery path; it tries to request the actual human session key only when `hooks.allowRequestSessionKey=true` and the requested key matches configured prefixes. When the flag is false, the hook runs in the default session (`agent:main:main`), so Telegram sender identity continues to appear as injected/system/`cli`, which is the accepted `v0.4.2` limitation documented in the README and changelog. Lifecycle events such as federation approvals now surface through these same hook-driven turns, so humans see the lifecycle update without needing to poll another channel.

On OpenClaw, human-facing federated work should be handled through the platform's hook-driven agent turn (`/hooks/agent`). Direct `sessions.send` injection is a lower-level fallback or sync mechanism, not the primary behavioral path.

**Multi-Framework note:** Policies are framework-local. Use `ogp --for openclaw ...` for OpenClaw state and `ogp --for hermes ...` for Hermes state.

## Interactive Flow

When invoked, guide the user through this flow:

### Step 1: Check Prerequisites

```bash
# Verify OGP is running and has peers
ogp config show
ogp --for openclaw status
ogp --for openclaw federation list --status approved
```

If no approved peers, inform the user they need to federate first.

### Step 2: Re-run the Delegated-Authority Interview First

When the user is configuring overall human-delivery or autonomy behavior, start with the canonical interview command instead of approximating it manually:

```bash
ogp --for openclaw agent-comms interview
```

Use the Hermes variant when the active framework is Hermes:

```bash
ogp --for hermes agent-comms interview
```

This command updates:
- `humanDeliveryTarget` when the framework supports it
- `inboundFederationPolicy.mode`
- delegated-authority defaults for human surfacing, relay handling, approval-required topics, and trusted-peer autonomy

After the interview, continue with per-peer or per-topic policy commands only if the user wants something more specific.

### Step 3: Show Current Configuration

```bash
# Show current policies
ogp --for openclaw agent-comms policies
```

### Step 4: Ask What to Configure

Present options:
1. **Global defaults** - Apply to all peers (current and future)
2. **Specific peer(s)** - Configure individual peers
3. **View current policies** - Just show what's configured

### Step 5: For Specific Peers - Multi-Select

If configuring specific peers, show the list and allow multi-select:

Use the peer list from:

```bash
ogp --for openclaw federation list --status approved
```

Prefer the peer ID shown in the list. Some commands also accept a display-name match, but the peer ID is the safest input.

Example interaction:
```
Select peers to configure:
  [x] Stanislav (302a300506032b65)
  [ ] Leonardo (5f8b2c...)
  [x] Alice (9d4e1f...)

Selected: Stanislav, Alice
```

### Step 6: Configure Topics

Ask which topics the agent should engage on:

```
Which topics should your agent discuss with these peers?
  [x] memory-management
  [x] testing
  [x] general
  [ ] calendar (add custom)
  [ ] personal (add custom)

Add custom topic: _______
```

### Step 6: Configure Response Level

For each topic (or all topics), set the response level:

| Level | Behavior |
|-------|----------|
| `full` | Respond openly, share details |
| `summary` | High-level responses only, no specifics |
| `escalate` | Ask human before responding |
| `deny` | Politely decline to discuss |
| `off` | Block the topic entirely |

### Step 7: Save Configuration

```bash
# Save policies for selected peers
ogp --for openclaw agent-comms configure <peer-id> \
  --topics "memory-management,testing,general" \
  --level full

# Or set global defaults
ogp --for openclaw agent-comms configure --global \
  --topics "general,testing" \
  --level summary
```

### Step 8: Confirm and Show Result

```bash
# Show the updated configuration
ogp --for openclaw agent-comms policies <peer-id>
```

## CLI Commands

### View All Policies

```bash
ogp --for openclaw agent-comms policies
```

Shows global defaults and per-peer overrides.

### View Peer Policy

```bash
ogp --for openclaw agent-comms policies 302a300506032b65
```

Shows effective policy for a specific peer (global + overrides).

### Configure Global Defaults

```bash
ogp --for openclaw agent-comms configure --global \
  --topics "general,testing" \
  --level summary \
  --notes "Default: be helpful but don't overshare"
```

### Configure Specific Peer

```bash
ogp --for openclaw agent-comms configure <peer-id> \
  --topics "memory-management,testing,general" \
  --level full \
  --notes "Stan is a trusted collaborator"
```

### Configure Multiple Peers at Once

```bash
ogp --for openclaw agent-comms configure 302a300506032b65,5f8b2c,9d4e1f \
  --topics "testing" \
  --level full
```

**Note:** Prefer peer IDs. Partial peer IDs or display-name matches may work, but peer IDs are canonical.

### Add Topic to Existing Policy

```bash
ogp --for openclaw agent-comms add-topic <peer-id> calendar --level escalate
```

### Remove Topic

```bash
ogp --for openclaw agent-comms remove-topic <peer-id> personal
```

### Reset to Global Defaults

```bash
ogp --for openclaw agent-comms reset <peer-id>
```

## Policy Inheritance

1. **Global defaults** apply to all peers
2. **Per-peer policies** override globals for that peer  
3. **Topic-level settings** are the most specific

Example:
```
Global: { "general": "summary", "testing": "full" }
Stan (302a300506032b65):   { "memory-management": "full" }

Effective for Stan:
  - general: summary (from global)
  - testing: full (from global)
  - memory-management: full (from Stan-specific)
```

## Response Policy Schema

Stored in the active framework's `peers.json` under each peer:

```json
{
  "id": "302a300506032b65",
  "alias": "Stanislav",
  "responsePolicy": {
    "memory-management": {
      "level": "full",
      "notes": "Stan is working on similar architecture"
    },
    "testing": {
      "level": "full"
    },
    "calendar": {
      "level": "escalate",
      "notes": "Ask me before sharing schedule"
    }
  }
}
```

**Note:** The `alias` field (formerly `petname`) is stored with the peer, but agent-comms commands should still prefer the peer ID shown by `ogp federation list`.

Global defaults live in the active framework config, for example `~/.ogp/config.json` or `~/.ogp-hermes/config.json`:

```json
{
  "humanDeliveryTarget": "telegram:123456789",
  "inboundFederationPolicy": {
    "mode": "summarize"
  },
  "agentComms": {
    "globalPolicy": {
      "general": { "level": "summary" },
      "testing": { "level": "full" }
    },
    "defaultLevel": "summary",
    "activityLog": true
  },
  "notifyTargets": {
    "main": "telegram:123456789",
    "scribe": "telegram:987654321"
  }
}
```

## How Your Agent Uses These Policies

When an agent-comms message arrives:

1. **Doorman** checks if the intent/topic is allowed (scope grants)
2. **Your agent** receives the message via the local platform backend
3. **Your agent** looks up the response policy:
   - Check peer-specific policy for this topic
   - Fall back to global policy for this topic
   - Fall back to defaultLevel
4. **Your agent** responds according to the level:
   - `full`: Engage openly
   - `summary`: Brief, high-level response
   - `escalate`: "Let me check with my human and get back to you"
   - `deny`: "I'm not able to discuss that topic"

**OpenClaw delivery path:** OGP should hand human-facing federated work to OpenClaw through `/hooks/agent`, letting the agent run a real turn and deliver via the configured human channel. A compact `sessions.send` note may still be used to keep session state synchronized, but that is secondary.

**Multi-Agent Routing:** When `notifyTargets` is configured, messages are routed to the appropriate agent who then applies their own policies.

**Human Delivery:** When `humanDeliveryTarget` is configured, the agent should treat "tell my human X" as a delivery obligation to that configured channel, not merely as something to mention in whatever session happens to be active.

## Activity Logging

When enabled, all agent-comms interactions are logged:

```bash
# View activity log
ogp --for openclaw agent-comms activity

# View for specific peer
ogp --for openclaw agent-comms activity <peer-id>

# View last N entries
ogp --for openclaw agent-comms activity --last 20
```

Log format:
```
2026-03-23 11:52:14 [IN]  Stanislav → testing: Hello from Stan!
2026-03-23 11:52:15 [OUT] → Stanislav: Hi Stan! Test received successfully.
2026-03-23 11:55:22 [IN]  Leonardo → calendar: What's David's availability?
2026-03-23 11:55:23 [OUT] → Leonardo: [ESCALATED] Checking with David...
```

## Example Configurations

### Trusted Collaborator (Full Access)

```bash
ogp --for openclaw agent-comms configure 302a300506032b65 \
  --topics "memory-management,testing,general,code-review" \
  --level full \
  --notes "Trusted peer, full collaboration"
```

### Business Contact (Limited)

```bash
ogp --for openclaw agent-comms configure 5f8b2c... \
  --topics "general,status-updates" \
  --level summary \
  --notes "Professional contact, keep it high-level"
```

### New Federation (Cautious)

```bash
ogp --for openclaw agent-comms configure --global \
  --topics "general,testing" \
  --level escalate \
  --notes "Default: check with human for new peers"
```

### Human Delivery Modes

These now have a first-class CLI interview via `ogp agent-comms interview`, and they remain part of the same operational policy:

- `forward` — forward all inbound federated requests/replies to the human
- `summarize` — summarize and escalate only important/actionable items
- `autonomous` — act independently unless blocked or explicitly told to relay something
- `approval-required` — do not act or reply until the human approves

Make the user's intent explicit during setup and documentation. Examples:

- "Tell me everything that comes in from peers."
- "Summarize most things, but escalate if you need me."
- "Act on your own unless you are blocked."
- "Never reply to a peer without clearing it with me first."

### Multi-Agent Setup

With `notifyTargets` configured in `~/.ogp/config.json`:

```json
{
  "notifyTargets": {
    "main": "telegram:123456789",
    "scribe": "telegram:987654321"
  }
}
```

Each agent can have independent policies. The main agent might have full access for operational topics, while the scribe agent handles content-related discussions.

## Troubleshooting

### Agent not following policies

1. Verify the policy is saved:
   ```bash
   ogp --for openclaw agent-comms policies <peer-id>
   ```

2. Check if the topic is in scope grants (doorman):
   ```bash
   ogp --for openclaw federation scopes <peer-id>
   ```

3. Restart daemon to reload config:
   ```bash
   ogp --for openclaw stop && ogp --for openclaw start --background
   ```

### Policy not taking effect for new peer

New peers inherit global defaults. Configure them specifically:
```bash
ogp --for openclaw agent-comms configure 302a300506032b65 --topics "..." --level "..."
```

### Multi-Agent Routing Issues

If notifications aren't reaching the right agent:
1. Check `notifyTargets` and `humanDeliveryTarget` in the active framework config
2. Verify the target format: `telegram:chat_id` or a raw session key like `agent:main:telegram:direct:<chat-id>`
3. For OpenClaw, verify hooks are enabled and the hook token is present
4. For OpenClaw Gateway RPC debugging, use `wss://localhost:18789` against a TLS-enabled local gateway, not `ws://`
5. Remember that a successful direct session injection is not the same thing as the agent correctly handling a human-delivery obligation
