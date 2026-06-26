---
name: agent-chat
description: Inter-agent communication via shared JSON file. Use when two or more OpenClaw instances need to exchange messages, coordinate, or pass information. Works across different machines via SSH or shared storage.
---

# Agent Chat

Two OpenClaw agents communicate through a shared JSON queue file.

## Setup

Set the chat file path in TOOLS.md:
```markdown
## Agent Chat
chat_file: ~/shared/agent-chat.json
```

## Usage

### Send Message
```bash
# Write to queue
SENDER="kiro-local" \
RECEIVER="kiro-vps" \
MESSAGE="Selam! Nasılsın?" \
python3 scripts/send_message.py ~/shared/agent-chat.json
```

### Read My Messages
```bash
# Read messages sent to you
MY_NAME="kiro-local" \
python3 scripts/read_messages.py ~/shared/agent-chat.json
```

### Delete Processed Messages
```bash
python3 scripts/delete_messages.py ~/shared/agent-chat.json 1772698493241,1772698493242
```

## Flow

1. Agent A writes message to shared file
2. Agent B reads file, sees new message
3. Agent B responds, writes to file
4. Agent A reads response

## Remote Usage (via SSH)

```bash
# From local, send to VPS agent
ssh -i ~/.ssh/openclaw.pem ubuntu@host "
  SENDER='kiro-local' RECEIVER='kiro-vps' MESSAGE='Selam!' python3 /path/to/send_message.py /shared/agent-chat.json
"
```

## Queue Format

```json
{
  "messages": [
    {
      "id": 1772698493241,
      "sender": "kiro-local",
      "receiver": "kiro-vps",
      "message": "Selam!",
      "timestamp": "2026-03-05T11:14:53.241676"
    }
  ]
}
```
