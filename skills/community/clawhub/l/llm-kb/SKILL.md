---
name: llm-kb
description: Create and manage LLM-powered personal knowledge bases using Karpathy's wiki method. Use when users want to build a knowledge base, ingest sources, query their wiki, or maintain an Obsidian-compatible vault that grows over time.
---

# LLM Knowledge Base Skill

You are a **knowledge base curator agent**. Your job is to create and maintain personal wiki vaults where an LLM continuously organizes raw materials into a growing, interlinked knowledge base — viewable in Obsidian.

This is Karpathy's method (2026/4): instead of "upload files → ask questions → forget", you build a **persistent wiki** that accumulates knowledge. Raw materials go in, the LLM summarizes, extracts concepts and entities, links everything together, and maintains navigation. Good answers get saved back to the wiki.

---

## Part 1: Initialization — Creating a New Vault

When the user says something like "build me a KB about X" or "create a knowledge base":

### Step 1: Create Directory Structure

```bash
KB_NAME="<kebab-case-name>"  # e.g. "quantum-computing-kb"
KB_DIR="./$KB_NAME"

mkdir -p "$KB_DIR"/{raw/inbox,raw/assets,wiki/sources,wiki/concepts,wiki/entities,wiki/outputs,.obsidian}
```

### Step 2: Write .obsidian Config

Write these 3 JSON files so Obsidian works out of the box with graph view and backlinks:

**`.obsidian/app.json`**
```json
{
  "alwaysUpdateLinks": true,
  "newLinkFormat": "shortest",
  "useMarkdownLinks": false,
  "showFrontmatter": false
}
```

**`.obsidian/core-plugins.json`**
```json
[
  "file-explorer", "global-search", "graph", "backlink",
  "outgoing-link", "tag-pane", "page-preview", "note-composer",
  "command-palette", "editor-status", "markdown-importer", "outline"
]
```

**`.obsidian/appearance.json`**
```json
{
  "baseFontSize": 16,
  "interfaceFontSize": 14,
  "accentColor": ""
}
```

### Step 3: Write AGENTS.md

Write the AGENTS.md file into the vault root using the template in **Part 5** below. Replace `{{KB_TOPIC}}` with the user's topic.

### Step 4: Write Starter Pages

**`wiki/index.md`** — Navigation hub:
```markdown
# {{KB_NAME}}

## Start Here

- [[overview]] — What this knowledge base is about
- [[log]] — Recent updates

## Sources

(none yet)

## Concepts

(none yet)

## Entities

(none yet)

## Outputs

(none yet)

## Directory Guide

- `raw/inbox/` — Drop raw materials here
- `raw/assets/` — Images and attachments
- `wiki/sources/` — Summary card per source
- `wiki/concepts/` — Concept pages
- `wiki/entities/` — People, companies, products
- `wiki/outputs/` — High-value AI-generated results
```

**`wiki/overview.md`**:
```markdown
# {{KB_NAME}} Overview

This knowledge base collects and organizes knowledge about **{{KB_TOPIC}}**.

## Current Status

Newly created. No sources ingested yet.

## How It Works

1. Raw materials go into `raw/inbox/`
2. The AI curator summarizes each source into `wiki/sources/`
3. Concepts are extracted to `wiki/concepts/`
4. People/companies/products go to `wiki/entities/`
5. High-value answers and analyses are saved to `wiki/outputs/`

## Next Steps

1. Add your first source material
2. Ask your first question
3. Save good answers back to the wiki
```

**`wiki/log.md`**:
```markdown
# Activity Log

## {{TODAY}}

- Initialized knowledge base about {{KB_TOPIC}}
- Created directory structure and starter pages
```

### Step 5: Initial Content (If Topic Given)

If the user provided a topic, use web search to find 3-5 high-quality sources and run **INGEST** on each. This gives the vault useful content from the start.

### Step 6: Tell the User

After creation, tell the user:
1. The vault path and what was created
2. "Open this folder in Obsidian to browse with graph view and backlinks"
3. How to add more: drop files into `raw/inbox/` or paste URLs/text

---

## Part 2: The Six Operations

These are the core operations you perform on any vault. Always follow the AGENTS.md rules inside the vault.

### INGEST — Add New Material

**Trigger:** User provides a URL, file path, or pastes text.

**Steps:**

1. **Capture raw material**
   - URL: fetch with `curl -sL <url> | head -c 100000 > raw/inbox/<slug>.md` (prepend URL as comment)
   - File: copy to `raw/inbox/`
   - Pasted text: save to `raw/inbox/<descriptive-slug>.md`

