---
name: hey-bible
description: Look up, search, and reference Bible verses and Scripture via the Hey Bible API. Use when the user asks to find, quote, look up, or cross-reference Bible verses, passages, chapters, or translations, or to read their saved Hey Bible favorites, notes, verse images, or chats. Returns Scripture text and structured JSON.
version: 1.0.0
license: MIT
compatibility: Requires Node.js and npx with network access to api.heybible.app
metadata:
  author: Hey Bible
  version: "1.0.0"
  homepage: https://heybible.app
  openclaw:
    requires:
      env:
        - HEY_BIBLE_API_KEY
      bins:
        - node
        - npx
    primaryEnv: HEY_BIBLE_API_KEY
    emoji: "books"
    homepage: https://heybible.app
    os:
      - darwin
      - linux
      - win32
    install:
      - kind: node
        package: "@hey-bible/cli"
        bins: [hey-bible]
        label: "Install Hey Bible CLI via npm"
---

# Hey Bible

Give your agent first-class access to the Bible. Look up verses across multiple
translations, browse the books of Scripture, and read the user's saved Hey Bible
data (favorites, notes, AI-generated verse images, and chats) — all returned as
clean, structured JSON.

This skill is powered by the [`@hey-bible/cli`](https://www.npmjs.com/package/@hey-bible/cli)
package, a thin wrapper over the [Hey Bible API](https://docs.heybible.app).

## Setup

The user needs a Hey Bible API key, available from
[heybible.app](https://heybible.app) under **Account > API Keys**. Set it as an
environment variable:

```bash
export HEY_BIBLE_API_KEY=your_api_key_here
```

## Method 1: CLI (preferred)

Use the `hey-bible` CLI via `npx`. No install required. **Always pass `--json`**
so the output is structured and easy to parse.

```bash
# Look up a verse or range (defaults to ESV)
npx -y @hey-bible/cli search John 3 --start-verse 16 --end-verse 18 --json

# Look up a whole chapter
npx -y @hey-bible/cli search Genesis 1 --json

# List available translations, then look up in a specific one
npx -y @hey-bible/cli bibles --json
npx -y @hey-bible/cli search Psalms 23 --bible-id kjv --json

# List the books of the Bible (names, 3-letter codes, chapter counts)
npx -y @hey-bible/cli books --json
```

### Reading the user's saved data

```bash
# Favorited verses (optionally filtered by tag)
npx -y @hey-bible/cli favorites --json
npx -y @hey-bible/cli favorites --tag faith --limit 10 --json

# Notes, AI-generated images, chats, and tags
npx -y @hey-bible/cli notes --json
npx -y @hey-bible/cli images --json
npx -y @hey-bible/cli images --id 42 --json    # returns a 24h signed URL
npx -y @hey-bible/cli chats --json
npx -y @hey-bible/cli tags --json
```

## Commands

| Command | Description |
|---------|-------------|
| `search <book> <chapter>` | Look up verses. Options: `--start-verse`, `--end-verse`, `--bible-id`. Saves the lookup to the user's account. |
| `bibles` | List available Bible translations (id, name, abbreviation, source). |
| `books` | List the 66 books with 3-letter codes and chapter counts. |
| `favorites` | List favorited verses with their notes, images, conversations, and tags. Options: `--tag`, `--limit`, `--offset`. |
| `notes` | List verse notes. Options: `--id`, `--limit`, `--offset`. |
| `images` | List AI-generated verse images. `--id` returns a signed URL. |
| `chats` | List chat conversations with verse context. Options: `--id`, `--limit`, `--offset`. |
| `tags` | List the user's tags. |

## Notes

- Verse `content` is returned as HTML (with `<sup>` verse numbers) inside the
  JSON. Strip tags when presenting the text to the user.
- The API is read-oriented. `search` is the only call with a side effect: it
  saves the looked-up passage to the user's Hey Bible account.
- Book names accept natural forms like `"John"`, `"Genesis"`, and
  `"1 Corinthians"`. Quote multi-word book names in the shell.

See [`references/api-reference.md`](./references/api-reference.md) for the full
endpoint and field reference.
