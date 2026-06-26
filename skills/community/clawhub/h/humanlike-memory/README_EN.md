# Human-Like Memory Skill for OpenClaw

An agent-usable memory skill for OpenClaw.

This skill is intentionally scoped for smart-trigger use:

- the agent may call recall/save when memory is useful
- no every-turn automatic recall
- no hook-level silent background saves
- no direct reads from `~/.openclaw/secrets.json`
- configuration comes from OpenClaw config or injected environment variables

If you want always-on memory automation, use the Human-Like Memory plugin instead of this skill.

[中文文档](README.md)

## Network Behavior

This skill only talks to the remote memory service when the agent or user invokes it:

- `recall` / `search` sends the query plus `user_id` and `agent_id`
- `save` / `save-batch` sends the message content you explicitly pass in
- runtime reads only the documented allowlisted `HUMAN_LIKE_MEM_*` environment variables

Default endpoint: `https://plugin.human-like.me`

## Installation

```bash
openclaw skills install human-like-memory
```

## Configuration

Get your `mp_xxx` API key from [plugin.human-like.me](https://plugin.human-like.me), then set it manually:

```bash
openclaw config set skills.entries.human-like-memory.enabled true --strict-json
openclaw config set skills.entries.human-like-memory.apiKey "mp_your_key_here"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_BASE_URL "https://plugin.human-like.me"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_USER_ID "openclaw-user"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AGENT_ID "main"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_RECALL_ENABLED "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_SAVE_TRIGGER_TURNS "5"
```

If the user explicitly provides the API key in the current session, the agent may run those commands on the user's behalf. Otherwise, keep configuration as a manual user step.

Verify:

```bash
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs config
```

## Usage

This skill is intended for smart agent invocation plus optional explicit user invocation.

Use it when you want the model to decide memory is useful, but you do not want always-on hook-based automation.

```bash
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs recall "what projects am I working on"
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs search "naming preference"
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs save "I prefer UTC+8 timestamps" "Understood"
echo '[{"role":"user","content":"Hi"},{"role":"assistant","content":"Hello"}]' | node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs save-batch
```

## Typical Memory Tasks

- Resume project context, decisions, and open work from prior sessions
- Recall user preferences, naming habits, identity facts, and long-lived constraints
- Reuse stable workflows, playbooks, checklists, and other procedural memory
- Search memory before answering continuity-heavy questions
- Save durable conclusions, corrections, and summaries for later sessions

## Memory Types

- Semantic memory: facts, preferences, identity, and durable context
- Procedural memory: workflows, routines, checklists, and repeatable ways of working
- Episodic memory: prior exchanges, project history, and session-specific decisions

## Suggested Queries And Saves

- Recall: `"roadmap decisions from last week"`
- Search: `"what name preference did I mention"`
- Save: `"I prefer UTC+8 timestamps"`

## Good Things To Save

- Stable preferences
- Confirmed decisions
- Identity or background facts that affect future collaboration
- Corrections to earlier misunderstandings
- Summaries worth keeping after a multi-turn discussion

If a conversation produces a reusable workflow or checklist, it can also be saved as procedural memory.

## Error Handling

- If the API key is missing, the script prints fix commands you can run directly
- If the remote service times out or errors, nothing is saved silently
- If no memories are found, treat that as a normal empty result

## Skill vs Plugin

| Feature | Skill | Plugin |
|---------|-------|--------|
| Invocation | Explicit | Automatic lifecycle hook |
| Recall | Only when invoked | Can be automatic |
| Save | Only when invoked | Can be automatic |
| Network activity | Explicit and predictable | More automated |

Plugin package: <https://www.npmjs.com/package/@humanlikememory/human-like-mem>

## Security

See [SECURITY.md](./SECURITY.md) for the exact transmitted fields and operational model.

## License

Apache-2.0
