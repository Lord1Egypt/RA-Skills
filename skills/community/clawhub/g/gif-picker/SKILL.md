---
name: gif-picker
description: "Select and send local reaction GIFs by tag — pat-on-back, celebration, salute, facepalm, etc."
homepage: https://github.com/mirza-alam/openclaw-gif-picker
emoji: 🖼️
requires:
  bins: [python3]
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins: [python3]
    install:
      - id: setup
        kind: setup
        label: "Create GIF library directory"
        run: "mkdir -p {baseDir}/gifs"
      - id: populate
        kind: populate
        label: "Download sample reaction GIFs"
        run: "bash {baseDir}/populate.sh"
---

# GIF Picker

Select and send local reaction GIFs by tag without depending on third-party CDNs or API keys.

## The Problem

OpenClaw agents can attach media via `MEDIA:<path-or-url>`. But Tenor URLs rot, GIPHY links expire, and a 404 on an attached URL causes Telegram to silently drop the entire message — text and all. There's no reliable, tag-based way for an agent to include a reaction GIF as a gesture.

## How It Works

A local GIF library with a Python tag-matching picker:

```
{baseDir}/
├── gifs/          # Local GIF files (user-provided or downloaded)
├── index.json     # Tag mapping: name → file, tags, mood, description
├── pick_gif.py    # Tag-based selection script (stdlib only)
└── populate.sh    # Download script for sample reaction GIFs
```

The agent calls `pick_gif.py` with tags describing the emotional context, and gets back a `MEDIA:` line it can include in its reply.

```
python3 {baseDir}/pick_gif.py praise well-done
# → MEDIA:~/.openclaw/workspace/gif-library/gifs/pat-on-back.gif
```

## Commands

```bash
# Pick by tag (returns best match MEDIA line)
python3 {baseDir}/pick_gif.py praise good-job

# List all GIFs with tags
python3 {baseDir}/pick_gif.py --list

# List all available search tags
python3 {baseDir}/pick_gif.py --list-tags

# Verify all GIFs exist and are valid
python3 {baseDir}/pick_gif.py --verify
```

## First-Time Setup

```bash
# 1. Create the library directory
mkdir -p ~/.openclaw/workspace/gif-library

# 2. Copy the contents of this skill to that directory
#    (pick_gif.py, index.json, populate.sh)

# 3. Populate with sample reaction GIFs
cd ~/.openclaw/workspace/gif-library && bash populate.sh

# 4. Verify
python3 pick_gif.py --verify
python3 pick_gif.py --list
```

## Adding New GIFs

1. Find a stable GIF URL (GitHub raw URLs are preferred — never use Tenor)
2. Download: `curl -sL <url> -o ~/.openclaw/workspace/gif-library/gifs/<name>.gif`
3. Add entry to `index.json`:
   ```json
   "my-gesture": {
     "file": "my-gesture.gif",
     "tags": ["tag1", "tag2", "tag3"],
     "mood": "descriptive/mood",
     "description": "What this GIF communicates"
   }
   ```
4. Verify: `python3 ~/.openclaw/workspace/gif-library/pick_gif.py --verify`

## Why This Over Tenor/GIPHY

| Aspect | Tenor/GIPHY with MEDIA: | Local GIF Picker |
|---|---|---|
| Delivery reliability | URL-dependent (404 = silent fail) | Local file = always available |
| API key needed | Yes | No |
| Custom curation | Algorithmic feed | Hand-curated tag matching |
| Works offline | No | Yes |
| Cost | Rate-limited / requires accounts | Free |

## Sample GIFs in populate.sh

The script downloads ~16 reaction GIFs from freely-available GitHub reaction repos:
- Pat on back (Community Abed-Troy)
- Fist bump (Top Gun volleyball high-five)
- Nod of respect (Big Lebowski cowboy nod)
- Facepalm (Picard TNG)
- Celebration (general win)
- Salute (Conan O'Brien salute-clap)
- Deal with it (sunglasses flourish)
- Mind blown (Tim & Eric)
- And more...

**Note:** GIF files are not shipped with the skill due to copyright. `populate.sh` downloads them from public repos with freely-licensed reaction media.

## In-Session Usage

```markdown
When the context calls for a non-textual gesture:
1. Identify the mood/occasion (praise, celebration, acknowledgment, apology)
2. Run: `python3 ~/.openclaw/workspace/gif-library/pick_gif.py <tag1> <tag2>`
3. Include the resulting `MEDIA:<path>` line in your reply on its own line
```

## Environment Variables (optional overrides)

| Variable | Default | Purpose |
|---|---|---|
| `GIF_LIBRARY_DIR` | `~/.openclaw/workspace/gif-library` | Root directory for the GIF library |
