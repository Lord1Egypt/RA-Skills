# LLM Knowledge Bases

Inspired by a public workflow shared by Andrej Karpathy (@karpathy).
From raw text, PDFs, images, and structured data to a living Markdown wiki that compounds with every question.

## Product Model

`LLM Knowledge Bases` is best understood as a local-first wiki operating system for research.

The core model is:

- `raw/` holds outside-world source material
- `wiki/` holds the persistent knowledge layer the agent maintains
- `schema` defines what kinds of pages belong in the wiki and how they relate
- every ingest, query, and maintenance pass should improve the wiki itself

The runtime provides deterministic guardrails for paths, IDs, validation, and writes.
The skill tells the agent how to grow the wiki into something durable and navigable.

## What 1.2.1 Changes

The old mental model was mostly text-first:

- compile raw notes into `wiki/sources/`
- archive answers into `wiki/outputs/`
- lint the structure

The upgraded multimodal model is:

- ingest text and structured data directly into source pages
- inspect PDFs and images through deterministic raw asset metadata
- store OCR, vision, page-note, metadata, and profiling artifacts under `.llm-kb/representations/`
- compile non-text source pages from the full source bundle instead of pretending `kb_read_raw` can read binary inputs
- repair stale legacy `src-untitled-*` source ids deterministically before maintenance or compile flows keep spreading them
- promote recurring ideas into `concept` and `entity` pages
- write cross-source analysis into `synthesis` pages
- keep `wiki/index.md` as a master catalog, `wiki/log.md` as a readable activity log, and `_indexes/` current
- let important answers write back into the wiki instead of disappearing into chat history

This is closer to the original Karpathy-style wiki workflow: the wiki is the product, not just a side effect of a runtime.

## Supported Raw Inputs

The runtime now recognizes:

- text: `.md`, `.txt`
- PDFs: `.pdf`
- images: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.svg`
- structured data: `.csv`, `.tsv`, `.json`, `.html`

## Current Page Types

Runtime-backed page kinds now include:

- `source` for grounded source notes compiled from `raw/`
- `output` for archived answers tied to a specific question
- `concept` for reusable ideas that recur across notes
- `entity` for named systems, people, products, orgs, methods, or datasets
- `synthesis` for higher-level cross-source thinking
- `index` for generated navigation pages
- `log` for the generated run log page

## Default Repository Shape

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
    representations/
```

## High-Level Actions

The skill should think in terms of four high-level actions:

- `ingest-source`: compile changed raw files into `source` pages, using the direct path for text/data and the representation-first path for PDFs/images
- `ask-and-file`: answer from retrieved notes and archive the result as an `output` or promote it into a richer wiki page
- `maintain-wiki`: improve navigation, derived pages, consistency, wiki-health signals, and repair stale source ids or manifest/source-note drift when needed
- `map-gaps`: identify missing concept/entity/synthesis pages, produce prioritized draft templates, and optionally promote the best current candidate straight into a real derived page

## Runtime-Backed Tools

The runtime now supports the core wiki-maintenance surface:

- `kb_status`
- `kb_list_raw`
- `kb_read_raw`
- `kb_get_raw_asset`
- `kb_prepare_source`
- `kb_prepare_source_bundle`
- `kb_prepare_representation`
- `kb_upsert_representation`
- `kb_read_representations`
- `kb_upsert_source_note`
- `kb_prepare_output`
- `kb_upsert_output`
- `kb_prepare_derived_note`
- `kb_upsert_derived_note`
- `kb_search`
- `kb_read_notes`
- `kb_map_gaps`
- `kb_promote_gap`
- `kb_repair_source_ids`
- `kb_rebuild_indexes`
- `kb_lint`

## Install

```bash
clawhub install llm-knowledge-bases
```

For Claude Code:

```bash
claude mcp add llm-knowledge-bases -- \
  npx -y --package @harrylabs/llm-knowledge-bases@latest \
  llm-knowledge-bases-mcp \
  --vault-root /absolute/path/to/your/obsidian-vault
```

For Codex, copy [`agents/codex-AGENTS.md`](agents/codex-AGENTS.md) into your project root as `AGENTS.md`.

For other MCP-capable agents:

```bash
npx -y --package @harrylabs/llm-knowledge-bases@latest \
  llm-knowledge-bases-configs --vault-root /absolute/path/to/your/obsidian-vault
```

To scaffold a new vault:

```bash
bash scripts/init_llm_kb_repo.sh my-knowledge-base
```

## Example Prompts

Users do not need to name canonical actions.
Short natural-language requests should still map onto the runtime workflow cleanly.
The explicit prefix `$llm-knowledge-bases` is optional; use it when you want the clearest possible routing.

```text
Use $llm-knowledge-bases to ingest changed text notes and refresh the wiki indexes.
```

```text
Use $llm-knowledge-bases to inspect changed PDFs, store any missing representations, compile grounded source pages, and refresh the indexes.
```

```text
Use $llm-knowledge-bases to answer "What are the tradeoffs between retrieval and memory finetuning?" and file the result back into the wiki.
```

