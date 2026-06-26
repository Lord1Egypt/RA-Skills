# Music Playlist Generation (PlaylistGen)

LLM-powered playlist generation for your local music library that contains music audio files such as mp3, flac, m4a, etc. Integrate this skill with your Agents (e.g., OpenClaw) to enable natural language music discovery and playlist curation through conversation. Point it at your music folder, run the indexer once, and get a natural language playlist generator — accessible via web browser or API.

---

## What it does

- Scans your local music directory and builds a SQLite database of all songs
- Extracts basic metadata (title, artist, album, duration, year) from audio tags via ffprobe and file path structure
- Uses an LLM (Claude Haiku or MiniMax M2.7) to enrich each song with genre, subgenre, mood, energy, language, region, and usage context
- Serves a local HTTP server with a search UI and player
- Accepts natural language prompts ("obscure 80s synth for late night driving") and generates curated playlists using LLM reasoning

---

## Setup

Work through these steps with the user. Each step requires user input or confirmation before proceeding.

### Step 0 — Install the skill

Clone or install PlaylistGen into the OpenClaw skills directory:

```bash
git clone https://github.com/asriverwang/playlistgen ~/.openclaw/skills/playlistgen
cd ~/.openclaw/skills/playlistgen
```

All subsequent commands assume PlaylistGen is located at `~/.openclaw/skills/playlistgen`.

### Step 1 — Gather requirements

Ask the user:
1. Where is their music directory? (e.g. `/home/user/Music`, `/media/data/Music`)
2. Do they have an Anthropic API key, MiniMax API key, or both? (Anthropic Haiku preferred)
3. What IP/port should playlist links use? (default `http://localhost:5678` works for local use; set `MUSIC_SERVER_URL` to a LAN/Tailscale IP if they want links to work on other devices)

### Step 2 — Create the virtual environment

```bash
cd ~/.openclaw/skills/playlistgen
python3 -m venv venv
venv/bin/pip install requests openai anthropic mutagen
```

Also check that `ffprobe` is available:
```bash
ffprobe -version
# If missing: sudo apt install ffmpeg   (Linux) or brew install ffmpeg (macOS)
```

### Step 3 — Create .env

Copy `env.sample.md` to `.env` and fill in the values from Step 1:

```bash
cp env.sample.md .env
```

Required keys:
- `MUSIC_DIR` — the user's music directory
- `ANTHROPIC_API_KEY` (recommended) and/or `MINIMAX_API_KEY`

Optional:
- `MUSIC_SERVER_URL` — public IP for playlist links (e.g. `http://192.168.1.100:5678`)
- `PORT` — default is 5678

### Step 4 — Present MUSIC_RULES.md for review

**Read `MUSIC_RULES.md` and summarize the two sections to the user:**

- **Prompt Interpretation** — how the LLM converts a natural language request into music tags (genre counts, long-tail rules, language/energy/era detection)
- **Final Playlist Curation** — how the LLM selects and orders the final tracks (diversity, transitions, artist limits)

**Ask the user:** "Do you want to use the default rules, or customize them before we start?"

If they want to customize:
- Walk through each rule and ask if they want to change it
- Common customizations: artist limit (currently 3), whether to bias toward niche/mainstream, energy transition strictness
- Write the changes directly into `MUSIC_RULES.md` — no code changes needed

If they use defaults: proceed.

### Step 5 — Index the music library

This enriches every song with LLM-generated tags (genre, subgenre, mood, energy, language, region, usage context). It runs once and is safe to resume if interrupted.

```bash
source .env
venv/bin/python3 smart_indexer.py \
  --path "$MUSIC_DIR" \
  --llm haiku \
  --key "$ANTHROPIC_API_KEY" \
  --db "${DB_PATH:-music.db}" \
  --batch 40 \
  --workers 1
```

> **Note:** When using haiku, always set `--workers 1`. Haiku is efficient enough for single-worker throughput, but will throw 429 (rate limit) errors if batches are sent in parallel.

