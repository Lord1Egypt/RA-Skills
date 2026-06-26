---
name: graphify-skill
description: "AI coding assistant skill for building and querying knowledge graphs from codebases, docs, and media. Use for: understanding complex codebases, architectural analysis, context sharing with OpenClaw/Claude Code, and extracting design rationale from multimodal sources. Always check graphify-out/GRAPH_REPORT.md before grepping or globbing to find relevant files."
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
      env:
        - name: ANTHROPIC_API_KEY
          description: "Required for semantic extraction (docs, PDFs, images). Not needed for AST-only code extraction."
          required: false
        - name: OPENAI_API_KEY
          description: "Alternative LLM backend for semantic extraction."
          required: false
    install:
      - kind: uv
        package: graphify
        bins: [graphify]
    primaryEnv: ""
    emoji: "🕸️"
    homepage: https://github.com/safishamsi/graphify
    os:
      - linux
      - macos
      - windows
---

# Graphify Skill

Graphify turns a folder of code, docs, images, and videos into a **queryable knowledge graph**. After running `graphify .`, the generated `GRAPH_REPORT.md` is referenced by the assistant when you ask it to explore the codebase. Use it to navigate unfamiliar codebases, trace architectural intent, and share context efficiently.

**Credential note:** Semantic extraction (docs, PDFs, images) calls an external LLM using your own API key (`ANTHROPIC_API_KEY` or `OPENAI_API_KEY`). AST code extraction and Whisper transcription run fully locally with no API key required.

> **Token efficiency:** Reading `GRAPH_REPORT.md` is ~71.5× cheaper than reading raw source files. Always check it first.

---

## Installation

### Minimum install
```bash
pip install graphify
```

### Recommended install with all extras
```bash
pip install "graphify[pdf,video,watch,svg]"
```

| Extra | Adds support for |
|-------|-----------------|
| `pdf` | PDF papers and documents |
| `video` | Video/audio transcription via faster-whisper |
| `watch` | `--watch` file monitoring |
| `svg` | `--svg` export |
| `mcp` | Model Context Protocol server |
| `neo4j` | Neo4j graph database integration |
| `office` | Word/Excel/PowerPoint documents |

### Register with OpenClaw
```bash
graphify claw install
```

This copies the skill into OpenClaw's global skill directory and writes an `AGENTS.md` to the project root so the graph is consulted on every tool call.

### Register with other platforms
```bash
graphify claude install     # Claude Code (CLAUDE.md + PreToolUse hook)
graphify cursor install     # Cursor (.cursorrules)
graphify codex install      # Codex (AGENTS.md)
graphify copilot install    # GitHub Copilot CLI
graphify gemini install     # Gemini CLI
graphify aider install      # Aider
```

### Git post-commit hook (optional, local project only)
Installs a hook in the current project's `.git/hooks/` — no global changes.
```bash
graphify hook install
```

---

## Building a Knowledge Graph

### First run
```bash
graphify .
```

Graphify runs a **three-pass pipeline**:
1. **AST extraction** — deterministic tree-sitter parsing of all code files (no LLM calls)
2. **Transcription** — local Whisper processing of any video/audio
3. **Semantic extraction** — parallel LLM calls (using your configured API key) analyze docs, papers, and images

### Incremental update (changed files only)
```bash
graphify . --update
```
Uses a SHA-256 cache in `graphify-out/cache/` — safe to run after every save.

### Watch mode (auto-sync as files change)
```bash
graphify . --watch
```

### Deep mode (aggressive inferred-edge extraction)
```bash
graphify . --mode deep
```
Adds `INFERRED` edges with confidence scores (0.0–1.0) and `AMBIGUOUS` edges flagged for review.

### Preserve edge directionality
```bash
graphify . --directed
```

### Re-cluster without re-extracting
```bash
graphify . --cluster-only
```

### Skip HTML visualization (faster CI runs)
```bash
graphify . --no-viz
```

---

## Output Artifacts

All artifacts land in `graphify-out/`:

