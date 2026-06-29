# append_note

## Names

- MCP: `append_note`
- OpenFang: `mcp_note-sync_append_note`

## Parameters

| Name | Type | Required |
|------|------|----------|
| `title` | string | yes |
| `content` | string | yes |

## Response

- OK: `已保存笔记：{title}`
- Error: message string

## Storage

File: `$NOTE_SYNC_REPO/mcp-server/notes/{sanitized_title}.md`

Sanitization: replace `\ / : * ? " < > |` and spaces with `_`.

## Entry format

```markdown
## YYYY-MM-DD HH:MM:SS
# {title}
{content}


```
