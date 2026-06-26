# Common Workflow Examples

All examples assume you have a `SESSION_ID` from creating a session.
Base URL: `https://motion-mcp-server.fly.dev`

## Connect with Agent Token (Preferred)

```bash
# Create workspace-only session with agent token
curl -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"agent_token": "YOUR_TOKEN", "agent_name": "Claude"}'

# Or connect to a specific document immediately
curl -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"agent_token": "YOUR_TOKEN", "document_id": "DOC_ID", "agent_name": "Claude"}'

# Read the document
curl $BASE/sessions/$SID/document
```

## Connect with Invite Token (Legacy)

```bash
# Create session with invite token
curl -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"document_id": "DOC_ID", "invite_token": "TOKEN", "agent_name": "Claude"}'
```

## Browse Pages First, Then Edit

```bash
# Create workspace-only session
curl -X POST $BASE/sessions \
  -H "Content-Type: application/json" \
  -d '{"agent_token": "YOUR_TOKEN", "agent_name": "Claude"}'

# List all pages
curl $BASE/sessions/$SID/pages

# Connect to a specific page
curl -X POST $BASE/sessions/$SID/connect \
  -H "Content-Type: application/json" \
  -d '{"document_id": "PAGE_ID_FROM_LIST"}'

# Now you can read and edit
curl $BASE/sessions/$SID/document
```

## Insert a Formatted Paragraph

By default, edits are in suggestion mode. Pass `"mode": "direct"` to apply immediately.

```bash
curl -X POST $BASE/sessions/$SID/blocks \
  -H "Content-Type: application/json" \
  -d '{
    "index": -1,
    "block": {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "This is " },
        { "type": "text", "text": "bold", "marks": [{ "type": "bold" }] },
        { "type": "text", "text": " and " },
        { "type": "text", "text": "linked", "marks": [{ "type": "link", "attrs": { "href": "https://example.com" } }] },
        { "type": "text", "text": " text." }
      ]
    }
  }'
```

## Create a Bullet List

```bash
curl -X POST $BASE/sessions/$SID/blocks \
  -H "Content-Type: application/json" \
  -d '{
    "index": -1,
    "block": {
      "type": "bulletList",
      "content": [
        { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "First item" }] }] },
        { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Second item" }] }] },
        { "type": "listItem", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Third item" }] }] }
      ]
    }
  }'
```

## Bold Existing Text

```bash
curl -X POST $BASE/sessions/$SID/blocks/$BLOCK_ID/format-by-match \
  -H "Content-Type: application/json" \
  -d '{ "text": "important word", "mark": "bold" }'
```

## Find and Replace

```bash
curl -X POST $BASE/sessions/$SID/blocks/$BLOCK_ID/replace \
  -H "Content-Type: application/json" \
  -d '{ "search": "old phrase", "replacement": "new phrase" }'
```

## Leave a Comment

```bash
# Create a comment thread
curl -X POST $BASE/sessions/$SID/comments \
  -H "Content-Type: application/json" \
  -d '{ "body": "This section needs more examples." }'

# Reply to the thread
curl -X POST $BASE/sessions/$SID/comments/$THREAD_ID/reply \
  -H "Content-Type: application/json" \
  -d '{ "body": "I will add some now." }'

# Resolve when done
curl -X POST $BASE/sessions/$SID/comments/$THREAD_ID/resolve
```

## Save a Version Before Big Changes

```bash
curl -X POST $BASE/sessions/$SID/versions \
  -H "Content-Type: application/json" \
  -d '{ "label": "Before restructure" }'
```

## Review Suggestions

```bash
# List all pending suggestions
curl $BASE/sessions/$SID/suggestions

# Accept a specific suggestion
curl -X POST $BASE/sessions/$SID/suggestions/$SUGGESTION_ID/accept

# Reject a specific suggestion
curl -X POST $BASE/sessions/$SID/suggestions/$SUGGESTION_ID/reject

# Accept all suggestions at once
curl -X POST $BASE/sessions/$SID/suggestions/accept-all
```

## Export as Markdown

```bash
curl "$BASE/sessions/$SID/export?format=markdown"
```

## Create a New Page and Edit It

```bash
# Create a page and connect to it in one step
curl -X POST $BASE/sessions/$SID/pages \
  -H "Content-Type: application/json" \
  -d '{ "title": "Meeting Notes - March 20", "auto_connect": true }'

# Response includes `connected: true` and `document_id`
# You can now immediately read and edit the new page
curl $BASE/sessions/$SID/document
```

## Create a Page Without Connecting

```bash
# Create a page without switching to it
curl -X POST $BASE/sessions/$SID/pages \
  -H "Content-Type: application/json" \
  -d '{ "title": "Draft Ideas" }'

# Connect to it later when ready
curl -X POST $BASE/sessions/$SID/connect \
  -H "Content-Type: application/json" \
  -d '{"document_id": "PAGE_ID_FROM_RESPONSE"}'
```

## Disconnect

```bash
curl -X DELETE $BASE/sessions/$SID
```
