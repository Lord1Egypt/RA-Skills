---
name: Personal Knowledge Base
description: Help users build a personal knowledge base by organizing whatever they send into structured notes.
metadata: {"clawdbot":{"emoji":"🧠","os":["linux","darwin","win32"]}}
---

## Core Behavior
- User sends anything: link, idea, quote, snippet, question, rambling thought
- Capture first, organize second — never lose input while deciding where it goes
- Create `~/kb/` as the workspace — flat folder of Markdown files initially
- Inbox pattern: `inbox.md` for quick capture, process later into proper notes

## When User Sends Content
- Link → fetch title and summary, save with source URL and capture date
- Idea/thought → save as atomic note with descriptive filename
- Quote → save with attribution, link to source if available
- Question → save as note, mark for future research
- Long rambling → extract key points, save as separate atomic notes

## File Naming Convention
- Lowercase with hyphens: `how-to-negotiate-salary.md`
- Descriptive over date-based — findable by topic, not when captured
- No rigid hierarchy initially — flat folder with good names beats complex structure
- Date prefix optional for journals: `2024-01-15-weekly-review.md`

## Note Structure
- Title as H1 — matches filename concept
- Tags at top or bottom — `#productivity #career` for filtering
- Source/reference if applicable — where it came from
- Related notes section — manual links build knowledge graph
- Keep notes atomic — one concept per note, link between them

## Inbox Processing
- Periodically ask: "Want to process your inbox?"
- For each item: create proper note, add tags, link to related notes
- Delete from inbox once processed — inbox should trend toward empty
- Don't force immediate organization — capture friction kills usage

## When To Add Structure
- 20+ notes: suggest consistent tagging system
- 50+ notes: suggest index.md or MOC (Map of Content) for key topics
- 100+ notes: suggest folder structure by domain if patterns emerge
- Only add structure when navigation becomes painful

## Tagging Strategy
- Start with 5-10 broad tags maximum — too many defeats purpose
- Tags are for retrieval, not categorization — "when would I search for this?"
- Multi-tag allowed — note about salary negotiation: #career #communication
- Review and consolidate tags periodically — synonyms fragment knowledge

## Linking Between Notes
- [[wiki-style]] links when supported, otherwise relative Markdown links
- Link liberally — connections are the value of knowledge base
- Backlinks show where note is referenced — surface hidden connections
- Don't force links — some notes are standalone

## What User Might Send
- "Just learned that..." → atomic note with insight
- "Interesting article: [URL]" → fetch, summarize, save with source
- "Reminder: X" → capture with context, might become action or reference
- "I keep forgetting how to..." → create or update how-to note
- Random thought → inbox immediately, process later

## Searching and Retrieval
- Full-text search with grep or specialized tool — must be fast
- Search by tag: find all notes with specific tag
- Recent notes list — often want "that thing I saved last week"
- Offer to search when user asks a question — might already have the answer

## Progressive Enhancement
- Week 1: inbox.md only, dump everything
- Week 2: process inbox into atomic notes with tags
- Week 3: start linking related notes
- Month 2: create index/MOC for main topics
- Month 3: folder structure if needed

## What NOT To Suggest Early
- Complex folder hierarchies — flat with good names first
- Database or app — Markdown files work until they don't
- Daily notes system — unless they specifically want journaling
- Templates — organic structure emerges, then standardize

## Sync and Backup
- Cloud folder (Dropbox/iCloud) for multi-device access
- Git repo for version history — see how thinking evolved
- Plain Markdown ensures portability — not locked to any tool
