---
name: minimax-music
description: "Generate AI music using MiniMax Music 2.5 API. Use when the user wants to: (1) generate instrumental/pure music, (2) generate songs with lyrics, (3) generate lyrics for songs. Supports various music styles (piano, pop, electronic, etc.) and Chinese/English lyrics. Triggers on phrases like '生成音乐', 'create music', '帮我写首歌', '生成纯音乐', 'AI作曲'."
---

# MiniMax Music Generation

Generate AI music using MiniMax Music 2.5 API.

## Prerequisites

Set the `MINIMAX_API_KEY` environment variable:

```bash
export MINIMAX_API_KEY="your-api-key-here"
```

## Quick Start

```bash
# Generate instrumental music
python3 ~/.openclaw/workspace/skills/minimax-music/scripts/minimax_music.py create \
  --prompt "Piano, Relaxing, Meditative" \
  --instrumental \
  --download ~/Music

# Generate song with lyrics
python3 ~/.openclaw/workspace/skills/minimax-music/scripts/minimax_music.py create \
  --prompt "Pop, Upbeat, Celebratory" \
  --lyrics "[Verse]\n阳光洒满大地\n[Chorus]\n快乐每一天" \
  --download ~/Music

# Generate lyrics first
python3 ~/.openclaw/workspace/skills/minimax-music/scripts/minimax_music.py lyrics \
  --prompt "一首关于春天的歌" \
  --output lyrics.txt
```

## Music Generation Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt` | Music style description (required) | - |
| `--lyrics` | Lyrics text with [Verse], [Chorus] markers | - |
| `--lyrics-file` | Path to lyrics file | - |
| `--instrumental` | Generate instrumental music (no vocals) | false |
| `--sample-rate` | Audio quality: 44100, 48000 | 44100 |
| `--bitrate` | Audio bitrate: 128000, 256000, 320000 | 256000 |
| `--format` | Output format: mp3, wav, flac | mp3 |
| `--download` | Directory to save audio file | - |
| `--model` | Model ID | music-2.5 |

## Prompt Examples

### Instrumental Music

```
# Relaxing piano
--prompt "Piano, Relaxing, Meditative, Soft, Ambient"

# Electronic ambient
--prompt "Electronic, Ambient, Atmospheric, Synthesizer, Chill"

# Orchestral
--prompt "Orchestra, Cinematic, Epic, Strings, Brass"

# Jazz
--prompt "Jazz, Smooth, Saxophone, Piano, Night Club"
```

### Songs with Lyrics

```bash
# Chinese pop
--prompt "Mandopop, Emotional, Ballad" \
--lyrics "[Verse]\n夜深人静\n思念着你\n[Chorus]\n心中的爱\n永不改变"

# English pop
--prompt "Pop, Upbeat, Energetic" \
--lyrics "[Verse]\nWalking down the street\nFeeling the beat\n[Chorus]\nLet's celebrate tonight"
```

## Lyrics Format

Use section markers to structure the song:

```
[Intro]
(Instrumental opening)

[Verse]
Main lyrics here

[Pre-Chorus]
Build-up section

[Chorus]
Main hook/refrain

[Bridge]
Contrast section

[Outro]
Ending section
```

## Daily Quota

MiniMax Token Plan subscriptions include:
- **music-2.5**: 7 generations/day (Plan 199)
- Quota resets daily at midnight

## Sending Audio via Feishu

After generating music, send to user's Feishu:

```python
import requests

# 1. Upload audio file
with open("music.mp3", "rb") as f:
    upload_resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/files",
        headers={"Authorization": f"Bearer {TENANT_ACCESS_TOKEN}"},
        files={"file": ("music.mp3", f, "audio/mpeg")},
        data={"file_type": "stream", "file_name": "music.mp3"}
    )
file_key = upload_resp.json()["data"]["file_key"]

# 2. Send file message
requests.post(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    headers={"Authorization": f"Bearer {TENANT_ACCESS_TOKEN}", "Content-Type": "application/json"},
    json={
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key}),
        "receive_id": USER_OPEN_ID
    }
)
```

## Rules

1. **Always check** `MINIMAX_API_KEY` is set before API calls.
2. **Use `--instrumental`** for pure music without vocals.
3. **Default to 44100 Hz, 256 kbps, MP3 format** for good quality and compatibility.
4. **Download immediately** - audio URLs expire after some time.
5. **Respect daily quota** - inform user if they've hit their limit.
6. **Provide audio file** to user after generation (download + share via Feishu if applicable).