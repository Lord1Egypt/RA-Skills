---
name: microsoft-edge-tts
description: Use Microsoft Edge online TTS service to convert text to speech. Supports command line and module invocation, no API key required.
---

# Microsoft Edge TTS

Use Microsoft Edge's online TTS service to convert text to speech without requiring an API key. Use this skill when users need to convert text to speech, generate audio files, or read content aloud.

## Trigger Conditions

Trigger this skill when the user mentions any of the following keywords:
- TTS
- Speech synthesis
- Text-to-speech
- text-to-speech
- Read aloud
- edge-tts

## Quick Start

### Command Line Usage

```bash
# Basic usage
npx node-edge-tts -t 'Hello World'

# Specify output file
npx node-edge-tts -t 'Hello World' -f './output.mp3'

# Specify voice and language
npx node-edge-tts -t 'Hello world' -v 'en-US-AriaNeural' -l 'en-US'

# Adjust speaking rate and pitch
npx node-edge-tts -t 'Hello World' -r '+10%' --pitch '-5%'

# Generate subtitle file
npx node-edge-tts -t 'Hello World' -s
```

### Module Invocation

```javascript
const { EdgeTTS } = require('node-edge-tts')
// or
import { EdgeTTS } from 'node-edge-tts'

const tts = new EdgeTTS()
await tts.ttsPromise('Hello World', './output.mp3')
```

## Full Parameters

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--text` | `-t` | Text to convert (required) | - |
| `--filepath` | `-f` | Output file path | `./output.mp3` |
| `--voice` | `-v` | Voice name | `zh-CN-XiaoyiNeural` |
| `--lang` | `-l` | Language code | `zh-CN` |
| `--outputFormat` | `-o` | Output format | `audio-24khz-48kbitrate-mono-mp3` |
| `--rate` | `-r` | Speaking rate | `default` |
| `--pitch` | | Pitch | `default` |
| `--volume` | | Volume | `default` |
| `--saveSubtitles` | `-s` | Save subtitles | `false` |
| `--proxy` | `-p` | Proxy settings | - |
| `--timeout` | | Timeout (ms) | `10000` |

## Advanced Configuration

```javascript
const tts = new EdgeTTS({
  voice: 'zh-CN-XiaoxiaoNeural',
  lang: 'zh-CN',
  outputFormat: 'audio-24khz-96kbitrate-mono-mp3',
  saveSubtitles: true,
  proxy: 'http://localhost:7890',
  pitch: '-10%',
  rate: '+10%',
  volume: '-50%',
  timeout: 10000
})

await tts.ttsPromise('Text to convert', './output.mp3')
```

## Available Voices

- **Chinese**: `zh-CN-XiaoyiNeural`, `zh-CN-XiaoxiaoNeural`, `zh-CN-YunjianNeural`, `zh-CN-YunxiNeural`, `zh-CN-YunxiaNeural`
- **English**: `en-US-AriaNeural`, `en-US-GuyNeural`, `en-US-JennyNeural`
- **Japanese**: `ja-JP-KeitaNeural`, `ja-JP-NanamiNeural`
- **More**: Refer to [Microsoft Voice Support Documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

## Subtitle Format

Enabling `-s` generates a `.json` subtitle file with the same name:

```json
[
  { "part": "Hello", "start": 100, "end": 500 },
  { "part": "World", "start": 500, "end": 900 }
]
```

Time units are in milliseconds, `part` is the text segment.

## Common Scenarios

### 1. Quick Speech Generation
```bash
npx node-edge-tts -t 'Welcome to speech synthesis'
```

### 2. Long Text Segmentation
For very long texts, it is recommended to process in segments and then merge.

### 3. Multilingual Mixed
```bash
# Chinese
npx node-edge-tts -t 'Hello World' -v 'zh-CN-XiaoxiaoNeural'

# English
npx node-edge-tts -t 'Hello World' -v 'en-US-AriaNeural'
```

## Important Notes

1. **No API Key Required**: Directly uses Microsoft Edge's free online service
2. **Network Dependent**: Requires internet connection
3. **Rate Limiting**: Frequent calls may be restricted; it is recommended to control call frequency appropriately
4. **Proxy Support**: If encountering network issues, set a proxy via the `-p` parameter