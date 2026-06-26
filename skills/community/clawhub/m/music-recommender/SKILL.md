---
name: music-recommender
description: "Analyze NetEase Cloud Music (网易云音乐) playlist and recommend songs matching their taste. Use when user asks for music recommendations, wants a daily playlist, says '推荐音乐', '今日歌单', 'music', or shares a NetEase playlist/album link. Recommend once per day, never repeat previously recommended songs. Supports free Bilibili links."
---

# Music Recommender

Analyze a user's NetEase Cloud Music playlist, profile their taste, and recommend songs with clickable Bilibili links (free, no membership required).

## Workflow

### Step 1 — Parse Playlist

Extract playlist ID from user's link. Supported formats:
- `https://music.163.com/playlist?id=XXXXX`
- `https://music.163.com/#/playlist?id=XXXXX`

Run the fetch script:

```bash
python3 {baseDir}/scripts/fetch_playlist.py <playlist_id> > /tmp/playlist_<id>.json
```

Output: JSON array of `{name, artists, album}` objects.

### Step 2 — Analyze Taste

Read the JSON output. Profile the user's taste:

1. **Top artists** — count occurrences, identify top 10-20
2. **Language mix** — estimate Chinese/English/Japanese/Korean ratio from song titles
3. **Genre tags** — infer from artists and song names (e.g. 气声唱法, 90s怀旧, indie folk, dream pop)
4. **Era** — identify decade distribution
5. **Mood** — upbeat/melancholic/dreamy/energetic based on song names and artists

Summarize the taste profile in 3-5 bullet points.

### Step 3 — Recommend

Based on the taste profile, recommend 10 songs that:
- **Match** the user's preferences (similar artists, genres, mood)
- **Are NOT** already in their playlist
- **Are diverse** — mix of Chinese and foreign, different sub-genres
- **Include both** well-known and lesser-known picks

For each recommended song, search Bilibili for a playable link:

```bash
python3 {baseDir}/scripts/search_bilibili.py "<artist> <song> 官方MV"
```

Output: `BV_ID|TITLE|URL`

### Step 4 — Format Output

Present the recommendations as a plain text list (NOT HTML/markdown links) for Telegram compatibility:

```
🎵 Vulpis 今日推荐歌单

**华语女声：**
1. 陈粒 — 奇妙能力歌
https://www.bilibili.com/video/BVxxxxx

2. ...

**欧美梦幻：**
6. ...
```

Rules for Telegram formatting:
- Use **bold** for section headers, NOT markdown links `[text](url)`
- Put URL on its own line after the song name
- Group by genre/language (华语/欧美/日语 etc.)
- Keep descriptions short (5-10 words)

### Step 5 — Record & De-duplicate

**IMPORTANT: Only recommend ONCE per day.** Before recommending:

1. Check if today's recommendation file exists:
   ```
   ~/.openclaw/workspace/music-history/YYYY-MM-DD.json
   ```
   If it exists, reply with today's list and say "今天已经推荐过了". Do NOT generate a new one.

2. If not, load the full history to avoid repeats:
   ```bash
   python3 {baseDir}/scripts/history.py show
   ```
   This outputs all previously recommended songs across all days.

3. When generating recommendations, exclude any song that appears in the history.

4. After generating, save today's recommendations:
   ```bash
   python3 {baseDir}/scripts/history.py save
   ```
   Pipe in JSON array: `[{"name":"...","artists":"...","bvid":"...","url":"..."}]`

### History Storage

```
~/.openclaw/workspace/music-history/
├── 2026-03-29.json
├── 2026-03-30.json
└── ...
```

Each file: JSON array of recommended songs for that day.

### Step 6 — (Optional) Extra Save

If user wants to save elsewhere, offer to:
- Write to Notion (Content Calendar or a Music DB)
- Generate an HTML page in the workspace
- Create a text file in the workspace

## Notes

- NetEase API endpoint: `https://music.163.com/api/v6/playlist/detail?id=<ID>&n=1000`
- Required headers: `User-Agent: Mozilla/5.0`, `Referer: https://music.163.com/`, `Cookie: os=pc;`
- Artist field is `ar` (not `artists`) in NetEase API response
- Bilibili search API: `https://api.bilibili.com/x/web-interface/search/all/v2?keyword=<query>`
- Required headers for Bilibili: `User-Agent: Mozilla/5.0`, `Referer: https://www.bilibili.com/`
- Default recommendation count: 10 songs
- Always use Bilibili links (free, no membership) instead of NetEase links
