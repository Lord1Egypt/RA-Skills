# Migration Guide: v2.x to v3.0

## What Changed

v3.0 adds **topic-based working memory** as the primary organizational layer.
The time-based hierarchy (daily/weekly/monthly/yearly) is preserved as an
optional archival layer.

| v2.x | v3.0 |
|------|------|
| MEMORY.md as lean index | MEMORY.md as routing table (same concept, clearer rules) |
| daily/ as primary intake | daily/ as intake (unchanged) |
| weekly/monthly/yearly as main distillation path | weekly/monthly/yearly as optional archival layer |
| No topic files | topics/ as primary working memory |
| No contact files | contacts/ for people information |

## What's Preserved

- All existing `memory/daily/` files — untouched
- All existing `memory/weekly/` files — untouched
- All existing `memory/monthly/` files — untouched
- All existing `memory/yearly/` files — untouched
- Existing `memory/sessions/` files — untouched
- Existing MEMORY.md — preserved, but may be refactored with user approval

## Migration Steps

### Automatic (agent-performed with user approval)

1. **Scan MEMORY.md** for project entries, contact references, and
   infrastructure details
2. **Propose topic files** for each active project or workstream found
3. **Propose contact files** for each person referenced
4. **Show migration plan** to user before executing
5. **Refactor MEMORY.md** into a routing table with pointers to new files
6. **Create topic and contact files** with content extracted from MEMORY.md

### Manual

If the user prefers to handle migration themselves:

1. Create `memory/topics/` directory
2. For each active project, create `memory/topics/<project-name>.md`
3. Move project-specific content from MEMORY.md to the topic file
4. Replace MEMORY.md content with one-line pointers to topic files
5. Repeat for contacts if desired

## Rollback

If the migration doesn't work out:

- Topic and contact files can be deleted without affecting anything
- MEMORY.md can be restored from git history
- The time-based layers are completely independent and unaffected
- To revert to v2.x behavior, set `preset: "minimal"` and `time_layers: true`

## Configuration for v2.x Parity

To get the exact same behavior as v2.x with no new features:

```json
{
  "memory_structure": {
    "preset": "minimal",
    "time_layers": true,
    "distillation": {
      "weekly": { "enabled": true },
      "monthly": { "enabled": true },
      "yearly": { "enabled": true }
    }
  }
}
```

This gives you daily/weekly/monthly/yearly without topics or contacts.
