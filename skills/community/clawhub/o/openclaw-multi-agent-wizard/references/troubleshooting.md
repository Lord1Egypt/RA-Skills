# Troubleshooting

Use this only when verification fails or the user gets stuck.

## Goal

Give one next action, not a giant theory dump.

## Common failure branches

### Gateway is not running

Say:

- "Your gateway is not running yet. I will start it first."

Then start it or guide the user through the single needed step.

### Feishu bot is configured but does not reply

Check:

- bot was added to the right Feishu group
- the app was published
- event subscription is using long connection WebSocket
- `im.message.receive_v1` was added
- credentials were written correctly
- bindings exist
- gateway was restarted after config changes

Say:

- "The bot is connected, but I still need to confirm the group binding. Please send one message in that group so I can identify it."

### Group routing is not working

Say:

- "I need one fresh message from that Feishu group so I can verify which group OpenClaw sees."

Then inspect local logs or state instead of asking the user to find technical IDs manually.

Helpful command:

```bash
openclaw logs --follow
```

### Existing config looks messy

Say:

- "You already have older multi-agent or Feishu settings. I will avoid overwriting them and add only the new pieces."

### Verification still fails after restart

Say:

- "The setup changes are saved, but the gateway still does not look healthy. I will check the local status and logs next."

Helpful commands:

```bash
openclaw gateway status
openclaw gateway restart
openclaw logs --follow
```

### The user feels overwhelmed

Say:

- "We can slow this down. Let’s finish just one bot or one group first, then repeat the same pattern."

## Rule for wording

- Always give the user one next move.
- Avoid listing many possible causes at once.
- Do the local inspection work yourself when possible.
