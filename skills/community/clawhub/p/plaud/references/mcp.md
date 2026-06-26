# Plaud MCP Reference

## Tools

| Tool | Use |
| --- | --- |
| `plaud__login` | Start OAuth sign-in |
| `plaud__logout` | Revoke auth |
| `plaud__get_current_user` | Verify auth and current account |
| `plaud__list_files` | List recordings, optionally filtered |
| `plaud__get_file` | Get detailed metadata for a recording |
| `plaud__get_note` | Get AI notes, summaries, action items, and topics |
| `plaud__get_transcript` | Get timestamped transcript and speakers |

## `plaud__list_files`

Parameters:

- `page`: default 1
- `page_size`: use 10 or higher
- `query`: case-insensitive name search
- `date_from`: `YYYY-MM-DD`
- `date_to`: `YYYY-MM-DD`

Notes:

- Some implementations reject `page_size` below 10.
- When filters are set, the MCP may scan multiple pages client-side.

## Empty notes or transcript

If `get_note` or `get_transcript` returns an empty array, do not invent content. State that no generated note or transcript is available. If metadata shows a very short duration, mention that this is likely why.

## Speaker handling

Only list speakers when transcript segments include speaker attribution. If speaker labels are generic, preserve them as given, for example `Speaker 1`, `Speaker 2`.