| File | Purpose |
|------|---------|
| `GRAPH_REPORT.md` | **Read this first.** God nodes, community structure, surprising connections, suggested questions. |
| `graph.html` | Interactive browser visualization — open for human review. |
| `graph.json` | Raw graph data for programmatic querying via CLI or script. |
| `cache/` | SHA-256 incremental cache — commit everything *except* this directory. |

### Additional export formats
```bash
graphify . --svg        # SVG visualization
graphify . --graphml    # Gephi / yEd compatible export
graphify . --wiki       # Wikipedia-style article per node
```

---

## Querying the Graph

```bash
# Natural-language semantic search
graphify query "where is authentication handled?"

# Trace a specific path (DFS traversal)
graphify query "how does the request reach the database?" --dfs

# Shortest path between two nodes
graphify path "AuthMiddleware" "PostgresAdapter"

# Plain-language explanation of a node
graphify explain "UserSessionManager"
```

---

## Adding External Content

```bash
graphify add <arxiv-url>     # Fetch and index a research paper
graphify add <x.com-url>     # Fetch and index a tweet
graphify add <video-url>     # Download and transcribe video/audio
```

After adding, run `graphify . --update` to integrate the new nodes into the graph.

---

## Ignoring Files

Create `.graphifyignore` in the project root (same syntax as `.gitignore`):

```
node_modules/
dist/
build/
.next/
vendor/
*.generated.*
*.min.js
*.lock
graphify-out/cache/
```

See `templates/graphifyignore.txt` in this skill for a comprehensive starter.

---

## Relationship Types

| Tag | Meaning |
|-----|---------|
| `EXTRACTED` | Found directly in source (AST, explicit reference) |
| `INFERRED` | Reasonable inference; includes `confidence` score 0.0–1.0 |
| `AMBIGUOUS` | Low-confidence; flagged for manual review |

Use `--mode deep` to maximize `INFERRED` coverage. Filter `AMBIGUOUS` edges when precision matters.

---

## Best Practices for OpenClaw / Claude Code

### 1. Always read the report before exploring
```
Read graphify-out/GRAPH_REPORT.md
```
The report identifies "god nodes" (highest-degree concepts), community clusters, and suggested entry-point questions. Use these to focus subsequent searches.

### 2. Map communities to features
Each community in the report corresponds to a functional area of the codebase. When fixing a bug or adding a feature, identify the relevant community first, then limit file reads to that cluster.

### 3. Use `graphify query` before `grep`
For open-ended questions ("where is X handled?"), prefer `graphify query` — it searches the semantic graph and returns ranked node paths rather than raw text matches.

### 4. Use `graphify path` for impact analysis
Before editing a node, run `graphify path "NodeA" "NodeB"` to find coupling chains and assess blast radius.

### 5. Use `--update` aggressively
After any significant edit, run `graphify . --update` to keep the graph current. The cache makes this cheap.

### 6. Team workflows
- Commit `graphify-out/` (excluding `graphify-out/cache/`) so teammates get graph context immediately on checkout.
- One team member builds the initial graph; all others benefit without LLM cost.
- Install `graphify hook install` to auto-rebuild on every commit.

### 7. Multimodal context
Place architecture diagrams, whiteboard photos, or design mockups in the project directory before running `graphify .`. Claude vision will link visual concepts to code nodes.

---

## Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia, Verilog, SystemVerilog, Vue, Svelte, Dart

Plus: Markdown, MDX, HTML, plain text, RST, PDF, PNG/JPG/WebP/GIF images, MP4/MOV/MKV/WebM/MP3/WAV/M4A/OGG media.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `graphify: command not found` | Run `pip install graphify` and ensure pip's bin directory is on PATH |
| Graph is stale after edits | Run `graphify . --update` |
| Missing nodes for a language | Confirm tree-sitter grammar is installed; run `graphify . --update` |
| Video transcription slow | Expected — Whisper runs locally. Add GPU acceleration or use `--no-viz` to skip unrelated steps |
| `AMBIGUOUS` edges dominating | Switch from `--mode deep` to default mode, or filter by `confidence > 0.7` in `graph.json` |
| `AGENTS.md` not picked up | Re-run `graphify claw install` from the project root |
