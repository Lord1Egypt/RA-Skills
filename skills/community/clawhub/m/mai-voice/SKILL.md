---
name: mai-voice
description: Synthesize speech with Microsoft's MAI-Voice-1 voices via Azure AI Speech REST API.
homepage: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/mai-voices
metadata: {"clawdbot":{"emoji":"🗣️","requires":{"bins":["bash","curl"],"env":["AZURE_SPEECH_KEY","AZURE_SPEECH_REGION"]},"primaryEnv":"AZURE_SPEECH_KEY"}}
---

# MAI-Voice-1

Synthesize speech with Azure AI Speech using Microsoft's **MAI-Voice-1** voices.

## Quick start

```bash
{baseDir}/scripts/speak.sh --text "Hello Steve"
```

Defaults:
- Voice: `en-us-Jasper:MAI-Voice-1`
- Output: `./mai-voice.mp3`
- Format: `audio-24khz-160kbitrate-mono-mp3`

## Useful flags

```bash
{baseDir}/scripts/speak.sh --text "Hello Steve" --voice en-us-Iris:MAI-Voice-1 --out /tmp/iris.mp3
{baseDir}/scripts/speak.sh --text-file /tmp/input.txt --voice en-us-June:MAI-Voice-1 --style empathy --out /tmp/june.mp3
{baseDir}/scripts/speak.sh --text "Let's go" --voice en-us-Jasper:MAI-Voice-1 --style excitement
{baseDir}/scripts/speak.sh --list-voices
```

## Required env vars

```bash
export AZURE_SPEECH_KEY="YOUR_SPEECH_RESOURCE_KEY"
export AZURE_SPEECH_REGION="eastus"
```

## How to get the API key and region

1. Go to the Azure portal and open your **Speech** or **Foundry Speech** resource.
2. Open **Keys and Endpoint**.
3. Copy one of the resource keys.
4. Copy the resource region, for example `eastus`.
5. Export them:

```bash
export AZURE_SPEECH_KEY="YOUR_SPEECH_RESOURCE_KEY"
export AZURE_SPEECH_REGION="eastus"
```

The MAI-Voice docs currently point at **East US** for preview access, so if you are not using `eastus`, double-check that your resource actually supports the model before blaming the script.

Optional:

```bash
export AZURE_SPEECH_OUTPUT_FORMAT="audio-24khz-160kbitrate-mono-mp3"
```

## Supported voices

- `en-us-Jasper:MAI-Voice-1`
- `en-us-June:MAI-Voice-1`
- `en-us-Grant:MAI-Voice-1`
- `en-us-Iris:MAI-Voice-1`
- `en-us-Reed:MAI-Voice-1`
- `en-us-Joy:MAI-Voice-1`

## API shape

The script calls:

```text
POST https://{AZURE_SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1
```

Headers:
- `Ocp-Apim-Subscription-Key: {AZURE_SPEECH_KEY}`
- `Content-Type: application/ssml+xml`
- `X-Microsoft-OutputFormat: {format}`
- `User-Agent: curl`

Body:
- SSML with a MAI voice name
- optional `mstts:express-as` style wrapper

## Notes

- This uses the Azure Speech REST API, not the Python SDK.
- Voice selection is user-configurable.
- Style is optional and applied via SSML.
- MAI-Voice-1 is currently public preview.
