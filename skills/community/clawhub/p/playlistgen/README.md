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

## OpenClaw Quick Start

The fastest way to get PlaylistGen running is to let your OpenClaw agent handle the entire setup for you.

**Step 1 — Add this repo as a skill**

In OpenClaw, install the PlaylistGen skill by pointing it at this folder:

```
Install the PlaylistGen skill from https://github.com/asriverwang/playlistgen
```

**Step 2 — Ask the agent to set it up**

Once the skill is loaded, just tell OpenClaw what you need:

```
Set up PlaylistGen. My music is at /home/user/Music. I have an Anthropic API key: sk-xxxx
```

The agent will:
1. Create the virtual environment and install dependencies
2. Check that `ffprobe` is available (and prompt you to install it if not)
3. Create `.env` with your music directory and API key
4. Walk you through `MUSIC_RULES.md` and ask if you want to customize the playlist rules before indexing
5. Index your music library — this takes roughly 1–3 hours per 5,000 songs depending on your LLM model. Progress is printed live. The agent will advise you to wait until at least 500 songs are enriched before proceeding.
6. Tell you where `music.db` is saved — this file holds all your indexed metadata and LLM enrichments. Keep it safe, don't delete it. If you migrate to a new machine or agent, copy this file to avoid re-indexing.
7. Start the server and confirm it's running

**Step 3 — Generate a playlist**

Once the server is up, ask OpenClaw naturally:

```
Give me a playlist of obscure 80s synth for late night driving
```

The agent calls `/api/generate`, receives a player URL, and shares it with you directly.

**Re-indexing after adding new music:**

```
Re-index my music library
```

---

## Requirements

- Python 3.10+
- `ffprobe` (part of ffmpeg) — for audio metadata extraction
- A music directory of MP3/FLAC/M4A/OGG/WAV files
- One of:
  - **Anthropic API key** (`ANTHROPIC_API_KEY`) — recommended, Claude Haiku used for both indexing and playlist generation
  - **MiniMax API key** (`MINIMAX_API_KEY`) — MiniMax M2.7 fallback

---

## Manual Setup

### 1. Clone / copy this folder

```bash
cp -r playlistgen/ ~/my-playlistgen
cd ~/my-playlistgen
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests openai anthropic mutagen
```

Also install ffmpeg if not already present:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### 3. Configure environment

```bash
cp env.sample.md .env
# Edit .env — set MUSIC_DIR and at least one API key
```

### 4. Index your music library

This scans your music directory and enriches each song with LLM-generated tags. Runs once; safe to re-run (skips already-indexed songs).

```bash
source .env
python3 smart_indexer.py --path "$MUSIC_DIR" --llm haiku --key "$ANTHROPIC_API_KEY" --db "$DB_PATH" --workers 1
```

> **Note:** When using Haiku, always set `--workers 1` to avoid 429 rate limit errors.

**Time estimate:** indexing takes roughly 1–3 hours per 5,000 songs depending on the response time and quality of your LLM model. Progress is saved after every batch — you can stop and resume at any time without losing work. The indexer prints a live `Phase 2 (LLM): N/M (X%)` progress line so you can track how far along it is.

Add `--verbose` to see per-batch logs and a full stats breakdown at the end.

> **Note:** Playlist generation quality depends directly on how many songs have been enriched. Wait until at least 500 songs have been indexed by the LLM before starting the server and using the service.

### 5. Start the server

```bash
bash start.sh
```

Server runs at `http://localhost:5678` (or the port in your `.env`).

---

## Customizing playlist rules

Open `MUSIC_RULES.md` and edit the two sections:

- **Prompt Interpretation** — how the LLM maps a free-form request to music tags (genre counts, long-tail rules, language/energy/era handling)
- **Final Playlist Curation** — how the LLM selects and orders the final tracks (diversity, energy transitions, artist limits)

Changes take effect on next server start (no code changes needed).

---

## Usage

**Web UI:** Open `http://localhost:5678` — search your library, click to play.

**Playlist from natural language:**
```
POST http://localhost:5678/api/generate
{"prompt": "melancholic shoegaze for a rainy afternoon", "max_count": 30}
```

**Full API reference:** See `TOOLS.md`.

---

## File overview

| File | Purpose |
|---|---|
| `playlist_server.py` | HTTP server — all API endpoints and web UI |
| `smart_indexer.py` | One-time LLM enrichment of your music library |
| `MUSIC_RULES.md` | Editable LLM rules for interpretation and curation |
| `TOOLS.md` | Full API reference |
| `env.sample.md` | Environment variable template |
| `start.sh` | Start the server |
