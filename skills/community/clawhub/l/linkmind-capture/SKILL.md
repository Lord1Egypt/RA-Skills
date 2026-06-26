---
name: linkmind-capture
description: >
  Capture social media links (Weibo, Xiaohongshu, WeChat, Xiaoyuzhou) — extract text, images,
  and metadata, then generate a Markdown note with AI deep summary,
  saved to the user's Obsidian vault.
triggers:
  - "让我记录"
  - "帮我保存"
  - "帮我记录"
  - "记录这个链接"
  - "capture this"
  - "save this link"
allowed-tools: Shell, Read, Write, Glob, Grep
metadata:
  openclaw:
    requires:
      bins:
        - node
      config:
        - obsidian_vault
    homepage: "https://github.com/tt-bltn/LinkMind"
---

# LinkMind — Social Media Content Capture

When the user provides a social media link and asks you to capture/record/save it,
follow the workflow below.

## Step 0: Read configuration

Read the config file at `skills/linkmind/config.json` to get the user's Obsidian
vault path. If the file does not exist, tell the user:

```
请先运行配置向导：cd skills/linkmind/scripts && npm run setup
```

This runs an interactive wizard that guides the user through setting their
Obsidian vault path, platform cookies, and ASR credentials.

The config file structure:

```json
{
  "obsidian_vault": "/absolute/path/to/vault"
}
```

Sensitive credentials (cookies, ASR keys) are configured in
`skills/linkmind/.env`. See the Cookie and ASR configuration sections below.
Cookies and ASR are **optional** — basic content capture works without them.

- If `obsidian_vault` is empty, ask the user to configure it.
- Verify the vault directory exists. If not, inform the user that the path is invalid.
- The output directory is `{obsidian_vault}/LinkMind/`. Create it if it does not exist.

## Step 1: Identify the platform

Match the URL against these patterns:

| Platform        | URL patterns                                                  |
|-----------------|---------------------------------------------------------------|
| **Weibo**       | `weibo.com`, `m.weibo.cn`                                    |
| **Xiaohongshu** | `xiaohongshu.com`, `xhslink.com`                             |
| **WeChat**      | `mp.weixin.qq.com`                                           |
| **小宇宙**       | `xyzfm.link`, `xiaoyuzhoufm.com`                            |

**小宇宙分享文本解析：** 用户分享的内容可能是纯文本（如 `分享播客《...》, 标记时点【17:03】https://xyzfm.link/s/xxx`），从中提取 URL 即可，时间点由脚本自动从重定向 URL 的 `#ts=` 片段解析。

If the URL does not match any supported platform, tell the user:
"目前 LinkMind 支持微博、小红书、微信公众号和小宇宙播客链接，该链接暂不支持。"

## Step 2: Run the handler script

The scripts live at `skills/linkmind/scripts/`.
Run the corresponding script from the project root:

**Weibo:**
```bash
npx tsx skills/linkmind/scripts/weibo.ts "<URL>" --config skills/linkmind/config.json
```

**Xiaohongshu:**
```bash
npx tsx skills/linkmind/scripts/xiaohongshu.ts "<URL>" --config skills/linkmind/config.json
```

**WeChat:**
```bash
npx tsx skills/linkmind/scripts/wechat.ts "<URL>" --config skills/linkmind/config.json
```

**小宇宙 (Xiaoyuzhou):**
```bash
npx tsx skills/linkmind/scripts/xiaoyuzhou.ts "<URL>" --config skills/linkmind/config.json
```

> `<URL>` 是短链接（如 `https://xyzfm.link/s/xxx`）或完整剧集链接。脚本自动解析重定向、提取时间戳、获取剧集元数据和字幕链接。

The script outputs JSON to stdout. If the JSON contains an `"error"` field,
the extraction failed — check the `"code"` field for the error category
(`NETWORK`, `AUTH`, `RATE_LIMIT`, `NOT_FOUND`, `PARSE`, `UNKNOWN`) and the
`"details"` field for a user-friendly suggestion. Report both to the user.

## Step 2.A: 下载小宇宙字幕（仅限小宇宙平台）

**仅在 platform 为 `xiaoyuzhou` 时执行此步骤。**

1. 检查 JSON 输出中的 `subtitleUrl` 字段：
   - 若为 `null`：字幕不可用，跳到 **Step 2.B**（标记 `subtitleAvailable = false`）。
   - 若非 `null`：继续下载字幕。

