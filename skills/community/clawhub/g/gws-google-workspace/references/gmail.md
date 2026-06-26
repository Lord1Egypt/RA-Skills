# Gmail Reference

## Helper Commands

```bash
gws gmail +triage                                                          # Unread inbox summary
gws gmail +read --params '{"userId":"me","id":"MSG_ID"}'                   # Read message body
gws gmail +reply --params '{"userId":"me","id":"MSG_ID"}' --json '{"body":"Reply"}'
gws gmail +reply-all --params '{"userId":"me","id":"MSG_ID"}' --json '{"body":"Reply"}'
gws gmail +forward --params '{"userId":"me","id":"MSG_ID"}' --json '{"to":"x@example.com"}'
gws gmail +send --json '{"to":"x@example.com","subject":"Hi","body":"Text"}'
gws gmail +watch                                                           # Stream new emails (NDJSON)
```

## Search Syntax

Pass via `q` parameter: `is:unread`, `is:starred`, `from:xxx`, `subject:keyword`, `label:xxx`, `has:attachment`, `newer_than:1d`, `after:YYYY/MM/DD`, `before:YYYY/MM/DD`, `category:primary|promotions|social|updates|forums`.

## List and Read

```bash
gws gmail users messages list --params '{"userId":"me","q":"is:unread","maxResults":20}'
gws gmail users messages list --params '{"userId":"me","q":"is:unread"}' --page-all

# Headers (match by name, not index)
gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"metadata","metadataHeaders":["From","Subject","Date"]}' \
  2>/dev/null | tail -n +2 | jq '.payload.headers | map({(.name): .value}) | add'

# Quick preview (no base64, length-limited)
gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"metadata"}' \
  2>/dev/null | tail -n +2 | jq -r '.snippet'
```

## Parallel Batch Read

Use `&` + `wait` to read N messages in ~3s instead of N×3s:

```bash
IDS=$(gws gmail users messages list --params '{"userId":"me","q":"is:unread","maxResults":10}' 2>/dev/null | tail -n +2 | jq -r '.messages[].id')
for id in $IDS; do
  gws gmail users messages get --params "{\"userId\":\"me\",\"id\":\"$id\",\"format\":\"metadata\",\"metadataHeaders\":[\"From\",\"Subject\",\"Date\"]}" \
    2>/dev/null | tail -n +2 | jq -r '.payload.headers | map({(.name): .value}) | add | "\(.From[:30]) | \(.Subject) — \(.Date)"' &
done; wait
```

## Batch Modify (up to 1000 IDs)

```bash
IDS=$(gws gmail users messages list --params '{"userId":"me","q":"is:unread","maxResults":100}' 2>/dev/null | tail -n +2 | jq -c '[.messages[].id]')
gws gmail users messages batchModify --params '{"userId":"me"}' --json "{\"ids\":$IDS,\"removeLabelIds\":[\"UNREAD\"]}"
```

## Single Message Modify

```bash
gws gmail users messages modify --json '{"removeLabelIds":["UNREAD"]}' --params '{"userId":"me","id":"MSG_ID"}'
gws gmail users messages modify --json '{"addLabelIds":["STARRED"],"removeLabelIds":["INBOX"]}' --params '{"userId":"me","id":"MSG_ID"}'
```

## Send Email

```bash
# Plain text
RAW=$(printf "To: x@example.com\r\nSubject: Hello\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nBody text" | base64 -w0)
gws gmail users messages send --json "{\"raw\":\"$RAW\"}" --params '{"userId":"me"}'

# HTML
RAW=$(printf "To: x@example.com\r\nSubject: Hello\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>Title</h1><p>Body</p>" | base64 -w0)
gws gmail users messages send --json "{\"raw\":\"$RAW\"}" --params '{"userId":"me"}'
```

## Attachments

```bash
# List attachments
gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}' \
  2>/dev/null | tail -n +2 | jq '[.payload.parts[] | select(.filename != "") | {filename, attachmentId: .body.attachmentId}]'

# Download (cd to target directory first)
cd /path/to/dir
gws gmail users messages attachments get --params '{"userId":"me","messageId":"MSG_ID","id":"ATT_ID"}' --output file.pdf
```

## Threads

```bash
gws gmail users threads list --params '{"userId":"me","q":"is:unread","maxResults":10}'
gws gmail users threads get --params '{"userId":"me","id":"THREAD_ID","format":"metadata"}'
```

## Labels

```bash
gws gmail users labels list --params '{"userId":"me"}' 2>/dev/null | tail -n +2 | jq '.labels[] | {id, name, type}'
gws gmail users labels get --params '{"userId":"me","id":"INBOX"}'
gws gmail users labels create --json '{"name":"Projects/AI","labelListVisibility":"labelShow","messageListVisibility":"show"}' --params '{"userId":"me"}'
```

## Trash / Settings

```bash
gws gmail users messages trash --params '{"userId":"me","id":"MSG_ID"}'
gws gmail users messages untrash --params '{"userId":"me","id":"MSG_ID"}'
gws gmail users settings getVacation --params '{"userId":"me"}'
gws gmail users settings sendAs list --params '{"userId":"me"}'
```
