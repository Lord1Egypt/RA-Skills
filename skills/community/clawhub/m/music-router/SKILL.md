# Music Router Skill

This skill solves the problem of incompatible music sharing links between different platforms. It provides direct links for Chinese platforms and automatically resolves all major international platforms via the Odesli (song.link) API.

## Features
- **Auto-Identification**: Automatically identifies the platform of the input music sharing link.
- **Precise Extraction**: Automatically extracts song name, artist information, and **album artwork**.
- **Multi-Platform Resolution**:
    - **Chinese Platforms**: Direct links for Netease Cloud Music and QQ Music.
    - **International Platforms**: Resolves direct links for Spotify, Apple Music, YouTube, YouTube Music, Amazon Music, Tidal, Deezer, and SoundCloud.
- **Optional Logging**: Conversion details can be recorded in `music-router/data/converter.log` via a command-line flag.

## Agent Usage Guide

### 1. Basic Call (Link Only)
The Agent can pass the sharing link directly.
```bash
python3 music-router/scripts/converter.py "https://y.music.163.com/m/song?id=1988907896"
```

### 2. Precise Call (Link + Song/Artist)
If the Agent already knows the song name and artist, it can be passed as the second argument to improve matching accuracy for Chinese platforms.
```bash
python3 music-router/scripts/converter.py "https://open.spotify.com/track/315aBOUD3xtj7sUMXtRgMV" "In The Stars Benson Boone"
```

### 3. Enabling Logs (Optional)
To enable detailed logging for debugging, add the `--log` flag. **Logging is disabled by default.**
```bash
python3 music-router/scripts/converter.py "https://open.spotify.com/track/123" --log
```

## Output Example (JSON)
```json
{
  "original_platform": "Spotify",
  "detected_song": "In The Stars Benson Boone",
  "thumbnail": "https://m.media-amazon.com/images/I/31OJGk6XaLL.jpg",
  "conversions": {
    "网易云音乐": "https://music.163.com/#/song?id=1941928009",
    "QQ音乐": "https://y.qq.com/n/ryqq/songDetail/001Paon617ueUC",
    "Apple Music": "https://geo.music.apple.com/us/album/_/1621221545?i=1621221910...",
    "YouTube": "https://www.youtube.com/watch?v=ZLck_PSMNew",
    "Amazon Music": "https://music.amazon.com/albums/B0B5FKVB4P?trackAsin=B0B5FK4MM1",
    "Tidal": "https://listen.tidal.com/track/226476015",
    "song.link (Aggregation)": "https://song.link/s/315aBOUD3xtj7sUMXtRgMV"
  }
}
```

## Supported Platforms
- **Direct Resolution**: Netease Cloud Music, QQ Music.
- **International Resolution**: Spotify, Apple Music, YouTube, YouTube Music, Amazon Music, Tidal, Deezer, SoundCloud.

## Notes
- **Odesli (song.link)**: This skill uses the Odesli API to resolve international links and fetch album artwork, ensuring high accuracy and a rich visual experience.
