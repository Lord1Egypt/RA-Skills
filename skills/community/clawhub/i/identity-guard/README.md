# Identity Guard

Identity Guard is a safety skill for OpenClaw that blocks sensitive requests unless the sender is authorized by `sender_id` (not by display name).

## Quickstart (60 seconds)

Option A (auto, no CLI):
1. DM the bot with `/identity-guard init`.
2. Done. The bot sets `master_id` to your `sender_id` if none exists for that channel.

Option B (manual):
1. DM the bot with `/identity-guard whoami` and copy the `sender_id`.
2. Put it into `identities.json` as the channel `master_id` (edit manually or run `./scripts/init.sh`).
3. Verify `identities.json` contains your `master_id`.

If `identities.json` is missing, run `/identity-guard init` to create it from the template. Unconfigured configs still deny all sensitive requests by default.

## Files

- `SKILL.md` - The rules and trigger logic
- `identities.json` - Authorization config (required, created from template)
- `identities.template.json` - Template for identities.json
- `scripts/guard.sh` - Verification script used by the skill
- `scripts/whoami.sh` - Best-effort sender ID discovery from recent sessions
- `scripts/init.sh` - Interactive initialization for `identities.json`
- `scripts/add-user.sh` - Add allowlist entries

## identities.json format

```json
{
  "channels": {
    "feishu": {
      "master_id": "ou_xxxxx",
      "allowlist": []
    },
    "telegram": {
      "master_id": "123456789",
      "allowlist": []
    }
  },
  "global_allowlist": []
}
```

## Notes

- IDs are sensitive. In group chats, prefer DM for `/identity-guard whoami`.
- If `sender_id` metadata is missing or untrusted, the skill must deny sensitive requests.
- If a conversation existed before installing this skill, the assistant may respond using pre-existing context that didn't include the guard. In that case, start a new conversation to ensure the skill is applied.
- You can initialize in chat (no CLI): send `/identity-guard init` in a DM. The bot will set `master_id` to your `sender_id` only if no master is configured yet for that channel. If `/identity-guard init` is sent in a group chat, it should refuse and ask for DM instead.
