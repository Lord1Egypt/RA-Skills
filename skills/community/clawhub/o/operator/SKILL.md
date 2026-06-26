---
name: operator
description: Manage your Operator fleet of AI agent instances. Create, configure, monitor, message, and manage OpenClaw agents. Handles authentication, instance lifecycle, secrets, automations, and webhooks.
---

# Operator Fleet Manager

This skill lets you manage your Operator fleet of OpenClaw agent instances by sending requests to the Operator chat API.

## When to Use This Skill

Use this skill when the user:
- Asks about their Operator instances or agents
- Wants to create, delete, restart, or configure instances
- Needs to check instance logs or status
- Wants to message a running agent
- Asks about secrets, automations, or webhooks
- Mentions "Operator", "fleet", or "OpenClaw"

## Authentication

### Step 1: Check for existing API key

Read the config file to check if the user is already logged in:

```bash
cat ~/.operator/config.json 2>/dev/null
```

Look for `operatorApiKey` (starts with `ck_`) and `operatorAppUrl` in the JSON. If the file exists and has a key, skip to "Using the API" below.

### Step 2: Login (if no key found)

If no API key is found, guide the user through browser-based login:

1. Generate a session ID:
```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

2. Tell the user to open this URL in their browser (replace `SESSION_ID` with the generated UUID):
```
https://www.operator.io/auth/cli?session=SESSION_ID
```

3. After the user confirms they've logged in, poll for the API key:
```bash
curl -s "https://www.operator.io/api/cli/poll?session=SESSION_ID"
```

The response will contain `operatorApiKey` when auth is complete.

4. Save the credentials:
```bash
mkdir -p ~/.operator
python3 -c "
import json
config = {'operatorApiKey': 'THE_KEY', 'operatorAppUrl': 'https://www.operator.io'}
with open('$HOME/.operator/config.json', 'w') as f:
    json.dump(config, f, indent=2)
print('Saved credentials to ~/.operator/config.json')
"
```

## Using the API

### Read credentials

```bash
OPERATOR_KEY=$(python3 -c "import json; c=json.load(open('$HOME/.operator/config.json')); print(c.get('operatorApiKey',''))")
OPERATOR_URL=$(python3 -c "import json; c=json.load(open('$HOME/.operator/config.json')); print(c.get('operatorAppUrl','https://www.operator.io'))")
```

### Health check

Verify auth is working:

```bash
curl -s "$OPERATOR_URL/api/cli/health" \
  -H "Authorization: Bearer $OPERATOR_KEY"
```

Returns `authenticated`, `email`, and `planName`.

### Send a request to the Operator manager

The Operator manager is an AI that has tools for managing your entire fleet. Send it natural language requests and parse the SSE response to extract text and tool results:

```bash
curl -sN "$OPERATOR_URL/api/chat" \
  -H "Authorization: Bearer $OPERATOR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","parts":[{"type":"text","text":"YOUR_MESSAGE_HERE"}]}]}' \
  | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line.startswith('data: '):
        continue
    try:
        event = json.loads(line[6:])
        t = event.get('type','')
        if t == 'text':
            print(event.get('value',''), end='')
        elif t == 'tool-result':
            result = event.get('result')
            if result is not None:
                print(json.dumps(result, indent=2))
        elif t == 'error':
            print('ERROR:', event.get('value',''))
    except:
        pass
print()
"
```

To continue a conversation (for follow-up requests), include the `id` field. The chat ID is returned in the stream's `start` event:

```bash
curl -sN "$OPERATOR_URL/api/chat" \
  -H "Authorization: Bearer $OPERATOR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"CHAT_ID","messages":[{"role":"user","parts":[{"type":"text","text":"YOUR_FOLLOWUP"}]}]}' \
  | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line.startswith('data: '):
        continue
    try:
        event = json.loads(line[6:])
        t = event.get('type','')
        if t == 'text':
            print(event.get('value',''), end='')
        elif t == 'tool-result':
            result = event.get('result')
            if result is not None:
                print(json.dumps(result, indent=2))
        elif t == 'error':
            print('ERROR:', event.get('value',''))
    except:
        pass
print()
"
```

### Understanding the SSE response

The API returns a Server-Sent Events stream. Each line is `data: {JSON}`. The important event types are:
- `{"type":"start"}` — stream started
- `{"type":"start-step"}` — the manager is beginning a step (may use tools)
- `{"type":"text","value":"..."}` — text response chunks (concatenate for full answer)
- `{"type":"tool-call","toolCallId":"...","toolName":"...","args":{}}` — the manager is calling a tool
- `{"type":"tool-result","toolCallId":"...","result":{}}` — tool result data (instance lists, config, logs, etc.)
- `{"type":"finish-step"}` — step complete
- `{"type":"finish","finishReason":"stop"}` — response complete

The python pipe above extracts just the text and tool results, giving you clean readable output. Always use this pipe when calling the API.

## What the Operator Manager Can Do

The manager has tools for:

- **Instances**: list, create, delete, restart, clone, get details, check capacity, get logs
- **Config**: update instance configuration (JSON patch), deploy skills, list/read/write workspace files
- **Agents**: message a running agent, check latest session activity
- **Secrets**: list user secrets, grant/revoke instance access
- **Automations**: list, create, update, delete scheduled cron automations
- **Webhooks**: list, create, update, delete webhook triggers
- **Checkpoints**: search and install agent checkpoint repos

## Important Notes

- Always read credentials from `~/.operator/config.json` before every API call.
- If a `401` error is returned, the API key may be expired. Run the login flow again.
- If a `429` error is returned, the user has hit their rate limit. Wait before retrying.
- The manager handles multi-step operations internally. Send one natural language request and it will use its tools as needed.
- Never expose the raw API key value to the user. Show only a masked version like `ck_...xxxx`.