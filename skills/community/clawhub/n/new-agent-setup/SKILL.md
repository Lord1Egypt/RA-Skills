---
name: new-agent-setup
description: Set up a new OpenClaw agent from scratch. Use when Tom asks to create, add, or onboard a new agent. Covers everything: gathering requirements, Discord bot setup, openclaw.json configuration, Mission Control registration, heartbeat, cron, OneDrive access, and final verification.
---

# New Agent Setup

Full step-by-step checklist: read `references/checklist.md` in this skill folder.

## Quick Overview (4 Phases)

**Phase 1 — Gather information first (do not start config without these):**
- Agent Name (capitalized, e.g. "Saul") → ID is lowercase ("saul")
- Role / domain
- Emoji for identity
- Discord Bot Token + Application ID (from developer.discord.com)
- Discord Channel ID (after channel is created by Tom)

**Phase 2 — Manual steps by Tom (before any config):**
- Create Discord bot in Developer Portal, invite to server
- Create Discord channel (lowercase agent name), move to "Agent Direct Lines" category
- Sync permissions with category, add bot user with all permissions set to Allow
- Prepare avatar image: `avatar-<agent-id>.png` (transparent background)

**Ask Tom before Phase 3:**
- Should this agent have OneDrive access? Which libraries?

**Phase 3 — Configuration (only after Tom confirms Phase 2 is done):**
1. Backup `openclaw.json`
2. Add agent to `agents.list[]` with identity + heartbeat block
3. Add Discord account + channel routing + agent routing
4. Gateway restart
5. `mc register <agent-id> --role "<role>"`
6. Create `HEARTBEAT.md` with mc workflow (never leave empty!)
7. Add staggered cron job for `mc checkin` (check existing slots first)
8. If OneDrive: `mkdir workspace-<id>/onedrive` + symlinks per library
9. Save session key to `MEMORY.md`
10. Send onboarding message via `sessions_send` (timeoutSeconds: 30)

**Phase 4 — Verify:**
- `mc fleet` shows new agent
- Gateway status OK
- Crontab correct
- HEARTBEAT.md not empty
- OneDrive symlinks work + agent created own subfolder
- Tom can see file on his laptop
- Avatar copied to workspace

## Key Rules
- Name: "Walt" → ID: "walt" → workspace: `workspace-walt` → avatar: `avatar-walt.png`
- Heartbeat: once ANY agent has a `heartbeat` block, ALL agents need one explicitly
- Cron slots: gus=0, walt=1, jesse=2, skyler=3, mike=4 → next agent gets minute 5
- OneDrive symlink points to `~/.openclaw/onedrive/<library>` (not `~/OneDrive/`)
- Never start config before Tom confirms Discord is set up
