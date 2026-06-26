---
name: mai-transcribe
description: Transcribe audio with Microsoft's MAI-Transcribe-1 model via Azure AI Speech.
homepage: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-transcribe
metadata: {"clawdbot":{"emoji":"🪟","requires":{"bins":["node"],"env":["AZURE_SPEECH_ENDPOINT","AZURE_SPEECH_KEY"]},"primaryEnv":"AZURE_SPEECH_KEY"}}
---

# MAI-Transcribe-1

Transcribe an audio file via Azure AI Speech using Microsoft's **MAI-Transcribe-1** model.

## Quick start

```bash
node {baseDir}/scripts/transcribe.js /path/to/audio.m4a
```

Defaults:
- Model: `mai-transcribe-1`
- Output: `<input>.txt`
- API version: `2025-10-15`

## Useful flags

```bash
node {baseDir}/scripts/transcribe.js /path/to/audio.ogg --out /tmp/transcript.txt
node {baseDir}/scripts/transcribe.js /path/to/audio.m4a --language en-GB
node {baseDir}/scripts/transcribe.js /path/to/audio.m4a --json --out /tmp/transcript.json
node {baseDir}/scripts/transcribe.js /path/to/audio.wav --model mai-transcribe-1
node {baseDir}/scripts/transcribe.js --help
```

## Required env vars

```bash
export AZURE_SPEECH_ENDPOINT="https://YOUR-RESOURCE.cognitiveservices.azure.com"
export AZURE_SPEECH_KEY="YOUR_SPEECH_RESOURCE_KEY"
```

## How to get the API key

1. Go to the Azure portal and open your **Speech** or **Foundry Speech** resource.
2. Open **Keys and Endpoint**.
3. Copy:
   - the resource endpoint, for example `https://your-resource.cognitiveservices.azure.com`
   - one of the resource keys
4. Export them:

```bash
export AZURE_SPEECH_ENDPOINT="https://YOUR-RESOURCE.cognitiveservices.azure.com"
export AZURE_SPEECH_KEY="YOUR_SPEECH_RESOURCE_KEY"
```

If `gh`-style copy-paste chaos is happening, the most important bit is that this skill expects the **Speech resource endpoint**, not a generic Foundry project URL.

Optional:

```bash
export AZURE_SPEECH_API_VERSION="2025-10-15"
```

## API shape

The script calls:

```text
POST {AZURE_SPEECH_ENDPOINT}/speechtotext/transcriptions:transcribe?api-version=2025-10-15
```

Headers:
- `Ocp-Apim-Subscription-Key: {AZURE_SPEECH_KEY}`

Multipart form fields:
- `audio`
- `definition`

Example `definition` payload:

```json
{
  "enhancedMode": {
    "enabled": true,
    "model": "mai-transcribe-1"
  }
}
```

## Notes

- This is the same style of skill as the Whisper one: a small documented script wrapper, not a built-in OpenClaw media pipeline.
- Tested successfully against a live Azure Speech resource.
- `--json` writes the raw Azure response for debugging or downstream processing.
- Audio is uploaded to Microsoft for processing.
