# agentskills.io Spec Compliance Checklist

Reference for auditing skills against the agentskills.io specification.
Source: https://agentskills.io/specification

## Required Fields

- [ ] `name` present
- [ ] `name` ≤ 64 characters
- [ ] `name` matches directory name
- [ ] `name` only contains `[a-z0-9-]`
- [ ] `name` does not start or end with `-`
- [ ] `name` does not contain `--` (consecutive hyphens)
- [ ] `description` present
- [ ] `description` ≤ 1024 characters
- [ ] `description` is non-empty and descriptive
- [ ] `description` includes trigger keywords for agent activation

## Recommended Fields

- [ ] `license` present (even `Proprietary` or `MIT` is valid)
- [ ] `metadata.version` present (conventional but not required)

## Hermes Extensions to Remove for Cross-Platform Publishing

These fields are valid in Hermes but NOT in the agentskills.io spec:

| Field | Action |
|-------|--------|
| `metadata.hermes` | Remove entirely |
| `metadata.email` | Remove or relocate to `metadata.author` |
| `metadata.openclaw` | Remove (legacy alias) |
| `metadata.requires` | Remove (Hermes-specific) |
| Top-level `version` | Move to `metadata.version` |
| Top-level `email` | Remove |
| Top-level `platforms` | Replace with `compatibility` field |
| `self_update` | Remove (non-standard top-level field) |
| `metadata.git_source` | Remove (internal tracking) |
| `metadata.skill_source` | Remove (internal tracking) |

## Directory Checklist

- [ ] `SKILL.md` exists at skill root
- [ ] Scripts in `scripts/` (not at root)
- [ ] Reference docs in `references/` (not at root)
- [ ] Templates/static resources in `assets/` or `templates/`
- [ ] LICENSE file present (for publishing)

## Body Content Checklist

- [ ] SKILL.md body under 500 lines
- [ ] Detailed content split into `references/` files
- [ ] File references use relative paths: `references/FILE.md`
- [ ] No deeply nested reference chains (max 1 level from SKILL.md)

## Validation Command

```bash
# If skills-ref is available:
skills-ref validate ./skill-name
```

## Quick Python Audit Script

```python
import yaml, pathlib, re

def audit_skill(skill_path):
    content = pathlib.Path(skill_path, 'SKILL.md').read_text()
    parts = content.split('---')
    if len(parts) < 3:
        return ['INVALID: no closing ---']
    
    fm = yaml.safe_load(parts[1])
    issues = []
    
    # Name checks
    name = fm.get('name', '')
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        issues.append(f'name format invalid: {name}')
    if len(name) > 64:
        issues.append(f'name too long: {len(name)}')
    
    # Description checks
    desc = fm.get('description', '')
    if len(desc) > 1024:
        issues.append(f'description too long: {len(desc)}')
    
    # Non-standard fields
    nonstandard = {'version', 'email', 'platforms'}
    for field in nonstandard:
        if field in fm:
            issues.append(f'non-standard top-level field: {field}')
    
    if 'hermes' in fm.get('metadata', {}):
        issues.append('metadata.hermes is Hermes extension')
    
    if 'license' not in fm:
        issues.append('missing license field')
    
    return issues
```

## Audit Results from OCAS Skills (2026-06-09)

All 29 OCAS skills pass with zero spec failures.
Warnings (non-blocking): missing `license`, `metadata.hermes` extension, `metadata.email`, non-standard top-level `version` (ocas-reach), `self_update` (ocas-finch).
See session notes for full breakdown.

## Nous Research Optional Skills — Additional Requirements

Source: https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog

Skills submitted to the Nous Research optional-skills catalog have additional requirements beyond the base agentskills.io spec:

### Description
- **≤ 60 characters, one sentence, ends with a period.** This is a hard limit enforced by reviewers.
- State the capability, not the implementation.
- No marketing words ("powerful", "comprehensive", "seamless", "advanced").
- Don't repeat the skill name in the description.

### Author Field
- **Credit the human contributor first**: `Author Name (github-handle)`.
- If the contributor used Hermes to draft the skill, replace "Hermes Agent" in git history with the contributor's actual name.
- **NEVER use the agent owner's name/email without explicit permission.** Default to the contributor's identity or a neutral attribution.

### Platform Gating
- Skills using POSIX-only primitives (`fcntl`, `termios`, `/proc`, `os.setsid`, `signal.SIGKILL`, hardcoded `/tmp` paths, `osascript`, `apt`, `systemctl`) **must** declare `platforms: [linux]` or `platforms: [macos]` in frontmatter.
- Default posture: fix cross-platform first. Gate only when the dependency is genuinely platform-bound.

### Section Order (Modern)
```
# <Skill> Skill
Intro (what it does, what it doesn't — 2-3 sentences max)

## When to Use
## Prerequisites
## How to Run
## Quick Reference
## Procedure
## Pitfalls
## Verification
```

### Target Length
- ~100 lines for a simple skill
- ~200 lines for a complex skill
- Cut redundant intro fluff and marketing prose

### Tests
- Required at `tests/skills/test_<skill>_skill.py`
- Use only stdlib + pytest + `unittest.mock`
- No live network calls
- Run via `scripts/run_tests.sh tests/skills/test_<skill>_skill.py -q`

### Do NOT Submit
- Skills with external dependencies (unless absolutely necessary — prefer stdlib)
- Skills that duplicate existing bundled skills
- Skills that are too narrow/specialized (better suited for Skills Hub)