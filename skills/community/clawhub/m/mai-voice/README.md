# mai-voice

Synthesize speech with Microsoft's **MAI-Voice-1** voices via **Azure AI Speech REST API**.

## Status

Reworked to use `curl` + SSML instead of the Azure Speech Python SDK, which is much less annoying and much easier to publish.

## Files

- `scripts/speak.sh` — speech synthesis CLI
- `_meta.json` — publishing metadata

## Required environment variables

```bash
export AZURE_SPEECH_KEY="YOUR_SPEECH_RESOURCE_KEY"
export AZURE_SPEECH_REGION="eastus"
```

## How to get the API key and region

1. Open the Azure portal.
2. Find your **Speech** or **Foundry Speech** resource.
3. Open **Keys and Endpoint**.
4. Copy one of the keys.
5. Note the resource region, for example `eastus`.
6. Export them as `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`.

If the voice API refuses to cooperate, the first thing to check is whether your Speech resource is in a region that actually supports MAI-Voice preview.

Optional:

```bash
export AZURE_SPEECH_OUTPUT_FORMAT="audio-24khz-160kbitrate-mono-mp3"
```

## Examples

```bash
bash scripts/speak.sh --text "Hello Steve"
bash scripts/speak.sh --text "Hello Steve" --voice en-us-Iris:MAI-Voice-1 --out /tmp/iris.mp3
bash scripts/speak.sh --text-file /tmp/input.txt --voice en-us-June:MAI-Voice-1 --style empathy --out /tmp/june.mp3
bash scripts/speak.sh --list-voices
```

## Supported voices

- `en-us-Jasper:MAI-Voice-1`
- `en-us-June:MAI-Voice-1`
- `en-us-Grant:MAI-Voice-1`
- `en-us-Iris:MAI-Voice-1`
- `en-us-Reed:MAI-Voice-1`
- `en-us-Joy:MAI-Voice-1`

## Caveats

- Not yet live-tested against your Azure account in this session.
- This script relies on Azure Speech REST behavior and SSML support for MAI voices.
- Style support is optional and uses `mstts:express-as`.

## Publish

Suggested publish command:

```bash
clawhub publish ./skills/mai-voice --slug mai-voice --name "MAI Voice" --version 0.1.0 --changelog "Initial release: Azure Speech REST MAI-Voice-1 synthesis skill with selectable voices"
```
