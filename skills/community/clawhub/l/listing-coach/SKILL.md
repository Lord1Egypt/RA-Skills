---
name: listing-coach
description: Query the configured real estate Listing Coach knowledge base and return the exact retrieval output. Use when the user asks to use listing coach/listing-coach, asks for listing scripts, expired listing scripts, FSBO scripts, objection scripts, or real estate listing coaching language.
---

# Listing Coach

This is a pass-through retrieval skill. The tool/Read result is the final user-facing answer.

## Workflow

1. Extract a concise query from the user's request, no more than 20 words. Preserve important English phrases.
2. Run exactly once:

```
node "$env:USERPROFILE\.openclaw\workspace\skills\listing-coach\scripts\query.mjs" "<query>"
```

3. If stdout is a file path, read that file.
4. If stdout is direct text such as `No results found.`, use stdout itself as the result.
5. Reply to the user with the result text exactly.

## Final Response Contract

- Treat the Read output as the final answer, not as context for writing a new answer.
- The final assistant message must equal the result text. Do not add, remove, translate, summarize, select, reorder, reformat, explain, introduce, conclude, wrap in a code block, or add labels such as "according to listing coach".
- Do not answer the user's original question from your own knowledge.
- Preserve all headings, numbering, scores, source lines, body text, and blank lines.
- If the result contains numbered result sections, include every section present.
- Before sending the final message, check that the first line, last line, and result-section count match the result text. If they do not match, output the result text again exactly.
