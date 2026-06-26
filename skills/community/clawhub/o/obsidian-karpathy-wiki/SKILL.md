---
name: obsidian-karpathy-wiki
description: Operate an Obsidian knowledge base as a persistent LLM wiki using a raw-to-source-to-wiki pattern. Use when Codex or another agent needs to ingest raw notes, reconcile loose inbox material, maintain source summaries, compile formal wiki pages, write back valuable query outputs, run heartbeat maintenance, lint contradictions and stale claims, or hand off ongoing wiki operations to another agent.
---

# Obsidian Karpathy Wiki

## Overview

Use this skill to maintain an Obsidian vault as a persistent, compounding knowledge base instead of a passive note archive.

The core pattern is:

- raw material enters the vault
- the agent summarizes it into `sources`
- stable conclusions are promoted into formal wiki pages
- valuable query results are saved into `outputs`
- outputs can later be written back into formal knowledge

This skill is designed for an agent that does recurring maintenance, not just one-off cleanup.

Read [references/object-model.md](references/object-model.md) before restructuring a vault.
Read [references/workflow.md](references/workflow.md) before ingest, query, lint, or migration work.
Read [references/adaptation-checklist.md](references/adaptation-checklist.md) before adapting this skill to a specific user's vault.
Read [references/heartbeat.md](references/heartbeat.md) before setting up recurring maintenance behavior.

## Core Idea

Do not treat the goal as organizing files.

Treat the goal as compiling knowledge once and then keeping it current.

A good vault maintained with this skill should let the agent answer questions by reading a living wiki, not by rediscovering everything directly from raw documents every time.

## Recommended Vault Shape

Prefer this logical structure, even if physical names differ:

- `raw/`
- `compile/` or another staging layer
- `wiki/`
- an output layer such as `outputs/` or `content-outputs/`
- governance files such as `CLAUDE.md` and a maintenance skill

Within `wiki/`, prefer this formal structure:

- `index.md`
- `log.md`
- `questions/`
- `methods/`
- `decisions/`
- `principles/`
- `domains/`
- `concepts/`
- `entities/`
- `sources/`
- `outputs/`

Questions, methods, and decisions are the main navigation axis.
Principles explain why methods and decisions stay valid across situations.
Sources are evidence bridges.
Outputs are reusable query artifacts.

## Operating Model

### Raw

Raw material is source-of-truth input.

Do not treat raw notes as formal knowledge by default.

Loose notes in the vault root should usually be treated as temporary inbox material and moved into a raw inbox folder unless the user explicitly wants them to remain in place.

### Sources

`wiki/sources/` is the bridge between raw material and formal knowledge.

A source page should summarize:

- what the material says
- which questions it informs
- which methods it supports
- which decisions it changes
- which principles it strengthens or challenges

### Formal Pages

Promote stable knowledge into:

- `questions/`
- `methods/`
- `decisions/`
- `principles/`

Avoid creating many thin formal pages from a single source.

### Outputs

Save high-value query results into `wiki/outputs/`.

Examples:

- syntheses
- comparison tables
- structured analysis
- decision memos
- topic briefs

Outputs are not automatically formal knowledge, but they are often new source material for future write-back.

## Core Operating Loop

### 1. Ingest

When new material appears:

1. Read the source.
2. If a loose note appears in the vault root, treat it as inbox material.
3. Move loose inbox notes to a human raw inbox folder unless the user explicitly wants them to remain in place.
4. Create or update a `wiki/sources/` page.
5. Extract only the stable upgrades:
   - question
   - method
   - decision
   - principle
   - concept
   - entity
6. Update only the few formal pages that truly benefit.
7. Update `wiki/index.md`.
8. Append a record to `wiki/log.md`.

Do not explode one source into many thin pages.

### 2. Query

When answering a user question:

1. Read `wiki/index.md` first.
2. Read the most relevant question, method, and decision pages.
3. Read principle, concept, entity, and source pages as supporting context.
4. Produce a structured answer.
5. If the answer is reusable, save it under `wiki/outputs/`.
6. Decide whether the output should later be written back into formal pages.

### 3. Weekly Compile

Use weekly compile to:

- review the last 5-7 days of source and staging material
- extract repeated questions
- promote stable methods
- update decisions if assumptions changed
- promote principles when repeated patterns explain why methods remain valid
- update domain maps, `index.md`, and `log.md`

### 4. Lint

Check for:

- questions with no linked methods
- methods with no scenario or caveat
- decisions with stale assumptions
- principles that duplicate lower-value pages
- source pages not connected to formal knowledge
- pages that contradict each other
- stale claims superseded by newer sources
- loose notes that never entered the ingest flow
- high-value outputs that should have been written back

### 5. Backfill

Treat output folders as write-back sources.

Backfill only:

- reusable methods
- recurring questions
- strategic decisions
- principle-level lessons

Do not promote finished drafts directly into formal wiki pages.

## Heartbeat Rule

Heartbeat should mean recurring maintenance, not empty status pings.

A good heartbeat checks:

- whether new loose notes appeared
- whether raw inbox has unread material
- whether source pages are piling up without promotion
- whether formal pages are missing principle-level explanation
- whether the vault has new orphan pages, stale assumptions, or contradictions
- whether query outputs are accumulating without write-back

Heartbeat should lead to either:

- direct maintenance work
- or a concrete maintenance findings page

## Publishing Safety

When publishing or sharing this skill:

- do not hardcode a specific local path
- do not include private automation ids
- do not include personal account names or bot nicknames
- do not assume the output folder must use one particular language name
- keep user-specific rules in a separate private operator layer if needed

## Writing Rules

- Use Markdown only.
- Use YAML frontmatter on formal pages.
- Use Obsidian wiki links.
- Keep source material distinct from formal conclusions.
- Prefer durable formal page titles over date-based titles.
- Treat loose root notes as temporary inbox material.

## Handoff Rule

This skill is suitable as a public foundation for persistent Obsidian wiki maintenance.

For a private deployment, pair it with a separate vault-specific governance file that defines:

- the actual vault path
- exact folder names
- any automations or heartbeat schedule
- user-specific output folders
- domain-specific operating rules
