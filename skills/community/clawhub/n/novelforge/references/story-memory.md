# File-backed story memory

The novel body, chapter blueprints, and direct story settings are organized directly
in the project root as native Markdown files with YAML frontmatter. Machine state and
execution evidence are stored under `.novelforge/` as deterministic JSON files for script
processing. There is no duplicate projection.

```text
<project>/
├── index.md                      # generated wiki index with [[wikilinks]]
├── outline.md                    # master story outline
├── blueprints/*.md               # chapter blueprints
├── chapters/*.md                 # chapter text drafts
├── characters/*.md               # character profiles (frontmatter + bio)
├── locations/*.md                # location settings
├── items/*.md                    # item & artifact settings
├── factions/*.md                 # faction & organization settings
├── hooks/*.md                    # hook & mystery tracking
├── timeline/*.md                 # chronicle & story events
├── entities/*.md                 # general entity settings
└── .novelforge/                  # machine state & review/audit ledgers
    ├── state/
    │   ├── project.json
    │   └── chapters/*.json
    ├── context/*.json
    ├── reviews/*.json
    ├── settlements/*.json
    ├── wiki-manifest.json
    ├── audit.jsonl
    └── locks/*.lock
```

## Context rules

Chapter blueprints must declare dependency IDs. `novelforgectl context build` loads
only those IDs and their explicitly allowed relationship edges deterministically,
avoiding probabilistic or fuzzy retrieval.

Every context ticket records the blueprint hash, dependency hashes, selected
engine card IDs, and a deterministic payload. A changed input invalidates the
ticket and all downstream chapter gates.

## Settlement rules

After both text and engine reviews pass, the writer submits a structured
settlement containing the chapter hash, events, entity changes, relationship
changes, knowledge changes, and hook changes. The script validates and applies
it idempotently, adding schema, an `applied` marker, and the exact text/engine
review hashes to the stored artifact. Facts are written directly into root creation
directories (`characters/`, `locations/`, `items/`, `hooks/`, `timeline/`, etc.)
as Markdown files with YAML frontmatter and Markdown body. Each written file records
the source chapter and body hash. A settlement with a different body hash is stale
and cannot be used for delivery. After the chapter is re-drafted and
re-reviewed, a stale settlement may be replaced; facts removed by that
replacement are deleted only when their file records the same source chapter.

The Wiki manifest records every page hash and the file set. Delivery validates
these hashes and the current non-stale source set, so manually writing an index
or reusing an old file cannot satisfy the final gate. A later Context Ticket
rejects a file whose owning chapter body or settlement no longer matches its
recorded source hash.
