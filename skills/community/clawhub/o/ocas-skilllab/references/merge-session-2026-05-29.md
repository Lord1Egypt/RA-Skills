# Skill Library Management — Session Notes

## Auto-Generated Skill Detection (May 29 2026)

**Mistake:** Only checked top-level `author:` and `metadata.author:` for auto-generated skills.
**Lesson:** Also check `metadata.hermes.generated_by`.

Full scan command:
```bash
grep -r "generated_by" ~/.hermes/skills/
```

Skills found and deleted: `deployment`, `delegate-task`, `skill-view`,
`mcp-google-workspace-get-gmail-messages-content-batch`,
`mcp-google-workspace-read-resource`, `mcp-google-workspace-search-custom`,
`mcp-mempalace-mempalace-kg-timeline`.

## Author Field Locations

When auditing skills for authorship, check BOTH:
1. Top-level `author:` in YAML frontmatter
2. Nested `metadata:` → `author:` — this is where the agent's skills store it

Example of nested (the agent's pattern):
```yaml
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "2.8.7"
```

## Merge Session (May 29 2026)

### Skills Merged or Renamed

| Source | Target | Action |
|--------|--------|--------|
| `git-operations` | `util-github` | Merged: basic workflow, stash, undo, errors, pitfalls → Part 1 |
| `util-amazon-history` | `util-buy` | Merged: 3 scripts + order history section → Part 5 |
| `deployment` | DELETED | auto-generated |
| `delegate-task` | DELETED | auto-generated |
| `skill-view` | DELETED | auto-generated |
| `mcp-google-workspace-*` | DELETED (4) | auto-generated |
| `headhunter` | `util-headhunter` | Renamed + moved to top-level + author fixed |
| `iamwrite` | `util-iamwrite` | Renamed + moved to top-level + author added |

### Rules Established
- `util-*` prefix = utilities authored by the agent
- `ocas-*` prefix = OCAS family
- Overlapping utilities → merge into the broader one
- After merge: delete source dir, add `metadata.merged-from: <name>` to target
- Update all references (cron jobs, SOUL.md, memory, skill frontmatter)

## Post-Merge Cleanup Checklist

1. Update cron job prompts referencing old skill names/paths
2. Update MEMORY.md entries referencing old skill names
3. Verify YAML frontmatter after edits
<<<<<<< Updated upstream
4. Check for doubled author fields (replace-all can double already-correct values like `Indigo Karasu (indigokarasu)` → `Indigo Karasu (indigokarasu) (indigokarasu)`)
=======
4. Check for doubled author fields (replace-all can double already-correct values like `<agent-name> (<agent-handle>)` → `<agent-name> (<agent-handle>) (<agent-handle>)`)
>>>>>>> Stashed changes
