# Blocks And Formatting Edge Cases

## Equation blocks

When writing an equation block, set `equation.expression` to the intended LaTeX content, not to a double-escaped display string.

Rules:
- Use normal LaTeX content such as `\int_0^1 x^2 \, dx = \frac{1}{3}`
- In a JSON payload, backslashes appear as `\\` because JSON escapes them; that does not mean the stored formula should contain doubled backslashes
- When reading an equation block back, distinguish between the JSON representation and the actual LaTeX content
- When reporting the value to the user, show the actual LaTeX content rather than the JSON-escaped form
- If a formula appears with doubled backslashes after writing, treat that as an escaping mistake and rewrite the block with the intended LaTeX expression

Example:

```bash
curl -sS -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: $NOTION_VERSION" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "object": "block",
        "type": "equation",
        "equation": {
          "expression": "\\int_0^1 x^2 \\, dx = \\frac{1}{3}"
        }
      }
    ]
  }' | jq
```

## Code content and table cells

When writing code-like content, distinguish between plain text that looks like code and rich text that is actually marked as code.

Rules:
- Backticks such as `` `x = 42` `` are only literal characters unless the API payload sets rich text annotations
- For inline code, use a rich text object with `"annotations": {"code": true}` instead of embedding backticks in the text
- Code blocks should be written as `type: "code"` blocks, not as paragraph text with triple backticks
- Table cells accept rich text arrays, but their UI rendering may differ from paragraph blocks
- In table cells, `annotations.code = true` can work for inline code styling; raw backticks usually render as normal text
- If the user wants reliable visible code formatting, prefer a paragraph with inline code or a dedicated code block over a table cell

When reading results back to the user:
- Do not claim inline code was created just because the text contains backticks
- Confirm whether the payload used `annotations.code = true`
- If the styling matters, mention that Notion UI rendering inside table cells may be more limited than in paragraphs

Example inline code rich text:

```json
{
  "type": "text",
  "text": {
    "content": "x = 42"
  },
  "annotations": {
    "code": true
  }
}
```

Example code block:

```json
{
  "object": "block",
  "type": "code",
  "code": {
    "language": "python",
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "print('hello')"
        }
      }
    ]
  }
}
```
