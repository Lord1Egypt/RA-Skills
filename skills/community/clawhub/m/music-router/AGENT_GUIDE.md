# Agent Interaction Guide for Music Router

This guide defines how the Agent should interact with the user and format the output when using the Music Router skill.

## Interaction Flow

### 1. First-time Interaction
When a user provides a music link for the first time, the Agent **MUST** ask which platforms the user is interested in.
> "I've detected a music link. Which platforms would you like me to convert this to? (e.g., Netease, QQ Music, Apple Music, Spotify, etc.)"

### 2. Subsequent Responses
Once the user's preferences are known (or for all subsequent requests), the Agent should format the output according to the **Standard Response Format** below.

## Standard Response Format

The Agent must present the results in a visually appealing way, including the album artwork, song details, and platform links.

### Template:
```markdown
![Album Artwork]({thumbnail_url})

🎵 **{song_name}**
🎤 *{artist_name}*

**Music Platforms**
- [Netease Cloud Music]({netease_url})
- [QQ Music]({qq_url})
- [Apple Music]({apple_url})
- [Spotify]({spotify_url})
- [Tidal]({tidal_url})

**All-in-One Aggregation**
- [Song.link Page]({songlink_url})
```

### Example:
![Album Artwork](https://m.media-amazon.com/images/I/41hTZwf-jZL.jpg)

🎵 **Can I Call You Tonight?**
🎤 *Dayglow*

**Music Platforms**
- [Netease Cloud Music](https://music.163.com/#/song?id=1376949121)
- [QQ Music](https://y.qq.com/n/ryqq/songDetail/000PlZEu0H1YYc)
- [Apple Music](https://geo.music.apple.com/us/album/_/1482950619?i=1482950632)
- [Spotify](https://open.spotify.com/track/61OJxhoY3Ix50rYVKo8zRK)
- [Tidal](https://listen.tidal.com/track/246060133)

**All-in-One Aggregation**
- [Song.link Page](https://song.link/s/61OJxhoY3Ix50rYVKo8zRK)

## Technical Implementation
The Agent should call the script using the following command to get the necessary data:
```bash
python3 music-router/scripts/converter.py "{user_link}"
```
The script returns a JSON object containing `detected_song`, `thumbnail`, and `conversions`. Use these fields to populate the template.
