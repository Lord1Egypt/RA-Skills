---
name: notion-brain
description: >
  Route high-value content into a Notion workspace with a quality gate,
  destination mapping, and exact MCP write patterns. ALWAYS trigger when the
  user says "save this to Notion", "put this in my brain", "add this to the
  knowledge base", "capture this for later", "log this in Notion", or any
  variation of saving, storing, or routing content to Notion. Also trigger
  when an agent produces a research summary, decision memo, project plan,
  status update, article draft, security audit, financial snapshot, weekly
  rollup, contact note, meeting prep, or other durable content that belongs
  in Notion. Trigger on mentions of a knowledge hub, Inbox DB, content hub,
  work hub, or finance hub as destinations. Skip for health workflows,
  property/equipment tracking, or workspace memory-only writes.
---

# Notion Brain

Use this skill to make **deliberate Notion saves**, not reflexive ones.

The job is fourfold:
1. decide whether the content deserves a durable home in Notion
2. route it to the right page or database
3. shape it into a clean structure before writing
4. push it with the correct Notion MCP call pattern

## Decision gate

Write to Notion only if at least one of these is true:
- the content will be useful again later
- it captures a decision, plan, status, insight, or reusable artifact
- it would be annoying or costly to reconstruct
- the owner would reasonably expect to find it in their second brain later

Do **not** write to Notion when the content is:
- trivial, obvious, or disposable
- already stored there in equivalent form
- better suited only for chat, scratch work, or transient memory
- part of a dedicated workflow this skill explicitly excludes

When unsure, prefer one of these outcomes:
- **Do not save**
- **Save a short capture to Inbox DB**
- **Save a fully structured page**

## Scope and non-scope

In scope:
- research summaries
- decision memos
- project plans and project status
- article drafts
- security audit reports
- financial snapshots
- weekly rollups
- contact notes
- meeting prep
- quick captures worth preserving

Out of scope:
- health database management
- property, vehicle, or equipment management
- replacing workspace memory or daily logs
- auto-pushing everything by default

Always write to workspace memory separately when the content also matters for agent continuity.

## Default workflow

1. **Classify the content**
 Choose the closest content type from `references/page-map.md`.

2. **Choose save depth**
 - durable artifact or polished note -> structured page under the destination page
 - uncertain but worth keeping -> Inbox DB capture
 - existing page needs more detail -> append blocks instead of creating a duplicate

3. **Load the right template**
 Read `references/templates.md` and use the smallest template that preserves value.

4. **Check for an existing page first**
 Use Notion search before creating a new page when the topic may already exist.

5. **Write with MCP**
 Read `references/mcp-commands.md` and use the exact command pattern for:
 - search
 - create page in a parent page
 - create item in Inbox DB
 - update page metadata
 - append blocks to an existing page

6. **Keep titles specific**
 Prefer titles that are searchable and date-aware, for example:
 - `Research Summary — Microsoft Copilot vs SecureAI — 2026-03-22`
 - `Decision Memo — Notion Routing Skill`
 - `Weekly Rollup — 2026-W12`

7. **Avoid junk writes**
 If the content is weak, incomplete, or duplicated, either tighten it first or do not save it.

## Routing rules

Read `references/page-map.md` when deciding destination.

Practical defaults:
- broad knowledge, synthesis, decisions, audits, rollups, and relationship notes -> **Knowledge Hub**
- work execution and meeting support -> **Work Hub**
- writing and publishing work -> **Content Hub**
- money and finance artifacts -> **Finance Hub**
- everything else worth saving but not yet sorted -> **Inbox DB**

## Formatting rules

Read `references/templates.md` when preparing the payload.

Default formatting standards:
- lead with a one-line summary
- use short sections, not walls of text
- preserve source links, dates, and decisions
- include `Next steps` only when action is implied
- avoid raw dump formatting unless using Inbox DB for quick capture

## MCP usage

Read `references/mcp-commands.md` before writing. Use **native Notion MCP tools** (notion-search, notion-create-pages, notion-update-page, notion-fetch) — not mcporter.

Command order:
1. search if collision is possible
2. create or identify target page/database item
3. add content (inline for new pages, append for existing)
4. update page properties only when needed

## Duplicate handling

Always search before creating when:
- the title contains a person name, project name, or recurring topic
- the content type recurs (weekly rollup, project status, financial snapshot)
- you are unsure whether the page already exists

When a duplicate is found:
- rollups and status pages → use `replace_content` to supersede the old version
- knowledge pages → use `update_content` to append new findings
- captures → skip the write and note the existing page

## Content size limits

Notion API constrains each rich text element to ~2000 characters. For content longer than ~1500 words, split into multiple calls. Keep each payload focused; add long sections via follow-up update_content calls.

## Review markers

After pushing content to Notion, consider adding a **comment** instead of editing the page body when:
- marking that the content was reviewed or verified
- flagging something as stale
- adding metadata about when/why the page was created

Use the Comments API pattern from `references/mcp-commands.md`.

## Setup

Before using this skill, replace the placeholder page and database IDs in the reference files with your own Notion IDs.

Minimum setup:
- `references/page-map.md` — set the destinations you want to use for knowledge, work, content, finance, and inbox capture
- `references/mcp-commands.md` — replace every `YOUR_*_ID` placeholder with the matching Notion page or data source ID
- optional: rename destination labels to match your workspace, while preserving the routing logic

Recommended destination mapping:
- **Knowledge Hub** — durable notes, research, decisions, audits, rollups, relationship notes
- **Work Hub** — active execution artifacts, meeting prep, project plans, project status
- **Content Hub** — drafts, outlines, posts, newsletters, content experiments
- **Finance Hub** — durable financial summaries and snapshots
- **Inbox DB** — quick captures worth saving before full structuring

How to get your IDs:
- open the target page or database in Notion
- copy the page URL
- extract the 32-character page/database identifier from the URL
- use the page ID for top-level pages and the data source ID for databases such as Inbox DB

Do not ship or publish your private Notion IDs in shared repositories.

## Output expectations

When using this skill, return a compact operator-style summary:
- **Decision:** save / do not save / save to inbox
- **Destination:** exact Notion page or database
- **Format:** template used
- **Action:** command pattern chosen or write completed
- **Memory note:** whether the same content should also be logged to workspace memory

## References

- `references/page-map.md` — content type to destination routing
- `references/templates.md` — section templates by content type
- `references/mcp-commands.md` — exact Notion MCP command patterns with placeholder IDs
