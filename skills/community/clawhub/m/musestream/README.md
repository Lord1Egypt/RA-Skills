# MuseStream

AI music generation and streaming server. Describe a mood or context — get a continuous, browser-playable music stream with songs saved to a local library.

**Provider-agnostic** — Sonauto is the default. Adding new music generation APIs requires only a config entry.

---

## Features

- **Continuous streaming player** — Agent sends user a URL; browser streams AI-generated music song after song with no interruption
- **Auto-queue** — Automatically requests the next song after 120 seconds of playback while the browser window stays active; click "Stop Stream" or close the window to stop queuing and save your Sonauto credits
- **Shareable links** — Player URLs can be shared externally; expose the server via a reverse proxy (e.g., Nginx, Caddy) or a tunnel (e.g., ngrok, Cloudflare Tunnel) with HTTPS and authentication to keep your stream secure
- **Context-aware prompts** — Converts real-world context (weather, mood, activity, location, traffic) into music generation prompts via a built-in rule-based engine; the agent uses its own LLM to interpret and refine prompts before sending them to the server
- **Persistent library** — All generated songs are saved locally with metadata (title, tags, lyrics) and browsable via a built-in player
- **Mobile context UI** — Form at `/context-ui` for sharing context from any device
- **Background save on stop** — Clicking Stop finishes saving the current song before ending
- **Messenger bot integration** — Connect MuseStream to your messaging bots (Telegram, Discord, Slack, etc.) so you can request AI music streams directly from a chat message and receive a playable link in reply

> [!CAUTION]
> Remember to click **Stop Stream** or close the browser window when you're done listening. The auto-queue will keep requesting new songs every 120 seconds, which consumes your Sonauto credits.

---

## OpenClaw Quick Start

If you have an OpenClaw Agent, it can set up and run MuseStream for you end-to-end:

**1. Clone the repo**

```bash
git clone <repo-url> ~/.openclaw/skills/
```

**2. Follow SKILL.md to build the skill**

> Read ~/.openclaw/skills/openclaw-musestream/SKILL.md

**3. Generate music**

Once the server is up, your agent will confirm with something like:

> Both keys loaded. Server's up on **http://localhost:5001** with MiniMax context prompts enabled. Want me to generate some music?

> [!NOTE]
> The port may differ from `5001` — your agent picks an available port to avoid conflicts with other services already running on your machine.

Try:

> Generate music about "A rock song about turtles flying"

Your agent will return a player link — click it and enjoy!

> [!TIP]
> - Browse and listen to all previously generated songs at **http://localhost:5001** (no path suffix needed). Streamed songs are saved to `~/Music/MuseStream` by default.
> - Never commit API keys to version control.
> - See **`SKILL.md`** for the full agent endpoint reference.

**4. Share a player URL externally**

By default, all player URLs use `localhost` and are only reachable on your machine. To send a link someone else can open, ask your agent:

> Replace `localhost` with my external IP address in the player URL so I can share it.

Your agent will substitute the host and return a link like:
```
http://203.0.113.42:5001/player?s=abc12345
```

> [!WARNING]
> **Be careful — exposing MuseStream to the internet opens your server to anyone who discovers the port.** They can trigger music generation, consume your API quota, and browse your saved library. Only use this feature on trusted networks and with the precautions below.

Before exposing externally, at minimum:

- **Firewall** — restrict port 5001 to known IPs ([ufw guide](https://help.ubuntu.com/community/UFW), [iptables](https://wiki.archlinux.org/title/iptables))
- **Secret token** — set `MUSESTREAM_TOKEN`; ask your agent to require `?token=<secret>` on all requests
- **Rate limiting** — ask your agent to add [Flask-Limiter](https://flask-limiter.readthedocs.io/) to `/generate` and `/start`
- **TLS proxy** — put [Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy) or [nginx](https://nginx.org/en/docs/beginners_guide.html) in front; never expose Flask's dev server directly
- **Avoid public/shared networks** without the above in place

---

## Manual Setup

### 1. Get a Sonauto API key
Register at **https://sonauto.ai** and copy your API key.

### 2. Configure
```bash
cp config.example.json config.json
# Edit config.json — set at minimum: "SONAUTO_API_KEY": "your_key"
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the server
```bash
./restart_musestream.sh
# or: python3 musestream_server.py
```

Server runs on **http://localhost:5001** by default (configurable via `MUSESTREAM_PORT`).

---

## Usage

### Generate music from a prompt
```bash
curl "http://localhost:5001/start?prompt=upbeat+indie+rock+morning+energy"
# → {"url": "http://localhost:5001/player?s=abc12345", ...}
```
Open the returned URL in a browser. Music starts streaming immediately.

### Generate from context (weather, mood, activity)
The agent uses its own LLM to interpret context and craft a music prompt, then calls `/start`. A rule-based fallback is also available:
```bash
curl -X POST http://localhost:5001/api/context \
  -H "Content-Type: application/json" \
  -d '{"time": "evening", "weather": "rainy", "mood": "relaxed", "activity": "working"}'
# → {"url": "...", "prompt": "focused lo-fi calming with soft rain ambiance for evening"}
```

### Browse the library
Open **http://localhost:5001/** in a browser — prev/next/shuffle player for all saved songs.

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/start?prompt=...` | GET | Create session → player URL |
| `/player?s=<key>` | GET | Streaming player page |
| `/generate?prompt=...` | GET | Start a generation job |
| `/status/<task_id>` | GET | Check job status |
| `/stream/<task_id>` | GET | Audio stream (browser connects here) |
| `/metadata/<task_id>` | GET | Song title, tags, lyrics |
| `/stop` | POST | Stop tasks `{"task_ids": [...]}` |
| `/api/context` | POST/GET | Context JSON → player URL |
| `/context-ui` | GET | Mobile-friendly context form |
| `/library` | GET | JSON list of saved songs |
| `/files/<filename>` | GET | Serve saved audio (seekable) |
| `/` | GET | Library player UI |

---

## Adding a New Provider

Add an entry to `PROVIDERS` in `musestream_server.py`:

```python
"udio": {
    "name":         "Udio",
    "register_url": "https://udio.com",
    "key_env":      "UDIO_API_KEY",
    "generate_url": "https://api.udio.com/v1/generate",
    "stream_base":  "https://api.udio.com/v1/stream",
    "status_url":   "https://api.udio.com/v1/status",
    "meta_url":     "https://api.udio.com/v1/songs",
    "audio_fmt":    "mp3",
    "mime":         "audio/mpeg",
},
```

Then add a branch in `start_generation()` for the provider's request format, set `MUSIC_PROVIDER=udio`, and restart.

---

## License

MIT
