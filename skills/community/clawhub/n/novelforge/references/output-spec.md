# Output contract

The project root is user-selected. The following paths are the machine-facing
contract; human-facing names and Markdown layout may be added beside them.

```text
<project>/
├── index.md                      # generated wiki index with [[wikilinks]]
├── outline.md                    # master story outline
├── blueprints/<chapter-id>.md    # chapter blueprint (YAML frontmatter + scene plan)
├── chapters/<chapter-id>.md      # chapter text draft
├── characters/<id>.md            # character profile (YAML frontmatter + bio)
├── locations/<id>.md             # location setting
├── items/<id>.md                 # item / artifact setting
├── factions/<id>.md              # faction setting
├── hooks/<id>.md                 # hook / foreshadowing setting
├── timeline/<id>.md              # event / chronicle setting
├── entities/<id>.md              # general entity setting
└── .novelforge/                  # machine-facing state & audit ledgers
    ├── state/project.json
    ├── state/chapters/<chapter-id>.json
    ├── context/<chapter-id>.json
    ├── reviews/<chapter-id>-text.json
    ├── reviews/<chapter-id>-engine.json
    ├── settlements/<chapter-id>.json
    ├── wiki-manifest.json
    ├── engines/<engine-id>/
    ├── locks/*.lock
    └── audit.jsonl
```

## File rules

- Direct novel settings, blueprints, and chapters reside directly in root creation directories as Markdown documents with YAML frontmatter. No duplicate JSON projection is used.
- `.novelforge/` strictly stores machine states, context tickets, reviews, settlement receipts, and audit logs in JSON/JSONL format for reliable script processing.
- IDs are path-safe, stable, and unique within their collection.
- JSON is UTF-8, deterministic, and written atomically by the scripts.
- Text and Markdown are plain UTF-8.
- The source chapter is authoritative for prose; the Settlement is authoritative
  for accepted facts and changes.
- The Wiki manifest (`.novelforge/wiki-manifest.json`) validates markdown file hashes and index integrity; delivery fails when the files are inconsistent or stale.

## Chapter order

```text
blueprint validate
  → context build
  → draft + chapter transition DRAFTED
  → text review PASS
  → engine review PASS
  → settlement apply
  → wiki rebuild
  → chapter transition DELIVERABLE
```

Every command returns non-zero on failure. A failed or stale artifact must be
recreated; hand-editing a state file is not a recovery path.
