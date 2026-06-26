---
name: senseaudio-jingle-forge
description: Create a brand jingle (5–15 seconds) from a brand name and tone keywords. Use when users want a brand sound logo, audio identity, jingle, intro music, or short branded audio clip. Triggers on "品牌 jingle", "开机音效", "广告片尾音乐", "品牌声音", "音频 logo", "短视频片头音乐", or any request to create a short branded musical piece.
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

# SenseAudio Jingle Forge

Turn brand information into a ready-to-use audio logo. A jingle is not a song — it's short (5–15s), memorable, and built around the brand name. This skill constrains the music generation API to that specific format.

## Step 1: Collect Brand Info

Ask the user for:

| Field | Example |
|-------|---------|
| 品牌名 | "极光科技" |
| 行业/产品 | "智能家居" |
| 调性关键词 | "科技感、温暖、未来" |
| 使用场景 | 开机音效 / 广告片尾 / 短视频片头 / APP 启动 |
| 人声偏好 | 有人声（男/女）/ 纯音乐 |

If the user provides partial info, infer reasonable defaults and proceed.

## Step 2: Generate Jingle Lyrics

Jingle lyrics have strict rules — explain this to the user if they ask why the lyrics look short:
- Total length: **≤ 20 characters**
- Must contain the brand name
- Last line ends with the brand name
- Should rhyme or have a strong rhythm
- No verse/chorus structure — just 1–2 punchy lines

Build the lyrics prompt with these constraints baked in:

```
为品牌"<品牌名>"创作一段 Jingle 歌词。
要求：
- 总字数不超过20字
- 必须包含品牌名"<品牌名>"
- 最后一句以品牌名结尾
- 押韵，朗朗上口
- 调性：<调性关键词>
- 场景：<使用场景>
```

```bash
LYRICS_RESP=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/lyrics/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"<PROMPT>\", \"provider\": \"sensesong\"}")

TASK_ID=$(echo $LYRICS_RESP | jq -r '.task_id // empty')
```

If async (`task_id` present), poll:
```bash
while true; do
  POLL=$(curl -s "https://api.senseaudio.cn/v1/song/lyrics/pending/$TASK_ID" \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
  STATUS=$(echo $POLL | jq -r '.status')
  { [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ]; } && break
  sleep 3
done
LYRICS=$(echo $POLL | jq -r '.response.data[0].text')
```

If sync, read directly: `LYRICS=$(echo $LYRICS_RESP | jq -r '.data[0].text')`

**Show the lyrics to the user and ask for approval or edits before composing.**

## Step 3: Match Style to Brand Tone

Map tone keywords to music style automatically:

| Tone keyword | Style suggestion |
|--------------|-----------------|
| 科技 / 未来 / 数字 | electronic, synthesizer, futuristic |
| 温暖 / 家庭 / 亲切 | acoustic guitar, piano, warm |
| 高端 / 奢华 / 精致 | strings, jazz, orchestral |
| 活力 / 年轻 / 运动 | pop, upbeat, energetic |
| 自然 / 健康 / 清新 | acoustic, folk, light |
| 专业 / 商务 / 信任 | corporate, clean, minimal |
| 可爱 / 儿童 / 萌 | playful, xylophone, cheerful |

Combine multiple keywords: "科技感、温暖" → `"electronic piano, warm synth, modern"`

Also add `"short jingle, 5-15 seconds, brand audio logo"` to the style to constrain length.

## Step 4: Generate Two Versions in Parallel

Always produce two versions — users almost always need both:

**Version A — 带唱版 (with vocals):**
```bash
SONG_A=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/music/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"sensesong\",
    \"lyrics\": \"<LYRICS>\",
    \"title\": \"<品牌名> Jingle\",
    \"vocal_gender\": \"<f|m>\",
    \"style\": \"<STYLE>, short jingle, 5-15 seconds, brand audio logo\",
    \"negative_tags\": \"long intro, extended outro, complex arrangement\"
  }")
TASK_A=$(echo $SONG_A | jq -r '.task_id')
```

**Version B — 纯音乐版 (instrumental):**
```bash
SONG_B=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/music/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"sensesong\",
    \"instrumental\": true,
    \"title\": \"<品牌名> Jingle Instrumental\",
    \"style\": \"<STYLE>, short jingle, 5-15 seconds, brand audio logo\",
    \"negative_tags\": \"vocals, long intro, extended outro\"
  }")
TASK_B=$(echo $SONG_B | jq -r '.task_id')
```

Poll both tasks (check every 5s, may take 30–120s):
```bash
for TASK in $TASK_A $TASK_B; do
  while true; do
    POLL=$(curl -s "https://api.senseaudio.cn/v1/song/music/pending/$TASK" \
      -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
    STATUS=$(echo $POLL | jq -r '.status')
    { [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ]; } && break
    sleep 5
  done
done
```

## Step 5: TTS Brand Name Read

Generate a clean spoken version of the brand name — useful for overlaying on the instrumental:

```bash
curl -s -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"SenseAudio-TTS-1.0\",
    \"text\": \"<品牌名>\",
    \"stream\": false,
    \"voice_setting\": {
      \"voice_id\": \"<VOICE_ID_MATCHING_TONE>\",
      \"speed\": 0.9
    },
    \"audio_setting\": { \"format\": \"mp3\" }
  }" -o brand_name.json

jq -r '.data.audio' brand_name.json | xxd -r -p > brand_name.mp3
```

Pick voice based on tone: 高端/专业 → `male_0004_a`; 温暖/亲切 → `female_0006_a`; 活力/年轻 → `male_0026_b`

## Output

Present all three deliverables:

```
品牌 Jingle 生成完成：

带唱版：  <audio_url_A>  （时长：<duration>秒）
纯音乐版：<audio_url_B>  （时长：<duration>秒）
品牌名朗读：brand_name.mp3（可叠加到纯音乐版）

使用建议：
- 开机音效 / APP 启动：纯音乐版
- 广告片尾：带唱版 或 纯音乐版 + 品牌名朗读叠加
- 短视频片头：带唱版
```