Use `--llm minimax --key "$MINIMAX_API_KEY"` if using MiniMax instead (MiniMax supports higher worker counts).

**Timing heads-up to give the user:** indexing takes roughly 1–3 hours per 5,000 songs depending on the response time and quality of the LLM model. Progress is saved after every batch so they can stop and resume without losing work. By default the indexer prints a live progress line with rate, ETA, and error counts:
```
Phase 2 (LLM): 2057 songs in 103 batches | haiku / claude-haiku | workers=1 | timeout=120s
Phase 2 (LLM): 45/103 (43.7%) [2.3 songs/s] | avg 8.7s/batch | ETA 4m12s
```
Errors, retries, and dropped batches are always printed (even without `--verbose`) so the agent can diagnose issues. Add `--verbose` for full per-batch detail including raw LLM response snippets.

> **Warning:** Playlist generation quality depends directly on how many songs have been enriched. Advise the user to wait until at least 500 songs have been indexed by the LLM before starting the server and using the service. They can monitor progress via the live `Phase 2 (LLM): N/M (X%)` output and resume at any time if they need to pause.

When done, tell the user:
- "Indexed N songs. Your music database is saved at `<absolute path to music.db>` — this file contains all your indexed metadata and LLM enrichments. Keep it safe and do not delete it. Indexing costs time and API credits, so this file is valuable. If you migrate to a different machine or agent, copy this file over and point `DB_PATH` to it to avoid re-indexing."

### Step 6 — Start the server

```bash
bash start.sh
```

Verify it's up:
```bash
curl -s http://localhost:5678/api/stats | python3 -m json.tool | head -5
```

Tell the user: "PlaylistGen is running at http://localhost:5678 — open it in a browser to search your library."

---

## Day-to-day operations

### Generate a playlist (API)

```
POST http://localhost:5678/api/generate
{"prompt": "obscure 80s synth for late night driving", "max_count": 30}
→ {"title": "...", "url": "http://.../player?saved=XXXX", "count": 28}
```

Share only the returned `url`. Do not construct player URLs manually.

### Search the library

```
GET http://localhost:5678/api/search?q=radiohead
```

### Re-index after adding new music

```bash
source .env
venv/bin/python3 smart_indexer.py --path "$MUSIC_DIR" --llm haiku --key "$ANTHROPIC_API_KEY" --db "${DB_PATH:-music.db}" --workers 1
```

Skips already-indexed songs automatically.

### Refresh catalog vocabulary (after re-indexing)

```
GET http://localhost:5678/api/catalog/vocab/refresh
```

Or just restart the server — it rebuilds on startup.

### Update playlist rules

Edit `MUSIC_RULES.md` directly. Changes take effect on next server start. Restart:

```bash
bash start.sh
```

### Check server status

```bash
curl -s http://localhost:5678/api/stats
tail -f playlist_server.log
```

---

## API Reference

Base URL: `http://localhost:5678` (or whatever `PORT` and `MUSIC_SERVER_URL` are set to).

**Never construct player URLs manually. Always use the `url` field returned by the server.**

### Generating a playlist — try automated first, fall back to manual

**Always try the automated endpoint first:**

```
POST /api/generate
{"prompt": "obscure 80s synth for late night driving", "max_count": 30}

→ {"title": "...", "url": "http://<host>:5678/player?saved=XXXX", "count": 28, "tags": {...}}
```

Share only the returned `url`. Do not modify it. One call handles everything (interpret → fetch → curate → save).

**If `/api/generate` returns `{"error": ...}`, switch to the manual workflow below.**

### Manual workflow (fallback)

Use this only when `/api/generate` fails. You participate in the pipeline directly.

**Step 1 — Interpret prompt → structured tags**

Fetch valid tags first: `GET /api/catalog/vocab`

