# Setup

## Files

Expected config file:

`~/.config/manus-openclaw-bridge/manus.env`

Example contents:

```bash
MANUS_API_KEY='your-manus-api-key'
MANUS_AGENT_PROFILE='manus-1.6'
MANUS_TASK_MODE='agent'
```

## Get the API key

- Docs: `https://open.manus.im/docs`
- Key entry: `http://manus.im/app?show_settings=integrations&app_name=api`
- REST base URL used by this skill: `https://api.manus.ai`

## Minimal API call

```bash
curl --request POST \
  --url 'https://api.manus.ai/v1/tasks' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header "API_KEY: $MANUS_API_KEY" \
  --data '{
    "prompt": "hello",
    "agentProfile": "manus-1.6",
    "taskMode": "agent"
  }'
```

## Environment notes

- Do not ship the actual key with the skill.
- Put the key on each machine separately.
- If a friend wants different defaults, change `MANUS_AGENT_PROFILE` or `MANUS_TASK_MODE` in their env file instead of editing scripts.
