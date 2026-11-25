---
name: musicwave-music-tools
description: Find the BPM and key of an audio file from a public link, and look up notes, chords, Camelot codes and delay times for any key or tempo. Free, with no account or API key. Sends requests to musicwave.ai.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://www.musicwave.ai/integrations/music-tools
---

# MusicWave Music Tools

Use this skill when someone asks for:

- the tempo (BPM), key or Camelot code of a song or audio file,
- the notes, chords or common progressions of a key, or which keys mix well with it,
- delay times, half time or double time for a tempo.

The tools are free and run on MusicWave's servers. They need no account or key.

## How to call them

Every call is one POST to the same address. Escape the person's text as JSON before you put it in the body.

```bash
curl -s https://www.musicwave.ai/mcp/music-tools \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_tempo_info","arguments":{"bpm":128}}}'
```

Read `result.content[0].text` for a plain summary, or `result.structuredContent` for the numbers.

| Tool | Arguments | What you get |
| --- | --- | --- |
| `get_key_info` | `{"key": "F# minor"}`: a key name such as "Bb major" or "Am", or a Camelot code such as "11A" | Notes, chords, progressions, Camelot code and mixing keys |
| `get_tempo_info` | `{"bpm": 128}`: from 20 to 300 | Delay times in milliseconds, half and double time, bar length and typical genres |
| `analyze_audio_file` | `{"file": {"download_url": "https://example.com/song.mp3", "file_id": "track"}}`: a direct public https link, and any short label as `file_id` | BPM, key, Camelot code, energy, danceability and loudness |

## Limits

- Audio: MP3, WAV, M4A, FLAC, OGG or Opus, up to 60 MB and 12 minutes. A typical song takes about 10 seconds; long files take longer. The file is read once and not stored.
- Links must point straight at the audio file, not at a web page that plays it.
- If you get "too many files", wait and try again later.

More: https://www.musicwave.ai/integrations/music-tools
Privacy: https://www.musicwave.ai/privacy
Support: support@musicwave.ai
