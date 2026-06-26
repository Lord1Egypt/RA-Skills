# Stem Separation Reference

## All Modes

| Mode | Stems | Output | Use Case |
|------|-------|--------|----------|
| single | 1 | Specified stem only | Vocal isolation, drum extraction |
| two | 2 | vocals + instrumental | Karaoke tracks |
| four | 4 | vocals, drums, bass, other | Standard remixing |
| six | 6 | + guitar, piano | Full instrument separation |
| producer | 8 | + kick, snare, hihat | Beat production |
| studio | 12 | + cymbals, sub_bass, synth | Professional mixing |
| mastering | 16 | Maximum detail | Forensic analysis |

## Single Stem Options

`stem` parameter: vocals, drums, bass, guitar, piano, other

## API Endpoint

**All requests:** `POST https://api.skillboss.co/v1/pilot`
**Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`

```json
{
  "type": "audio",
  "capability": "stem separation",
  "inputs": {
    "url": "https://youtube.com/watch?v=VIDEO_ID",
    "mode": "four"
  },
  "prefer": "quality"
}
```

For single stem:
```json
{
  "type": "audio",
  "capability": "stem separation",
  "inputs": {
    "url": "https://youtube.com/watch?v=VIDEO_ID",
    "mode": "single",
    "stem": "vocals"
  },
  "prefer": "quality"
}
```

For local file (base64):
```json
{
  "type": "audio",
  "capability": "stem separation",
  "inputs": {
    "audio_data": "<base64-encoded-audio>",
    "filename": "song.mp3",
    "mode": "six"
  },
  "prefer": "balanced"
}
```

## Response Format

```json
{
  "data": {
    "result": {
      "download_urls": {
        "vocals": "https://...",
        "drums": "https://...",
        "bass": "https://...",
        "other": "https://..."
      },
      "quality_scores": {
        "vocals": 0.95,
        "drums": 0.88
      }
    }
  }
}
```

Result path: `result["data"]["result"]["download_urls"]`
