# Azure TTS Voice Reference

## Recommended voices by language

Each voice is the best-quality `MultilingualNeural` option for its language. Speech rates are approximate and used to estimate segment text length limits.

| Language | Voice Name | Speech Rate | Unit |
|----------|-----------|-------------|------|
| English | `en-US-AndrewMultilingualNeural` | ~150 | words/min |
| Chinese (Mandarin) | `zh-CN-YunxiMultilingualNeural` | ~250 | chars/min |
| Japanese | `ja-JP-MasaruMultilingualNeural` | ~350 | chars/min |
| Korean | `ko-KR-HyunsuMultilingualNeural` | ~300 | chars/min |
| French | `fr-FR-VivienneMultilingualNeural` | ~150 | words/min |
| German | `de-DE-FlorianMultilingualNeural` | ~140 | words/min |
| Spanish | `es-ES-XimenaMultilingualNeural` | ~160 | words/min |

## For unlisted languages

Search Azure TTS documentation for the best available voice. Prefer `MultilingualNeural` variants, falling back to the highest-quality `Neural` voice.

## Estimating segment length

```
speech_rate_per_second = speech_rate_per_minute / 60
max_units = time_window_seconds * speech_rate_per_second * 0.8   # 80% safety margin
```

For English: a 10-second window fits ~10 * 2.5 * 0.8 = 20 words.
For Chinese: a 10-second window fits ~10 * 4.2 * 0.8 = 33 characters.
