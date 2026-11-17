---
name: markdown-summarizer
description: Summarize long markdown documents into structured key-point summaries. Use when a user pastes or points to a long markdown file and wants a concise structured summary with main sections, key findings, and action items.
metadata:
  openclaw:
    emoji: 📝
---

# Markdown Summarizer

Extract and summarize structured content from markdown documents.

## When to use

- User shares a long markdown document and wants a summary
- User needs to review meeting notes, design docs, or articles quickly
- User wants key points extracted without reading the whole file

## Input requirements

- A markdown file path or raw markdown text
- Optional: desired summary length (brief/standard/detailed)

## Steps

1. Read the full markdown content.
2. Identify top-level sections (`#` headings) and second-level sections (`##` headings).
3. For each major section, extract the core argument, data points, and conclusions.
4. Produce a structured summary:
   - **Overview** (1-2 sentences)
   - **Key Points** (bulleted, 3-8 items)
   - **Details by Section** (one paragraph per major section)
   - **Action Items / Next Steps** (if present in source)
5. If the document is >5000 words, first produce a section outline, then summarize each section separately.

## Output format

Return the summary as markdown with the structure above. Keep the total summary under 20% of the original length unless "detailed" is requested.

## Notes

- Preserve links and references from the original document.
- If the markdown contains tables, summarize the table data as text rather than reproducing the table.
- If the document is code-heavy, focus on the prose and note that code blocks exist without reproducing them.
