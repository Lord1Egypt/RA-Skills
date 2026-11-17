---
name: manage-agent-skills
description: Find installed skills by task or description, including disabled skills, and enable exact matches when requested. Audit and manage skill visibility on Codex, Claude Code, Copilot CLI, OpenClaw, Hermes, Antigravity, Gemini CLI, and OpenCode. Use when users need a skill, cannot find one, or want fewer active skills. Does not install skills or measure actual token savings.
metadata:
  version: "1.1.1"
---

# Manage Agent Skills

Use `scripts/skillctl.py` for on-demand discovery and scoped changes. Resolve
this skill's directory first; use `python` or `python3` available on the host.
PyYAML is required for safe metadata parsing. Never start a watcher.

## Choose the workflow

- **Inventory:** `--platform all status --json` reports configured state.
- **Diagnose:** `--platform all audit --json` reports malformed metadata,
  duplicate identities, configuration layers, and compatibility limitations.
  `audit --strict` returns nonzero for warnings as well as errors. It does not
  decide whether arbitrary skill instructions are factually up to date.
- **Find:** `--platform <host> search <query> --report --json` searches names,
  descriptions, groups and paths, including disabled skills. Use short task
  keywords; all space-separated words must match. Results are ranked and limited
  to 20; `--limit 5` reduces output. Mutations remain exact.
- **Fast repeat lookup:** `index --output <new-private-file.json>` exports metadata;
  `search <query> --index <file> --report --json` avoids host calls. This is a dated
  snapshot; rebuild after installations/updates. It cannot authorize mutations.
- **Check activation:** `--platform <host> inspect <exact-selector> --json`
  previews enablement and reports refresh guidance without writing.
- **Change:** resolve the requested scope, preview with `--dry-run`, then apply
  the same command. Existing user authorization is sufficient; do not ask for
  confirmation again solely because a preview completed.
- **Repeat a profile:** read [references/presets.md](references/presets.md).
- **Check host/version compatibility:** read
  [references/platforms.md](references/platforms.md), including its evidence
  dates and limits. Do not infer current host support from a cache directory.

```powershell
$skillctl = "<skill-directory>/scripts/skillctl.py"
python $skillctl --platform all audit --json
python $skillctl --platform codex search deploy
python $skillctl --platform codex disable deploy --dry-run
python $skillctl --platform codex disable deploy
```

Put global options before the command; `--json` also works after it.
Mutations require one explicit platform. Supported selectors are exact name,
`group:<name>`, `path:<native-absolute-path>`, and `all`. Quote selectors with
spaces. Names can match multiple installed copies: review every target.

Unknown names fail by default. Only use `--allow-undiscovered` for an explicitly
requested literal host key on Copilot/OpenClaw/Hermes; it is not typo correction.
Groups normally identify discovery sources. A `--groups file.json` can define
user taxonomy; never infer groups from skill names without that file.

## On-demand activation

When a user needs installed expertise, search short task keywords first. If the
user's language differs from metadata, also search translated keywords; optional
`--aliases file.json` supplies explicit word-to-synonym arrays. Read only the
top matching descriptions, not every SKILL.md. Do not call lexical matching semantic search.

Select the exact host and path/key from results. If multiple skills fit, compare
their descriptions and scope before choosing. Inspect and preview the exact
target. Enable when the user has requested using/enabling that capability; a
search-only request does not authorize a configuration change. Stop on blocked
results and report the reason rather than enabling an entire plugin or weakening
another policy. Follow returned refresh guidance and verify with the host's
native listing/invocation before claiming the skill is usable in this session.
If a restart is required, state that boundary. The manager does not restart hosts.

Keep this small management entry discoverable when using a lean skill profile.
Implicit invocation is allowed in Codex; this does not guarantee host selection
or zero metadata cost. Search errors are isolated by platform; partial results
return nonzero, so inspect `errors` instead of treating the catalog as complete.

## Data and process scope

Discovery reads skill metadata and the selected host settings needed to report
skill state. It does not search unrelated files or inspect config values for
credentials. Backups of host settings may contain secrets and must remain
private. The OpenClaw child CLI receives only `PATH`, OS home/temp/runtime paths,
documented OpenClaw path/profile variables, and the selected
`OPENCLAW_CONFIG_PATH`; arbitrary process variables such as provider API tokens
are not forwarded. Host CLIs still run with the current OS user's permissions;
this skill does not sandbox them.

## Host-specific decisions

**Codex:** default writes documented path rules. Existing name rules are
preserved. Use `--codex-selector name` only when the exact host build has been
verified to support name selectors. In that explicit mode, `reconcile`
converts managed plugin paths into stable names; default reconcile preserves
paths. Enabling cannot override a disable outside the manager's block.
Re-scan after a plugin update; path rules may refer to an old version.

**Claude Code:** `enable` / `disable` map to `on` / `off`. Use `set name-only`
to keep discoverability with less description text, or `set user-invocable-only`
for manual invocation. Target directory keys printed by `search`. Only the
selected settings file is written; project, managed, frontmatter and plugin
controls can affect the actual host result.

**Copilot / OpenClaw / Hermes:** use their native configuration semantics.
OpenClaw requires its CLI for writes. Hermes `--hermes-scope telegram` targets
a platform list; global disables still win. Its essential `hermes-agent` skill
cannot be disabled, even with `--force`.

**Gemini CLI:** `--platform gemini` manages `skills.disabled` in user settings;
`--gemini-scope workspace` selects `<cwd>/.gemini/settings.json`. Local workspace,
user and shared roots are indexed. Built-in/extension skills and other settings
layers require host verification. A global `skills.enabled=false` blocks enable.

**OpenCode:** `--platform opencode` manages exact `permission.skill` rules;
enable is `allow`, disable is `deny`. Other permissions are preserved, and exact
rules follow existing wildcard rules. Select `--opencode-config` explicitly for
JSONC. Project/per-agent/tool controls may still override the selected file.

**Antigravity:** select the surface explicitly when managing CLI skills:

```text
<python> <skillctl> --platform antigravity --antigravity-surface cli status
<python> <skillctl> --platform antigravity --antigravity-surface app disable demo --dry-run
```

App/IDE defaults to `~/.gemini/config`; current CLI defaults to
`~/.gemini/antigravity-cli`. `--antigravity-config` overrides either root.
This adapter parks whole global skill directories in sibling `skills_disabled`;
explain that move in the preview. It does not manage workspace/plugin copies.
Do not equate a parked directory with verified absence from a prompt.

## Recovery and reporting

- Keep installed files unchanged, except the documented Antigravity directory
  moves. Never overwrite a parked directory or silently recover a failed move.
- Configuration writes preserve unrelated values. JSONC/YAML formatting can
  normalize. The first backup is `.manage-agent-skills.bak`; later backups have
  unique suffixes. Use the exact returned backup path for recovery.
- Protected authoring/management skills require explicit `--force` to disable.
  Do not add it automatically to make a bulk operation succeed.
- Presets preflight all actions; runtime failures may still leave partial
  changes. Native OpenClaw batches are not transactional. Stop, inspect current
  state and report recovery evidence before retrying.
- Report platform/surface, targets, configured scope, changes, backup/move paths,
  and restart guidance. Distinguish preview, saved configuration, and live host
  verification. Do not claim measured context savings from local state alone.
- `doctor` / `status` continue past a broken adapter and return nonzero. Treat
  zero discovered skills on an errored adapter as unknown, not an empty host.

See [references/auditing.md](references/auditing.md) for compatibility review,
exit codes, recovery, and a safe upgrade validation procedure.
