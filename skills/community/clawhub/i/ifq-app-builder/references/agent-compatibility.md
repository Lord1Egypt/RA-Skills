# Agent Compatibility

How to register `ifq-app-builder` with each host.

## Codex CLI

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/peixl/ifq-app-builder ~/.codex/skills/ifq-app-builder
```

Codex auto-loads `SKILL.md` and surfaces examples from `agents/openai.yaml`. Invoke with `$ifq-app-builder` or natural language ("做一个 Mac 工具…").

## Claude Code

Workspace-level:
```bash
mkdir -p .claude/skills
git clone https://github.com/peixl/ifq-app-builder .claude/skills/ifq-app-builder
```

User-level: clone under `~/.claude/skills/ifq-app-builder/`.

Claude Code loads `SKILL.md` automatically when its `description` matches the user's intent.

## Cursor / OpenCode

Reference from workspace `AGENTS.md`:

```markdown
## Skills
- ifq-app-builder: ~/Documents/skills/ifq-app-builder/SKILL.md
```

## GitHub Copilot (VS Code agent customization)

This skill is compatible with VS Code's agent-customization layer. Place under one of:

- `.github/copilot/skills/ifq-app-builder/SKILL.md` (workspace)
- VS Code user prompts folder: `<userDir>/skills/ifq-app-builder/SKILL.md`

The front-matter `description` field is the trigger Copilot uses for routing.

## OpenClaw / ClawHub

`SKILL.md` front-matter already contains `metadata.openclaw` and `metadata.clawhub` blocks:

```bash
openclaw skill install peixl/ifq-app-builder
clawhub install peixl/ifq-app-builder
```

No env vars required; `requires.bins` lists only `node`.

## Hermes

`metadata.hermes` carries category + tags. The Hermes loader reads the same front-matter.

## Generic AgentSkills (`agentskills.io/v1`)

Front-matter declares `metadata.agentskills.standard = "agentskills.io/v1"`. Any compliant host can load this skill by reading `SKILL.md` alone.

## Verifying registration

After installing into any host:

1. Ask the agent "list available skills" — `ifq-app-builder` should appear.
2. Ask "用 ifq-app-builder 做一个 Mac 工具，把 PDF 转 Excel" — the agent should route to A-01, fork `pc-tauri.prompt.md`, and produce a bundle.
3. Run `npm run verify:lite -- <bundle>` against the produced file.

If any step fails, file an issue with the host name + error trace.