2. 下载字幕文件：
   ```bash
   curl -s "<subtitleUrl>" -o /tmp/linkmind-subtitle.srt
   ```

3. 解析字幕（SRT 或 WebVTT 格式）：
   - 解析每条字幕：序号、时间戳行（`HH:MM:SS,mmm --> HH:MM:SS,mmm` 或 `.` 分隔）、文本内容。
   - 将时间戳转换为秒数：`startSeconds` / `endSeconds`。

4. 标记 `subtitleAvailable = true`，将解析结果存入 `subtitleEntries`（用于下一步过滤）。

**如果 curl 失败或文件为空：** 标记 `subtitleAvailable = false`，继续流程，不中止。

## Step 2.B: 时间窗口过滤（仅限小宇宙平台）

**仅在 platform 为 `xiaoyuzhou` 时执行此步骤。**

根据 JSON 中的 `timestampSeconds` 决定摘要范围：

**情况一：`timestampSeconds` 不为 null（用户分享了时间打点）**

- 窗口范围：`[timestampSeconds - 120, timestampSeconds + 120]`（前后各 2 分钟）
- 从 `subtitleEntries` 中过滤满足条件的条目（条目与窗口有任意重叠即选入）：
  `entry.startSeconds < windowEnd && entry.endSeconds > windowStart`
- 存入 `filteredEntries`，并记录 `summaryScope = "time_window"`。
- **即使有完整字幕，也只对 `filteredEntries` 生成深度摘要**（用户明确指定了关注范围）。

**情况二：`timestampSeconds` 为 null（完整收听）**

- 不过滤，`filteredEntries = subtitleEntries`（使用全部字幕）。
- 记录 `summaryScope = "full"`。

**若 `subtitleAvailable = false`：**

- `filteredEntries = []`，在生成摘要时注明字幕不可用。
- 若 `timestampSeconds` 不为 null，在 Step 3 中提示用户：
  "⚠️ 平台字幕不可用，无法提取该时间点的内容。如需转写，请配置 ASR 服务。"

**格式化字幕文本：** 将 `filteredEntries` 转为纯文本（去掉时间戳行，每条以换行分隔），
存入 `subtitleText`，供深度摘要使用。

## Step 2.5: Download images to vault

If the JSON contains an `images` array with one or more URLs, download them
locally so the note is fully viewable offline in Obsidian.

1. Determine the slug (see file naming rules in Step 3).
2. Set the attachments directory: `{obsidian_vault}/LinkMind/attachments/{date}-{slug}/`
3. Run the download script:

```bash
npx tsx skills/linkmind/scripts/download-images.ts \
  --urls "{comma-separated image URLs}" \
  --output-dir "{attachments directory}" \
  --referer "{platform homepage: https://weibo.com / https://www.xiaohongshu.com / https://mp.weixin.qq.com}"
```

4. The script outputs a JSON mapping: `{ "original_url": "img-001.jpg", ... }`.
   A `null` value means that image failed to download.
5. For successfully downloaded images, use the relative path in Markdown:
   `![image](attachments/{date}-{slug}/img-001.jpg)`
6. For failed downloads, fall back to the original remote URL.

**For WeChat articles specifically:** after obtaining the download mapping, also
prepare the final `richContent` by replacing each `![](original_url)` in the
`richContent` field with `![图片](attachments/{date}-{slug}/img-NNN.jpg)` (using
the local filename from the mapping, or the original URL if download failed).
Store this as the "resolved richContent" — you will use it in Step 3.

If the `images` array is empty, skip this step.

## Step 2.6: Analyze image content (multimodal)

If images were successfully downloaded in Step 2.5, analyze each image to extract
visual content using your multimodal capabilities.

1. For each successfully downloaded image (where the download mapping value is not `null`):
   a. Read the image file from the local path using the Read tool:
      `{obsidian_vault}/LinkMind/attachments/{date}-{slug}/img-001.jpg`
   b. Analyze the image and extract:
      - **Visible text**: Any readable text, captions, watermarks, labels, or OCR content
      - **Key visual elements**: Charts, screenshots, UI elements, notable objects
      - **Contextual information**: Anything that supplements the original post text
   c. Write a concise description (1-3 sentences) capturing the information value.

2. Store the per-image analysis results — you will use them in two places:
   - **Step 3 (Markdown)**: Append as a blockquote immediately after each image
   - **Deep Summary**: Use all image analysis results as supplementary input

