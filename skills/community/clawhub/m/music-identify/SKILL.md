---
name: music-identify
description: Identify songs from audio clips using AudD API and optionally queue them to Spotify. Triggers on /songsearch command, voice messages with song identification intent, or when user asks "what song is this." Also handles recall queries like "what did I shazam" or "what was that song" by reading the music log. Works with any audio file (OGG, MP3, WAV, etc.).
---

# Music Identify

Identify songs from audio using AudD, return song info with Spotify link, and optionally queue to the user's active Spotify session.

## Runtime Dependencies

Required on `$PATH`:
- `curl` — HTTP requests to AudD and Spotify APIs
- `jq` — JSON parsing for all API responses
- `python3` — Spotify OAuth flow only (`scripts/spotify-auth.py`)

## Credentials

| Credential | Location | Required | Purpose |
|---|---|---|---|
| AudD API key | `~/.config/audd/api_key` | Yes | Song identification |
| Spotify OAuth tokens | `~/.config/spotify/tokens.json` | No (optional) | Queue to Spotify |
| Spotify app credentials | `~/.config/spotify/credentials.json` | No (optional) | Token refresh |

**Security notes:**
- All credential files should be restricted: `chmod 600`.
- This skill does not read, store, or access any platform tokens (Telegram, Discord, etc.). Audio file download from messaging platforms is handled by the host agent, not by this skill.

## Trigger

- User sends `/songsearch` then follows with a voice message or audio file
- User asks to identify a song from audio ("what song is this", "identify this song", "shazam this")
- User asks to recall previously identified songs ("what was that song", "what did I shazam")

## Setup

### AudD API Key (required)

1. Sign up at <https://audd.io> (free tier: 300 requests, no credit card)
2. Save key:
   ```bash
   mkdir -p ~/.config/audd
   echo "YOUR_KEY" > ~/.config/audd/api_key
   chmod 600 ~/.config/audd/api_key
   ```

### Spotify Integration (optional)

1. Create a Spotify Developer app at <https://developer.spotify.com/dashboard>
2. Set redirect URI to your callback URL
3. Save credentials:
   ```bash
   mkdir -p ~/.config/spotify
   cat > ~/.config/spotify/credentials.json << 'EOF'
   {"client_id": "...", "client_secret": "...", "redirect_uri": "https://your-host/callback"}
   EOF
   chmod 600 ~/.config/spotify/credentials.json
   ```
4. Run the auth flow: `python3 scripts/spotify-auth.py`
5. Open the printed URL in a browser, authorize, tokens save automatically
6. `chmod 600 ~/.config/spotify/tokens.json`

## Workflow — Song Identification

When a song identification is triggered:

1. Prompt user for a voice clip if not already provided.
2. Save the audio file to a temp location (e.g., `/tmp/music-identify-<timestamp>.ogg`). The host agent handles downloading audio from the messaging platform (Telegram, Discord, etc.) — this skill only needs the local file path.
3. Run identification:
   ```bash
   scripts/identify.sh /path/to/audio-file.ogg
   ```
4. Parse the JSON result and respond.
5. If Spotify is configured and active, queue the track.
6. Log the identification to `memory/music-log.json`.

**Supported formats:** OGG/Opus, MP3, WAV, FLAC, M4A. No transcoding needed — AudD accepts all common audio formats.

## Workflow — Spotify Queue

After a successful identification, if Spotify tokens exist at `~/.config/spotify/tokens.json`:

```bash
# Check if anything is playing
scripts/spotify-queue.sh status

# Queue the identified track
scripts/spotify-queue.sh queue "spotify:track:<track_id>"
```

If no active Spotify session is found, fall back to returning the Spotify link only.

Token refresh is handled automatically by `spotify-queue.sh` on 401 responses.

## Response Format

- **Found**: `🎵 {title} by {artist}` + Spotify link on next line. If Spotify active, note it was queued.
- **Found, no Spotify match**: `🎵 {title} by {artist}` (no link)
- **Not found**: "Couldn't identify that one. Try a longer clip with more of the melody (5+ seconds works best)."
- **Error**: "Something went wrong with the identification. Try again."
- **Missing AudD key**: "AudD API key not configured. Get one at https://audd.io and save to ~/.config/audd/api_key"

## Memory Logging

Append identified songs to `memory/music-log.json` (one JSON object per line):
```json
{"date":"2026-03-22","time":"14:30","title":"Viva La Vida","artist":"Coldplay","album":"Viva la Vida","spotify":"https://open.spotify.com/track/..."}
```

Create the file if it doesn't exist. For recall queries, read and present this log.

## Scripts

| Script | Purpose | Dependencies |
|---|---|---|
| `scripts/identify.sh <audio_file>` | POST audio to AudD, return JSON | curl, jq |
| `scripts/spotify-auth.py [--url]` | One-time Spotify OAuth flow | python3 |
| `scripts/spotify-queue.sh queue <uri>` | Queue track to active Spotify | curl, jq |
| `scripts/spotify-queue.sh status` | Check current Spotify playback | curl, jq |

Exit codes for `identify.sh`: 0=found, 1=not found, 2=error.

## API Reference

See `references/audd-api.md` for AudD endpoint details, parameters, and response format.
