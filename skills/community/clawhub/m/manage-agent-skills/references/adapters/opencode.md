# OpenCode (v1.1.1 adapter; checked 2026-10-23)

CLI platform: `opencode`.

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

## Operational notes

`--platform opencode` manages exact `permission.skill` rules;
enable is `allow`, disable is `deny`. Other permissions are preserved, and exact
rules follow existing wildcard rules. Select `--opencode-config` explicitly for
JSONC. Project/per-agent/tool controls may still override the selected file.
