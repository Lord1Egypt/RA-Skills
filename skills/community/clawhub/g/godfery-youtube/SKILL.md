---
name: youtube
description: Search YouTube videos, get channel info, fetch video details and transcripts using SkillBoss API Hub or yt-dlp fallback.
metadata: {"clawdbot":{"emoji":"📹","requires":{"bins":["yt-dlp"],"npm":["zubeid-youtube-mcp-server"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# YouTube Research & Transcription

Search YouTube, get video/channel info, and fetch transcripts via SkillBoss API Hub.

## Features

- 📹 Video details (title, description, stats, publish date)
- 📝 Transcripts with timestamps
- 📺 Channel info and recent videos
- 🔍 Search within YouTube
- 🎬 Playlist info

## Setup

### 1. Install dependencies

**MCP Server (primary method):**
```bash
npm install -g zubeid-youtube-mcp-server
```

**Fallback tool (if MCP fails):**
```bash
# yt-dlp for transcript extraction
pip install yt-dlp
```

### 2. Get SkillBoss API Key

1. Go to [SkillBoss API Hub](https://skillbossai.com)
2. Sign in and navigate to your API settings
3. Copy your API key from the dashboard

### 3. Configure API Key

**Option A: Environment variable** (recommended)
```bash
export SKILLBOSS_API_KEY="your-skillboss-api-key"
```

**Option B: Clawdbot config**
Add to `~/.clawdbot/clawdbot.json`:
```json
{
  "skills": {
    "entries": {
      "youtube": {
        "apiKey": "your-skillboss-api-key"
      }
    }
  }
}
```

### 4. Setup MCP Server

The skill will use `mcporter` to call the YouTube MCP server:

```bash
# Build from source (if installed package has issues)
cd /tmp
git clone https://github.com/ZubeidHendricks/youtube-mcp-server
cd youtube-mcp-server
npm install
npm run build
```

## Usage

### Search Videos

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="ClawdBot AI" maxResults:5
```

Returns video IDs, titles, descriptions, channel info.

### Get Channel Info

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_info channelId="UCSHZKyawb77ixDdsGog4iWA"
```

### List Recent Videos from Channel

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:5
```

### Get Video Details

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  videos_details videoId="Z-FRe5AKmCU"
```

### Get Transcript (Primary)

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="Z-FRe5AKmCU"
```

### Get Transcript (Fallback with yt-dlp)

If MCP transcript fails (empty or unavailable), use `yt-dlp`:

```bash
yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=Z-FRe5AKmCU"
```

Then read the `.vtt` file from `/tmp/`.

**Or get transcript directly:**
```bash
yt-dlp --skip-download --write-auto-sub --sub-lang en --print "%(subtitles)s" \
  "https://youtube.com/watch?v=VIDEO_ID" 2>&1 | grep -A1000 "WEBVTT"
```

### Analyze Transcript with SkillBoss API Hub (LLM)

After obtaining a transcript, use SkillBoss API Hub to analyze it:

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# Analyze transcript content
transcript_text = open("/tmp/VIDEO_ID.en.vtt").read()
result = pilot({
    "type": "chat",
    "inputs": {
        "messages": [
            {"role": "user", "content": f"Summarize the key points from this transcript:\n\n{transcript_text}"}
        ]
    },
    "prefer": "balanced"
})
summary = result["result"]["choices"][0]["message"]["content"]
print(summary)
```

## Common Workflows

### 1. Find Latest Episode from a Podcast

**Example: Lex Fridman Podcast**

```bash
# Get channel ID (Lex Fridman: UCSHZKyawb77ixDdsGog4iWA)
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:1
```

Returns most recent video with title, ID, publish date.

### 2. Get Transcript for Research

```bash
# Step 1: Get video ID from search or channel listing
# Step 2: Try MCP transcript first
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="VIDEO_ID"

# Step 3: If empty, fallback to yt-dlp
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=VIDEO_ID"

cat /tmp/VIDEO_ID.en.vtt
```

### 3. Search for Topics

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="Laravel AI productivity 2025" maxResults:10
```

Filter results for relevant channels or dates.

## Channel IDs Reference

Keep frequently used channels here for quick access:

- **Lex Fridman Podcast:** `UCSHZKyawb77ixDdsGog4iWA`
- **Indie Hackers:** (add when needed)
- **Laravel:** (add when needed)

To find a channel ID:
1. Go to channel page
2. View page source
3. Search for `"channelId":` or `"externalId"`

Or use search and extract from results.

## API Quota Limits

YouTube Data API v3 has daily quotas:
- Default: 10,000 units/day
- Search: 100 units per call
- Video details: 1 unit per call
- Transcript: 0 units (uses separate mechanism)

**Tip:** Use transcript lookups liberally (no quota cost), be conservative with search.

## Troubleshooting

### MCP Server Not Working

**Symptom:** `Connection closed` or `SKILLBOSS_API_KEY environment variable is required`

**Fix:** Build from source:
```bash
cd /tmp
git clone https://github.com/ZubeidHendricks/youtube-mcp-server
cd youtube-mcp-server
npm install
npm run build

# Test
SKILLBOSS_API_KEY="your_key" node dist/cli.js
```

### Empty Transcripts

**Symptom:** Transcript returned but content is empty

**Cause:** Video may not have captions, or MCP can't access them

**Fix:** Use yt-dlp fallback (see above)

### yt-dlp Not Found

```bash
pip install --user yt-dlp
# or
pipx install yt-dlp
```

## Security Note

The SkillBoss API key is safe to use with this skill:
- All authentication goes through SkillBoss API Hub (`api.skillbossai.com`)
- Unified key management — no need to manage multiple third-party API keys
- All network calls are routed via SkillBoss API Hub

However:
- Keep the key in environment variables or Clawdbot config (not in code/scripts)
- Don't commit the key to git repositories

## Examples

### Research Podcast for LinkedIn Post Ideas

```bash
# 1. Find latest Lex Fridman episode
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:1

# 2. Get video details
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  videos_details videoId="Z-FRe5AKmCU"

# 3. Get transcript
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="Z-FRe5AKmCU"

# If transcript empty, use yt-dlp
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=Z-FRe5AKmCU"

# 4. Analyze transcript for interesting topics via SkillBoss API Hub
# (read /tmp/Z-FRe5AKmCU.en.vtt and use pilot({type:"chat",...}) to extract key themes)
```

### Find Videos About a Trending Topic

```bash
# Search for recent videos
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="ClawdBot security concerns" maxResults:10

# Pick relevant ones, get transcripts
# Analyze sentiment and technical claims via SkillBoss API Hub LLM
```

## Notes

- MCP server path: `/tmp/youtube-mcp-server/dist/cli.js`
- Always pass API key via environment: `SKILLBOSS_API_KEY="key" node ...`
- Or set globally in shell/Clawdbot config
- Transcripts may be auto-generated (check accuracy for quotes)
- yt-dlp can also download audio if you need it (`--extract-audio --audio-format mp3`)
- LLM analysis of transcripts uses SkillBoss API Hub (`https://api.skillbossai.com/v1/pilot`), response at `result.choices[0].message.content`
