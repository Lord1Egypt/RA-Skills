# Music Generator TopMediai

Generate AI music, BGM, or lyrics from natural language using TopMediai API.

## Installation
1. Place this skill in your workspace:
   `~/.openclaw/workspace/skills/music-generator-topmediai/`
2. Copy `.env.example` to `.env`
3. Fill your key:
   - `TOPMEDIAI_API_KEY=YOUR_KEY`
   - `TOPMEDIAI_BASE_URL=https://api.topmediai.com` (optional)
4. Install dependencies:
   - `pip install -r requirements.txt`

## Main Command
```text
/music_generator_topmediai mode=normal|bgm|lyrics prompt="..." style="Pop" mv="v5.0" gender="male"
```

### Modes
- `mode=normal` (default)
  - Generate lyrics first, then submit custom song generation, then poll.
- `mode=bgm`
  - Generate instrumental music with `instrumental=1`, then poll.
- `mode=lyrics`
  - Return lyrics only.

## Extra Commands
- Query tasks:
  - `topmediai_task_query ids="id1,id2"`
- Convert to MP4:
  - `topmediai_generate_mp4 song_id="..."`

## Under-the-Hood APIs
- `POST /v1/lyrics`
- `POST /v3/music/generate`
- `GET /v3/music/tasks?ids=...`
- `POST /v3/music/generate-mp4?song_id=...`
