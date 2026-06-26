# Poe Connector — Agent Quick Reference

Run these with the **bash** tool. Nothing else works.

| Task | Command |
|---|---|
| Chat | `bash ~/.openclaw/workspace/skills/poe-connector/poe.sh chat <message>` |
| Image | `bash ~/.openclaw/workspace/skills/poe-connector/poe.sh image <prompt>` |
| Video | `bash ~/.openclaw/workspace/skills/poe-connector/poe.sh video <prompt>` |
| Audio | `bash ~/.openclaw/workspace/skills/poe-connector/poe.sh audio <text>` |
| List models | `bash ~/.openclaw/workspace/skills/poe-connector/poe.sh models` |
| Search models | `bash ~/.openclaw/workspace/skills/poe-connector/poe.sh search <keyword>` |

## ⚠ Sending generated media to the user

After image/video/audio generation, the script auto-downloads the file and prints a `[MEDIA_SEND_HINT]`.
**You MUST use the `message` tool to send the file** — do NOT embed URLs in markdown text.

```
message send --media "/path/to/poe_generated_image.png"
```

Telegram cannot render markdown images (`![alt](url)`) — only `sendPhoto` works, which the `message` tool handles.
