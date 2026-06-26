---
name: senseaudio-pronunciation-coach
description: Foreign language pronunciation coach — listen to standard TTS pronunciation, record yourself, get word-by-word feedback on what was wrong, then practice targeted drills. Use when users want to improve pronunciation, practice speaking a foreign language, or ask for "发音练习", "跟读", "纠音", "外语口语练习", "pronunciation practice", "how to pronounce", or any request to check or improve spoken language accuracy.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
        - xxd
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Pronunciation Coach

Listen → Record → Compare → Drill. The loop that actually improves pronunciation.

## Step 1: Choose Practice Material

Three input modes:

**A — Direct input:** User pastes a word, phrase, or sentence.

**B — Scene presets:** Offer these if the user isn't sure what to practice:

| Scene | Sample phrase |
|-------|--------------|
| 机场值机 | "I'd like a window seat, please." |
| 餐厅点餐 | "Could I have the menu, please?" |
| 商务会议 | "Let me walk you through the agenda." |
| 酒店入住 | "I have a reservation under my name." |
| 购物 | "Do you have this in a different size?" |
| 问路 | "Excuse me, how do I get to the station?" |

**C — Topic-based:** User says "练习 th 发音" or "练习 r 和 l 的区别" — generate 5 sentences targeting that phoneme.

Also ask: **目标语言？** (default: English)

## Step 2: Generate Standard Pronunciation

Produce two versions — slow for learning, normal for natural rhythm:

```bash
# Slow version (speed 0.75)
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"SenseAudio-TTS-1.0\",
    \"text\": \"<TEXT>\",
    \"stream\": false,
    \"voice_setting\": { \"voice_id\": \"<VOICE_ID>\", \"speed\": 0.75 },
    \"audio_setting\": { \"format\": \"mp3\" }
  }" -o slow.json
jq -r '.data.audio' slow.json | xxd -r -p > standard_slow.mp3

# Normal version (speed 1.0)
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"SenseAudio-TTS-1.0\",
    \"text\": \"<TEXT>\",
    \"stream\": false,
    \"voice_setting\": { \"voice_id\": \"<VOICE_ID>\", \"speed\": 1.0 },
    \"audio_setting\": { \"format\": \"mp3\" }
  }" -o normal.json
jq -r '.data.audio' normal.json | xxd -r -p > standard_normal.mp3
```

**Voice selection by language:**
- English: `female_0006_a` (clear, neutral accent)
- Chinese: `female_0008_c` (standard Mandarin)
- Default: `female_0006_a`

Tell the user: "慢速版和正常速版已生成。先听慢速版，感受每个音的发音，再听正常版感受自然节奏。准备好后，录一段你的跟读发给我。"

## Step 3: Transcribe User Recording

When the user uploads their recording:

```bash
curl -s -X POST https://api.senseaudio.cn/v1/audio/transcriptions \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -F "file=@<USER_RECORDING>" \
  -F "model=sense-asr-pro" \
  -F "response_format=verbose_json" \
  -F "language=<LANGUAGE_CODE>" \
  -F "timestamp_granularities[]=word" \
  > asr_result.json
```

Language codes: English → `en`, Chinese → `zh`, Japanese → `ja`, French → `fr`, Spanish → `es`

Extract the transcript: `jq -r '.text' asr_result.json`

## Step 4: Word-by-Word Comparison (LLM task)

Compare the ASR transcript against the original text yourself. Align words and identify mismatches:

**Comparison approach:**
1. Tokenize both original and ASR output into words
2. Use sequence alignment (like diff) to match them
3. Flag words where ASR output differs from original

**Diagnosis output format:**
```
跟读分析：

✓ "I'd like a"  — 正确
✗ "window"      — 识别为 "winder"（可能是 -ow 结尾发音问题）
✓ "seat"        — 正确
✗ "please"      — 识别为 "pleas"（末尾 -z 音可能不够清晰）

准确率：3/5 词 (60%)
```

**Common phoneme issues for Chinese speakers (English):**

| Misrecognized as | Likely problem | Phoneme |
|-----------------|----------------|---------|
| "free" for "three" | th → f | /θ/ |
| "light" for "right" | r → l confusion | /r/ |
| "wery" for "very" | v → w | /v/ |
| "sit" for "seat" | short vs long vowel | /ɪ/ vs /iː/ |
| "fink" for "think" | th → f | /θ/ |
| dropped final consonant | final stop deletion | /t/, /d/, /k/ |

When a word is misrecognized, infer the likely phoneme issue and name it specifically.

## Step 5: Targeted Drill

For each identified problem phoneme, generate a focused drill set:

**Phoneme drill library:**

| Phoneme | Drill words |
|---------|------------|
| /θ/ (th) | think, three, through, both, weather, teeth, breathe |
| /r/ | red, right, road, very, sorry, around, mirror |
| /r/ vs /l/ | right/light, road/load, rice/lice, pray/play |
| /v/ | very, voice, love, live, over, never, river |
| /iː/ vs /ɪ/ | seat/sit, beat/bit, sheep/ship, feel/fill |
| final /t/ | cat, hat, right, night, about, what, that |
| final /d/ | road, said, good, food, bad, head |

Present 3–5 drill words and generate slow TTS for each.

## Step 6: Track Progress

Save session results to `pronunciation_progress.json` in the current directory:

```json
{
  "sessions": [
    {
      "date": "<ISO date>",
      "text": "<practice text>",
      "accuracy": 0.6,
      "errors": ["window (/ow/)", "please (final /z/)"],
      "phonemes_drilled": ["/ow/", "/z/"]
    }
  ]
}
```

After 3+ sessions, show a summary:
```
发音弱项分析（最近5次练习）：

/θ/ (th)  ████████░░  4次出错  ← 重点练习
/r/       ████░░░░░░  2次出错
/iː/      ██░░░░░░░░  1次出错

建议：重点练习 th 发音，可以说"把舌尖放在上下牙之间，轻轻吹气"。
```

## Iteration

After each round, ask: "再来一遍，还是换一个句子？" Keep the loop going until the user is satisfied or accuracy reaches 90%+.
