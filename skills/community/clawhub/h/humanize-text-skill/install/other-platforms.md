# Install on Other Platforms

`humanize-text-skill` works on any agent runtime that supports the agentskills.io `SKILL.md` format.

## Files you need

- `SKILL.md`
- `references/`
- `policy/`
- `detector/` if you want the local engine available

Do not omit `policy/`. The detector loads `policy/*.toml` at runtime, and
voice analysis should fail loudly when that directory is missing.

## Cursor

Use [`../cursor-rules/humanize-text-skill.mdc`](../cursor-rules/humanize-text-skill.mdc).

## Codex, OpenClaw, Hermes, and similar runtimes

Point the runtime at the repository root or copy the required files into that runtime's skill directory.

## Packaged layouts

| Path | Purpose |
|---|---|
| `plugins/humanize-text-skill/` | Plugin packaging |
| `cursor-rules/humanize-text-skill.mdc` | Cursor rule port |
| `detector/` | Zero-dependency engine |
