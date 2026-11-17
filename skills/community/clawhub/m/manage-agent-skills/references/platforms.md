# Platform contracts and evidence

Reviewed against primary sources on **2026-10-21**. Documentation checks do not
certify every installed host version. The adapter reports local configuration;
none of these adapters measures the current model prompt or actual token savings.

## Support matrix

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

All filesystem paths use the current OS's native rules. Use the absolute path
printed by `search`; paths are not translated between Windows, macOS and Linux.
Python 3.11+ and PyYAML are required. The CI matrix covers all three OSes, with
additional Python versions on Linux; configured CI is not proof of a completed run.

## Codex

The [skills guide](https://learn.chatgpt.com/docs/build-skills) demonstrates a
`SKILL.md` path, while the
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
describes a containing folder path. The manager recognizes both when reading,
and writes `SKILL.md` paths by default. Both documents specify `enabled`;
neither establishes portable `name` selector support.

`--codex-selector name` preserves the previous optional stable-name workflow
for a host verified to support it. It uses `plugin:skill` identities for cached
plugin skills. `reconcile` migrates managed plugin paths only in this mode.
It does not migrate external rules, remove installed files, or prove prompt
metadata exclusion. The legacy `CODEX_SKILL_MANAGER` block remains recognized.
Malformed managed markers and unsupported manager-owned entries fail closed.

Plugin activation is inferred from the selected config; inherited policy and
host defaults may differ. Multiple cache versions and marketplace replacement
heuristics are reported as inventory evidence, not authoritative host selection.
Read `audit` warnings before treating reported `on/off` as effective host state.

## Claude Code

[Skills](https://code.claude.com/docs/en/skills) documents these settings:

| Value | Catalog | Slash menu |
| --- | --- | --- |
| `on` | Name and description | Visible |
| `name-only` | Name | Visible |
| `user-invocable-only` | Hidden | Visible |
| `off` | Hidden | Hidden |

The adapter uses directory keys and accepts `user-only` as an alias. Its selected
settings file is only one layer. `audit` flags other project/local files rather
than guessing a merged result. Frontmatter invocation flags are a separate
host concern. Plugin skills require `/plugin`; bundled skills and legacy
commands are not discovered here. The host's `/skill-doctor` is the appropriate
source for actual usage/context statistics on versions that support it.

## GitHub Copilot CLI

The [configuration directory reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
documents `disabledSkills` and repository/user union semantics. Removing a user
entry does not cancel a repository disable. The adapter preserves unrelated
JSON values, but normalizes JSONC formatting after backing it up. Native
inventory is preferred when it returns usable JSON; fallback is less complete.

## OpenClaw

[Skills](https://docs.openclaw.ai/tools/skills) documents
`skills.entries.<key>.enabled`, optional `metadata.openclaw.skillKey`, gating
and allowlists. [Config CLI](https://docs.openclaw.ai/cli/config) is used for
writes, preserving native JSON5 handling. Filesystem fallback does not fully
parse JSON5, so unresolved state must remain unknown. A native batch can fail
after earlier commands succeed; the error reports completed commands and the
backup. Do not automatically retry an interrupted mutation.

## Hermes

The [native configuration implementation](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/skills_config.py)
and [skill utilities](https://github.com/NousResearch/hermes-agent/blob/main/agent/skill_utils.py)
confirm global union platform disable semantics and the essential `hermes-agent`
exception. The manager refuses to disable that essential skill even with force,
and excludes common cache and bundled support directories from inventory.
YAML formatting/comments may normalize; returned backups preserve original bytes.

Hermes also has external directories and runtime eligibility gates. This adapter
does not replicate the entire resolver; verify those surfaces with Hermes itself.

## Antigravity and Gemini CLI

[Antigravity skills](https://antigravity.google/docs/skills) now distinguishes
App/IDE and CLI global locations. This supersedes the old adapter's agy 1.2.11
assumption. The local audit observed agy 1.4.3; only version/help were executed.
Choose `--antigravity-surface app|cli`, or supply an explicit config directory
for a known legacy installation. The existing default remains `app` to avoid
silently changing the meaning of existing commands.

Parking is a manager convention, not a native disable API. The manager moves
only direct children of the selected roots, refuses redirected roots and
collisions, attempts batch rollback, and reports incomplete rollback honestly.
Workspace/plugin copies can remain active. No context visibility is claimed.

[Gemini CLI](https://geminicli.com/docs/cli/skills/) is a separate host with native
skill management and user/workspace scopes. Do not treat it as Antigravity.
Version 1.1.1 adds a separate Gemini adapter; v1.0.1 did not include it.
It discovers user/workspace `.gemini/skills` and `.agents/skills`, honors
`GEMINI_CLI_HOME`, and edits `skills.disabled` in one selected JSON/JSONC file.
`--gemini-scope workspace` uses `<cwd>/.gemini/settings.json`. Global
`skills.enabled=false` in that file blocks enable. Built-in/extension roots,
system configuration and trust gates are not replicated. Settings-file edits
require a restart according to the [configuration reference](https://geminicli.com/docs/reference/configuration/);
`/skills reload` alone is not evidence that an externally edited config was read.

## OpenCode (v1.1.1 adapter; checked 2026-10-23)

The [skills contract](https://opencode.ai/docs/skills/) and
[permissions reference](https://opencode.ai/docs/permissions/) define
`permission.skill` allow/deny/ask. The adapter manages exact names in one selected
config and preserves last-matching-rule order. `ask` is represented as unknown
invocability, not disabled. It discovers global/project skills and `.claude`/
`.agents` compatibility roots. `XDG_CONFIG_HOME`, `OPENCODE_CONFIG`, and the
`OPENCODE_CONFIG_DIR` skill root are honored. Select JSONC explicitly with
`--opencode-config`. Permission-wide string shorthand is refused rather than
rewritten; skill-only shorthand is safely retained as a wildcard default.
Remote, inline, managed, project and per-agent configuration may override this
selected layer. Local configuration is not live verification or version certification.

## Other surfaces

Claude Desktop/Cowork and account-hosted skill pools are outside these local
adapters. Manage them in their host UI. This is a current adapter boundary,
not a claim that future account APIs can never support management.
