# Antigravity

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


## Operational notes

select the surface explicitly when managing CLI skills:

```text
<python> <skillctl> --platform antigravity --antigravity-surface cli status
<python> <skillctl> --platform antigravity --antigravity-surface app disable demo --dry-run
```

App/IDE defaults to `~/.gemini/config`; current CLI defaults to
`~/.gemini/antigravity-cli`. `--antigravity-config` overrides either root.
This adapter parks whole global skill directories in sibling `skills_disabled`;
explain that move in the preview. It does not manage workspace/plugin copies.
Do not equate a parked directory with verified absence from a prompt.
