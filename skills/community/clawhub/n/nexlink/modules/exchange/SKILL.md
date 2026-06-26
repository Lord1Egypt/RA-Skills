---
name: exchange
description: Email, Calendar, and Tasks for Exchange on-premises (2016/2019). Use for reading/sending emails, managing calendar events, creating tasks, and syncing with Exchange server. Triggers on phrases like "send email", "check calendar", "create task", "exchange mail", "outlook calendar".
---

# Exchange Module

Email, Calendar, and Tasks operations for Microsoft Exchange Server on-premises (2016/2019) via EWS.

## Requirements

- Exchange Server 2016 or 2019 (on-premises)
- EWS enabled on server
- Account with mailbox permissions

## Configuration

Set environment variables:

```bash
export EXCHANGE_SERVER="https://mail.example.com/EWS/Exchange.asmx"
export EXCHANGE_USERNAME="your-username"
export EXCHANGE_PASSWORD="your-password"
export EXCHANGE_EMAIL="your-email@example.com"
```

Or use a config file `config.yaml`:

```yaml
exchange:
  server: https://mail.example.com/EWS/Exchange.asmx
  username: ${EXCHANGE_USERNAME}
  password: ${EXCHANGE_PASSWORD}
  email: your-email@example.com
  verify_ssl: false  # for self-signed certs
```

## Commands

### Email (mail)

```bash
# Test connection
python3 -m modules.exchange mail connect

# List emails
python3 -m modules.exchange mail read --limit 10
python3 -m modules.exchange mail read --folder Inbox --unread
python3 -m modules.exchange mail read --from "boss@company.com"

# Send email
python3 -m modules.exchange mail send --to "user@example.com" --subject "Hello" --body "Message"

# Reply/Forward
python3 -m modules.exchange mail reply --id EMAIL_ID --body "Reply text"
python3 -m modules.exchange mail forward --id EMAIL_ID --to "other@example.com"

# Attachments
python3 -m modules.exchange mail list-attachments --id EMAIL_ID
python3 -m modules.exchange mail download-attachment --id EMAIL_ID --name "file.pdf"
```

### Calendar (cal)

```bash
# List events
python3 -m modules.exchange cal list --days 7
python3 -m modules.exchange cal today
python3 -m modules.exchange cal week

# Create event
python3 -m modules.exchange cal create --subject "Meeting" --start "2024-01-15 14:00" --duration 60

# With attendees
python3 -m modules.exchange cal create --subject "Team Meeting" --start "2024-01-15 14:00" --to "user1@example.com,user2@example.com"

# Update/Delete
python3 -m modules.exchange cal update --id EVENT_ID --location "Room 101"
python3 -m modules.exchange cal delete --id EVENT_ID

# Respond to meeting
python3 -m modules.exchange cal respond --id EVENT_ID --response accept
```

### Tasks (tasks)

```bash
# List tasks (own mailbox)
python3 -m modules.exchange tasks list
python3 -m modules.exchange tasks list --overdue
python3 -m modules.exchange tasks list --status in_progress

# List tasks from another mailbox (delegate access)
python3 -m modules.exchange tasks list --mailbox user@example.com

# Create task (in your own mailbox)
python3 -m modules.exchange tasks create --subject "Review proposal" --due "+7d" --priority high

# Create task in another user's mailbox (requires delegate permissions)
python3 -m modules.exchange tasks create --assign-to user@example.com --subject "Review report" --due "2024-01-20"

# Get task details
python3 -m modules.exchange tasks get --id TASK_ID
python3 -m modules.exchange tasks get --id TASK_ID --mailbox user@example.com

# Update task
python3 -m modules.exchange tasks update --id TASK_ID --subject "Updated subject"
python3 -m modules.exchange tasks update --id TASK_ID --status in_progress

# Complete task
python3 -m modules.exchange tasks complete --id TASK_ID

# Move task to Deleted Items (trash)
python3 -m modules.exchange tasks trash --id TASK_ID
python3 -m modules.exchange tasks trash --mailbox user@example.com --id TASK_ID  # Requires delete permission
```

**Note on trash:** The `trash` command moves tasks to the Deleted Items folder. For delegate mailboxes, the service account has Editor permissions (can create/edit/complete tasks) but **cannot delete tasks**. This is intentional - tasks are preserved until you manually delete them from Outlook. When trash fails, the error message suggests completing the task or deleting manually from Outlook.

### Error Handling

All task commands return informative error messages in Romanian with:

- `error`: Clear error message
- `cause`: Why it happened
- `alternatives`: Available options

**Example - Permission denied:**
```json
{
  "ok": false,
  "error": "Task-urile pot fi șterse doar manual din Outlook.",
  "cause": "Asistentul are permisiuni de Editor (poate crea/edita/completa), dar nu poate șterge task-urile. Aceasta e o limitare intenționată - task-urile se păstrează până le ștergi tu.",
  "alternatives": [
    {"action": "complete", "description": "Marchează task-ul ca finalizat (recomandat)"},
    {"action": "manual_delete", "description": "Șterge manual din Outlook sau OWA"}
  ]
}
```

**Example - Task not found:**
```json
{
  "ok": false,
  "error": "Task-ul nu a fost găsit.",
  "cause": "Task ID xxx nu există sau este invalid.",
  "alternatives": [
    {"action": "list", "description": "Listează task-urile disponibile"}
  ]
}
```

### Sync (sync)

```bash
# Bidirectional sync with Exchange
python3 -m modules.exchange sync sync

# Show sync status
python3 -m modules.exchange sync status

# Send reminders for overdue/upcoming tasks
python3 -m modules.exchange sync reminders --hours 24

# Dry-run (show what would be sent)
python3 -m modules.exchange sync reminders --hours 24 --dry-run

# Create calendar event from task
python3 -m modules.exchange sync link-calendar --id TASK_ID --time "14:00" --duration 60
```

## Notes

- Tasks are created in your own Tasks folder by default
- **Task Assignment**: Use `--assign-to user@example.com` to create tasks directly in another user's Exchange mailbox. This requires the service account to have delegate permissions on the target mailbox (configured on the Exchange server).
- For collaborative tasks, use calendar events with attendees
- For Exchange Online (Office 365), configuration may differ
- Self-signed certificates require `verify_ssl: false`