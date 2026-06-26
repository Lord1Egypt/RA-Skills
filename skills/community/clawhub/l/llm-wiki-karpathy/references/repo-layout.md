# Repository Layout

This skill works best when the knowledge base stays easy to browse for both humans and agents, and when the runtime owns the canonical write boundaries.

## Default Layout

```text
<vault>/
  raw/
    inbox/
    web/
    notes/
    papers/
    repos/
    datasets/
    images/
  wiki/
    sources/
    outputs/
    concepts/
    entities/
    syntheses/
    _indexes/
    index.md
    log.md
  .llm-kb/
    manifest.json
    runs.jsonl
```

## Folder Contract

- `raw/`: source-of-truth artifacts captured from the outside world. Preserve filenames, provenance, and local assets. Runtime support is currently centered on `.md` and `.txt` raw files.
- `wiki/sources/`: one source page per raw source, written only through the runtime.
- `wiki/outputs/`: archived answers that preserve the original question context.
- `wiki/concepts/`: durable concept pages for reusable ideas or frameworks.
- `wiki/entities/`: durable pages for named systems, people, organizations, tools, methods, or datasets.
- `wiki/syntheses/`: cross-source pages for tradeoffs, comparisons, theses, and higher-order analysis.
- `wiki/_indexes/`: generated collection indexes such as `sources.md`, `outputs.md`, `concepts.md`, `entities.md`, and `syntheses.md`.
- `wiki/index.md`: generated wiki home page.
- `wiki/log.md`: generated run log page.
- `.llm-kb/manifest.json`: canonical mapping of raw files to source notes and hashes.
- `.llm-kb/runs.jsonl`: append-only run log for audit and generated `wiki/log.md`.

## Recommended Page Shapes

### Source Page

Store source pages in `wiki/sources/` with the runtime-issued `doc_id`.

Required headings:

- `Summary`
- `Key Points`
- `Evidence`
- `Open Questions`
- `Related Links`

Required frontmatter:

- `id`
- `type: source`
- `title`
- `raw_path`
- `raw_hash`
- `source_kind`
- `tags`
- `created_at`
- `updated_at`
- `status`

### Output Page

Store question-specific answer archives in `wiki/outputs/`.

Required headings:

- `Answer`
- `Sources Used`
- `Follow-up Questions`

Required frontmatter:

- `id`
- `type: output`
- `title`
- `query`
- `source_refs`
- `created_at`
- `updated_at`

### Concept Page

Use `wiki/concepts/` for reusable ideas that recur across source notes and answers.

Required headings:

- `Summary`
- `Definition`
- `Key Points`
- `Evidence`
- `Open Questions`
- `Related Notes`

### Entity Page

Use `wiki/entities/` for named things that deserve durable context.

Required headings:

- `Summary`
- `Who or What`
- `Key Facts`
- `Evidence`
- `Open Questions`
- `Related Notes`

### Synthesis Page

Use `wiki/syntheses/` for cross-source analysis and tradeoff pages.

Required headings:

- `Summary`
- `Thesis`
- `Supporting Evidence`
- `Tensions`
- `Open Questions`
- `Related Notes`

### Derived Frontmatter

For `concept`, `entity`, and `synthesis`, include:

- `id`
- `type`
- `title`
- `aliases`
- `source_refs`
- `tags`
- `created_at`
- `updated_at`
- `status`

## Naming

- source notes: `wiki/sources/src-<slug>.md`
- outputs: `wiki/outputs/YYYY-MM-DD-<slug>.md`
- concepts: `wiki/concepts/concept-<slug>.md`
- entities: `wiki/entities/entity-<slug>.md`
- syntheses: `wiki/syntheses/synthesis-<slug>.md`

## Growth Rule

Start with these page kinds and let the wiki earn more structure gradually.

Good growth:

- promote repeated ideas into `concept` pages
- promote repeated named items into `entity` pages
- promote recurring cross-source reasoning into `synthesis` pages

Bad growth:

- inventing a huge taxonomy before the wiki needs it
- creating many directories with no durable workflow behind them
- archiving every thought as an `output` when it should really become a reusable wiki page
