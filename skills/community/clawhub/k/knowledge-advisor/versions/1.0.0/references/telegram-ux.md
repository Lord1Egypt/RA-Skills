# Telegram UX Reference

Patterns and guidelines for delivering knowledge-advisor responses through OpenClaw's Telegram channel.

## Constraints

| Constraint | Limit | Design Response |
|-----------|-------|----------------|
| Message length | ~4,096 characters | Split at 3,000 chars; send as multiple messages |
| No filesystem paths | Users send files as attachments or URLs | Never ask for a path; accept attachments and URLs |
| No rich UI | No buttons, dropdowns, forms | Use numbered lists for choices; natural language |
| Linear conversation | No parallel threads | Multi-turn flows must be sequential |
| Markdown support | Limited (bold, italic, code, links) | Use bold for emphasis; avoid tables |

## Response Length Rules

1. Advisory responses: aim for 1,500-2,500 characters.
2. If response exceeds 3,000 characters, split into logical parts:
   - Part 1: Primary framework + application steps
   - Part 2: Anti-patterns + related frameworks + not-in-KB gaps
3. Ingestion summaries: can be longer (up to 3,000) since user expects detail.
4. Health reports: keep under 1,500 characters.
5. List/search results: keep under 2,000 characters.

## Splitting Strategy

When splitting a long response:
- End each part with a natural break (after a complete section)
- Do NOT add "continued..." or "Part 1 of 2" headers
- Send parts back-to-back so they appear as a natural flow
- The final part should end with a call-to-action

## Formatting for Telegram

### Do
- **Bold** for framework names and key terms
- Emoji for visual anchors (sparingly): 🎯 📖 ✅ ❌ ⚠️ 📊 📋
- Short bullet points (1-2 lines each)
- Numbered lists for steps
- Line breaks between sections
- Indented arrows (→) for specific examples or scripts

### Do Not
- Tables (render as plain text in Telegram — hard to read)
- Code blocks for non-code content
- Long paragraphs (break into bullets)
- Multiple emoji per line
- Headers (# marks) — Telegram doesn't render them; use **bold** instead

## Ingestion Flow in Telegram

**From file attachment:**
```
[User sends file attachment]
User: Please ingest this book

→ Acknowledge: "I'll extract knowledge from this material. Reading now..."
→ Present summary (numbered items, suggested tags)
→ Ask for review: "Please review. You can correct, add, remove, or say 'finalize'."
→ Wait for user response
→ Apply corrections, confirm each
→ On "finalize": commit + show health status
```

**From URL:**
```
User: Please ingest this article https://example.com/leadership-guide

→ Acknowledge: "I'll fetch and extract knowledge from this page. Reading now..."
→ Fetch the URL content
→ Same extraction and review flow as file attachment
→ Store source_type as "url" and source URL in meta.json
```

**URL-specific notes:**
- The user sends a URL in the chat message (no file attachment needed)
- Use the web fetch tool to retrieve the page content
- If the URL is unreachable or behind authentication, tell the user: "I couldn't access this URL. Please paste the content directly or send it as a file."
- Store the source URL in meta.json for reference
- Treat web content the same as any other source once fetched

## Advisory Flow in Telegram

```
User: [describes situation]

→ Lead with primary framework (🎯 + 📖 citation)
→ Application steps (numbered, with → examples)
→ Anti-pattern warning (⚠️)
→ Related frameworks (📖)
→ Not-in-KB declaration (❌) if applicable
→ Call-to-action ("Want me to help draft this?" / "Need more detail?")
```

## Call-to-Action Templates

End advisory messages with one of:
- "Would you like me to help draft this conversation?"
- "Want more detail on any of these frameworks?"
- "Should I search for related frameworks?"
- "Need me to walk through the steps in more detail?"

End ingestion messages with:
- "Anything else to correct, or shall I finalize?"
- "Would you like to review the extracted frameworks in detail?"

End health reports with:
- "Would you like me to explain the upgrade steps?"
- "Shall I perform the recommended restructure now?"

## Error Handling

- If the knowledge base doesn't exist: "Your knowledge base is empty. Send me a book or material to get started!"
- If a file can't be read: "I couldn't read this file. Please try sending it in a different format (PDF, text, or paste the content directly)."
- If no frameworks match: Use the standard "not in KB" pattern from advisor-patterns.md.
