---
name: guitar-tab-finder
description: Find guitar tabs/sheet sources for a song from a title or link (especially YouTube), rank the best matches, and produce a clean practice note. Use when a user asks to locate tabs/chords/fingerstyle arrangements and optionally create/update an Obsidian note (or generic markdown/json output) for a learning queue.
---

# Guitar Tab Finder

## Overview

Use this skill to turn a song link/title into a usable practice packet:
1) identify the song/arrangement,
2) find likely tab/sheet sources,
3) rank results with confidence notes,
4) write structured output in the user’s preferred format.

Default to flexible output (markdown/json). Use Obsidian formatting only when the user explicitly wants vault notes.

## Consent + Filesystem Guardrails

- Default behavior is **web lookup + text output only** (`markdown` or `json`).
- Perform any local file/vault action **only when explicitly requested**.
- Before writing files, require a user-provided target path/folder (or clearly confirmed default).
- Do not read/write outside the approved target path.
- If the user does not want local file operations, stay in non-local mode (`markdown`/`json`).

## Workflow

1. **Parse input**
   - Accept song title, artist, and/or URL.
   - If URL is YouTube, resolve video title/channel first (oEmbed is enough).
   - Detect arrangement intent when present (e.g., fingerstyle, drop D, capo).

2. **Search tabs/sheet sources**
   - Use web search with multiple queries:
     - `"<song>" "<artist>" guitar tab`
     - `"<song>" fingerstyle tab`
     - `"<video title>" tab`
   - Prefer useful sources with direct learning value (tabs/sheet/video with tab links).

3. **Rank and filter**
   - Return top 3–5 links.
   - For each result include:
     - source name
     - URL
     - short reason (exact match, arrangement match, likely match, etc.)
     - confidence (`high`/`medium`/`low`)
   - Call out likely paywalled links clearly.

4. **Build practice note content**
   - Include fields (unless user wants a different template):
     - `status`
     - `song`
     - `artist`
     - `arrangement`
     - `tuning`
     - `capo`
     - `difficulty`
     - `best tab links`
     - `next practice step`
   - Keep compact and editable.

5. **Output mode**
   - `markdown` (default): portable note body.
   - `json`: machine-friendly object.
   - `obsidian`: include wikilinks/embeds and vault-friendly file naming.

## Obsidian Mode Rules (optional)

Use these only when user asks for Obsidian output.

- Do not duplicate title in body if vault UI already shows filename as title.
- Use one note per song under user-specified folder.
- If a local PDF is provided, place/copy it near the note and link with:
  - `[[file.pdf]]` for link
  - `![[file.pdf]]` for embed preview
- Deduplicate by checking for existing note with same normalized song+artist name before creating a new one.

## Quality Bar

- Prefer accuracy over volume.
- Be explicit when uncertain.
- Do not claim tabs are free if not confirmed.
- Keep notes concise and practical (ready for immediate practice).

## Example Prompts

- “find guitar tabs for this song: https://www.youtube.com/watch?v=bApQqay1iJA”
- “get me the best fingerstyle tab sources for bee gees how deep is your love”
- “build a practice note for blackbird with top tab links and difficulty”
- “return json only with ranked links + confidence for this song”
- “obsidian mode: create a note in `guitar projects/songs to learn` and include tab links”
- “i uploaded a pdf tab. in obsidian mode, create note + embed the pdf”

## Output Templates

### Markdown template

```markdown
- status: to learn
- song: <title>
- artist: <artist>
- arrangement: <arrangement>
- tuning: <if known>
- capo: <if known>
- difficulty: <beginner/intermediate/advanced/unknown>

- best tab links:
  - <source> — <url> (<confidence>; <reason>)
  - <source> — <url> (<confidence>; <reason>)

- next practice step: <single concrete step>
```

### JSON template

```json
{
  "song": "",
  "artist": "",
  "arrangement": "",
  "tuning": "",
  "capo": "",
  "difficulty": "unknown",
  "links": [
    {"source":"","url":"","confidence":"high","reason":""}
  ],
  "next_step": ""
}
```
