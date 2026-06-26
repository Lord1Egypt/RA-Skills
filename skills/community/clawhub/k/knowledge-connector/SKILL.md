---
name: knowledge-connector
description: "Knowledge workbench connector. Input notes, documents, or a local knowledge folder; output import guidance, relationship maps, cross-document answers, and concrete next actions. Privacy boundary: do not upload sensitive notes unless the user explicitly chooses an external tool."
---
# Knowledge Connector

Knowledge Connector should feel like a product line, not another graph utility.

Its job is not just to extract concepts. Its job is to help the user:
- import notes and documents with low friction
- verify the connector is installed and writable before a long import
- search across multiple documents from one query
- visualize concept relationships in a way that is easy to inspect
- get actionable graph results such as what to connect, review, or expand next

## What This Skill Optimizes For

Default toward five high-value outcomes:
- reliable first-run setup
- fast document import
- guided import onboarding
- cross-document knowledge retrieval
- relationship-aware graph views
- actionable next steps

Avoid drifting into “yet another adjacent knowledge skill”.

## Primary Workflows

### 1. First-Run Check

Use `kc doctor` when:
- the user just installed the skill
- `kc` is not found or a command fails before doing useful work
- the user is about to import a large notes folder

Good doctor behavior means:
- confirm the data directory is writable
- confirm JSON stores are readable
- confirm the CLI entrypoint exists
- warn clearly if `kc` is not on PATH

If `kc` is not available, tell the user to reinstall or repair the Clawhub install before continuing with import/search commands.
If dependencies are missing but the files are present, `node bin/cli.js doctor` still works as a fallback diagnostic.
If the default data directory is not writable, set `KC_DATA_DIR` to a writable folder before running import/search commands.

### 2. Import Experience

Use `kc import-docs` when the user wants to build a graph from multiple files or a notes directory.
Use `kc import-wizard` when the user wants a preview-first onboarding flow.

Good import behavior means:
- accept files or a directory
- avoid duplicate source records when the same file is imported again
- preserve source titles and paths
- show how many documents, concepts, and relations were created
- keep the user oriented after import

### 3. Cross-Document Search

Use `kc search` or `kc query` when the user asks:
- where an idea appears across notes
- which documents mention a concept
- what concepts connect several documents

Results should show:
- matching concepts
- matching source documents
- matched keywords when helpful
- useful next actions

### 4. Relationship Visualization

Use `kc visualize` for full graph export and `kc map` for a concept-centered actionable subgraph.

Visualization should help the user answer:
- what is central
- what is weakly connected
- what deserves review

### 5. Actionable Results

Do not stop at “here is the graph”.

The output should usually recommend one or more actions such as:
- import more source material
- auto-connect newly imported concepts
- inspect a concept-centered subgraph
- verify weak relationships from source documents
- export a graph view for sharing or review

## Core Commands

### Import

```bash
kc doctor
kc import-wizard --dir notes/
kc import-docs --dir notes/
kc import-docs --files a.md b.md c.txt
```

### Search

```bash
kc search "machine learning"
kc answer "哪些文档把强化学习和规划连在一起？"
kc query "transformer" --sources
kc query --ask "哪些文档同时提到了强化学习和规划？"
```

### Map And Visualize

```bash
kc map --concept "人工智能" --depth 2
kc visualize --format html --output graph.html
kc visualize --concept "机器学习" --depth 2 --output ml-graph.html
```

### Manage

```bash
kc stats
kc export --output backup.json
kc import --file backup.json
```

## Output Standard

When the skill returns results, prefer this structure:

### What Matched
Show concepts and source coverage.

### Why It Matters
Explain the meaningful relationship or pattern.

### Next Step
Tell the user what to do next with the graph.

## Product Positioning

Knowledge Connector is strongest when the user has:
- a growing notes corpus
- repeated concepts spread across files
- a need to move from storage to understanding

It is weaker if it only acts like a raw extractor with no import flow, no source-aware search, and no next-step guidance.
