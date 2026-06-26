# Feishu Workspace

**Turn OpenClaw into a Feishu-native teammate.**

Feishu Workspace brings **Feishu Docs**, **Wiki**, and **Bitable** into OpenClaw so your agent can do real team work directly from chat.

## Why this exists

A lot of teams already run on Feishu:

- Docs for notes and plans
- Wiki for internal knowledge
- Bitable for trackers and workflows

But most agent integrations stop at raw APIs or one-off demos.

**Feishu Workspace** is built for practical, everyday work:

- write meeting notes into docs
- search internal knowledge before answering
- update structured project tables
- turn messy conversations into useful team artifacts

## What it supports

### Feishu Docs
Read, write, append, and structure documents for notes, summaries, briefs, and reports.

### Feishu Wiki
Search and navigate knowledge spaces to find context, references, and internal documentation.

### Feishu Bitable
Create and update records for project tracking, action items, owners, deadlines, and status.

## Best use cases

### 1. Meeting notes
Summarize a discussion and write clear notes into a Feishu doc.

### 2. Knowledge lookup
Search the wiki before drafting, answering questions, or preparing proposals.

### 3. Project tracking
Extract action items from chat and write them into a Bitable with owner, due date, and status.

### 4. Team operations
Keep recurring docs and trackers updated without switching tools.

## Example prompts

- “Summarize this discussion and write it to our Feishu doc.”
- “Search the Feishu wiki for onboarding docs and give me a concise summary.”
- “Turn this conversation into action items and add them to our Bitable.”
- “Append today’s standup notes to the project doc.”
- “Create a project brief in Feishu based on this chat.”

## Who this is for

- Teams already using Feishu / Lark
- PMs and operators
- Founders and chiefs of staff
- Anyone who wants OpenClaw to work inside an existing team workflow

## Design goals

This skill is optimized for:

- high-frequency workflows
- clean outputs
- structured writing
- low-friction day-to-day use

It is intentionally focused on workflows people actually repeat, not just raw API surface area.

## Why install this

Because your team already works in Feishu.

Feishu Workspace helps OpenClaw operate inside the docs, knowledge base, and trackers you already use instead of forcing you into a separate tool or workflow.

## Notes

Available operations depend on:

- Feishu app scopes
- document permissions
- wiki access
- Bitable visibility and field configuration

If something fails, common causes include:

- missing app permissions
- missing access to a document or wiki node
- incorrect Bitable URL or table selection
- unsupported target type

## Roadmap

Planned improvements may include:

- stronger PM workflows
- cleaner document templates
- better knowledge-to-doc workflows
- richer Bitable helpers
- more opinionated team automation patterns

## License

MIT
