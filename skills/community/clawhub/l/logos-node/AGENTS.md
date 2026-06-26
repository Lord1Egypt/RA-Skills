# ai-integrations — logos-node branch

This branch contains the Logos Blockchain node operator skill for AI agents.

## What's in this branch

```
skill/
├── SKILL.md               # Main wizard (AgentSkills standard)
├── install-procedure.md   # Fresh node installation steps
├── update-procedure.md    # Breaking upgrade steps
├── sharp-edges.md         # Known operational gotchas
└── status-checks.md       # Health-check commands and interpretation

mcp/
└── README.md              # Future RAG/MCP integration notes

.claude-plugin/
└── plugin.json            # Claude Code plugin metadata

install.sh                 # Bash installer (no npm required)
```

## Agent roles

When working with this skill as a subagent, follow this workflow order:

1. **research** — Before modifying any procedure file, verify the current
   [Logos release notes](https://github.com/logos-blockchain/logos-blockchain/releases/latest).
   Do not invent endpoints, peer IDs, or version numbers.

2. **executor** — Perform node operations conservatively. Log exact commands,
   paths, and outcomes. Never skip a checklist step.

3. **review** — After changes, verify: path correctness, no hardcoded versions
   that should be dynamic, no secrets committed, rollback steps present.

## Updating this skill

When Logos releases a new version:

1. Check if it is a breaking release
2. If breaking: update `update-procedure.md` checklist and `sharp-edges.md`
3. Do NOT hardcode bootstrap peers in procedure files — they come from GitHub API at runtime
4. The `SKILL.md` dynamic fetch already handles new binary/circuits URLs automatically

## Other networks (other branches)

- `main` — npm installer `@citizenweb3/ai-integrations`
- `darkfi-node` — DarkFi node skill (planned)
- `genlayer-node` — GenLayer node skill (planned)