**For WeChat articles**: after analyzing all images, update the "resolved richContent"
(prepared in Step 2.5) by inserting each image's analysis blockquote immediately
after the corresponding `![图片](...)` line. The final richContent should look like:

```markdown
Some text paragraph.

![图片](attachments/{date}-{slug}/img-001.jpg)

> **图片内容：** （Step 2.6 对该图片的分析结果）

More text paragraph.

![图片](attachments/{date}-{slug}/img-002.jpg)

> **图片内容：** （Step 2.6 对该图片的分析结果）

Final text paragraph.
```

**Output format per image (used in the Markdown):**

```markdown
> **图片内容：** （简要描述图片中的关键信息，包括可见文字和重要视觉元素）
```

**Analysis guidelines:**

- Focus on **information value** — extract meaningful text and data first,
  then briefly describe the visual scene.
- Be specific: include actual text content, numbers, names from the image.
- Do NOT describe obvious formatting (e.g., "这是一张图片" or "图片显示了文字").
- If the image is purely decorative with no informational value, write:
  `> **图片内容：** 装饰性图片，无额外信息内容。`
- If reading the image fails, write:
  `> **图片内容：** ⚠️ 图片分析失败`

**Skip conditions (do NOT perform analysis):**

- `images` array is empty → no images to analyze
- All images failed to download in Step 2.5 → no local files to read

## Step 2.C: 小宇宙音频 ASR 降级（仅限小宇宙平台）

**仅在以下所有条件同时成立时执行：**
- `platform == xiaoyuzhou`
- `subtitleAvailable == false`（Step 2.A 字幕不可用）
- `audioUrl` 不为 null
- `.env` 中已配置 ASR 服务（讯飞或 OpenAI）

若条件不满足（ASR 未配置），跳过此步骤，在 Step 3 中提示：
"⚠️ 平台字幕不可用，ASR 服务未配置，无法转写音频。请在 .env 中配置 ASR 凭据。"

**执行步骤：**

1. 确定时间参数（用于只转写用户关心的片段，避免对整集做 ASR）：
   - 若 `timestampSeconds` 不为 null：
     - `startSeconds = max(0, timestampSeconds - 120)`
     - `endSeconds = timestampSeconds + 120`
   - 若 `timestampSeconds` 为 null：不传时间参数（转写全集）

2. 确保 attachments 目录存在（同 Step 2.5）。

3. 运行音频转写脚本：

**有时间窗口时（timestampSeconds 不为 null）：**
```bash
npx tsx skills/linkmind/scripts/extract-transcript.ts \
  --media-url "<audioUrl>" \
  --output-dir "{attachments directory}" \
  --config skills/linkmind/config.json \
  --referer "https://www.xiaoyuzhoufm.com" \
  --start "{startSeconds}" \
  --end "{endSeconds}"
```

**转写全集时（timestampSeconds 为 null）：**
```bash
npx tsx skills/linkmind/scripts/extract-transcript.ts \
  --media-url "<audioUrl>" \
  --output-dir "{attachments directory}" \
  --config skills/linkmind/config.json \
  --referer "https://www.xiaoyuzhoufm.com"
```

4. 脚本输出 JSON：
   ```json
   { "srtPath": "transcript.srt", "fullText": "转写纯文本..." }
   ```
   - 成功后：标记 `asrAvailable = true`，将 `fullText` 存入 `subtitleText`，用于深度摘要
   - 失败后（含 `"error"` 字段）：标记 `asrAvailable = false`，**不中止流程**，在 Step 3 中报告错误

## Step 2.7: Extract video transcript (if applicable)

**此步骤适用于微博、小红书等有 `videoUrl` 的平台。小宇宙平台请使用 Step 2.C。**

If the JSON contains a non-null `videoUrl` field **and** the user has configured
ASR credentials in `.env`, extract the audio and transcribe it.

1. Ensure the attachments directory exists (same as Step 2.5):
   `{obsidian_vault}/LinkMind/attachments/{date}-{slug}/`
2. Run the transcript extraction script:

```bash
npx tsx skills/linkmind/scripts/extract-transcript.ts \
  --media-url "<MEDIA_URL>" \
  --output-dir "{attachments directory}" \
  --config skills/linkmind/config.json \
  --referer "{platform homepage: https://weibo.com / https://www.xiaohongshu.com / https://mp.weixin.qq.com}"
```

