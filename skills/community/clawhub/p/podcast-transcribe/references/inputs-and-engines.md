# Inputs and Engines

## Supported Inputs

| Input Type | Example | Notes |
|------------|---------|-------|
| Xiaoyuzhou URL | `https://www.xiaoyuzhoufm.com/episode/...` | Resolved directly |
| Apple Podcasts URL | `https://podcasts.apple.com/us/podcast/.../id...?i=...` | Uses iTunes lookup |
| YouTube URL | `https://www.youtube.com/watch?v=...` | Requires `yt-dlp` |
| Pocket Casts URL | `https://pca.st/episode/...` | oEmbed plus embed-page discovery |
| Castro URL | `https://castro.fm/episode/...` | HTML audio extraction |
| Ximalaya URL | `https://www.ximalaya.com/sound/...` | Mobile track API |
| Podcast Addict URL | `https://podcastaddict.com/episode/...` | Decodes audio URL from the path |
| Podcast page URL | `https://example.fm/episodes/42` | Looks for `og:audio`, RSS, audio tags, or JSON-LD |
| Direct audio URL | `https://.../file.mp3` | Download then transcribe |
| Local file | `./audio/interview.mp3` | Transcribe directly |

Spotify URLs are detected but rejected because the audio is DRM-protected.

Generic episode-page support works best when the page exposes:

- `og:audio` or similar metadata
- `<audio>` or `<source>` tags
- JSON-LD `AudioObject` or `PodcastEpisode`
- an RSS or Atom feed that links back to the current episode page

## Engine Selection

Provider environment variables:

| Provider | Env Variable | Engine Flag |
|----------|--------------|-------------|
| Local (Apple Silicon) | none | `mlx-whisper` |
| ElevenLabs | `ELEVENLABS_API_KEY` | `elevenlabs` |
| OpenAI | `OPENAI_API_KEY` | `openai` |
| Groq | `GROQ_API_KEY` | `groq` |
| Deepgram | `DEEPGRAM_API_KEY` | `deepgram` |
| Gladia | `GLADIA_API_KEY` | `gladia` |
| AssemblyAI | `ASSEMBLYAI_API_KEY` | `assemblyai` |
| Rev.ai | `REVAI_API_KEY` | `revai` |

Auto-detection order:

1. Local `mlx-whisper`, if installed
2. ElevenLabs, OpenAI, Groq, Deepgram, Gladia, AssemblyAI, Rev.ai
3. Fallback to `mlx-whisper`

Use `--engine <provider>` only when the user explicitly wants a backend or when offline local transcription is required.

## External Dependencies

| Scenario | Dependency | Install |
|----------|------------|---------|
| YouTube extraction | `yt-dlp` | `brew install yt-dlp` or `pip install yt-dlp` |
| Local transcription | `ffmpeg`, `python3` | `brew install ffmpeg` |
| `mlx-whisper` runtime | `podcast-helper setup mlx-whisper` | Installs the stable local runtime |

Quick environment check:

```bash
printenv ELEVENLABS_API_KEY
podcast-helper doctor
```
