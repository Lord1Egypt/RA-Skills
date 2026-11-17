# Markdown Heading Syntax

## ATX vs Setext

- ATX: `# Heading 1`, `## Heading 2`, etc.
- Setext: `Heading 1\n===`, `Heading 2\n---`

When converting Setext to ATX:
- Line under `===` → `#`
- Line under `---` → `##`

## Rules

1. Headings should start at `#` for the document title.
2. No level skipping (e.g., `#` directly to `###`).
3. One blank line before and after a heading.
4. Maximum heading level: `#####` (5 levels deep).