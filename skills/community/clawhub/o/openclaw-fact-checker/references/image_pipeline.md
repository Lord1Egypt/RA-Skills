# Image Verification Pipeline

This file is loaded when `modality = image`. Execute steps in order.
Skip the text pipeline (Stages 1-4) unless the user also provided a text claim.

---

## Step 1: Visual Analysis (Multimodal LLM)

Examine the image directly using your vision capability. Analyze for:

- **AI generation indicators**: unnatural textures, distorted hands/fingers, asymmetric facial features, blurred or inconsistent backgrounds, text rendering errors, repeating patterns, unrealistic lighting/shadows
- **Manipulation signs**: inconsistent lighting across the image, mismatched edges or blending artifacts, cloned regions, unnatural proportions
- **Content description**: describe what the image shows — who, what, where, when. This description is used in subsequent search steps.
- **Text extraction (OCR)**: if the image contains text (screenshots, headlines, social media posts, documents), extract all visible text. This text may be routed to the text pipeline for verification.

Record your visual assessment and extracted text.

---

## Step 2: Reverse Image Search

Use **WebSearch** to find the original source or prior appearances of this image:

1. Formulate a search query using the key visual elements from Step 1 (e.g., names, locations, events visible in the image). Include terms like "photo" or "image" to target visual results.
2. If the user provided context about the image (e.g., "this photo claims to show X"), include that context in the query.
3. Analyze search results to determine:
   - Has this image appeared before? When was the earliest appearance?
   - Is it being used in its original context, or has it been repurposed (out-of-context)?
   - Does the claimed event/location match the actual source?
4. If results are inconclusive, try ONE reformulated query.

---

## Step 3: Metadata Extraction (Optional)

Check if `exiftool` is available:
```bash
which exiftool 2>/dev/null
```

**If available** AND the image is a local file or has been downloaded:
```bash
exiftool -json "<FILE_PATH>"
```

Analyze the EXIF data for:
- **Camera/device info**: Make, Model — if missing, may be screenshot, download, or AI-generated
- **Software field**: "Adobe Photoshop", "GIMP", "Stable Diffusion", "DALL-E", "Midjourney" indicate editing or AI generation
- **Date/time**: does the creation date match the claimed timeframe?
- **GPS coordinates**: if present, do they match the claimed location?
- **AI generation markers**: some AI tools embed identifiers in metadata

**If not available**, skip silently. Do not ask the user to install it.

---

## Step 4: C2PA Content Credential Verification (Optional)

Check if `c2patool` is available:
```bash
which c2patool 2>/dev/null
```

**If available** AND the image is a local file:
```bash
c2patool "<FILE_PATH>"
```

Analyze the C2PA manifest for:
- **Digital signature**: signed by a known publisher (Reuters, AP, Adobe)?
- **Creation history**: what tools were used to create or edit?
- **AI disclosure**: does the manifest declare AI generation?
- **Tampering evidence**: has the signature been broken?

C2PA data provides **high-confidence** provenance evidence.

**If not available**, skip silently.

---

## Step 5: Synthesize Image Verdict

Combine all signals from Steps 1-4 to assign a verdict:

| Verdict | When to use |
|---------|-------------|
| **AUTHENTIC** | Image appears genuine — consistent metadata, original source found, no manipulation signs |
| **MANIPULATED** | Image has been edited, cropped misleadingly, or digitally altered |
| **AI_GENERATED** | Image was created by AI (Stable Diffusion, DALL-E, Midjourney, etc.) |
| **OUT_OF_CONTEXT** | Image is real but used in a misleading context (wrong date, location, or event) |
| **DEEPFAKE_SUSPECTED** | Facial/body anomalies suggest AI face-swap or synthesis |
| **UNVERIFIED** | Insufficient evidence to determine authenticity |

Assign confidence using the Confidence Framework from the main SKILL.md.

### Source Attribution

**Source Attribution 是必填项。** 每份报告必须包含此部分，它帮助用户区分"谁发布的"和"内容是什么"——这是核查报告中最关键的上下文信息之一。

| Field | Description |
|-------|-------------|
| **Published by** | Who shared/published this image? (verified account, unknown, impersonation) |
| **Content origin** | Real photograph / AI-generated / Edited from original |
| **Propagation** | How did it spread? (original platform → reshares → media coverage) |
| **Analysis method** | Which steps produced evidence (visual analysis, reverse search, EXIF, C2PA) |

This disambiguates cases like "AI-generated image published by the person themselves" vs "AI-generated image falsely attributed to someone."

**If the user also provided a text claim alongside the image**, route that claim through the text pipeline's Stage 4 (Deep Verification) and combine results in the report.

---

## Report Template (English)

```
# Image Verification Report

## Verdict: [VERDICT] (Confidence: [SCORE]%)

**Image Description:** [what the image shows]

### Source Attribution  ← 必填，不可省略
- **Published by:** [who published — verified/unknown/impersonation]
- **Content origin:** [real photograph / AI-generated / edited]
- **Propagation:** [how it spread]
- **Analysis method:** [visual analysis / reverse search / EXIF / C2PA]

### Visual Analysis
[LLM visual analysis findings] — Source: [Source Name](url) (if based on search reports)

### Reverse Image Search
[Original source findings] — Source: [Source Name](url)

### Metadata Analysis
[EXIF findings, or "No metadata tool available — skipped"]

### C2PA Content Credentials
[C2PA findings, or "No C2PA tool available — skipped"]

**All Sources:**
- [url1]
- [url2]
```

## Report Template (中文)

**当用户使用中文时，必须使用此模板。标题、标签、verdict 全部使用中文，不得混用英文。**

```
# 图片验证报告

## 判定：[判定结果]（置信度：[分数]%）

**图片描述：** [图片内容描述]

### 来源归属  ← 必填，不可省略
- **发布者：** [谁发布的——已验证/未知/冒充]
- **内容来源：** [真实拍摄 / AI 生成 / 编辑加工]
- **传播路径：** [传播方式]
- **分析方法：** [视觉分析 / 反向搜索 / EXIF / C2PA]

### 视觉分析
[分析结果] — 来源：[来源名称](url)（如果是基于搜索报道的）

### 反向图片搜索
[搜索结果] — 来源：[来源名称](url)

### 元数据分析
[EXIF 分析结果，或"元数据工具不可用——已跳过"]

### C2PA 内容凭证
[C2PA 分析结果，或"C2PA 工具不可用——已跳过"]

**所有来源汇总：**
- [url1]
```
