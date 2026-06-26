# mai-transcribe

Transcribe audio with Microsoft's **MAI-Transcribe-1** model via **Azure AI Speech**.

## Status

Working, and actually tested, which is refreshing.

Confirmed against a live Azure Speech resource using the documented endpoint:

```text
POST /speechtotext/transcriptions:transcribe?api-version=2025-10-15
```

## Files

- `scripts/transcribe.js` — transcription CLI
- `scripts/common.js` — env, validation, extraction, and error helpers
- `_meta.json` — package metadata for publishing

## Required environment variables

```bash
export AZURE_SPEECH_ENDPOINT="https://YOUR-RESOURCE.cognitiveservices.azure.com"
export AZURE_SPEECH_KEY="YOUR_SPEECH_RESOURCE_KEY"
```

## How to get the API key

1. Open the Azure portal.
2. Find your **Speech** or **Foundry Speech** resource.
3. Open **Keys and Endpoint**.
4. Copy the endpoint and one of the keys.
5. Export them as `AZURE_SPEECH_ENDPOINT` and `AZURE_SPEECH_KEY`.

Use the Speech resource endpoint, for example:

```bash
export AZURE_SPEECH_ENDPOINT="https://your-resource.cognitiveservices.azure.com"
```

Do not use a random Foundry project URL here, unless you enjoy debugging 404s for sport.

Optional:

```bash
export AZURE_SPEECH_API_VERSION="2025-10-15"
```

## Examples

```bash
node scripts/transcribe.js /path/to/audio.wav
node scripts/transcribe.js /path/to/audio.ogg --out /tmp/transcript.txt
node scripts/transcribe.js /path/to/audio.m4a --json --out /tmp/transcript.json
node scripts/transcribe.js /path/to/audio.wav --language en-GB
node scripts/transcribe.js /path/to/audio.wav --help
```

## Output behavior

- default output is plain text
- default output path is `<input>.txt`
- `--json` writes the raw Azure response instead

## Caveats

- The script currently buffers the whole audio file into memory before upload. Fine for normal voice notes, less cute for giant recordings.
- This package is intentionally **transcription-only**. Voice and image were removed until they have real, confirmed endpoints.
- Audio is uploaded to Microsoft for processing. Don't send sensitive material unless you're comfortable with that.

## How this compares to the Whisper skill

This follows the same basic pattern as `openai-whisper-api`:

- a small script in `scripts/`
- a `SKILL.md` that tells the agent how to use it
- explicit environment variables
- no automatic Telegram or media-hook integration by itself

So if you want Whisper-like *agent behavior* in chat, that still depends on the agent deciding to run the script, or on adding a first-class OpenClaw tool/media integration later.

## Publish

Suggested publish command:

```bash
clawhub publish ./skills/mai-transcribe --slug mai-transcribe --name "MAI Transcribe" --version 0.1.0 --changelog "Initial release: Azure Speech MAI-Transcribe-1 transcription skill"
```
