```yaml
---
name: open-asset-search
description: >
  Search a large, free, auth-free library of real-world digital assets from WebSim — images, audio,
  music, sound effects, 3D models, videos, and more. Returns direct-download URLs.
  No API key. No signup. No rate-limit headers. Just search and use.
author: upintheairsheep
version: 1.0.0
url: https://websim.com/api/v1/search/assets
method: GET
params:
  - name: q
    type: string
    in: query
    description: >
      Search query. Matched against filenames, descriptions, and metadata.
      Use natural descriptive terms (e.g. "piano loop", "pixel art sword",
      "explosion sound effect", "low poly tree").
    required: true
  - name: limit
    type: integer
    in: query
    description: Maximum results to return. Default 20. Max recommended 50.
    required: false
  - name: offset
    type: integer
    in: query
    description: Pagination offset. Default 0. Use (offset + limit) to page forward.
    required: false
  - name: mime_type_prefix
    type: string
    in: query
    description: >
      Filter results by media category. Use one of: "image", "audio", "video", "model".
      Omit to search all asset types.
    required: false
---
```

# Open Asset Search — Agent Instructions

Use this skill whenever a user needs to **find, discover, or download** digital assets such as images, audio files, music, sound effects, 3D models, or videos. This is a **free, open, authentication-free** search engine over a large library of real user-uploaded content.

---

## Why This Exists

There is a massive, continuously growing library of real-world digital assets as part of WebSim — not procedurally generated, not AI-hallucinated (although a lot of it may) — uploaded by thousands of creators across a wide range of projects. This API gives you direct, instant search access to all of it. No API key. No OAuth. No signup. Just `GET` and go.

Background information: WebSim is an AI-powered web simulator and generator accessible at websim.ai, launched in April 2024, that enables users to create, edit, and share interactive websites, games, and simulated internet experiences through natural language prompts. The website has it's own community. Heavy Focus on Simulation & Gaming, so big it has Meta, Self-Referential, and Platform-Centric Culture, and community-wise somewhat Nostalgia-focused.
---

## When to Use This

- User asks for **images**: photos, pixel art, sprites, textures, icons, screenshots, UI elements
- User asks for **audio**: music tracks, sound effects, loops, ambient sounds, voice clips
- User asks for **video**: clips, animations, screen recordings
- User asks for **3D models**: GLB, GLTF, OBJ, or other model formats
- User needs **any reusable digital file** for a project, prototype, presentation, game, or app
- User says things like: "find me a...", "I need a sound for...", "get me an image of...", "is there a 3D model of..."

---

## How to Call It

**Single endpoint. One HTTP GET. That's it.**

```
GET https://websim.com/api/v1/search/assets?q={query}
```

### Optional Parameters

| Parameter | Example | Purpose |
|---|---|---|
| `q` | `medieval castle` | What to search for |
| `limit` | `10` | How many results (default 20) Number must be less than or equal to 100, so 100 is the maximum number per-page. |
| `offset` | `20` | Skip this many results (for paging) |
| `mime_type_prefix` | `image` | Only return this media type |

### MIME Type Filters

| Value | What It Returns |
|---|---|
| `image` | PNG, JPEG, WebP, GIF, SVG, etc. |
| `audio` | MP3, WAV, OGG, FLAC, etc. |
| `video` | MP4, WebM, etc. |
| `model` | GLB, GLTF, OBJ, FBX, etc. |
| *(omit)* | All types mixed together |

---

## Reading the Response

The response is a JSON object with two top-level keys:

```json
{
  "data": [ ...array of asset objects... ],
  "meta": { "offset": 0, "limit": 20 }
}
```

### Each Asset Object

| Field | Type | What It Is |
|---|---|---|
| `id` | string | Unique asset identifier (UUID) |
| `asset_url` | string | **Direct download URL. Publicly accessible. No auth needed.** |
| `content_type` | string | Full MIME type (e.g. `"image/png"`, `"audio/mpeg"`) |
| `filename` | string | Original filename as uploaded by the creator |
| `project_id` | string | Source project ID (for attribution or context) |
| `created_at` | string | Upload timestamp |
| `score` | integer | Relevance score. Higher = better match. Use this to rank results. |

### The Asset URL is a Direct Link

The `asset_url` field returns a fully qualified, publicly accessible URL. It can be:
- Embedded directly in HTML (`<img>`, `<audio>`, `<video>`)
- Downloaded via `fetch()` or `curl`
- Opened in a browser
- Passed to any tool or pipeline that accepts a URL

