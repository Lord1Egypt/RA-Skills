# Deep Summary Guidelines

When writing the "深度总结" section, follow these rules:

## 1. Classify the content type

First, silently determine which category the content falls into:

| Type | Signals |
|------|---------|
| **观点/分析** | Opinion piece, commentary, hot take, editorial |
| **教程/攻略** | How-to, step-by-step, tips, guide |
| **新闻/事件** | Breaking news, event report, announcement |
| **个人故事** | Personal experience, diary, travel log |
| **产品/测评** | Product review, comparison, unboxing |
| **清单/推荐** | List post, recommendations, resources |

## 2. Write a structured summary

Use **structured fields + bullet points / tables**, NOT narrative paragraphs.
All text in **Chinese**. Use third-person perspective, NOT AI perspective
("我为您总结了…"). Every summary must contain the following header fields:

```markdown
**内容类型：** （类型标签，如 教程/攻略、观点/分析 等）
**核心主题：** （一句话概括，≤30 字）
```

Then, based on content type, add the structured body below the header fields.
Choose the most appropriate format for the content:

### Format A: Table — for lists, comparisons, tech stacks, recommendations

Use when the original content enumerates items with clear attributes.

```markdown
**选型/清单：**

| 分类 | 工具/选项 | 关键理由 |
|------|-----------|----------|
| … | … | … |
```

### Format B: Steps — for tutorials, guides, workflows

Use when the original content describes a sequential process.

```markdown
**流程/步骤：**

1. **步骤名** — 简要说明
2. **步骤名** — 简要说明
3. …
```

### Format C: Bullet points — for opinions, stories, news, reviews

Use for content that doesn't fit a table or steps format.

```markdown
**要点：**

- **论点/事件/观点** — 展开说明（一句话）
- **论点/事件/观点** — 展开说明（一句话）
- …
```

## 3. Add key takeaways

After the structured body, always add 2-3 bullet points:

```markdown
**关键要点：**
- （要点一）
- （要点二）
- （要点三）
```

## 4. Incorporate image analysis

If Step 2.6 produced image analysis results, treat them as **supplementary input
alongside the original text** when generating the summary:

- For image-heavy posts (many images with short text), the image content provides
  essential context — the summary should incorporate visual information such as
  text extracted from screenshots, data from charts, or scene descriptions.
- For posts with both substantial text and rich images, synthesize both sources.
  Mention insights from images where they add value beyond the text.
- Add a header field when image analysis is available:
  ```markdown
  **内容来源：** 文字 + 图片分析
  ```

## 5. Incorporate video transcript

If Step 2.7 produced a `fullText`, treat it as **primary input alongside the
original text** when generating the summary:

- For video-heavy posts (short text + long transcript), the transcript is the
  main content source — the summary should primarily reflect what was said in
  the video.
- For posts with both substantial text and transcript, synthesize both sources.
  Note where information comes from if they differ.
- Add a header field when transcript is available:
  ```markdown
  **内容来源：** 文字 + 视频转写
  ```
- If **both** image analysis and video transcript are available:
  ```markdown
  **内容来源：** 文字 + 图片分析 + 视频转写
  ```

## 6. Style rules

- NO narrative paragraphs — use fields, bullets, and tables only.
- Be specific — include names, numbers, and concrete details from the original.
- Keep each bullet to 1-2 sentences max.
- Do NOT pad with filler phrases like "总的来说" or "值得一提的是".
- Do NOT repeat the title verbatim in the summary.
- If the original content mixes formats (e.g., steps + a list of tools),
  combine Format A and B as needed.
