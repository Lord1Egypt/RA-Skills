# CLI Wrapper Skill — Eval Template

For skills that wrap command-line tools (weather, gh, 1password, etc.)

## Quick Start (3 steps)

1. **Copy to your skill's evals directory**:
   ```bash
   cp -r templates/cli-wrapper/ evals/your-skill/
   ```

2. **Replace placeholders in both JSON files**:
   - `<tool-name>` → your tool name (e.g., `gh`, `op`, `wttr`)
   - `<command>` → common command (e.g., `gh pr list`, `op read`)
   - `<common-task>` → what users typically ask for (e.g., "list PRs", "get password")
   - `<goal>` → user goal (e.g., "manage GitHub issues", "access my vault")
   - `<similar-tool>` → a related but different tool (e.g., `gitlab` for `gh`)

3. **Run eval**:
   ```
   evaluate your-skill
   ```

## Files

| File | Purpose |
|------|---------|
| `triggers.json` | Tests if agent reads SKILL.md at the right times |
| `quality.json` | Tests if skill improves output quality |

## Customization Tips

### triggers.json

- **Add 2-3 more positive_direct** queries using your tool's actual command syntax
- **Critical: Add negative_similar** queries for tools users might confuse with yours
- Keep 60% positive / 40% negative ratio

### quality.json

- **Replace assertions** with your tool's expected behavior
- **Add error scenarios** specific to your tool (auth failures, network errors)
- Each eval should have 3-5 assertions, at least 1 marked `"priority": true`

## Example: Customizing for `gh` skill

**triggers.json**:
```json
{"id": 1, "query": "List my open pull requests", "expected": true, "category": "positive_direct"}
{"id": 6, "query": "Show GitLab merge requests", "expected": false, "category": "negative_similar"}
```

**quality.json**:
```json
{
  "id": 1,
  "prompt": "List PRs that need my review",
  "assertions": [
    {"id": "a1", "description": "Uses gh pr list command", "type": "output_contains", "value": "gh pr list"}
  ]
}
```
