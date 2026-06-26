# Security Notes

This skill is designed to be smart-triggered and reviewable.

## Security Posture

- No automatic every-turn recall
- No hook-level silent background save
- No direct reads from `~/.openclaw/secrets.json`
- No direct reads from per-skill `config.json`
- No server-supplied upgrade URL execution or display
- Configuration comes from OpenClaw config or injected environment variables only

## What Triggers Network Requests

Network requests happen only when the agent or user runs one of these commands:

- `recall`
- `search`
- `save`
- `save-batch`

If you do not invoke the skill, it does not contact the remote service.

## What Data Is Sent

### `recall` / `search`

Sent to the memory service:

- `query`
- `user_id`
- `agent_id`
- retrieval settings such as `memory_limit_number` and `min_score`

### `save` / `save-batch`

Sent to the memory service:

- the message content you explicitly provide
- `user_id`
- `agent_id`
- generated `conversation_id`
- fixed tag `openclaw-skill`
- session metadata used to group that save request

## What Is Not Read Or Sent

- `~/.openclaw/secrets.json`
- per-skill local `config.json`
- arbitrary local files
- shell history
- unrelated environment variables
- browser data

## Configuration Model

Recommended OpenClaw paths:

- `skills.entries.human-like-memory.apiKey`
- `skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_BASE_URL`
- `skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_USER_ID`
- `skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AGENT_ID`

OpenClaw injects these values into the process environment at runtime. The CLI then reads only:

- `HUMAN_LIKE_MEM_API_KEY`
- `HUMAN_LIKE_MEM_BASE_URL`
- `HUMAN_LIKE_MEM_USER_ID`
- `HUMAN_LIKE_MEM_AGENT_ID`
- optional tuning env vars such as `HUMAN_LIKE_MEM_LIMIT_NUMBER`

The code uses an explicit allowlist for these variables and does not iterate through or upload the broader process environment.

This skill no longer depends on registry secret-form metadata or a bundled setup script. Configuration is expected to be done through `openclaw config set ...` or by explicit environment injection.

## Privacy Guidance

- Only send content you are comfortable storing on your configured memory server
- Do not send passwords, private keys, tokens, or other secrets
- Review the server privacy policy before use: https://plugin.human-like.me/privacy

## Source Code

- GitHub: https://github.com/humanlike2026/humanlike-memory
- ClawHub: https://clawhub.ai/humanlike2026/humanlike-memory
