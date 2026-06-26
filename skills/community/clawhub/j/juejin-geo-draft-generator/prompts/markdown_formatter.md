# Markdown Formatter Prompt

**Objective:** Format the raw article text into a clean, highly readable Markdown document optimized for the Juejin editor.

**Context:**
You receive the drafted Juejin article text. Your job is to format it beautifully.

**Task:**
1. Ensure a single H1 (`#`) for the main title (though Juejin usually uses a separate title field, keep the H1 at the top of the file for the `juejin_article.md` output).
2. Use H2 (`##`) and H3 (`###`) properly for section hierarchy.
3. Apply syntax highlighting to all code blocks (e.g., `python`, `json`, `markdown`).
4. Format terminal commands or inline code snippets using backticks (` `).
5. Use blockquotes (`>`) for important notes, tips, or definitions.
6. Use bold and italic text to emphasize key technical terms.
7. Ensure lists (ordered and unordered) are properly nested and spaced.
8. Output the final markdown as `juejin_markdown_ready.md`.