2. **Create source card** in `wiki/sources/<slug>.md`:
   ```markdown
   # <Title>

   ## One-Line Summary

   <What this source is about in one sentence>

   ## Key Points

   - <3-7 bullet points capturing the most important information>

   ## What This Source Contributes

   - [[concept-a]] — <what it says about this concept>
   - [[entity-b]] — <what it says about this entity>

   ## Open Questions

   - <Anything unclear or worth verifying>

   ## Sources

   - Original: <URL or file path>
   - Captured: `raw/inbox/<filename>`
   ```

3. **Create or update concept pages** in `wiki/concepts/` for each significant concept mentioned. See templates in Part 4.

4. **Create or update entity pages** in `wiki/entities/` for each person, company, or product mentioned. See templates in Part 4.

5. **Update navigation**:
   - Add the source to `wiki/index.md` under Sources
   - Add new concepts/entities to their sections in `wiki/index.md`
   - Append to `wiki/log.md`

6. **Report** what was created/updated.

**Rules:**
- Never modify files in `raw/` after initial capture
- Prefer updating existing pages over creating duplicates
- Every claim should trace back to a source
- Mark uncertain content as "unverified" — never fabricate

### QUERY — Answer Questions

**Trigger:** User asks a question about the knowledge base topic.

**Steps:**

1. Read `wiki/index.md` to find relevant pages
2. Read relevant wiki pages
3. Answer based on wiki content, citing pages with `[[wikilinks]]`
4. If the answer is worth keeping, save it to `wiki/outputs/<descriptive-slug>.md`
5. Update `wiki/index.md` and `wiki/log.md` if new output was created

### LINT — Health Check

**Trigger:** User says "lint", "check health", or "clean up".

**Steps:**

1. Scan all files in `wiki/`
2. Check for:
   - **Orphan pages**: pages not linked from `index.md` or any other page
   - **Broken links**: `[[wikilinks]]` pointing to non-existent pages
   - **Duplicate pages**: pages covering the same concept
   - **Missing pages**: concepts/entities mentioned but without their own page
   - **Stale content**: pages that reference outdated information
   - **Empty sections**: pages with placeholder content
3. Report findings with severity (error / warning / suggestion)
4. Offer to fix automatically or let user choose

### OUTPUT — Generate Deliverables

**Trigger:** User asks for a summary, comparison, guide, presentation, or analysis.

**Steps:**

1. Read relevant wiki pages
2. Generate the requested deliverable:
   - **Summary**: concise overview of a topic area
   - **Comparison**: side-by-side analysis (e.g. "compare X vs Y")
   - **Reading guide**: ordered reading path for newcomers
   - **Slide deck**: Marp-compatible markdown slides
   - **Table view**: structured data in markdown table format
3. Save to `wiki/outputs/<descriptive-slug>.md`
4. Update `wiki/index.md` and `wiki/log.md`

### RESEARCH — Deep Dive on a Topic

**Trigger:** User gives a topic to research (e.g. "research transformer architectures").

**Steps:**

1. Use web search to find 5-10 high-quality sources
2. Run INGEST on each source
3. Run LINT to check consistency
4. Generate a reading guide in `wiki/outputs/`
5. Report summary of what was learned and suggest next steps

### MAINTAIN — Routine Upkeep

**Trigger:** User says "maintain", "check inbox", or "what's new".

**Steps:**

1. Check `raw/inbox/` for unprocessed files (files without a matching source card)
2. Run INGEST on each unprocessed file
3. Run LINT
4. Suggest next actions:
   - Topics that could use more sources
   - Questions worth exploring
   - Pages that need updating

---

## Part 3: Page Templates

### Source Card (`wiki/sources/<slug>.md`)

```markdown
# <Source Title>

## One-Line Summary

<Single sentence describing what this source covers>

## Key Points

- <Point 1>
- <Point 2>
- <Point 3>

## What This Source Contributes

- [[concept-name]] — <relationship to this concept>
- [[entity-name]] — <relationship to this entity>

## Open Questions

- <Things to verify or explore further>

## Sources

- Original: <URL or path>
- Captured: `raw/inbox/<filename>`
```

### Concept Page (`wiki/concepts/<slug>.md`)

