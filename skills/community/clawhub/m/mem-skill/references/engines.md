# Memory Engine Architecture

mem-skill uses a pluggable memory engine architecture. The engine determines how knowledge and experience entries are indexed, searched, and retrieved.

## Engine Interface

Every memory engine must support these operations:

| Operation    | Description                                      |
|-------------|--------------------------------------------------|
| `init`      | Set up storage, indexes, and configuration       |
| `search`    | Find relevant entries by keywords or query        |
| `read`      | Load a specific knowledge or experience file      |
| `write`     | Store a new entry and update the index            |
| `sync`      | Re-index after writes (if applicable)             |

## Available Engines

### `default` — JSON/Markdown Index

- **How it works**: Simple keyword matching against `_index.json` files, plain Markdown storage.
- **Pros**: Zero dependencies, human-readable, instant startup.
- **Cons**: No semantic search, linear scan on keywords.
- **Init command**: `/mem-skill init`
- **Config**:
  ```json
  { "engine": "default", "version": "1.0.0" }
  ```

### `qmd` — QMD Semantic Search

- **How it works**: Uses [QMD](https://github.com/tobi/qmd) for BM25 + vector + LLM re-ranking search over Markdown files.
- **Pros**: Semantic/fuzzy search, hybrid ranking, MCP server support, scales to large knowledge bases.
- **Cons**: Requires Node.js >= 22, ~2GB model cache, heavier setup.
- **Init command**: `/mem-skill init --mem-engine=qmd`
- **Config**:
  ```json
  {
    "engine": "qmd",
    "version": "1.0.0",
    "scope": "project",
    "mask": "**/*.md",
    "collections": {
      "knowledge": "<user-chosen-name>",
      "experience": "<user-chosen-name>"
    }
  }
  ```
  The `scope` field records whether collections are project-scoped or global.
  The `mask` field records the file glob pattern used for indexing.
  Collection names are chosen by the user during init (or via `--qmd-*` flags).
- **Detailed reference**: See [qmd-engine.md](qmd-engine.md)

## Adding a New Engine

To add a new memory engine (e.g., `sqlite-fts`, `chroma`, `pinecone`):

1. Create a new reference file: `references/<engine-name>-engine.md`.
2. Document the engine's setup, search commands, write/sync flow, and requirements.
3. Update this file to add the engine to the "Available Engines" table.
4. In `SKILL.md`, add engine-specific branches in the Init, Step 3 (Experience Read), Step 4 (Knowledge Read), and Step 5 (Post-Write Sync) sections.
5. The `/mem-skill init --mem-engine=<engine-name>` command should:
   - Create the standard `knowledge-base/` and `experience/` directories.
   - Perform engine-specific setup (install dependencies, create indexes, etc.).
   - Write `.mem-skill.config.json` with `"engine": "<engine-name>"`.

### Design Principles for New Engines

- **Markdown is the source of truth**: All engines read from the same `knowledge-base/*.md` and `experience/*.md` files. Engines add indexing on top, they do not replace the files.
- **Graceful fallback**: If the engine becomes unavailable (e.g., QMD not installed), fall back to the default JSON index engine.
- **Prompt for dependencies**: During init, check for required tools and prompt the user to install missing ones before proceeding.
- **Consistent config**: Always write `.mem-skill.config.json` with the engine name and engine-specific settings.