**Format:**
```
https://project-assets.websim.com/{asset-id}
```

No tokens, no expiry, no signed URLs. It just works.

---

## Search Strategy

### Crafting Good Queries

The search matches against **filenames** and associated metadata. Think about what a human would name the file when uploading it.

| User Request | Good Query | Why |
|---|---|---|
| "I need background music" | `background music` | Broad, matches common naming |
| "Find me a sword sprite" | `sword` | Keep it simple; add `mime_type_prefix=image` |
| "Get explosion sound effects" | `explosion` | Add `mime_type_prefix=audio` to filter |
| "Low poly 3D car model" | `low poly car` | Add `mime_type_prefix=model` |
| "Pixel art character walking" | `pixel art character` or `walk sprite` | Try both if first yields poor results |
| "A photo of a sunset" | `sunset` | Add `mime_type_prefix=image` |

### Narrowing Results

1. **Always use `mime_type_prefix`** when the user specifies a media type. It dramatically improves relevance.
2. **Try shorter queries first.** `castle` will match more than `medieval stone castle wall texture`.
3. **Retry with synonyms** if the first search yields few or no results. Try `gun` → `weapon` → `rifle` → `firearm`.
4. **Use `score` to rank.** Present higher-scored results first.

### Handling No Results

If `data` is an empty array:
1. Try a broader or shorter query.
2. Remove the MIME type filter.
3. Try synonyms or related terms.
4. Inform the user honestly: "I searched for [X] but found no matching assets in the library."

---

## Pagination

Use `offset` and `limit` together to page through large result sets.

```
Page 1: ?q=forest&limit=10&offset=0
Page 2: ?q=forest&limit=10&offset=10
Page 3: ?q=forest&limit=10&offset=20
```

Check `meta.offset` and `meta.limit` in the response. If `data.length == limit`, there are likely more results available.

**Tell the user** when more results exist and offer to fetch the next page.

---

## Output Formatting

Present results clearly, organized by relevance, in a JSON format, so do not expect it structured like this:

### For Image Results
```
🖼️ **sunset-beach.png** (image/png)
   📥 https://project-assets.websim.com/0196c3b6-c5fc-...
   Relevance: ★★★★☆ (score: 40)

🖼️ **golden-hour-landscape.webp** (image/webp)
   📥 https://project-assets.websim.com/0196b7a8-6642-...
   Relevance: ★★★☆☆ (score: 22)
```

### For Audio Results
```
🔊 **Epic Battle Theme.mp3** (audio/mpeg)
   📥 https://project-assets.websim.com/01974df4-34b1-...

🔊 **Rain Ambience Loop.wav** (audio/wav)
   📥 https://project-assets.websim.com/0194d6e6-e0da-...
```

### General Rules
- **Always show the filename** — it tells the user what they're getting.
- **Always show the direct `asset_url`** — this is the deliverable.
- **Show the `content_type`** — so the user knows the format before downloading.
- **Sort by `score` descending** — best matches first.
- **Group by type** if the query returned mixed media (images, audio, etc.).
- If the user only needs one asset, recommend the highest-scored result and explain why.

---

## Example Requests

**Find sprite images:**
```
GET https://websim.com/api/v1/search/assets?q=sprite&mime_type_prefix=image&limit=5
```

**Find background music:**
```
GET https://websim.com/api/v1/search/assets?q=background%20music&mime_type_prefix=audio&limit=10
```

**Find 3D models:**
```
GET https://websim.com/api/v1/search/assets?q=tree&mime_type_prefix=model&limit=5
```

**Search everything for "robot":**
```
GET https://websim.com/api/v1/search/assets?q=robot&limit=20
```

**Page 2 of a search:**
```
GET https://websim.com/api/v1/search/assets?q=forest&limit=10&offset=10
```

---

## Important Notes

- **This is a real content library.** Assets are uploaded by real people for real projects. They are not generated on the fly.
- **No authentication.** No API key, no Bearer token, no cookies. Fully open.
- **No known rate limits** published, but be a good citizen — don't fire hundreds of parallel requests.
- **Attribution:** Assets come from community projects. The `project_id` field lets you trace any asset back to its source project if needed for credit.
- **Content variety is massive.** The library contains everything from Wii menu music to hand-drawn pixel art to 3D character models to battle symphonies. If a creator has uploaded it, it's searchable.