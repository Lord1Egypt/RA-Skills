# MuseStream Skill

AI music generation and streaming. Give the user a shareable player URL — music generates and plays continuously in their browser. All songs are saved to a local library.

**Provider-agnostic** — Sonauto is the default. Adding new music generation APIs requires only a config entry.

---

## Features

- **Continuous streaming player** — Agent sends user a URL; browser streams AI-generated music song after song with no interruption
- **Auto-queue** — Automatically requests the next song after 120 seconds of playback while the browser window stays active; click "Stop Stream" or close the window to stop queuing and save your Sonauto credits
- **Shareable links** — Player URLs can be shared externally; expose the server via a reverse proxy (e.g., Nginx, Caddy) or a tunnel (e.g., ngrok, Cloudflare Tunnel) with HTTPS and authentication to keep your stream secure
- **Context-aware prompts** — The agent uses its own LLM to interpret user intent and real-world context (weather, mood, activity, location, traffic) into effective music generation prompts; the server also provides a rule-based fallback via `/api/context`
- **Persistent library** — All generated songs are saved locally with metadata (title, tags, lyrics) and browsable via a built-in player
- **Mobile context UI** — Form at `/context-ui` for sharing context from any device
- **Background save on stop** — Clicking Stop finishes saving the current song before ending
- **Messenger bot integration** — Connect MuseStream to your messaging bots (Telegram, Discord, Slack, etc.) so you can request AI music streams directly from a chat message and receive a playable link in reply

> [!CAUTION]
> Remember to click **Stop Stream** or close the browser window when you're done listening. The auto-queue will keep requesting new songs every 120 seconds, which consumes your Sonauto credits.

---

## Setup for Agent (first time)

### 0. Clone the repo
```bash
git clone https://github.com/asriverwang/openclaw-musestream.git ~/.openclaw/skills/openclaw-musestream
```

All subsequent commands assume MuseStream is located at `~/.openclaw/skills/openclaw-musestream`. Adjust paths if you cloned it elsewhere.

### 1. Get Sonauto API key

Guide the user to sign up at **https://sonauto.ai** and copy their API key.

### 2. Configure environment

Once the user provides their key:
```bash
cp config.example.json config.json
```
Set the values in `config.json`:
```json
{
  "SONAUTO_API_KEY": "<user's key>",
  "MUSIC_PROVIDER": "sonauto",
  "MUSESTREAM_OUTPUT_DIR": "<user's preferred path>",
  "MUSESTREAM_PORT": <user's preferred port>
}
```
Ask the user where they want generated songs saved. If they don't specify, remind them the default is `~/Music/MuseStream`.
Ask the user which port to use. If they don't specify, remind them the default is `5001`. The agent should pick an available port to avoid conflicts.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the server
```bash
./restart_musestream.sh
# Server at http://localhost:5001
```

The server loads `config.json` automatically at startup.

---

## Quick start for agent

### 1. Check if server is running
```bash
curl -s http://localhost:5001/library | python3 -m json.tool | head -5
```
If it returns JSON → server is up. If connection refused → start it:
```bash
./restart_musestream.sh
```

### 2. Quick test
```bash
curl "http://localhost:5001/start?prompt=upbeat+indie+rock+morning+energy"
```

### 3. Generate music from a prompt
```
GET http://localhost:5001/start?prompt=<url-encoded description>
```
Returns `{ "url": "http://localhost:5001/player?s=<key>", "key": "...", "prompt": "..." }`

**Important: The agent must interpret and refine the user's prompt before calling `/start`.** The server passes the prompt directly to Sonauto — it does not rewrite it. If the user says something non-musical (e.g., "a rock song about turtles flying", "music for a rainy afternoon"), the agent should use its own LLM to convert it into an effective music generation prompt describing artist, genre, era, mood, energy, usage context, and sonic texture.

Send the `url` to the user. They open it in a browser — music streams automatically.

**Prompt guidelines for the agent:**
- If the prompt includes artist names, genres, or musical descriptors → pass through or improve slightly
- Describe genre, era, mood, energy, usage, texture. No real song names.
- Non-musical input → interpret and rewrite (e.g., "turtles flying" → `"energetic rock with soaring melodies, playful and whimsical, bright guitar riffs"`)
- Already-musical input → pass through or improve slightly
- Examples of good prompts:
  - `"upbeat indie rock with jangly guitars, morning energy"`
  - `"dark ambient electronic, late night focus, minimal percussion"`
  - `"smooth jazz piano trio, warm and intimate, chill evening"`

### 4. Generate from user context

**Preferred approach:** The agent should gather context from the user (time, weather, mood, activity, etc.), use its own LLM to synthesize a music prompt, and call `/start?prompt=...` directly.

**Fallback:** The server provides a rule-based context-to-prompt endpoint:
```
POST http://localhost:5001/api/context
Content-Type: application/json

{
  "time": "evening",
  "weather": "rainy",
  "mood": "relaxed",
  "activity": "working from home",
  "driving": "",
  "traffic": "",
  "destination": ""
}
```
Returns `{ "url": "...", "prompt": "<rule-based music prompt>", "key": "..." }`

Mobile-friendly form: `http://localhost:5001/context-ui` (uses the rule-based engine)

### 5. Browse the library
```
GET http://localhost:5001/library      # JSON list of all saved songs
GET http://localhost:5001/             # Browser library player
```

### 6. Stop streaming
```
POST http://localhost:5001/stop
{"task_ids": ["<task_id>"]}
```
Current song finishes saving before stopping.

---

## All endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/start?prompt=...` | GET | Create session → player URL |
| `/player?s=<key>` | GET | Streaming player page |
| `/generate?prompt=...&session=...` | GET | Start generation job |
| `/status/<task_id>` | GET | Check generation status |
| `/stream/<task_id>` | GET | Audio stream |
| `/metadata/<task_id>` | GET | Title, tags, lyrics |
| `/stop` | POST | Stop tasks `{"task_ids": [...]}` |
| `/api/context` | POST/GET | Context → prompt → player URL |
| `/context-ui` | GET | Mobile context form |
| `/library` | GET | JSON list of saved songs |
| `/files/<filename>` | GET | Serve saved audio (range-capable) |
| `/` | GET | Library player UI |

---

## Adding a new provider

Add an entry to `PROVIDERS` in `musestream_server.py`:

```python
"myprovider": {
    "name":         "MyProvider",
    "register_url": "https://myprovider.com",
    "key_env":      "MYPROVIDER_API_KEY",
    "generate_url": "https://api.myprovider.com/v1/generate",
    "stream_base":  "https://api.myprovider.com/v1/stream",
    "status_url":   "https://api.myprovider.com/v1/status",
    "meta_url":     "https://api.myprovider.com/v1/songs",
    "audio_fmt":    "mp3",
    "mime":         "audio/mpeg",
},
```
Add a branch in `start_generation()` for the provider's payload format.
Set `"MUSIC_PROVIDER": "MyProvider"` and `"MYPROVIDER_API_KEY": "<your_key>"` in config.json and restart.
