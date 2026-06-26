# OpenClaw Weather Brief Skill

Local OpenClaw skill repository to be packaged and published.

This skill provides a concise spoken weather brief for a configured city,
including current conditions and a short recommendation for the day.

## Contents

- `SKILL.md` - skill manifest and package metadata
- `hooks/` - local lifecycle scripts used during packaging
- `assets/` - prompt snippets and icon assets
- `examples/` - sample invocation payloads

## Development

Run the prepare hook before packaging:

```bash
bash hooks/prepare.sh
```

Validate the manifest:

```bash
bash hooks/validate.sh
```

The prepare hook copies packaged assets into `build/` so the repository can be
published as a self-contained skill bundle.