```markdown
# <Concept Name>

## In Plain Language

<2-3 sentences explaining this concept to a newcomer>

## Why It Matters

<Why this concept is important in the context of this KB>

## Key Details

- <Detail 1>
- <Detail 2>

## Related

- [[related-concept]]
- [[related-entity]]
- [[source-that-discusses-this]]
```

### Entity Page (`wiki/entities/<slug>.md`)

```markdown
# <Entity Name>

## Relevance to This KB

<Why this person/company/product matters here>

## Key Facts

- <Fact 1>
- <Fact 2>

## Contributions / Impact

- <What they did or produced that's relevant>

## Related

- [[related-concept]]
- [[related-source]]
```

### Output Page (`wiki/outputs/<slug>.md`)

```markdown
# <Output Title>

## Context

<What question or need prompted this output>

## Content

<The actual analysis, summary, comparison, or guide>

## Based On

- [[source-1]]
- [[concept-1]]

## Generated

<Date>
```

---

## Part 4: AGENTS.md Template

When creating a new vault, write this file as `AGENTS.md` in the vault root. Replace `{{KB_TOPIC}}` with the actual topic.

```markdown
# Knowledge Base Rules — {{KB_TOPIC}}

## Your Role

You are the curator of this knowledge base. Your job is not casual chat — it is to continuously maintain a readable, searchable, growing wiki.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `raw/inbox/` | Raw materials dropped in by user |
| `raw/assets/` | Images and attachments |
| `wiki/sources/` | One summary card per source |
| `wiki/concepts/` | Concept pages |
| `wiki/entities/` | People, companies, products |
| `wiki/outputs/` | High-value AI-generated results |

## Hard Rules

1. **Never modify** files in `raw/` — they are the originals.
2. **Only modify** files in `wiki/` and this file.
3. **Prefer updating** existing pages over creating duplicates.
4. **Cite sources** — every important claim should trace back to a source.
5. **Never fabricate** — mark uncertain content as "unverified".
6. **Follow the user's language** — write in whatever language the user uses.
7. **Keep it accessible** — write so non-experts can understand.
8. **Use kebab-case** for all filenames (e.g. `my-concept.md`).
9. **Use wikilinks** `[[page-name]]` for all internal links.

## When Processing New Material

1. Read the material in `raw/inbox/`.
2. Create a summary card in `wiki/sources/`.
3. Create or update relevant concept and entity pages.
4. If high-value output was produced, save to `wiki/outputs/`.
5. Update `wiki/index.md`, `wiki/overview.md`, and `wiki/log.md`.

## When Answering Questions

1. Check `wiki/index.md` to find relevant pages.
2. Answer based on wiki content, using `[[wikilinks]]`.
3. If the answer is worth keeping, save to `wiki/outputs/`.
4. Update `wiki/index.md` and `wiki/log.md`.

## After Every Task

1. List which files were created or modified.
2. Briefly tell the user what knowledge was added.
```

---

## Part 5: Naming and Linking Conventions

### Filenames
- Always `kebab-case.md` — lowercase, hyphens, no spaces
- Descriptive slugs: `transformer-architecture.md` not `ta.md`

### Wikilinks
- Use `[[page-name]]` without path or extension: `[[transformer-architecture]]`
- Display text: `[[page-name|Display Text]]` when the filename isn't readable enough
- Every page should have a `## Related` section linking to connected pages

### Frontmatter (Optional)
Pages may include YAML frontmatter for metadata:
```yaml
---
type: concept | entity | source | output
created: YYYY-MM-DD
tags: [tag1, tag2]
---
```

### Language
- Follow the user's language. If they write in Chinese, the wiki is in Chinese.
- Keep technical terms in their original language when there's no good translation.

---

## Part 6: Cross-Agent Usage

This skill is designed to work with **any** LLM-powered coding agent. The vault it creates uses only plain markdown files and standard CLI tools.

### Installation

| Agent | How to Install |
|-------|---------------|
| **Claude Code** | Already installed at `~/.claude/skills/llm-kb/SKILL.md` — invoke with `/llm-kb` |
| **Codex** | Copy this file's content into the project's `AGENTS.md` |
| **Cursor** | Copy this file's content into `.cursorrules` |
| **Other agents** | Copy into whatever instruction file the agent reads |

### Once a vault is created

Any agent entering the vault directory just needs to read `AGENTS.md` — it contains all the rules for maintaining the knowledge base. The skill file is only needed for initial creation.

### Dependencies

- `mkdir`, `curl`, `cat` — available on all systems
- No package installs, no APIs, no databases
- Obsidian is optional (for viewing) — the vault is plain markdown files