Pick tags following these field rules:
- `genres` — 2 values
- `subgenres` — 3 regular + 1 long-tail (count ≤ 2)
- `moods` — 2 regular + 1 long-tail
- `usage_contexts` — 2 regular + 1 long-tail
- `year` — `[start_year, end_year]` if era implied, else `[]`
- `energy` — `["high"]`, `["low", "medium"]`, etc., or `[]`
- `language` — single value if language-specific, else `""`
- `regions` — list if geography implied, else `[]`
- `popularity_hint` — `"mainstream"`, `"indie"`, `"niche"`, `"obscure"`, or `"any"`

**Step 2 — Fetch candidates**

Language is a hard filter. Region and popularity are NOT filtered here — pass them to Step 3.
```
GET /api/songs?genre=Rock,Indie&subgenre=Shoegaze,Dream+Pop&mood=Melancholic,Dreamy&usage_context=night&language=&limit=300
→ {"songs": [...], "count": N}
```
All params are substring-matched, comma-separated for multiple values. Returns up to 300 songs with full metadata.

**Step 3 — Curate: select and order final playlist**

Each song has: `path` (use as ID), `artist`, `title`, `genre`, `subgenre`, `mood`, `energy`, `language`, `region`, `year`, `popularity`. Select and order them yourself, then pass the paths to Step 4.

**Step 4 — Save and get player URL**
```
POST /api/playlist/save
{"title": "My Playlist", "songs": ["path1", "path2", ...]}
→ {"url": "http://<host>:5678/player?saved=XXXX", "title": "...", "count": N}
```

Share only the returned `url`. Do not modify it.

### Other endpoints

| Endpoint | Description |
|---|---|
| `GET /api/stats` | Library stats: total songs, top artists/albums |
| `GET /api/search?q=<text>` | Keyword search on title/artist/album (50 results) |
| `GET /api/interpret?q=<prompt>&provider=claude\|minimax` | LLM prompt → structured tags (default: claude) |
| `GET /api/catalog/vocab` | Full tag→count dict for all fields |
| `GET /api/catalog/vocab/refresh` | Rebuild vocab from DB, rewrite catalog JSON file |
| `GET /` | Web search UI |
| `GET /player?saved=<key>` | Playlist player page |

### Song fields

| Field | Type | Notes |
|---|---|---|
| `path` | string | Absolute filesystem path — use as song ID in all API calls |
| `url` | string | Relative path — use as audio `src` in browser |
| `title` | string | |
| `artist` | string | |
| `album` | string | |
| `year` | string | |
| `genre` | string | e.g. `"Rock"`, `"Electronic"` |
| `subgenre` | string | e.g. `"Shoegaze"`, `"Synthpop"` |
| `mood` | string | Comma-separated, e.g. `"Melancholic, Dreamy"` |
| `usage_context` | string | e.g. `"night"`, `"driving"` |
| `energy` | string | `"low"`, `"medium"`, or `"high"` |
| `language` | string | e.g. `"English"`, `"Mandarin"` |
| `region` | string | e.g. `"UK"`, `"USA"`, `"Taiwan"` |
| `popularity` | string | `"mainstream"`, `"indie"`, `"niche"`, `"obscure"` |
| `duration` | float | Seconds |

---

## Architecture summary

| Component | Role |
|---|---|
| `playlist_server.py` | HTTP server: all API endpoints, web UI, player |
| `smart_indexer.py` | One-time LLM enrichment — run standalone |
| `MUSIC_RULES.md` | Editable rules for interpret and curate LLM prompts |
| `music.db` | SQLite: songs table + playlists table |
| `music_catalog_vocab.json` | Auto-generated tag→count snapshot (written at server start) |

**Playlist generation pipeline (inside `/api/generate`):**
1. Interpret prompt → structured tags (LLM, guided by `MUSIC_RULES.md`)
2. Fetch candidates from DB — language is a hard filter; region/popularity are not
3. Curate: LLM selects and orders final playlist (guided by `MUSIC_RULES.md`)
4. Save playlist to DB → return player URL

**Key design principles:**
- All LLM rules live in `MUSIC_RULES.md`, not in code
- The catalog vocabulary is pre-built at startup (zero DB I/O per request)
- Language is enforced at fetch time; region/popularity are soft hints at curation time
- Player URLs come from the server — never construct them manually
