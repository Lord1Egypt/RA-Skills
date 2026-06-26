---
name: gladia-youtube-transcribe
description: "Transcribe speech from YouTube videos or audio URLs into text using Gladia API with up to 10 free hours of monthly transcription. Use when: you need to summarize YouTube videos (especially Cantonese/Chinese content without captions), convert MP3/audio to text, or extract speech from any video URL. NOT for: private/unlisted content, real-time transcription needs, or when Gladia quota is exhausted."
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "env": ["GLADIA_API_KEY"],
            "bins": ["curl", "python3"]
          },
        "credentials": ["GLADIA_API_KEY"],
        "install": []
      }
  }
---

# Video/Audio Transcription Skill

## Overview

This skill provides automated transcription for video and audio content using Gladia API. It converts spoken content from YouTube videos, MP3 files, or any accessible audio/video URL into text, which can then be summarized by an LLM.

## Use Cases

- **YouTube Video Summary** - Transcribe YouTube videos for LLM summarization (especially useful for Cantonese/Chinese content without captions)
- **MP3/WAV to Text** - Convert audio files to transcript
- **Video Content Extraction** - Extract speech from any publicly accessible video URL
- **Podcast Transcription** - Convert podcast episodes to text

## Service: Gladia API

### What is Gladia?

Gladia is an audio transcription API that supports multiple languages including Cantonese. It provides both async (pre-recorded) and real-time transcription.

### Free Tier (as of March 2026)

| Feature | Free Tier |
|---------|-----------|
| Monthly transcription | **10 hours** |
| Renewal | **Monthly** (resets automatically) |
| New streams limit | 5 per minute |
| Languages | All included |
| Cost after quota | $0.61/hour (async) / $0.75/hour (real-time) |

### How to Sign Up

1. Visit [gladia.io](https://gladia.io)
2. Click "Try for free" → Sign up with email
3. Go to Dashboard → API Keys
4. Create a new API key
5. Copy the key (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Checking Usage

1. Log in to [Gladia Dashboard](https://app.gladia.io)
2. Navigate to **Usage** or **Billing** section
3. View current month consumption (hours/minutes used)

Alternatively, you can check via API:
```bash
curl -X GET "https://api.gladia.io/v2/usage" -H "x-gladia-key: YOUR_API_KEY"
```

## Setup

### Step 1: Save Your API Key

**Recommended: Set in current session**
```bash
export GLADIA_API_KEY="your-api-key-here"
```

**Or add to ~/.bashrc** (ensure ~/.bashrc is in .gitignore):
```bash
echo 'export GLADIA_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Note:** Storing secrets in shell rc files is discouraged due to risk of accidental commits. Prefer setting the environment variable directly in your session or use a secrets manager.

### Step 2: Verify Key Works

Test that your API key is valid by checking usage:
```bash
curl -X GET "https://api.gladia.io/v2/usage" -H "x-gladia-key: $GLADIA_API_KEY"
```

If successful, you'll see your usage information. If you get an auth error, check your API key.

## How to Use

### Command Line

```bash
# Navigate to skill directory (where you installed the skill)
cd /path/to/video-transcription

# Basic usage
./scripts/youtube_transcribe.sh "YOUTUBE_URL"

# Save to specific file
./scripts/youtube_transcribe.sh "YOUTUBE_URL" /path/to/output.txt
```

### Via OpenClaw

1. Provide a YouTube URL or video link
2. The skill will:
   - Submit transcription job to Gladia
   - Poll for completion (~1-2 min for 10-15 min videos)
   - Return the full transcript

### Script Location

```
/path/to/video-transcription/scripts/youtube_transcribe.sh
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GLADIA_API_KEY` | Yes | Your Gladia API key |

### Output

The script saves transcripts to a `transcripts/` subdirectory in the skill folder:
```
/path/to/video-transcription/transcripts/
```

## Privacy & Security Notes

- **NEVER** share your API key publicly
- **NEVER** include your API key in any skill documentation or code commits
- **IMPORTANT**: Do NOT store API keys in shell rc files (~/.bashrc, ~/.zshrc) or config files that might be committed to version control
- Use session-only environment variables: `export GLADIA_API_KEY='your-key'`
- Or use a secrets manager (e.g., 1Password, AWS Secrets Manager)
- Output transcripts may contain sensitive content - handle accordingly

## Limitations

- Video must be publicly accessible (no private/unlisted content)
- Audio quality affects transcription accuracy
- Some copyrighted content may have restrictions
- Processing time depends on video length (~10 seconds per minute of video)
- Free quota resets monthly; excess usage incurs charges

## Troubleshooting

### "Failed to call the url"
- The video URL may be inaccessible or private
- Try a different video URL

### "Quota exceeded"
- You've reached the 10-hour monthly limit
- Wait for quota reset next month, or upgrade to paid plan

### "Authentication failed"
- Check your API key is correct
- Ensure `GLADIA_API_KEY` environment variable is set

## Alternative Services

If Gladia quota is exhausted:

| Service | Free Tier | Notes |
|---------|-----------|-------|
| AssemblyAI | Limited | Requires credit card |
| Deepgram | $0 credit | Pay-per-use |
| YouTube Transcript | Free (if available) | Only works if video has captions |

## Future Enhancements

Potential improvements:
- Add speaker diarization (identify different speakers)
- Support real-time transcription
- Automatic LLM summarization after transcription
- Multi-language translation
- Save transcripts to cloud storage

---

*Last updated: March 2026*
