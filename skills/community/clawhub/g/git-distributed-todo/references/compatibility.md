# Runtime compatibility

Read this file only when installing or adapting `git-distributed-todo` to an agent host.

## Portable contract

The skill requires only:

1. A runtime that can load or follow `SKILL.md` instructions.
2. Shell/command execution.
3. Git.
4. Python 3.10+.

The Python CLI is the source of truth for task state transitions. Host-specific schedulers and messaging systems are only adapters around `due` and `mark-notified`.

## Hermes Agent

Install the skill through Hermes Skills/Skills Hub or place it in the configured Hermes skills location. Let Hermes invoke `scripts/git_todo.py` through its terminal tools. Use one Hermes cron job only when this Hermes instance is the designated notifier.

Recommended one-time init on each host (non-interactive works from an agent):

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" setup \
  --repo ~/shared-todo --agent <this-host-id> --remote <shared-remote-url>
```

`setup` records the agent id in `.git-distributed-todo.json`, so Hermes can run later commands without `AGENT_TODO_ID` being set. The env vars in the main instructions are optional overrides; if you use them, put them where the Hermes process reads them at startup (e.g. `~/.hermes/.env`), not only in a shell profile — non-interactive agent terminals do not source `.zshrc`.

## OpenClaw

Place the skill directory under an OpenClaw skills root, for example `~/.openclaw/workspace/skills/git-distributed-todo`. OpenClaw resolves `{baseDir}` to the directory containing the active skill; map the conceptual `SKILL_DIR` in the main instructions to `{baseDir}`.

Verify discovery with `openclaw skills list`. Schedule reminder polling only on the designated notifier agent.

## ChatGPT / Codex

Use the standard Agent Skills directory/package form: `SKILL.md` plus `scripts/` and `references/`. The host must provide local/shell execution for the bundled CLI. Resolve the active skill directory from the path supplied by the runtime rather than hardcoding a machine-specific path.

## Tencent WorkBuddy / CodeBuddy

Use the product's custom Skill/Skill Marketplace flow. Keep this `SKILL.md` and bundled script together when importing or adapting the skill. CodeBuddy-compatible environments expose the skill directory as `${CODEBUDDY_SKILL_DIR}`; map the conceptual `SKILL_DIR` to that directory. If the WorkBuddy version generates additional YAML metadata, keep that host metadata as an adapter and do not duplicate task logic there.

## Other agents

For any agent capable of reading Agent Skills or executing shell commands, install this directory as a skill or provide `SKILL.md` as persistent instructions. Resolve the skill directory, configure `AGENT_TODO_REPO` and `AGENT_TODO_ID`, and call the same Python CLI.

If a runtime cannot execute local commands, it cannot directly operate this version of the skill. Use an MCP/tool wrapper around `git_todo.py` rather than reimplementing the state machine.
