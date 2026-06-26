# Examples

Real-world usage patterns for the OpenClaw Microsoft Graph skill.

## Quick Links

- **[common_workflows.py](common_workflows.py)** — Email/calendar operations (daily standup, search, create events)
- **[llm_integration.py](llm_integration.py)** — How to integrate with OpenAI, Claude, etc.

## Running Examples

### Prerequisites

```bash
# Set up your Client ID first
cp ../config.example.ini ../config.ini
# Edit config.ini with your Client ID

# Authenticate
python ../scripts/auth.py login
```

### Common Workflows

```bash
python common_workflows.py --example standup     # Daily email + calendar summary
python common_workflows.py --example organize    # Folder organization pattern
python common_workflows.py --example search      # Search emails
python common_workflows.py --example unread      # Unread count by folder
python common_workflows.py --example create      # Create calendar event
```

### LLM Integration

```bash
python llm_integration.py
```

Shows how to:

1. Format email/calendar data for LLM context
2. Send to LLM (OpenAI, Claude, etc)
3. Parse structured responses
4. Execute resulting commands

## Pattern 1: Daily Standup

```python
from common_workflows import daily_standup

daily_standup()
# Outputs: Recent emails + today's events
```

## Pattern 2: Search & Filter

```python
from common_workflows import search_recent_emails

search_recent_emails("from:alice@example.com", days=7)
# Outputs: Matching emails with dates
```

## Pattern 3: Email Summary

```python
from common_workflows import email_summary

email_summary("<message-id>")
# Outputs: Message with HTML stripped and formatted
```

## Pattern 4: LLM Integration

```python
from llm_integration import EmailCalendarAssistant, format_inbox_for_context

# Get formatted context
context = format_inbox_for_context(10)

# Send to LLM
response = llm_client.chat.completions.create(
    messages=[
        {"role": "user", "content": f"Here's my email:\n{context}\nSummarize."}
    ]
)

# Process any actions in response
assistant = EmailCalendarAssistant()
assistant.process_llm_response(response.choices[0].message.content)
```

## Pattern 5: Folder Organization

```python
# List all folders
folders = graph_api.graph_get("/me/mailFolders", {"$select": "displayName"})

# Resolve custom folder by name
folder_id = mail.resolve_folder_id("Newsletters")

# Move a message
graph_api.graph_post(
    f"/me/messages/{msg_id}/move",
    {"destinationId": folder_id}
)
```

## Pattern 6: Create Events with Attendees

```python
from common_workflows import create_meeting

create_meeting(
    subject="Weekly Sync",
    attendees=["alice@example.com", "bob@example.com"],
    start_time="2026-03-10T14:00",
    end_time="2026-03-10T15:00"
)
```

## Error Handling

All examples handle common errors:

- **Not authenticated**: `auth.load_tokens()` returns None
- **API errors**: Caught and printed
- **Invalid input**: Validated before API calls

Example:

```python
try:
    result = graph_api.graph_get(path, params)
except Exception as e:
    print(f"Error: {e}")
```

## Extending Examples

Add your own patterns:

1. **Email processing pipeline**
   - Fetch inbox
   - Apply rules/filters
   - Archive, label, or summarize

2. **Calendar analytics**
   - Count meetings by attendee
   - Find free/busy slots
   - Suggest meeting times

3. **Notification system**
   - Check for unread emails every N minutes
   - Alert on specific senders or keywords
   - Post to Slack, Discord, etc.

4. **AI-powered summarization**
   - Format long emails
   - Create action items from meetings
   - Generate status updates

## Tips

- **Always check auth first**: `if not auth.load_tokens(): ...`
- **Use try/except for API calls** — network issues happen
- **Format results for users** — don't dump raw JSON
- **Respect rate limits** — Group operations if possible
- **Cache when appropriate** — Email subjects don't change every second

## See Also

- [Skill Guide](../skill.md) — Command reference
- [Setup Guide](../references/SETUP.md) — Auth and troubleshooting
- [API Reference](../references/api.md) — Microsoft Graph endpoints
