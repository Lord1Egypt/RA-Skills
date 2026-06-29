# Pi Skills Reference

Pi implements the [Agent Skills standard](https://agentskills.io/specification) with progressive, on-demand loading.

## Locations

```
~/.pi/agent/skills/        # global
~/.agents/skills/          # global (generic)
.pi/skills/                # project
.agents/skills/            # project (ancestor traversal to git root)
```

- All locations recursively discover SKILL.md directories; `.pi/skills/` and `~/.pi/agent/skills/` additionally discover root .md files
- `--no-skills` disables discovery (`--skill <path>` still loads)
- Share other harness skills: `"skills": ["~/.claude/skills", "~/.codex/skills"]`

## How It Works

1. On startup, scan all locations, extract name + description
2. System prompt includes an XML list of available skills
3. Agent loads full SKILL.md on demand via `read` (progressive loading)
4. Agent follows instructions to use relative paths for scripts/references/assets

## Skill Commands

`/skill:name` or `/skill:name args` — force-load and execute.

## SKILL.md Format

```markdown
---
name: my-skill
description: What this does and when the agent should use it.
license: MIT
compatibility: Requires Node 20+
allowed-tools: read bash write
disable-model-invocation: false
---

# My Skill
## Usage
./scripts/process.sh <input>
```

### Frontmatter

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | 1-64 chars, lowercase/numbers/hyphens |
| `description` | ✅ | ≤1024 chars, basis for trigger decisions |
| `license` | | License |
| `compatibility` | | ≤500 chars |
| `metadata` | | Arbitrary key-value |
| `allowed-tools` | | Pre-approved tools (experimental) |
| `disable-model-invocation` | | `true` = only triggered via `/skill:name` |

The description is what the agent uses to decide when to load — be specific, not generic. Pi allows name to differ from directory name (unlike the standard, for shared skill directory compatibility).

### Validation

- Most violations are warnings only, still load
- Missing `description` → not loaded at all
- Name conflicts → first discovered wins

## Directory Structure

```
my-skill/
├── SKILL.md          # required
├── scripts/          # helper scripts
├── references/       # detailed references (loaded on demand)
└── assets/           # templates/assets
```

## Skill Repositories

- [Anthropic Skills](https://github.com/anthropics/skills) - document processing, web development
- [Pi Skills](https://github.com/badlogic/pi-skills) - web search, browser automation, Google APIs, transcription