---
name: obsidian-wiki
description: "Work with Rodion's Obsidian vault via Nextcloud. Handle ingest/query/lint for Karpathy wiki pattern. Triggers: add to wiki, ingest, wiki, knowledge base"
metadata:
  openclaw:
    os: ["linux"]
    requires:
      bins: ["docker"]
      config: ["nextcloud.path", "nextcloud.container"]
---

# Obsidian Wiki

## Vault
```
/home/rodrigo/services/nextcloud/data/admin/files/Obsidian/
```

## Sync After Changes
```bash
docker exec nextcloud php occ files:scan admin --path="/admin/files/Obsidian" -q
```
See [sync.md](references/sync.md)

## Wiki Structure
See [wiki-structure.md](references/wiki-structure.md)

## Operations
See [operations.md](references/operations.md)

## Quick Reference

| Action | Command |
|--------|---------|
| Read file | `cat <path>` |
| Create page | `write <path>` |
| Sync | `docker exec nextcloud php occ files:scan...` |
| List notes | `ls *.md` |

## Log Format
```
## [YYYY-MM-DD] type | Description
- Created: wiki/summaries/...
```
