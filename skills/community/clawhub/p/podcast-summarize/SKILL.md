---
name: podcast-summarize
description: Summarize podcast episodes into concise, actionable insights. Use when users want to get the key points from a podcast episode without listening to the entire audio. Supports audio files, URLs, RSS feeds, and podcast platform links.
---

# Podcast Summarize

Transform podcast episodes into structured, actionable summaries.

## When to Use

- User wants podcast episode key points
- User needs to quickly review podcast content
- User prefers reading over listening
- User wants to extract actionable insights from podcasts
- User shares podcast and wants a summary accompany

## Supported Inputs

1. **Audio file path** - Local MP3, M4A, WAV files
2. **Audio URL** - Direct link to audio file
3. **YouTube video** - Podcast on YouTube
4. **RSS feed URL** - Podcast RSS feed
5. **Podcast episode URL** - Link to episode on podcast platforms

## Summary Format

Provide summaries in this structure:

```
## 🎙️ 播客摘要

### 基本信息
- **标题**: [Episode Title]
- **时长**: [Duration]
- **日期**: [Publish Date]
- **播客**: [Podcast Name]

### 💡 核心要点 (3-5条)
1. [Key point 1]
2. [Key point 2]
3. ...

### 📝 详细摘要
[2-3 paragraph summary]

### 🎯 行动项 (如有)
- [Actionable insight 1]
- [Actionable insight 2]

### 🔗 相关链接
- [Mentioned resources]
```

## Process

1. **Audio Extraction**
   - For YouTube: Use yt-dlp to extract audio
   - For local files: Verify format and duration
   - For URLs: Download if needed

2. **Transcription**
   - Use Whisper (local or API) for transcription
   - Support multiple languages
   - Handle long audio (chunk if needed)

3. **Summarization**
   - Extract key themes
   - Identify actionable insights
   - Note timestamps for important sections
   - Highlight guest/host insights

## Tips

- Ask user preference: Brief (3 bullets) vs Detailed (full summary)
- Offer to extract specific segments if user has timestamps
- Provide follow-up questions based on content
- Suggest related podcasts if available

## Example Triggers

- "summarize this podcast"
- "这个播客讲的什么"
- "podcast summary"
- "播客摘要"
