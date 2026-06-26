# Missing Frontmatter Skill

## When to Use
- "test error handling"

## Process

```code
Unclosed code block

### Broken Header Hierarchy (### before ##)

This is intentionally malformed to test parser error handling.
- No YAML frontmatter (name, description missing)
- Unclosed code block above
- Header hierarchy violation (### without parent ##)
- Missing trigger section format
