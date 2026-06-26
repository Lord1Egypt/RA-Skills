# OpenClaw Notes

This skill is designed to be portable, but it also includes small OpenClaw-specific niceties.

## Install location

OpenClaw loads skills from these locations, in precedence order:

1. `<workspace>/skills`
2. `~/.openclaw/skills`
3. bundled skills

Practical recommendation: put this skill in the current workspace if you want it to override a shared copy.

## Environment injection

OpenClaw can inject environment variables for a single agent run through `skills.entries.<skill-name>.env`.

Example `~/.openclaw/openclaw.json` snippet:

```json5
{
  skills: {
    entries: {
      "meta-ads-control": {
        enabled: true,
        env: {
          META_ACCESS_TOKEN: "YOUR_TOKEN_HERE",
          META_AD_ACCOUNT_ID: "act_1234567890",
          META_API_VERSION: "v25.0"
        }
      }
    }
  }
}
```

If you prefer a provider-backed secret flow, use the mechanism your OpenClaw deployment supports for secret references, then map it into `META_ACCESS_TOKEN`.

## Session behaviour

OpenClaw snapshots eligible skills for the session. After changing `SKILL.md` or skill config, start a new session or rely on the skills watcher to refresh before the next turn.

## Sandboxing

If the agent runs inside a sandbox, `python3` must exist **inside the sandbox** as well as on the host. This skill requires outbound HTTPS access to `graph.facebook.com`.

## Security

Treat the token like a production credential:

- inject it via environment or secret config, not directly in the prompt,
- do not echo it in logs,
- do not write it into working files,
- rotate it if you suspect it leaked.

The skill itself follows a live-safety model:

- read before write,
- dry-run before confirm,
- default new delivery objects to paused,
- verify after mutations.
