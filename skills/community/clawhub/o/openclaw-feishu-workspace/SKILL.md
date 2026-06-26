---
name: Feishu Workspace
description: Use when the user wants to work with Feishu Docs, Wiki, or Bitable for practical team workflows such as meeting notes, knowledge lookup, and project tracking.
---

# Feishu Workspace

Use this skill when a request involves Feishu/Lark content or workflows.

## Primary areas

- Feishu Docs
- Feishu Wiki
- Feishu Bitable

## Use this skill for

- writing or updating Feishu docs
- searching wiki knowledge before answering or drafting
- creating and updating Bitable records
- turning conversations into structured team artifacts
- supporting lightweight PM and ops workflows in Feishu

## Preferred workflow

1. First identify the target surface:
   - doc
   - wiki
   - bitable

2. Prefer structured, useful outputs over raw dumps.

3. For docs:
   - use short sections
   - use bullets where appropriate
   - make outputs immediately readable by humans

4. For wiki:
   - search before drafting when internal context matters
   - summarize findings clearly
   - cite page titles or locations when useful

5. For bitable:
   - inspect table metadata and fields before writing when a URL is provided
   - map values carefully into the right columns
   - prefer fewer, more structured writes

## Output style

When generating Feishu content:
- concise
- clean
- structured
- useful to a real teammate

Avoid:
- long fluff
- vague summaries
- unstructured walls of text

## High-value workflows

- meeting notes → doc
- internal knowledge lookup → summary
- action items → bitable
- standup updates → project doc
- planning discussion → structured brief

## Failure handling

If an operation fails, explain the likely cause clearly:
- missing app scope
- missing file/document access
- unsupported target type
- invalid URL/token/table selection

## Not for

- unrelated non-Feishu requests
- giant migrations unless the user explicitly wants a staged plan
- blind table writes without understanding the fields
