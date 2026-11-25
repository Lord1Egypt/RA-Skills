# Claude Code

CLI platform: `claude`.

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

## Desktop and synced copies

`doctor` and `audit` additionally read `~/.claude/skills/synced/**/SKILL.md`.
Use repeatable `--claude-desktop-root <absolute-skills-plugin-directory>` before
`doctor` or `audit` to inspect Desktop copies, including nested account/session
folders. Pass the actual observed `Claude-Data/.../skills-plugin` directory.
These diagnostic roots never enter search/enable/disable/preset target discovery.
Snapshots have unknown activation; duplicate identity does not prove all copies
are active. Older manager versions, unknown versions and missing scripts are
reported per path; no snapshot is changed. Symlink aliases are deduplicated.

Desktop's private cache location varies by installation and is not an official
stable discovery contract, so automatic whole-AppData/home scanning is deliberately
unsupported. Explicit roots allow bounded read-only diagnosis without guessing.
Official references: [Claude skills](https://code.claude.com/docs/en/skills),
[custom skill upload](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
The [official synced-skills contract](https://code.claude.com/docs/en/skills#names-reserved-for-synced-skills) reserves `anthropic-skills` for claude.ai sync, not authorship. Synced bodies treat dynamic commands, @ imports and placeholders differently by surface; use explicit reads of relative reference links.

The local adapter cannot manage account-hosted skills. Use the host UI for that scope. A cloud shell does not establish access to the user computer; Desktop Code uses this adapter only when local execution is confirmed.

## Operational notes

`enable` / `disable` map to `on` / `off`. Use `set name-only`
to keep discoverability with less description text, or `set user-invocable-only`
for manual invocation. Target directory keys printed by `search`. Only the
selected settings file is written; project, managed, frontmatter and plugin
controls can affect the actual host result.
