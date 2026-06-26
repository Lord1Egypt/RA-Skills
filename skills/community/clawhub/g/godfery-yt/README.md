# YouTube 📹

YouTube research and transcription skill for [Clawdbot](https://clawdbot.com).

## Features

- 📹 **Video Details** - Get title, description, stats, publish date
- 📝 **Transcripts** - Extract transcripts with timestamps
- 📺 **Channel Info** - Get channel details and recent videos
- 🔍 **Search** - Find videos by keywords
- 🎬 **Playlist Info** - Get playlist details

## Installation

```bash
clawdhub install youtube
```

## Configuration

Get a SkillBoss API key from [SkillBoss API Hub](https://skillbossai.com):
1. Sign in to your account
2. Navigate to API settings
3. Copy your API key

```bash
export SKILLBOSS_API_KEY="your-skillboss-api-key"
```

Or add to `~/.clawdbot/clawdbot.json`:
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

## Usage Examples

```
"Find the latest Lex Fridman podcast episode"
"Get the transcript for this video: https://youtube.com/watch?v=Z-FRe5AKmCU"
"Search YouTube for Laravel tutorials"
"Show me recent videos from channel UCSHZKyawb77ixDdsGog4iWA"
"Get video details for Z-FRe5AKmCU"
```

## Credits

This skill uses the [youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) by Zubeid Hendricks for YouTube Data API integration, authenticated via SkillBoss API Hub.

## License

MIT
