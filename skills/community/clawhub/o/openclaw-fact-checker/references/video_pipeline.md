# Video Verification Pipeline

This file is loaded when `modality = video`. Execute steps in order.

**Architecture: Search-first, ffmpeg as enhancement.**
Most video verification can be accomplished through web search and context analysis alone. ffmpeg enables deeper technical analysis (keyframe extraction, audio transcription) but is NOT required for the primary verification path.

---

## Step 1: Context Search & Source Verification (Primary Path — always runs)

This is the **main verification step** — it runs regardless of whether ffmpeg is available.

1. **Gather context**: Collect all available information about the video:
   - User-provided description or claims about the video
   - Video URL or source platform (YouTube, TikTok, Twitter, Telegram, etc.)
   - Any visible text, titles, or watermarks described by the user
   - If the user's LLM supports direct video input, ask it to describe the video content

2. **Search for the video's origin**: Use **WebSearch** with queries targeting:
   - The video's claimed content (key people, events, locations)
   - The platform/account that published it
   - Known fact-checks about this video (add "fact check" or "debunk" to query)
   - Search in both the user's language AND English for maximum coverage

3. **Analyze search results** to determine:
   - Has this video been fact-checked before by established organizations?
   - Is it attributed to the correct source, or falsely attributed?
   - Is it from the claimed time period, or old footage reused?
   - Has it been identified as AI-generated or deepfake by credible sources?

4. **Determine the video's propagation path** (if identifiable):
   - Original source → which platforms → how widely shared
   - Was it removed by platforms? (removal suggests policy violation)
   - Are credible news outlets reporting on it?

Record all findings from this step.

---

## Step 2: ffmpeg Technical Analysis (Enhancement Path — when available)

Check if `ffmpeg` is available:
```bash
which ffmpeg 2>/dev/null
```

**If ffmpeg is NOT available**, recommend installation:
> ⚠️ **For deeper video analysis, install ffmpeg** (one command, ~30 seconds):
> - **Ubuntu/Debian**: `sudo apt install ffmpeg`
> - **macOS**: `brew install ffmpeg`
> - **Windows**: `winget install ffmpeg`

Then skip to Step 3. The search-based analysis from Step 1 is sufficient for a verdict.

**If ffmpeg IS available**, perform technical analysis:

### 2a. Keyframe Extraction
```bash
mkdir -p /tmp/factcheck_frames && ffmpeg -i "<FILE_PATH>" -vf "select=eq(pict_type\,I),scale=1280:-1" -vsync vfr -frame_pts 1 /tmp/factcheck_frames/frame_%04d.jpg -y 2>/dev/null
```

If too many frames (>20), take uniform sample:
```bash
ffmpeg -i "<FILE_PATH>" -vf "fps=1/10,scale=1280:-1" /tmp/factcheck_frames/frame_%04d.jpg -y 2>/dev/null
```

Extract video metadata:
```bash
ffprobe -v quiet -print_format json -show_format -show_streams "<FILE_PATH>" 2>/dev/null
```

### 2b. Keyframe Visual Analysis

For up to 8 representative keyframes, analyze using multimodal LLM:
- **Cross-frame consistency**: faces, lighting, backgrounds consistent across frames?
- **Temporal anomalies**: sudden jumps in visual quality, lighting, or scene composition?
- **Deepfake indicators**: facial distortions, unnatural blinking, mouth-audio mismatch
- **Out-of-context reuse**: footage from a different time/place than claimed?

Run reverse image search on 1-3 most representative frames to find original source.

### 2c. Audio Extraction & Transcription

Extract audio:
```bash
ffmpeg -i "<FILE_PATH>" -vn -acodec pcm_s16le -ar 16000 /tmp/factcheck_audio.wav -y 2>/dev/null
```

Attempt transcription (check in order):

1. **Whisper CLI** (if installed):
   ```bash
   which whisper 2>/dev/null && whisper /tmp/factcheck_audio.wav --model base --output_format txt --output_dir /tmp/ 2>/dev/null
   ```

2. **OpenAI Whisper API** (if API key available):
   ```bash
   echo "${OPENAI_API_KEY:-}"
   ```
   If set:
   ```bash
   curl -s https://api.openai.com/v1/audio/transcriptions \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -F file="@/tmp/factcheck_audio.wav" \
     -F model="whisper-1"
   ```

3. If neither available, skip transcription. Note in report.

### 2d. Transcript Fact-Check

If transcription succeeded:
1. Extract verifiable claims from transcript (same rules as text pipeline Stage 2).
2. Route claims through text pipeline's Stage 3 (Triage) and Stage 4 (Deep Verification).
3. Record results separately.

### 2e. Cleanup
```bash
rm -rf /tmp/factcheck_frames /tmp/factcheck_audio.wav /tmp/factcheck_audio.txt 2>/dev/null
```

---

## Step 3: Synthesize Video Verdict

Combine all available evidence (from Step 1, and Step 2 if ffmpeg was available).

### ⚠️ Verdict 标签必须严格使用以下预定义选项，不得自创标签（如 DEEPFAKE 不是有效标签）。

