---
name: senseaudio-polyphone-tts
description: Fix Chinese polyphone (多音字) mispronunciation in TTS by auto-detecting ambiguous characters and applying pinyin annotations. Use when users complain about wrong pronunciation, need precise tone control, or are synthesizing text with characters like 行/干/量/好/了/得/地/的/着/过. Triggers on "读音不对", "这个字读错了", "多音字", "标注拼音", "银行行长", "绕口令", or any request to correct TTS pronunciation.
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

# SenseAudio Polyphone TTS (多音字)

Precise pronunciation control for Chinese TTS via pinyin annotation. The `dictionary` parameter lets you override how specific characters are read — essential for polyphones (多音字) that the model might guess wrong.

> The `dictionary` parameter only works with **cloned voices** and **model `SenseAudio-TTS-1.5`**. System voices (male_0004_a etc.) do not support it.

## Step 1: Scan for Polyphones

When the user provides text, scan it for these common polyphones and flag any that appear:

| Character | Readings | Context clues |
|-----------|----------|---------------|
| 行 | háng (行业/银行/行列) / xíng (行走/行动/可行) | 银行、行长、行业 → háng |
| 干 | gān (干净/干燥) / gàn (干活/干部) | 干部、干活 → gàn |
| 量 | liáng (量体温/测量) / liàng (数量/重量) | 数量、质量 → liàng |
| 铺 | pū (铺床/铺路) / pù (店铺/铺子) | 店铺、铺面 → pù |
| 好 | hǎo (好的/很好) / hào (好奇/爱好) | 爱好、好学 → hào |
| 了 | le (吃了/来了) / liǎo (了解/了结) | 了解、了不起 → liǎo |
| 得 | de (跑得快) / dé (得到) / děi (得去) | 得到 → dé；必须 → děi |
| 地 | de (慢慢地) / dì (土地/地方) | 副词用法 → de |
| 的 | de (我的) / dí (的确) / dì (目的) | 目的、的确 → dì/dí |
| 着 | zhe (看着) / zháo (着火) / zhuó (着装) | 着火、着急 → zháo；着装 → zhuó |
| 长 | cháng (长度/很长) / zhǎng (成长/行长) | 行长、生长 → zhǎng |
| 重 | zhòng (重量/重要) / chóng (重复/重新) | 重复、重新 → chóng |
| 中 | zhōng (中间/中国) / zhòng (中奖/中毒) | 中奖、中毒 → zhòng |
| 还 | hái (还有/还是) / huán (还钱/归还) | 还钱、偿还 → huán |
| 发 | fā (发现/发展) / fà (头发/理发) | 头发、理发 → fà |
| 数 | shù (数字/数量) / shǔ (数数/数一数) | 数数、数落 → shǔ |
| 参 | cān (参加/参考) / shēn (人参/党参) | 人参、党参 → shēn |
| 差 | chā (差别/差距) / chà (差不多) / chāi (出差) | 出差 → chāi；差不多 → chà |

Show the user which polyphones were found and your best guess at the intended reading, then ask them to confirm or correct before synthesizing.

**Example:**
```
检测到多音字：
- "行" (第2个): 银行 → 建议读 háng [hang2] ✓ 还是 xíng [xing2]?
- "行" (第4个): 行长 → 建议读 zhǎng [zhang3] ✓ 还是 cháng [chang2]?
```

## Step 2: Build the Dictionary

Convert confirmed readings into the `dictionary` array. Each entry covers one phrase containing the polyphone:

```
原文片段 → replacement 格式：在多音字前加 [pinyin]，其余字保持原样
```

**Pinyin format:** `[声母韵母声调数字]` — e.g., `[hang2]`、`[xing2]`、`[zhang3]`

**Example:**
- original: `银行行长`
- replacement: `银[hang2]行[zhang3]长`

Build the full dictionary array:
```json
"dictionary": [
  {"original": "银行行长", "replacement": "银[hang2]行[zhang3]长"},
  {"original": "好奇心", "replacement": "[hao4]奇心"}
]
```

Each `original` should be a short phrase (3–8 chars) that uniquely identifies the occurrence in context. Avoid single-character originals — they may match unintended occurrences.

## Step 3: Synthesize

The user must provide a cloned voice ID. If they don't have one, remind them that `dictionary` requires a cloned voice and suggest using the `senseaudio-voice-cloner` skill first.

```bash
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "SenseAudio-TTS-1.5",
    "text": "<TEXT>",
    "stream": false,
    "voice_setting": {
      "voice_id": "<CLONED_VOICE_ID>"
    },
    "audio_setting": {
      "format": "mp3"
    },
    "dictionary": <DICTIONARY_ARRAY>
  }' -o response.json

jq -r '.data.audio' response.json | xxd -r -p > output.mp3
```

Check `base_resp.status_code == 0` before decoding.

## Step 4: Iterate

After the user listens, they may find additional mispronunciations. Update the `dictionary` array and re-synthesize. Keep the previous `response.json` until the new one succeeds.

Report: file path, duration (`jq '.extra_info.audio_length' response.json` ms), character count, and which dictionary entries were applied.