3. The script outputs JSON to stdout:
   ```json
   {
     "srtPath": "transcript.srt",
     "fullText": "完整的转写纯文本..."
   }
   ```
   - `srtPath`: the SRT filename saved in the output directory
   - `fullText`: the complete transcript as plain text (for use in the summary)
4. If the script outputs an `"error"` field, the transcript extraction failed.
   **Do NOT abort the entire workflow** — continue to Step 3 without the transcript.
   Report the error to the user alongside the final result.

**Skip conditions (do NOT run the script):**
- `videoUrl` is `null` → no video to transcribe
- `.env` has no ASR variables configured → ASR not configured;
  inform the user: "视频转写需要配置 ASR 服务（科大讯飞或 OpenAI Whisper），请在 .env 中配置。参考 .env.example。"

**Multilingual transcripts:** If `fullText` is in a non-Chinese language, translate
and present the key points in Chinese when writing the deep summary. The SRT file
itself is kept in the original language.

## Step 3: Generate the Markdown file

Using the JSON output, local image paths from Step 2.5, image analysis from
Step 2.6 (if available), and transcript from Step 2.7 (if available), create
a Markdown file with this structure.

**YAML frontmatter safety rules:**

String values in YAML frontmatter MUST be properly quoted to avoid parse errors.
Apply these rules to `title`, `author`, and `original_url`:

1. **Default to single quotes** `'...'` for `title` and `author` — these fields
   frequently contain characters that break double-quoted YAML strings (Chinese
   curly quotes `""`, pipes `|`, colons `:`, etc.).
2. If the value itself contains a single quote `'`, use double quotes `"..."` and
   backslash-escape any inner double quotes.
3. Always wrap `original_url` in double quotes `"..."` — URLs contain `?`, `=`,
   `&` which are special in YAML.
4. Never leave string values unquoted if they contain any of: `: | ? = & " " ' # [ ] { }`.

