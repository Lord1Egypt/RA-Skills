# OpenClaw Integration

How to use the memegen skill with [OpenClaw](https://github.com/open-claw/openclaw).

## Installation

Copy the skill into your OpenClaw workspace:

```bash
# Option 1: Clone the repo as a skill
cd ~/.openclaw/workspace/skills/
git clone https://github.com/ArtemioPadilla/memegen-skill memegen

# Option 2: Just copy the files you need
mkdir -p ~/.openclaw/workspace/skills/memegen/references
cp SKILL.md ~/.openclaw/workspace/skills/memegen/
cp references/* ~/.openclaw/workspace/skills/memegen/references/
```

## How OpenClaw Discovers the Skill

OpenClaw reads the YAML frontmatter in `SKILL.md`:

```yaml
---
name: memegen
description: >
  Generate meme images using the memegen.link API. Use when the user asks to create,
  make, send, or generate a meme, funny image, reaction image, or similar request.
---
```

The `description` field is what OpenClaw uses to decide when to activate the skill. It matches against user messages.

## Delivering Memes

In OpenClaw, after downloading a meme image, deliver it using the `message` tool:

```python
# Download the meme
# curl -s -o /tmp/meme.png "https://api.memegen.link/images/drake/top/bottom.png"

# Send to a target (user, group, channel)
message(action="send", filePath="/tmp/meme.png", target="...", caption="Your caption here")
```

### Important: Always download first

memegen.link returns HTTP 404 status but valid image body — the OpenClaw gateway rejects 404 URLs. Always download to a local file first, then send the file.

## Meme History (Variety Rule)

OpenClaw agents can maintain a `references/meme-history.json` file to track recently used templates:

```json
{
  "history": [
    {"template": "drake", "date": "2026-04-05", "context": "coding meme"},
    {"template": "fine", "date": "2026-04-05", "context": "production outage"}
  ]
}
```

Check this before selecting a template to keep your memes varied. Keep only the last 20 entries.

## Platform-Specific Notes

### WhatsApp
- Send as `filePath` — URLs won't preview correctly due to the 404 issue
- Keep captions short
- GIFs work with `gifPlayback: true`

### Discord
- Can send as file attachment or embed
- Consider using `caption` for the meme context

### Telegram
- Send as photo or document
- Use `caption` for text