**AI_GENERATED vs DEEPFAKE_SUSPECTED 的区分：**
- **AI_GENERATED**：整个视频由 AI 工具从零生成（如 Sora、Runway 等），不基于任何真实人物的原始视频。例如：Trump 发布的 AI 生成的奥巴马被捕视频。
- **DEEPFAKE_SUSPECTED**：基于真实人物的视频，通过换脸/换声技术伪造其言行。例如：泽连斯基投降视频（用泽连斯基的脸合成了虚假的投降声明）。

### Visual verdict

| Verdict | When to use |
|---------|-------------|
| **AUTHENTIC** | Video appears genuine, source verified, no manipulation signs |
| **MANIPULATED** | Visual evidence of editing, splicing, or digital alteration |
| **AI_GENERATED** | Entire video generated from scratch by AI tools (Sora, Runway, etc.) — not based on real footage of a specific person |
| **DEEPFAKE_SUSPECTED** | Real person's face/voice swapped or synthesized onto another body/audio to fabricate their actions or speech |
| **OUT_OF_CONTEXT** | Real footage used in misleading context (wrong date, location, or event) |
| **UNVERIFIED** | Insufficient evidence to determine visual authenticity |

### Transcript verdict
For each claim extracted from audio: use standard text claim verdicts (TRUE / FALSE / PARTIALLY_TRUE / MISLEADING / UNVERIFIED).

### Source Attribution

**Source Attribution 是必填项。** 每份报告必须包含此部分，它帮助用户区分"谁发布的"和"内容是什么"——这是核查报告中最关键的上下文信息之一。

| Field | Description |
|-------|-------------|
| **Published by** | Who published this video? (verified account, unknown, impersonation) |
| **Content origin** | Real footage / AI-generated / Deepfake / Edited |
| **Propagation** | How did it spread? (original platform → reshares → media coverage) |
| **Analysis method** | Search-based only / Search + ffmpeg keyframe analysis / Search + audio transcription |

This disambiguates cases like "AI video posted by the subject themselves" (e.g., Trump posting his own AI video) vs "AI video falsely attributed to someone" (e.g., fake Zelensky surrender).

### Confidence assignment
- Use the Confidence Framework from the main SKILL.md
- **Search-only verdicts** (no ffmpeg): cap at 85% unless 3+ authoritative sources agree
- **Search + ffmpeg analysis**: full 0-100 range

---

## Report Template (English)

```
# Video Verification Report

## Visual Verdict: [VERDICT] (Confidence: [SCORE]%)

**Video Info:** [duration/source/format if known]

### Source Attribution  ← 必填，不可省略
- **Published by:** [who published — verified/unknown/impersonation]
- **Content origin:** [real footage / AI-generated / deepfake / edited]
- **Propagation:** [how it spread]
- **Analysis method:** [search-based / search + keyframe analysis / search + transcription]

### Context & Source Verification
[Search findings — origin, fact-checks, media coverage] — Source: [Source Name](url)

### Visual Analysis
[Keyframe analysis findings if ffmpeg was used, or "Direct keyframe analysis not performed (ffmpeg not available)"] — Source: [Source Name](url) (if based on search reports)

### Metadata / C2PA
[File metadata findings if available]

---

## Transcript Fact-Check
[If audio was transcribed, include claim verdicts. If not: "Audio transcription not available."]

### claim_001: [VERDICT] (Confidence: [SCORE]%)
> [claim from transcript]

**Evidence:**
1. [evidence point 1] — [Source Name](url1)
2. [evidence point 2] — [Source Name](url2)

**All Sources:**
- [url1]
- [url2]
```

## Report Template (中文)

**当用户使用中文时，必须使用此模板。标题、标签、verdict 全部使用中文，不得混用英文。**

```
# 视频验证报告

## 视觉判定：[判定结果]（置信度：[分数]%）

**视频信息：** [时长/来源/格式]

### 来源归属  ← 必填，不可省略
- **发布者：** [谁发布的——已验证/未知/冒充]
- **内容来源：** [真实拍摄 / AI 生成 / 深度伪造 / 编辑加工]
- **传播路径：** [传播方式]
- **分析方法：** [基于搜索 / 搜索+关键帧分析 / 搜索+音频转录]

### 上下文与来源验证
[搜索发现——来源、已有核查、媒体报道] — 来源：[来源名称](url)

### 视觉分析
[关键帧分析结果（如有 ffmpeg），或"未执行关键帧分析（ffmpeg 不可用）"] — 来源：[来源名称](url)（如果是基于搜索报道的）

### 元数据 / C2PA
[文件元数据分析结果（如有）]

---

## 音频内容核查
[音频转录核查结果。如无转录："音频转录不可用。"]

### 声明一：[判定结果]（置信度：[分数]%）
> [转录文本中的声明]

**证据：**
1. [论据 1] — [来源名称](url1)
2. [论据 2] — [来源名称](url2)

**所有来源汇总：**
- [url1]
- [url2]
```
