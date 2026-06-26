---
name: personal-knowledge-hub
description: Record, organize, search, and connect personal knowledge. Use when the user wants to capture notes, build a knowledge base, search personal notes, review saved ideas, extract tags/entities, summarize learning material, or explore relationships between concepts. Supports English and Chinese requests such as 记录知识、整理笔记、搜索笔记、复习、个人知识库、知识图谱、第二大脑.
version: v0.2.0
tags: personal-knowledge, note-taking, knowledge-management, search, knowledge-graph
---

# Personal Knowledge Hub

## When To Use

Use this skill when the user wants help with:

- capturing a new note, idea, quote, article summary, book insight, or meeting takeaway
- searching or reviewing personal notes by keyword, topic, tag, or entity
- organizing scattered notes into a small knowledge structure
- extracting tags, titles, entities, and follow-up questions from raw text
- exploring relationships between concepts in a personal knowledge base

Chinese triggers include: 记录知识、整理笔记、知识管理、搜索笔记、复习、个人知识库、知识图谱、第二大脑、读书笔记、卡片笔记、知识沉淀.

## Workflow

1. Identify the request type:
   - `ingest`: capture/store a new knowledge item
   - `search`: find relevant notes or saved ideas
   - `analyze`: summarize and extract metadata from text or a topic
   - `explore`: build a lightweight concept graph
2. Use the smallest useful output:
   - for capture: title, tags, entities, note template, and next action
   - for search: ranked matches, snippets, matched terms, and related queries
   - for analysis: summary, tags, entities, and open questions
   - for graph: central topic, entities, connections, and missing links
3. Keep the user's own knowledge separate from generic advice. If no source knowledge is supplied, say that the result is based on the local sample/index only.

## Output Shape

Prefer structured JSON-like output when a tool or automation is calling the skill:

```json
{
  "status": "ok",
  "requestType": "search|ingest|analyze|explore",
  "message": "...",
  "results": []
}
```

For human-facing answers, summarize the useful result first, then include the structured fields only if they help the next action.

## Boundaries

Do:

- help organize user-owned notes and knowledge
- suggest tags, summaries, review prompts, and concept links
- identify gaps and next review actions

Do not:

- claim access to private notes unless they are supplied or connected by the environment
- invent citations, memories, or prior notes
- support unauthorized access, scraping, or data exfiltration