```text
Use $llm-knowledge-bases to inspect the wiki for missing concept or entity pages around agent memory systems.
```

```text
Use $llm-knowledge-bases to run map-gaps and tell me the next five pages this wiki should gain.
```

```text
Use $llm-knowledge-bases to run map-gaps and immediately promote the top synthesis candidate into the wiki.
```

```text
Use $llm-knowledge-bases to run a wiki maintenance pass and tell me which pages are stale, missing, or weakly grounded.
```

```text
Use $llm-knowledge-bases to check my wiki, run kb_status and kb_lint, tell me the current counts, the top 5 issues, and the single best next action. Do not modify anything yet.
```

```text
Use $llm-knowledge-bases to fill missing source notes under raw/书评 1/. Run kb_list_raw with changed_only=true and limit=200, prioritize missing_source_note, compile the first 10 text raw files, rebuild indexes, and tell me what remains missing.
```

```text
Use $llm-knowledge-bases to clean up AI-related pages. Focus on AI, AIGC, ChatGPT, prompt engineering, and AGI; fix placeholder titles, open questions, and related links on 5 notes, then rebuild indexes.
```

```text
Use $llm-knowledge-bases to add concept pages around agent memory. Search first, read the supporting notes, run kb_map_gaps, land the top 3 concept pages, and rebuild indexes.
```

```text
Use $llm-knowledge-bases to repair source-id and manifest drift. Dry-run kb_repair_source_ids first, explain the repair plan, apply it if the plan is sound, then rebuild indexes and report the repair counts.
```

```text
Use $llm-knowledge-bases to answer "What recurring judgments show up across my AI-related book reviews?" Read only the most relevant notes first, then write the durable result back as a concept or synthesis page if it is reusable.
```

## Chinese Compact Prompts

```text
用 $llm-knowledge-bases 检查一下我的 wiki，先别改，告诉我当前数量、最重要的 5 个问题、以及最值得做的下一步。
```

```text
用 $llm-knowledge-bases 补一下缺失的 source notes，只处理 raw/书评 1/，先做前 10 个，再刷新索引。
```

```text
用 $llm-knowledge-bases 整理一下 AI 相关页面，优先修标题像占位词、Open Questions 还是待整理、Related Links 还是待补充的 source notes。
```

```text
用 $llm-knowledge-bases 补 3 个最值得做的 concept pages，先搜索和读证据，再落地页面。
```

```text
用 $llm-knowledge-bases 继续推进这份库：保守地跑一轮，小批量补缺失、修占位页，并在证据足够时补 1 个 derived page。
```

## Scenario Shortcuts

```text
用 $llm-knowledge-bases 整理一下 AI 相关内容。
```

```text
用 $llm-knowledge-bases 补书评前 10 个。
```

```text
用 $llm-knowledge-bases 继续推进我的这份库。
```

## One-Line Chinese Pack

直接复制下面任意一句就能用：

```text
用 $llm-knowledge-bases 检查一下我的 wiki，先别改。
```

```text
用 $llm-knowledge-bases 补书评前 10 个。
```

```text
用 $llm-knowledge-bases 整理一下 AI 相关内容。
```

```text
用 $llm-knowledge-bases 补 3 个 concept pages。
```

```text
用 $llm-knowledge-bases 修一下 source id 漂移，先 dry run。
```

```text
用 $llm-knowledge-bases 继续推进我的这份库。
```

如果上下文已经明确是在操作这个知识库，通常也可以直接省略 `$llm-knowledge-bases`，例如：

```text
检查一下我的 wiki，先别改。
```

```text
补书评前 10 个。
```

```text
整理一下 AI 相关内容。
```

## Daily 3-Pack For This Vault

如果只保留 3 句，优先保留这 3 句：

```text
用 $llm-knowledge-bases 检查一下我的 wiki，先别改，告诉我当前数量、最重要的 5 个问题、以及今天最值得做的一步。
```

```text
用 $llm-knowledge-bases 继续推进我的这份库：只处理 raw/书评 1/，优先补前 10 个 missing source notes，然后刷新索引。
```

```text
用 $llm-knowledge-bases 整理一下 AI 相关内容：先修一小批占位感强的 source notes，再补 1 个最值得做的 concept 或 synthesis page。
```

## Writing Style

This skill prefers durable wiki artifacts over chat-only answers:

- source-grounded pages
- explicit multimodal review trails through `raw_kind`, `mime_type`, `asset_paths`, and `# Visual Notes` when needed
- explicit `source_refs`
- linked Markdown pages that humans can browse
- generated indexes and logs that keep the vault navigable
- warnings from `kb_lint` that highlight missing or stale representations, inconsistent `asset_paths`, isolated draft pages, missing cross-links, stale source coverage, unresolved research gaps, unsupported claims, contradiction candidates, placeholder content, and medium/high-value missing pages before those problems spread
- `kb_repair_source_ids` when source note ids, paths, manifest entries, or stored raw hashes have drifted and need a deterministic repair pass

Outward-facing artifacts default to English unless the user explicitly asks otherwise.
