---
name: minimax-lyrics
description: Generate song lyrics with structure tags using MiniMax lyrics_generation API. Use when user asks to write lyrics, generate a song, or create a song. Triggers on: "帮我写歌词", "生成歌词", "写首歌词", "generate lyrics", "song lyrics".
---

# MiniMax Lyrics Generation

Generate structured song lyrics using MiniMax `lyrics_generation` API.

## Setup

Create `~/.openclaw/workspace/skills/minimax-lyrics/lyrics_config.json`:

```json
{
  "api_key": "YOUR_MINIMAX_API_KEY"
}
```

## Quick Use

```bash
python3 ~/.openclaw/workspace/skills/minimax-lyrics/scripts/generate_lyrics.py \
  --prompt "轻柔抒情流行，温柔女声，慢节奏，深情浪漫" \
  --title "夏日海风"
```

## API Parameters

| 参数 | 说明 |
|------|------|
| `mode` | `write_full_song`（写完整歌曲）或 `edit`（编辑/续写） |
| `prompt` | 歌曲主题、风格描述（0-2000字符） |
| `title` | 歌曲标题（传入后输出保持该标题） |
| `lyrics` | 现有歌词（仅 `edit` 模式） |

## Output

Returns:
- `song_title`: 生成的歌名
- `style_tags`: 风格标签（如 `Mandopop, Summer Vibe`）
- `lyrics`: 带结构标签的完整歌词，支持14种标签：`[Intro]` `[Verse]` `[Pre-Chorus]` `[Chorus]` `[Hook]` `[Drop]` `[Bridge]` `[Solo]` `[Build-up]` `[Instrumental]` `[Breakdown]` `[Break]` `[Interlude]` `[Outro]`

歌词可直接传给 `minimax-feishu-music` skill 生成歌曲。

## Example Output

```
song_title: 夏日海风的约定
style_tags: Mandopop, Summer Vibe, Romance, Lighthearted, Beach Pop
lyrics: |
  [Intro]
  (Ooh-ooh-ooh)
  (Yeah)
  阳光洒满了海面

  [Verse 1]
  海风轻轻吹拂你发梢
  Smiling face, like a summer dream
  浪花拍打着脚边
  Leaving footprints, you and me

  [Pre-Chorus]
  你说这感觉多么奇妙
  (So wonderful)
  想要永远停留在这一秒

  [Chorus]
  Oh, 夏日的海边，我们的约定
  阳光下，你的身影，如此动听

  [Hook]
  永远在一起

  [Bridge]
  时间慢慢走，我们一起老

  [Solo]
  器乐演奏段落

  [Interlude]
  (Ooh-ooh)

  [Break]
  突然安静

  [Outro]
  (Ooh-ooh-ooh)
```

## Notes

- `write_full_song` 模式：根据 prompt 自动生成完整歌词结构
- `edit` 模式：续写或修改已有歌词
- 生成后展示给用户看，用户确认后再生成歌曲
