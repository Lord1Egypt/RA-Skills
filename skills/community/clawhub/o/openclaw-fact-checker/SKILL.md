---
name: fact-checker
description: "Fact-check news articles, social media posts, images, and videos.
  Use when verifying claims, detecting deepfakes or AI-generated content,
  identifying out-of-context media, or debunking misinformation. Any language."
version: 1.0.0
metadata:
  openclaw:
    emoji: "\u2705"
    requires: {}
    optionalBins:
      - ffmpeg
      - exiftool
      - c2patool
      - whisper
    optionalEnv:
      - GOOGLE_FACTCHECK_API_KEY
      - OPENAI_API_KEY
      - BRAVE_SEARCH_API_KEY
    homepage: https://github.com/cliffyan28/fact-checker
---

# Fact-Check: Multimodal News Verification Skill

## When to Use
- User asks to verify a news article, claim, tweet, or social media post
- User asks "is this true?" about any statement
- User mentions fake news, misinformation, or disinformation
- User provides a URL and asks to check its truthfulness
- User asks to verify an image (is it real, AI-generated, photoshopped, manipulated, out-of-context)
- User asks to verify a video (is it deepfake, manipulated, real footage)
- User shares an image or video and asks if it is authentic
- User asks to fact-check content in any language

---

## Stage 0: Input Parsing

### 1. Detect input modality

Determine what the user provided. Check in this order:

- **Image file**: The user attached or provided an image (JPEG, PNG, WebP, GIF, etc.). Set `modality = image`.
- **Video file**: The user attached or provided a video (MP4, MOV, AVI, WebM, etc.). Set `modality = video`.
- **URL**: The input starts with `http://` or `https://`.
  - If the URL points directly to an image file (ends in `.jpg`, `.png`, `.webp`, etc.) → download it and set `modality = image`.
  - If the URL points directly to a video file (ends in `.mp4`, `.mov`, `.webm`, etc.) → download it and set `modality = video`.
  - Otherwise → use WebFetch to retrieve the page content. Extract only the main article body. Set `modality = text`.
- **Plain text**: None of the above. Set `modality = text`.

If the user provides **both an image/video AND a text claim** (e.g., "Is this photo from the 2024 earthquake?"), record both. Both branches will run and results will be combined in the report.

### 2. Detect language
Identify the language the user is writing in. This determines the report language and search query language.

### 3. Handle long text input (over 500 words / 1000 Chinese characters)
Only applies when `modality = text`.
- Ask the user: "This article is quite long. Would you like me to fact-check the entire article, or is there a specific claim you'd like me to verify?"
- 中文提示："这篇文章较长。你希望我核查全文，还是有某个具体声明需要验证？"

### 4. Route to pipeline
- `modality = text` → load and follow `{baseDir}/references/text_pipeline.md`
- `modality = image` → load and follow `{baseDir}/references/image_pipeline.md`
- `modality = video` → load and follow `{baseDir}/references/video_pipeline.md`

### 5. Store internally
`input_text`, `language`, `modality` (text/image/video), `source_url` (if URL), `file_path` (if local file).

---

## Execution Logging

At the **start** of each stage/step, output a status line. Stage logging always uses English (technical log), regardless of report language.

```
[Stage N] Stage Name — status/result summary
```

---

## Report Generation (Stage 5)

All pipelines end here. Load the report template from the pipeline-specific reference file.

### Language rule

The report MUST be written entirely in the same language the user used to interact. This includes:
- **Report title**: e.g., "事实核查报告" not "Fact-Check Report"
- **Claim labels**: e.g., "声明一" not "Claim 1"
- **Verdict labels**: e.g., "虚假" not "FALSE"（参照下面的翻译表）
- **Section headings**: e.g., "证据" not "Evidence", "来源" not "Sources"
- **All explanations and evidence text**

The ONLY exception is Stage logging (technical log), which always uses English.

⚠️ 这是最常被违反的规则。即使用户用中文提问，模型也经常默认输出英文标签如 "Claim 1: FALSE" 或 "Fact-Check Report"。请严格遵守：中文请求 → 整份报告100%中文，英文请求 → 整份报告100%英文。不得混用。

