# Graphify API Reference

Complete reference for the `graphify` CLI (package `graphify`, v0.4.23+).

---

## Command Overview

```
graphify <target> [options]       Build or update a knowledge graph
graphify query "<question>"       Semantic search on the graph
graphify path "NodeA" "NodeB"     Shortest path between two nodes
graphify explain "NodeName"       Plain-language node explanation
graphify add <url>                Add external content to the graph
graphify <platform> install       Register with an AI assistant platform
graphify hook install             Install git post-commit rebuild hook
```

---

## Build Commands

### `graphify <target>`

Build a knowledge graph from a directory.

```bash
graphify .                    # current directory
graphify ./src                # specific subdirectory
graphify /absolute/path       # absolute path
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--mode deep` | Aggressive INFERRED edge extraction with confidence scores |
| `--update` | Reprocess only files changed since last run (uses SHA-256 cache) |
| `--directed` | Preserve edge directionality in the output graph |
| `--cluster-only` | Re-run Leiden community detection without re-extracting nodes/edges |
| `--no-viz` | Skip generating `graph.html` (faster; useful in CI) |
| `--watch` | Auto-sync graph as files change (requires `graphify[watch]`) |
| `--wiki` | Generate Wikipedia-style article per node |
| `--svg` | Export SVG visualization (requires `graphify[svg]`) |
| `--graphml` | Export GraphML file for Gephi / yEd |

**Extraction pipeline (in order):**
1. **AST extraction** — tree-sitter deterministic parsing; no LLM calls; produces `EXTRACTED` edges
2. **Transcription** — faster-whisper local audio/video processing; domain-aware prompts
3. **Semantic extraction** — parallel LLM subagents for docs, PDFs, images; produces `EXTRACTED` and `INFERRED` edges

---

## Query Commands

### `graphify query "<question>"`

Semantic natural-language search across the knowledge graph.

```bash
graphify query "where is rate limiting enforced?"
graphify query "what calls the payment processor?" --dfs
```

| Flag | Description |
|------|-------------|
| `--dfs` | Depth-first traversal; traces a specific execution path instead of ranking |

**Returns:** Ranked list of matching nodes with relationship context and source file references.

---

### `graphify path "NodeA" "NodeB"`

Find the shortest path between two named nodes in the graph.

```bash
graphify path "AuthMiddleware" "PostgresAdapter"
graphify path "UserController" "EmailService"
```

**Use for:** Impact analysis before editing a module, tracing coupling chains, verifying isolation.

---

### `graphify explain "NodeName"`

Generate a plain-language explanation of a node and its relationships.

```bash
graphify explain "UserSessionManager"
graphify explain "RateLimiter"
```

**Returns:** What the node does, what it connects to, and which community it belongs to.

---

## Content Addition

### `graphify add <url>`

Fetch and index external content into the existing graph.

```bash
graphify add https://arxiv.org/abs/2305.12345     # research paper
graphify add https://x.com/user/status/123456     # tweet
graphify add https://youtube.com/watch?v=abc123   # video (transcribed locally)
```

After adding, run `graphify . --update` to integrate new nodes into the graph.

---

## Platform Installation

### `graphify <platform> install`

Registers graphify with an AI assistant platform by writing steering files and (where supported) hooks.

| Command | Platform | Mechanism |
|---------|----------|-----------|
| `graphify claw install` | OpenClaw | Copies skill + writes `AGENTS.md` |
| `graphify claude install` | Claude Code | Writes `CLAUDE.md` entry + PreToolUse hook |
| `graphify codex install` | OpenAI Codex | Writes `AGENTS.md` |
| `graphify cursor install` | Cursor | Writes `.cursorrules` |
| `graphify copilot install` | GitHub Copilot CLI | Writes steering config |
| `graphify gemini install` | Gemini CLI | Writes steering config |
| `graphify aider install` | Aider | Writes `.aider.conf.yml` entry |

Run from the **project root**. Re-run if you move the project or reinstall the assistant.

---

## Git Hook

### `graphify hook install`

Installs a git `post-commit` hook **locally** in the current project's `.git/hooks/` directory. Runs `graphify . --update` automatically after every commit. No global or system-level changes are made.

```bash
graphify hook install
```

