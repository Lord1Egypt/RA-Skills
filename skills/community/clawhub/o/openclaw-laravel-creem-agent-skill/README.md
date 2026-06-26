# Laravel Creem Agent — OpenClaw Skill

A single-file OpenClaw skill that connects the OpenClaw assistant to a running Laravel Creem Agent endpoint. Only `SKILL.md` is needed — no shell scripts required.

## Install

Copy the `SKILL.md` file into your OpenClaw workspace skills directory:

```bash
mkdir -p ~/.openclaw/workspace/skills/openclaw-laravel-creem-agent-skill
cp SKILL.md ~/.openclaw/workspace/skills/openclaw-laravel-creem-agent-skill/SKILL.md
```

If you are following the demo VM layout from this repository, the checked-out bundle lives at `/home/www`, so copy it from there:

```bash
mkdir -p ~/.openclaw/workspace/skills/openclaw-laravel-creem-agent-skill
cp /home/www/openclaw-laravel-creem-agent-skill/SKILL.md \
  ~/.openclaw/workspace/skills/openclaw-laravel-creem-agent-skill/SKILL.md
```

Or use the OpenClaw CLI:

```bash
# If published to ClawHub:
openclaw skills install openclaw-laravel-creem-agent-skill
```

## Configure

No extra skill config is required. This skill is intentionally hard-wired to the local demo endpoint:

```text
http://127.0.0.1:8000/creem-agent/chat
```

It is designed for the checked-in local demo stack running on the same machine as OpenClaw.

## Telegram setup

Configure Telegram natively in OpenClaw (`~/.openclaw/openclaw.json`):

```json5
{
  channels: {
    telegram: {
      botToken: "YOUR_BOT_TOKEN",
      allowFrom: ["YOUR_TELEGRAM_CHAT_ID"]
    }
  }
}
```

For a direct private chat with the bot, `allowFrom` can reuse the same numeric value as `message.chat.id`.

See https://docs.openclaw.ai/channels/telegram for details.

## Verify

Send a test message via OpenClaw (Telegram, WebChat, or CLI):

```
what is the store status?
How many succesful transactions were completed today?
```

The skill teaches the OpenClaw agent to forward your message to the Laravel endpoint and relay the response back.

## Troubleshooting

If Telegram answers with generic runtime text such as `Runtime: Direct`, the OpenClaw base assistant is replying directly and the skill was not selected.

Check these items in order:

```bash
sudo su - openclaw
test -f ~/.openclaw/workspace/skills/openclaw-laravel-creem-agent-skill/SKILL.md && echo "skill present"
curl -fsS -X POST http://127.0.0.1:8000/creem-agent/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"status","source":"openclaw"}'
```

If the `curl` call returns JSON with a `response` field, Laravel is reachable and the remaining problem is OpenClaw skill loading or skill selection.

After copying or editing `SKILL.md`, restart the gateway and test with store-specific prompts instead of generic assistant prompts:

```text
what is the store status?
how many customers paid today?
How many succesful transactions were completed today?
show recent transactions
any payment issues?
```

If the assistant says things like `I don't have transaction data loaded in this workspace yet` or asks where your transactions are stored, the skill still was not followed correctly. For store questions, it should call the Laravel endpoint first, not ask for local files.

This published skill does not support arbitrary endpoint overrides.