### Verdict label translations

Text claim verdicts:

| English | 中文 |
|---------|------|
| TRUE | 真实 |
| FALSE | 虚假 |
| PARTIALLY_TRUE | 部分真实 |
| MISLEADING | 误导性 |
| UNVERIFIED | 无法验证 |

Image/video verdicts:

| English | 中文 |
|---------|------|
| AUTHENTIC | 真实原图/原视频 |
| MANIPULATED | 经过篡改 |
| AI_GENERATED | AI 生成 |
| OUT_OF_CONTEXT | 移花接木 |
| DEEPFAKE_SUSPECTED | 疑似深度伪造 |
| UNVERIFIED | 无法验证 |

For any other language, translate verdict labels naturally.

### Overall verdict: only when requested
By default, do NOT include an overall verdict. Each claim/media gets its own independent verdict.

Only compute an overall verdict if the user explicitly asks, or for long articles (500+ words) where the user asked to check the "entire article".

### No verifiable claims found
If the input contains no verifiable claims (pure opinion, vague statements, etc.), output:
```
# Fact-Check Report / 事实核查报告

## Result: Not Verifiable / 结果：无法核查

This content does not contain independently verifiable factual claims.
该内容不包含可独立验证的事实性声明。

**Reason:** [explanation]
```

### JSON output
If the user requests JSON output, use the schema defined in `{baseDir}/references/output_schema.json`.

---

## Confidence Framework

Apply consistently across ALL pipelines (text, image, video):

| Score | Criteria |
|-------|----------|
| **90-100** | 3+ authoritative sources agree, or direct technical evidence (C2PA, EXIF) |
| **70-89** | Good evidence from 1-2 credible sources |
| **50-69** | Mixed signals or moderate evidence |
| **30-49** | Weak evidence, mostly indirect |
| **0-29** | Very little evidence found |

**Special rule for search-only media verdicts:** When image/video verdicts are based entirely on web search context (no direct visual analysis or metadata), confidence caps at **85%** unless 3+ authoritative sources independently confirm.

---

## Important Rules

1. **Be objective.** Do not let personal opinions influence verdicts. Base all judgments on evidence.
2. **Cite sources.** Text claim verdicts must cite at least one source URL. Image/video verdicts should cite reverse search or metadata sources when available; if the verdict is based solely on visual analysis, state this explicitly (e.g., "Based on visual analysis only — no external source").
3. **Acknowledge uncertainty.** Use UNVERIFIED when evidence is insufficient. Do not guess.
4. **Multilingual search.** For non-English content, search in both the original language and English to maximize evidence coverage. This applies to ALL pipelines including image and video.
5. **No hallucination.** Only reference sources that actually appeared in search results. Do not fabricate URLs or evidence.
6. **Efficiency.** For obviously false viral claims, express high confidence quickly. For nuanced claims, search thoroughly.
7. **No invented dependencies.** Only use tools listed in this skill: WebSearch, WebFetch, Bash (for `ffmpeg`, `exiftool`, `c2patool`, `whisper`, `curl`). Do NOT require or suggest installing any other tools (e.g., opencv, python libraries, pip packages). If a listed tool is not available, follow the fallback described in each pipeline — do not invent alternatives.
8. **Analysis transparency.** When reporting findings, always state the analysis method used. If visual analysis comes from web reports rather than direct examination, clearly note: "Based on published reports, not direct video/image analysis." Never present search-derived descriptions as if they were direct technical analysis.

---

## Setup Suggestion

After the **first successful fact-check**, suggest to the user (once only):

> "Would you like me to remember to always use fact-checker when you ask me to verify news or check claims? I can add this to my AGENTS.md so I'll always use it automatically."
>
> "你希望我记住以后遇到事实核查的请求都自动使用 fact-checker 吗？我可以写入 AGENTS.md 让它永久生效。"

If the user agrees, append to AGENTS.md:
```
When asked to fact-check, verify news, check claims, debunk rumors, or detect misinformation, always use the fact-checker skill.
```