This keeps the graph current without manual intervention. No LLM calls are made for files that haven't changed.

---

## Output Files

All output lands in `graphify-out/` in the target directory.

| File | Format | Description |
|------|--------|-------------|
| `GRAPH_REPORT.md` | Markdown | **Primary AI context file.** God nodes, communities, surprising connections, suggested questions. Read before grepping. |
| `graph.html` | HTML | Interactive vis.js visualization. Open in browser. |
| `graph.json` | JSON | Raw graph data for programmatic querying. |
| `cache/` | Directory | SHA-256 incremental cache. **Do not commit this directory.** |
| `graph.svg` | SVG | Static visualization (only with `--svg`) |
| `graph.graphml` | GraphML | Gephi/yEd export (only with `--graphml`) |

### `graph.json` schema

```json
{
  "nodes": [
    {
      "id": "string",
      "label": "string",
      "type": "module|class|function|concept|document|media",
      "file": "relative/path/to/source.py",
      "line": 42,
      "community": 3,
      "degree": 17,
      "summary": "One-line description"
    }
  ],
  "edges": [
    {
      "source": "NodeId",
      "target": "NodeId",
      "relation": "EXTRACTED|INFERRED|AMBIGUOUS",
      "confidence": 0.85,
      "label": "calls|imports|implements|references|extends"
    }
  ],
  "communities": [
    {
      "id": 3,
      "label": "Authentication Layer",
      "members": ["NodeId1", "NodeId2"],
      "god_nodes": ["NodeId1"]
    }
  ],
  "metadata": {
    "graphify_version": "0.4.23",
    "generated_at": "2026-04-19T10:00:00Z",
    "target_dir": ".",
    "total_nodes": 248,
    "total_edges": 891
  }
}
```

---

## Relationship Tags

| Tag | Source | Meaning |
|-----|--------|---------|
| `EXTRACTED` | AST / explicit reference | Found directly in source code |
| `INFERRED` | LLM semantic analysis | Reasonable inference; has `confidence` (0.0–1.0) |
| `AMBIGUOUS` | LLM with low confidence | Flagged for manual review |

**Edge labels (non-exhaustive):** `calls`, `imports`, `implements`, `extends`, `references`, `uses`, `defines`, `depends_on`, `documents`, `transcribed_from`

---

## .graphifyignore

Uses `.gitignore` syntax. Place in the project root.

```
# Dependencies
node_modules/
vendor/
.venv/
__pycache__/

# Build outputs
dist/
build/
.next/
out/
target/

# Generated files
*.min.js
*.min.css
*.generated.*
*.lock
*.sum

# Test fixtures / snapshots
__snapshots__/
testdata/

# Graphify cache
graphify-out/cache/
```

See `templates/graphifyignore.txt` for a comprehensive starter.

---

## Supported File Types

### Code (AST extraction via tree-sitter)

Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia, Verilog, SystemVerilog, Vue, Svelte, Dart

### Documents (LLM semantic extraction)

Markdown (`.md`, `.mdx`), HTML, plain text (`.txt`), RST, PDF (requires `graphify[pdf]`)

### Images (Claude vision)

`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`

### Video / Audio (local Whisper transcription; requires `graphify[video]`)

`.mp4`, `.mov`, `.mkv`, `.webm`, `.mp3`, `.wav`, `.m4a`, `.ogg`

---

## Python Requirements

- Python 3.10 or higher
- For video/audio: significant CPU/GPU resources; Whisper model weights (~150 MB–1.5 GB) downloaded on first run

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `command not found: graphify` | pip bin not on PATH | Add `$(python -m site --user-base)/bin` to PATH |
| Nodes missing for a language | tree-sitter grammar not installed | Run `pip install "graphify" --upgrade` |
| Stale graph after edits | Graph not rebuilt | Run `graphify . --update` |
| `AMBIGUOUS` edges dominating | `--mode deep` too aggressive | Remove `--mode deep` or filter `confidence > 0.7` |
| Video transcription very slow | Running on CPU only | Install CUDA-enabled torch for GPU acceleration |
| `AGENTS.md` not respected by OpenClaw | Wrong working directory | Re-run `graphify claw install` from the project root |
| PDF nodes empty | Missing pdf extra | `pip install "graphify[pdf]"` |
