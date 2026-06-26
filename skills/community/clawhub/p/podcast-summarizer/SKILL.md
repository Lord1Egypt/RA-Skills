---
name: podcast-summarizer
description: Summarize podcast episodes from Spotify, Apple Podcasts, or RSS feeds. Extracts transcripts and generates summaries.
---

# Podcast Summarizer 🎙️

Summarize podcast episodes from various platforms.

## Supported Platforms
- Spotify (via page scraping + RSS lookup)
- Apple Podcasts
- Direct RSS/MP3 URLs

## Usage

```bash
# Summarize a Spotify episode
python3 {baseDir}/scripts/summarize_podcast.py "https://open.spotify.com/episode/xxx"

# Summarize from RSS feed
python3 {baseDir}/scripts/summarize_podcast.py "https://example.com/feed.xml" --episode 1

# Summarize from direct MP3
python3 {baseDir}/scripts/summarize_podcast.py "https://example.com/episode.mp3"
```

## Options
- `--language zh` - Specify language for transcription (default: auto)
- `--length short|medium|long` - Summary length
- `--transcript-only` - Output transcript without summary
- `--output FILE` - Save to file

## Requirements
- `whisper` CLI for transcription
- `OPENAI_API_KEY` or `GEMINI_API_KEY` for summarization

## How it works
1. **Spotify/Apple**: Scrapes episode info, finds RSS feed, downloads audio
2. **RSS**: Parses feed, downloads episode audio
3. **MP3**: Downloads directly
4. **Transcribe**: Uses Whisper for speech-to-text
5. **Summarize**: Uses LLM to generate structured summary

## Notes
- Spotify doesn't provide direct audio access; we try to find the original RSS feed
- For best results, use the podcast's RSS feed directly
- SoundOn podcasts can often be accessed via their RSS feeds

## SoundOn Podcasts (台灣)

SoundOn 是台灣主要的 Podcast 託管平台。RSS feed 格式：
```
https://feeds.soundon.fm/podcasts/{podcast-id}/soundon.xml
```

找到 RSS feed 的方法：
1. 去 player.soundon.fm 搜尋節目
2. URL 中的 `feed_url` 參數是 base64 編碼的 RSS URL
3. 解碼後可取得完整的 RSS feed

音檔 URL 格式：
```
https://rss.soundon.fm/rssf/{podcast-id}/feedurl/{episode-id}/rssFileVip.mp3
```

## Example: 藝視 Art.Market

```bash
# RSS Feed
https://feeds.soundon.fm/podcasts/5c1bdcf0-8ef0-4342-a82e-8803ff85f10c/soundon.xml

# 下載並轉錄最新一集
curl -o episode.mp3 "https://rss.soundon.fm/rssf/5c1bdcf0-8ef0-4342-a82e-8803ff85f10c/feedurl/{episode-id}/rssFileVip.mp3"
whisper episode.mp3 --language zh --model small
```
