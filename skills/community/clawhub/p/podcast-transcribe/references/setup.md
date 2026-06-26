# Setup

This file is for installation and platform-specific activation details. It is not needed for routine transcription runs.

## Claude Code

Project-local install:

```bash
npx skills add dairui1/podcast-helper --skill transcribe
```

Global install:

```bash
npx skills add dairui1/podcast-helper --skill transcribe -g
```

Manual install from a local checkout:

```bash
mkdir -p ~/.claude/skills
cp -R skills/transcribe ~/.claude/skills/transcribe
```

Optional reminder hook:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'podcast-helper transcribe'; then echo 'Transcription complete; ask whether cleanup is needed.'; fi"
          }
        ]
      }
    ]
  }
}
```

## OpenClaw

Recommended install:

```bash
clawdhub install dairui1/podcast-helper --skill transcribe
```

Manual install from a local checkout:

```bash
mkdir -p ~/.openclaw/skills
cp -R skills/transcribe ~/.openclaw/skills/transcribe
```

## Other Agents

For agents that do not auto-load `SKILL.md`, add a short pointer in `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

```markdown
Use podcast-helper for podcast transcription:
- `npx podcast-helper transcribe <input> --output-dir <dir> --json`
- ask before cleanup
- see `skills/transcribe/SKILL.md` for workflow details
```
