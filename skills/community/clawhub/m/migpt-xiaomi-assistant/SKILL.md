---
name: migpt-xiaomi-assistant
description: "Deploy MiGPT on a Xiaomi smart speaker to replace the built-in AI with a custom LLM-powered voice assistant. Use when: (1) setting up mi-gpt on a Xiaomi/Redmi speaker, (2) troubleshooting MiNA vs MIoT TTS issues, (3) fixing Xiaomi account security verification loops, (4) optimizing voice assistant response latency, (5) configuring wake words and trigger keywords for mi-gpt. Covers X08E and other speaker models. NOT for: Google Home, Alexa, or non-Xiaomi smart speakers."
---

# MiGPT Xiaomi Voice Assistant Deployment

Deploy [mi-gpt](https://github.com/idootop/mi-gpt) v4.2.0+ on a Xiaomi smart speaker to replace the built-in AI with a custom LLM assistant.

## Prerequisites

- Node.js >= 18
- Xiaomi account with a supported smart speaker
- An OpenAI-compatible LLM API (DashScope, DeepSeek, OpenRouter, etc.)

## Quick Start

### 1. Initialize project

```bash
mkdir -p ~/projects/mi-gpt && cd ~/projects/mi-gpt
```

Create `package.json`:
```json
{
  "type": "module",
  "dependencies": { "dotenv": "^17.0.0", "mi-gpt": "^4.2.0" }
}
```

```bash
npm install
```

### 2. Create files

**app.js:**
```js
import "dotenv/config";
import config from "./.migpt.js";
import { MiGPT } from "mi-gpt";
const client = MiGPT.create(config);
await client.start();
```

**.env:**
```bash
OPENAI_MODEL=your-model
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://your-api-endpoint/v1
```

**.migpt.js** — See `references/config-template.md` for full template with comments.

### 3. Find your device's MIoT commands

Different speaker models use different MIoT siid/aiid values. Look up your model in [mi-gpt issues](https://github.com/idootop/mi-gpt/issues) or the [MIoT spec](https://home.miot-spec.com/).

Common values:

| Model | ttsCommand | wakeUpCommand | streamResponse |
|-------|-----------|---------------|----------------|
| X08E (Redmi 8寸) | [7, 3] | [7, 1] | false |
| LX04 | [5, 1] | [5, 3] | true |
| L05C | [5, 1] | [5, 3] | true |
| LX06 | [5, 1] | [5, 3] | true |
| L09A | [5, 1] | [5, 3] | true |

### 4. Run

```bash
nohup node app.js > migpt.log 2>&1 &
```

## Critical Issues & Fixes

### Issue 1: MiNA TTS returns success but no audio (X08E and some models)

**Symptom**: `mina.play({tts: '...'})` returns `true` but speaker stays silent.

**Cause**: Some models (notably X08E) don't support MiNA's `ubus mibrain/text_to_speech`. They require MIoT's `doAction`.

**Fix**: Ensure `ttsCommand` is set correctly. MiGPT will use MIoT `doAction(siid, aiid, text)` when `ttsCommand` is configured.

### Issue 2: MIoT login triggers security verification every time

**Symptom**: `securityStatus: 16` on every startup, even after completing SMS verification multiple times.

**Root cause**: `mi-service-lite` generates a random `deviceId` on every startup → Xiaomi treats each login as a new device → perpetual verification loop.

**Fix**: See `references/miot-auth-bypass.md` for the browser cookie injection method.

### Issue 3: streamResponse causes hang on some models

**Symptom**: MiGPT says "让我想想" then freezes.

**Cause**: `streamResponse: true` polls `MiNA.getStatus()` for playback state. On models where MiNA doesn't control the speaker (e.g., X08E), status always returns `"paused"`, causing the poll loop to malfunction.

**Fix**: Set `streamResponse: false`. If you also need keepAlive (continuous conversation) mode, patch `enterKeepAlive()` in `node_modules/mi-gpt/dist/index.js` to remove the `streamResponse` check. See `references/patches.md`.

### Issue 4: Native 小爱 AI races with custom AI

**Symptom**: Both 小爱 and your custom AI respond to the same query ("split personality").

**Mitigations** (pick one or combine):
1. Set `onAIAsking: ["嗯"]` — immediately interrupts 小爱 with a short TTS
2. Disable voice reply in 小爱 App (device settings → 语音回复 → off)
3. Use 全量接管模式: `callAIKeywords: [""]` — responds to all queries

### Issue 5: Wake word misrecognition

**Symptom**: 小爱's ASR mishears custom keywords (e.g., "花卷卷" → "花姐姐").

**Fix**: Add common misrecognition variants to `callAIKeywords` and `wakeUpKeywords`.

## LLM Model Selection

For voice assistants, **latency > intelligence**. Test your API endpoint:

```bash
time curl -s --max-time 15 YOUR_BASE_URL/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL","messages":[{"role":"user","content":"一句话回答：今天星期几"}],"max_tokens":30}'
```

Target: **< 3 seconds** for acceptable voice experience. Total end-to-end latency ≈ LLM time + 3-4s (polling + MIoT overhead).

## Reference Files

- `references/config-template.md` — Full `.migpt.js` configuration template with all options explained
- `references/miot-auth-bypass.md` — Browser cookie injection to bypass MIoT security verification
- `references/patches.md` — Required code patches for mi-gpt and mi-service-lite
- `references/latency-analysis.md` — End-to-end latency breakdown and optimization tips
