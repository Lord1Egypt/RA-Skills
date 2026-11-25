# Platform adapter index

Read only the guide for the management target; execution host may differ.
Python 3.11+ and PyYAML are required.

| Host | Discovery / write scope | Control | Evidence boundary |
| --- | --- | --- | --- |
| Codex | User/shared, project `.agents/skills`, plugin caches; selected TOML | Managed `[[skills.config]]` | Paths are publicly documented; name mode is host-dependent. Cache presence is not an authoritative installed-plugin registry. |
| Claude Code | Personal and ancestor project `.claude/skills`, one directory deep; selected user JSON by default | `skillOverrides` | Does not merge managed/local/project settings or implement plugin/bundled controls. |
| Copilot CLI | Native inventory, otherwise filesystem fallback including `COPILOT_HOME/skills`; selected JSONC | `disabledSkills` | Repository disable lists can further restrict user state. |
| OpenClaw | Native inventory or workspace/user/shared fallback | Native `config set` | Requires installed CLI for mutation; eligibility and agent allowlists remain host decisions. |
| Hermes | `$HERMES_HOME/skills`; selected YAML | Global/per-platform disable lists | External skill directories, profiles, environment/app gates are not fully enumerated. |
| Antigravity App/IDE | Selected global `~/.gemini/config/skills` | Directory parking | Workspace, legacy IDE and plugin roots are not managed. |
| Antigravity CLI | `--antigravity-surface cli`: `~/.gemini/antigravity-cli/skills` | Directory parking | Plugin controls belong to `agy plugin`; older releases may use different paths. |
| Gemini CLI (v1.1.1) | Local user/workspace/shared roots; selected JSON/JSONC | `skills.disabled` | Built-in, extension and other settings layers are not merged. |
| OpenCode (v1.1.1) | Global/project/compatible roots; selected JSON/JSONC | `permission.skill` allow/deny | Remote, inline, per-agent and other layers are not merged. |


## Guides

- [codex](adapters/codex.md)
- [claude](adapters/claude.md)
- [copilot](adapters/copilot.md)
- [openclaw](adapters/openclaw.md)
- [hermes](adapters/hermes.md)
- [antigravity](adapters/antigravity.md)
- [gemini](adapters/gemini.md)
- [opencode](adapters/opencode.md)

Unknown target: [Add a platform adapter](add-platform.md).