```markdown
---
title: '{title}'
date: {date}
platform: {platform}
author: '{author}'
original_url: "{originalUrl}"
captured_at: {fetchedAt}
has_video: {true/false}
has_transcript: {true/false}
has_image_analysis: {true/false}
---

(For WeChat articles only, also add these frontmatter fields:)
---
account_name: '{accountName}'
digest: '{digest}'
---

(For 小宇宙 episodes only, also add these frontmatter fields:)
---
podcast: '{podcast}'
episode_id: '{episodeId}'
duration_seconds: {durationSeconds}
timestamp_seconds: {timestampSeconds or null}
---

# {title}

> 来源：{platform display name} @{author} | {date}

## 深度总结

(Generate the deep summary following the **Deep Summary Guidelines** below.
If image analysis results are available from Step 2.6, incorporate them.
If a video transcript is available from Step 2.7, incorporate it as well.
All sources — original text, image analysis, video transcript — should be
synthesized together.)

## 原文内容

(For **WeChat** articles: use the "resolved richContent" prepared in Steps 2.5–2.6
— this is the Markdown with inline images and analysis blockquotes interleaved
at their original positions. Do NOT add a separate 图片 section for WeChat.)

(For **Weibo / Xiaohongshu**: use `{text}` here — images are listed separately
in the 图片 section below.)

## 视频转写

(Only include this section if Step 2.7 produced a transcript.)

> 📎 字幕文件：[transcript.srt](attachments/{date}-{slug}/transcript.srt)

**金句摘录：**

(Read the SRT file and select the 3 most insightful or quotable sentences from the
full transcript. Parse total entry count (N_total) and estimate video duration from
the last entry's end timestamp. If end timestamp is unavailable, use N_total × 3
seconds as the total duration. For each selected quote at SRT entry index i, calculate:
  approx_seconds = (i / N_total) × total_duration_seconds
  percent = round(i / N_total × 100)
  display as: `~MM:SS`（视频约 {percent}% 处）

> "（金句原文）"
> —— `~MM:SS`（视频约 X% 处）

> "（金句原文）"
> —— `~MM:SS`（视频约 X% 处）

> "（金句原文）"
> —— `~MM:SS`（视频约 X% 处）

**Selection criteria for quotes:**
- Choose sentences that best capture a core insight, key argument, or memorable phrasing
- Spread timestamps across the video (one from early, one from middle, one from late)
- Do NOT pick 3 consecutive or near-consecutive entries

(If Step 2.7 was skipped because videoUrl is null, omit this section entirely.
If Step 2.7 was skipped because ASR is not configured, add a note:
"⚠️ 视频转写未执行：ASR 服务未配置。"
If Step 2.7 failed, add: "⚠️ 视频转写失败：{error message}")

## 图片

(For **Weibo / Xiaohongshu** only: list each image followed by its multimodal
analysis from Step 2.6. Use the local path if downloaded, otherwise the remote URL:)

![图片](attachments/{date}-{slug}/img-001.jpg)

> **图片内容：** （Step 2.6 对该图片的分析结果）

![图片](attachments/{date}-{slug}/img-002.jpg)

> **图片内容：** （Step 2.6 对该图片的分析结果）

(If Step 2.6 was skipped because no images exist, omit the 图片 section entirely.
If an individual image's analysis failed, use:
> **图片内容：** ⚠️ 图片分析失败)

(For **WeChat** articles: OMIT this 图片 section entirely — images are already
embedded inline in the 原文内容 section above.)

## 字幕摘录

(仅限小宇宙平台，且 `subtitleAvailable = true` 或 `asrAvailable = true` 时包含此区块。)

(来源标注：)
- 若字幕来自平台字幕文件：`> 📝 来源：平台字幕`
- 若字幕来自 ASR 音频转写：`> 🎙️ 来源：ASR 音频转写`

(若 `timestampSeconds` 不为 null，标注摘录范围：)
> 📍 以下内容为打点时间 `{MM:SS}` 前后 2 分钟的字幕（共 {filteredEntries.length} 条）

(将 `filteredEntries` 的文本按顺序输出，每行格式：)
> `[{startMM:SS}]` 字幕文本

(若 `summaryScope = "full"`，省略范围提示，直接输出全部字幕文本。)

(若 `subtitleAvailable = false` 且 `asrAvailable = false`，输出：)
> ⚠️ 该剧集平台字幕不可用，ASR 转写也未成功。

**金句摘录：**

从 `filteredEntries`（或全集字幕）中选取 3 句最具洞见或值得引用的话，格式如下：

- 计算条目总数 N_total 和时间范围（窗口模式：startSeconds ~ endSeconds；全集模式：0 ~ durationSeconds）
- 若字幕来自 ASR（SRT 时间戳为相对于片段起始的偏移），实际剧集时间 = SRT 时间戳 + startSeconds
- 对每条选出的金句（条目索引 i），计算剧集时间：
  - 窗口模式：`approx_episode_seconds = startSeconds + (i / N_total) × (endSeconds - startSeconds)`
  - 全集模式：`approx_episode_seconds = (i / N_total) × durationSeconds`
  - `percent = round(approx_episode_seconds / durationSeconds × 100)`
  - 显示为：`` `~MM:SS` ``（全集约 {percent}% 处）

> "（金句原文）"
> —— `~MM:SS`（全集约 X% 处）

> "（金句原文）"
> —— `~MM:SS`（全集约 X% 处）

> "（金句原文）"
> —— `~MM:SS`（全集约 X% 处）

**金句选取标准：**
- 选最能捕捉核心洞见、关键论点或令人印象深刻的表述
- 分散时间分布（窗口内靠前、中间、靠后各一句）
- 不选连续或相邻条目

## 节目简介

(仅限小宇宙平台，输出 `description` 字段内容，即 shownotes / 节目简介。)

## 元信息

(For Weibo — use reposts/comments/likes stats:)
- 转发: {stats.reposts} | 评论: {stats.comments} | 点赞: {stats.likes}

(For Xiaohongshu — use likes/collects/comments stats:)
- 点赞: {stats.likes} | 收藏: {stats.collects} | 评论: {stats.comments}

(For WeChat — use readCount/likeCount/inLookCount; show '—' for null values:)
- 阅读: {readCount ?? '—'} | 点赞: {likeCount ?? '—'} | 在看: {inLookCount ?? '—'}
- 公众号: {accountName}
- 摘要: {digest}

(For 小宇宙 — use podcast name and duration:)
- 节目：{podcast}
- 时长：{Math.floor(durationSeconds/60)} 分钟
(若 timestampSeconds 不为 null:)
- 打点：{MM:SS}（{timestampSeconds} 秒）

(Omit stats lines that are null for all fields.)
```

**小宇宙笔记的深度摘要要求：**

