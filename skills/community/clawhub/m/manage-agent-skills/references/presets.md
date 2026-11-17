# Preset file format

Preset files are JSON and use exact selectors. The optional `groups` section
defines your own `group:<name>` taxonomy; pass the same file to `--groups` to
make those groups resolvable. Without it, groups are only the discovery
sources reported by `search`, which vary per machine and per host.

```json
{
  "version": 1,
  "groups": {
    "azure": ["azure-*", "entra-*"]
  },
  "presets": {
    "lean": {
      "codex": {
        "disable": ["group:azure", "group:gmail"],
        "enable": ["manage-agent-skills", "openai-docs"]
      },
      "claude": {
        "disable": ["legacy-context"],
        "enable": ["manage-agent-skills"]
      },
      "copilot": {
        "disable": ["unused-skill"],
        "enable": ["manage-agent-skills"]
      },
      "openclaw": {
        "disable": ["browser-tools"],
        "enable": ["manage-agent-skills"]
      },
      "hermes": {
        "disable": ["shell-tools"],
        "enable": ["manage-agent-skills"]
      }
    }
  }
}
```

Rules:

- Nothing is grouped by name out of the box. Group patterns are `fnmatch`
  style and are matched, case-insensitively, against the skill's display name,
  its host identifier, and its directory name.
- Platform keys are `codex`, `claude`, `copilot`, `openclaw`, `hermes`, `antigravity`, `gemini`, or `opencode`.
- Explicit enables win: overlapping disable targets are removed before any write.
  All remaining actions are preflighted before mutation. A later runtime failure
  can still leave partial changes; presets are not transactions. Unknown action
  keys are rejected to catch typos.
- Selectors are exact skill names, `group:<name>`, `path:<path>`, or `all`.
- A mutation requires the matching `--platform`; one invocation changes one
  platform.
- For Hermes, `--hermes-scope` applies to the entire preset invocation.
- Antigravity uses the selected `--antigravity-surface` or explicit root.
- Always preview with `--dry-run`.
