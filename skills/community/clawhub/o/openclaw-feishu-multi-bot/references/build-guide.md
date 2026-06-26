# Build Guide: Feishu Multi-Bot Setup

## Prerequisites

- OpenClaw installed and gateway running
- At least one Agent already working via Feishu (your main agent)
- Access to [Feishu Developer Console](https://open.feishu.cn/app)
- Admin rights on your Feishu organization

## Phase 1: Plan Your Bot Roster

Before touching any config, decide:

1. **How many Agents need independent Feishu bots?** Not every agent needs one — sub-agents that only run in the background don't need direct user access.
2. **Which agent is the orchestrator?** This is usually your existing main agent.
3. **Group structure**: Which bots go in which Feishu groups?

Example roster:

| Agent ID | Feishu Bot Name | accountId | Groups |
|----------|----------------|-----------|--------|
| main | 总调度 | orchestrator-bot | All groups |
| content-writer | 写作助手 | writer-bot | Content group |
| code-expert | 开发助手 | coder-bot | Dev group |
| analyst | 数据分析 | analyst-bot | Analytics group |

## Phase 2: Create Feishu Apps

For each agent that needs a bot:

1. Go to [open.feishu.cn/app](https://open.feishu.cn/app)
2. Click "Create Custom App" (创建企业自建应用)
3. Set the app name (this becomes the bot's display name in Feishu)
4. Upload an avatar (make each bot visually distinct)
5. Under "Capabilities" (应用能力), enable **Bot** (机器人)
6. Under "Event Subscriptions" (事件订阅), configure as needed
7. Record the **AppID** (`cli_xxx...`) and **AppSecret**
8. **Publish the app** (发布应用) — draft apps cannot receive messages

Repeat for all agents. You should now have N apps with N pairs of AppID/AppSecret.

## Phase 3: Generate Configuration

Use the setup script:

```bash
./scripts/setup-feishu-bots.sh \
  orchestrator:cli_orch_id:orch_secret \
  content-writer:cli_writer_id:writer_secret \
  code-expert:cli_coder_id:coder_secret \
  analyst:cli_analyst_id:analyst_secret
```

This outputs three JSON blocks. Or build manually — see `references/architecture.md` for the full structure.

## Phase 4: Edit openclaw.json

Merge the three generated blocks into your existing `openclaw.json`:

1. Add all accounts under `channels.feishu.accounts`
2. Add all route bindings to `bindings[]`
3. Add all agents to `agents.list`
4. Update the orchestrator's `allowAgents` to include all spawnable agent IDs

**Tip**: After editing, validate JSON syntax before restarting:
```bash
python3 -c "import json; json.load(open('openclaw.json'))"
```

## Phase 5: Create Agent Workspaces

Each agent needs its own workspace directory with at minimum an AGENTS.md:

```bash
mkdir -p ~/.openclaw/workspace-{agent-id}
# Write AGENTS.md with role definition
# Write TOOLS.md with tool reminders
```

If using the symlink pattern (shared OUTPUT/KNOWLEDGE), create symlinks:
```bash
ln -s /absolute/path/to/primary-workspace/OUTPUT ~/.openclaw/workspace-{agent-id}/OUTPUT
```

## Phase 6: Validate and Restart

```bash
# Check configuration health
openclaw doctor

# Auto-fix known issues
openclaw doctor --fix

# Full restart (kill existing + start fresh)
openclaw gateway restart

# Verify all agents registered
openclaw agents list --bindings
```

## Phase 7: Smoke Test

Test each bot independently:

| Test | Expected |
|------|----------|
| DM each bot in Feishu | Each responds with its own identity |
| Add bot to its assigned group | Bot is visible as group member |
| Send message in group @bot | Correct agent processes the message |
| Orchestrator spawns sub-agent | Announce returns to orchestrator's channel |

## Phase 8: Incremental Rollout

Do not deploy all bots simultaneously. Recommended sequence:

1. **Day 1**: Orchestrator bot only (your existing main agent)
2. **Day 2**: Add 1 specialist bot, verify routing works
3. **Day 3**: Add remaining bots one by one
4. **Day 4**: Test group isolation and spawn workflows

Each addition: edit openclaw.json → restart gateway → test → confirm → next.