在 `## 深度总结` 部分，若 `timestampSeconds` 不为 null（用户指定了时间点）：
- 明确标注摘要的时间范围：`> 内容范围：{startMM:SS} — {endMM:SS}`
- 仅基于 `filteredEntries` 内容生成摘要，不延伸到窗口外
- 说明该时间段的主要观点/讨论内容
- 如有需要，从 `description`（节目简介）提供背景上下文

若 `summaryScope = "full"`（用户未指定时间点）：
- 基于全部 `subtitleText` 生成完整剧集摘要
- 参考 `description` 补充节目背景

### File naming

Name the file as: `{date}-{slug}.md`

- `{date}` is `YYYY-MM-DD` format
- `{slug}` is derived from the title — take the first 30 chars, replace spaces with
  hyphens, remove special characters, and lowercase. If the title is in Chinese,
  use the first 10 Chinese characters joined by hyphens.
- Example: `2026-03-22-张三分享成都美食推荐.md`

### Output directory

Save the file to `{obsidian_vault}/LinkMind/` (the vault path from Step 0).
Create the `LinkMind/` subdirectory if it does not exist.

## Step 4: Report result

After saving, tell the user:
- The file path where the note was saved (the full Obsidian vault path)
- The title extracted from the content
- The platform and author
- How many images were analyzed and key findings (if image analysis was performed)
- Whether video transcript was generated (and SRT file location if so)
- A brief overview of the deep summary

## Deep Summary Guidelines

Read and follow the full guidelines in
`skills/linkmind/references/deep-summary-guide.md`.

Key points: classify the content type (观点/教程/新闻/故事/测评/清单),
write structured fields + bullets/tables in Chinese, add 2-3 key takeaways,
incorporate image analysis and video transcript when available.

## Error handling

- If the handler script fails, report the error to the user clearly.
- Use the `code` field to tailor your response:
  - `NETWORK` — suggest checking network and retrying
  - `AUTH` — tell the user the content may require login; suggest configuring
    cookies (see below)
  - `RATE_LIMIT` — suggest waiting a few minutes before retrying
  - `NOT_FOUND` — ask the user to verify the link is correct
  - `PARSE` — the platform structure may have changed; suggest reporting the issue
- If a timeout occurs, suggest the user try again later.
- Never silently fail — always give the user feedback.

## Cookie configuration (optional)

Cookies are **optional**. They are only needed when capturing content that
requires login (e.g. private or restricted posts). Public content can be
captured without any cookie configuration.

Configure platform cookies in `skills/linkmind/.env`
(copy from `.env.example` if the file does not exist):

```bash
LINKMIND_WEIBO_COOKIE="SUB=xxx; SUBP=yyy"
LINKMIND_XHS_COOKIE="a1=xxx; web_session=yyy"
LINKMIND_WXMP_COOKIE="appmsgticket=xxx; wxuin=xxx; ..."
```

> 注：WeChat Cookie 用于获取阅读/点赞/在看统计数据，不影响基础文章提取。

You can also set cookies via `config.json`:

```json
{
  "obsidian_vault": "/path/to/vault",
  "cookies": {
    "weibo": "SUB=xxx; SUBP=yyy",
    "xiaohongshu": "a1=xxx; web_session=yyy",
    "wechat": "appmsgticket=xxx; wxuin=xxx; ..."
  }
}
```

Environment variables take precedence over `config.json` values.

To obtain cookies: log in to the platform in a browser, open DevTools → Application →
Cookies, and copy the relevant cookie values as a semicolon-separated string.

## ASR configuration (optional — required for video transcript)

ASR is **optional**. Without it, video posts are still captured normally — only
the transcript feature is unavailable.

Configure ASR credentials in `skills/linkmind/.env`
(copy from `.env.example` if the file does not exist):

```bash
LINKMIND_IFLYTEK_APP_ID=your_app_id
LINKMIND_IFLYTEK_API_KEY=your_api_key
LINKMIND_IFLYTEK_API_SECRET=your_api_secret
LINKMIND_OPENAI_API_KEY=sk-xxx
```

- Configure at least one service to enable video transcript
- If both are configured, iFlytek is tried first; on failure,
  OpenAI is used as fallback
- To obtain iFlytek credentials: register at https://www.xfyun.cn/, create an
  app, enable "语音转写" service, and copy the App ID / API Key / API Secret
- To obtain OpenAI key: https://platform.openai.com/api-keys
