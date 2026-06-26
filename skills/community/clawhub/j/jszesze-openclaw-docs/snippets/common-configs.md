# Verified OpenClaw config snippets

These are small snippets copied from current docs pages at cleanup time. Re-verify against fetched docs before editing a live config.

## Absolute minimum

Source: `gateway/configuration-examples`

```json5
{
  agent: { workspace: "~/.openclaw/workspace" },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

## Telegram quick setup

Source: `channels/telegram`

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Telegram pairing commands

Source: `channels/telegram`

```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

## Configuration pages to verify before edits

- `gateway/configuration`
- `gateway/configuration-reference`
- `gateway/configuration-examples`
