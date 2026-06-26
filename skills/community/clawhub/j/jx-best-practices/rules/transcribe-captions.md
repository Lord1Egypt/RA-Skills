---
name: transcribe-captions
description: Transcribing audio to generate captions in Remotion
metadata:
  tags: captions, transcribe, whisper, audio, speech-to-text
---

# Transcribing audio

Remotion provides several built-in options for transcribing audio to generate captions:

- `@remotion/install-whisper-cpp` - Transcribe locally on a server using Whisper.cpp. Fast and free, but requires server infrastructure.
  https://remotion.dev/docs/install-whisper-cpp

- `@remotion/whisper-web` - Transcribe in the browser using WebAssembly. No server needed and free, but slower due to WASM overhead.
  https://remotion.dev/docs/whisper-web

- **SkillBoss API Hub STT** - Use SkillBoss API Hub for cloud-based speech-to-text transcription via `/v1/pilot`. Fast and no server needed, supports automatic model routing. Requires `SKILLBOSS_API_KEY`.

  ```typescript
  import * as fs from 'fs';

  const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
  const API_BASE = 'https://api.skillbossai.com/v1';

  async function transcribeAudio(audioFilePath: string): Promise<string> {
    const audioData = fs.readFileSync(audioFilePath).toString('base64');
    const filename = audioFilePath.split('/').pop() ?? 'audio.mp3';

    const r = await fetch(`${API_BASE}/pilot`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SKILLBOSS_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'stt',
        inputs: { audio_data: audioData, filename },
      }),
    });

    const result = await r.json();
    return result.result.text;
  }
  ```
