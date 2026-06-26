---
name: senseaudio-lyric-flip
description: Rewrite a song with a new theme while preserving the original's rhyme scheme, line structure, and rhythmic skeleton. Use when users want to parody a song, write new lyrics to a familiar tune, or create structured lyrics with controlled rhyme patterns. Triggers on "旧瓶装新酒", "改编歌词", "用《xxx》的结构写", "仿写", "填词", "把这首歌改成关于xxx的", or any request to rewrite lyrics with a new theme.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Lyric Flip

Rewrite a song with a new theme while keeping the original's structure. The key insight: AI-generated lyrics drift without constraints. By extracting a structural skeleton first and using it as a hard constraint, the output stays tight and singable.

## Step 1: Collect Inputs

Ask the user for:
1. **参考歌词** — paste the original lyrics (or a verse/chorus excerpt)
2. **新主题** — what the new song should be about (e.g., "程序员加班", "失恋的猫", "创业失败")
3. **风格保留还是改变？** — keep the original vibe, or shift it (e.g., "结构照搬但从抒情改成摇滚")

## Step 2: Extract the Skeleton (LLM task)

Analyze the reference lyrics yourself — no API call needed for this step. Extract:

**Structure map:**
- Segment labels: verse / chorus / bridge / pre-chorus / outro
- Number of lines per segment
- Character count range per line (e.g., 7–9 chars)

**Rhyme scheme:**
- Label each line's end sound: A, B, C...
- Example: AABB means lines 1&2 rhyme, lines 3&4 rhyme
- Note which segments rhyme internally vs. across segments

**Rhythm feel:**
- Syllable density: sparse (≤6 chars/line) / medium (7–10) / dense (11+)
- Repetition patterns: does the chorus repeat a phrase? Does a hook line recur?
- Emotional arc: builds up / stays level / drops at bridge

**Example skeleton output to show the user:**
```
段落结构：
  [verse] × 2 (各4行，7-9字/行，ABAB韵)
  [chorus] × 2 (各4行，6-8字/行，AABB韵，第4行重复)
  [bridge] × 1 (2行，自由韵)

情绪走向：verse 平静叙述 → chorus 情绪爆发 → bridge 转折收尾

韵脚示例（verse）：
  行1: __韵A
  行2: __韵B
  行3: __韵A
  行4: __韵B
```

Show this to the user and confirm before proceeding.

## Step 3: Generate New Lyrics via API

Build a tightly constrained prompt using the extracted skeleton:

```
请根据以下结构约束，为主题"<新主题>"创作歌词：

段落结构：<从骨架提取的结构>
每行字数：<范围>
韵脚模式：<AABB/ABAB等>
情绪走向：<从骨架提取>
风格：<保留原风格 或 用户指定的新风格>

硬性要求：
- 严格遵守每段行数
- 每行字数在指定范围内
- 韵脚必须对齐（同一韵组的行必须押韵）
- 不要超出段落结构，不要添加额外段落
```

```bash
LYRICS_RESP=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/lyrics/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"<PROMPT>\", \"provider\": \"sensesong\"}")

TASK_ID=$(echo $LYRICS_RESP | jq -r '.task_id // empty')
```

Poll if async:
```bash
while true; do
  POLL=$(curl -s "https://api.senseaudio.cn/v1/song/lyrics/pending/$TASK_ID" \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
  STATUS=$(echo $POLL | jq -r '.status')
  [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ] && break
  sleep 3
done
LYRICS=$(echo $POLL | jq -r '.response.data[0].text')
```

## Step 4: Rhyme Check

After getting the lyrics, verify rhyme alignment yourself before showing the user. For each rhyme group in the skeleton:

- Extract the last 1–2 characters of each line in the group
- Check if they share a vowel sound (approximate check is fine)
- Flag lines that clearly don't rhyme with their group

**Show the user a marked-up version:**
```
[verse]
行1: 深夜还在敲代码 ✓ (韵A: -ā)
行2: 需求改了又改了 ✓ (韵B: -le)
行3: 眼睛快要睁不开 ✓ (韵A: -āi ≈ ā)
行4: 产品说明天上线了 ⚠ (韵B: -le ✓ 但字数偏长)
```

If rhyme issues are minor, note them and ask if the user wants to regenerate those lines. If structure is badly off, regenerate the full lyrics with a stricter prompt.

## Step 5: Compose the Song

Once lyrics are approved, infer the style from the reference song and user preferences:

| Reference vibe | Suggested style |
|----------------|----------------|
| 流行抒情 | pop ballad, piano, emotional |
| 摇滚 | rock, electric guitar, energetic |
| 民谣 | folk, acoustic guitar, storytelling |
| 电子舞曲 | electronic, synth, upbeat |
| 古风 | traditional Chinese, guqin, cinematic |

If the user wants to shift the style, use their specified direction instead.

```bash
SONG_RESP=$(curl -s -X POST "https://api.senseaudio.cn/v1/song/music/create" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"sensesong\",
    \"lyrics\": \"<APPROVED_LYRICS>\",
    \"title\": \"<新主题 + 仿 原曲名>\",
    \"vocal_gender\": \"<f|m>\",
    \"style\": \"<INFERRED_STYLE>\"
  }")

SONG_TASK=$(echo $SONG_RESP | jq -r '.task_id')
```

Poll until done (30–120s):
```bash
while true; do
  POLL=$(curl -s "https://api.senseaudio.cn/v1/song/music/pending/$SONG_TASK" \
    -H "Authorization: Bearer $SENSEAUDIO_API_KEY")
  STATUS=$(echo $POLL | jq -r '.status')
  [ "$STATUS" = "SUCCESS" ] || [ "$STATUS" = "FAILED" ] && break
  echo "作曲中..."
  sleep 5
done
```

## Output

```
改编完成：

原曲结构：<骨架摘要>
新主题：<用户输入>
风格：<使用的曲风>

歌词预览：
<最终歌词>

音频：<audio_url>
封面：<cover_url>
时长：<duration> 秒
```

If the user wants to iterate — adjust rhymes, change a line, shift the style — update the lyrics and re-submit to the music API. The skeleton stays fixed; only the words change.
