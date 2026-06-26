---
name: plume-notecard
description: |
  Plume AI Notecard Generation Service. Triggered when users want to convert topics, long-form text, or reference images into notecards.
  Supports: topic notecards, long-form text to notecard, reference image notecards (sketch/style transfer/product embed/content rewrite), batch notecards, image-based slide deck notecards (cover+content+back cover), retry.
  Activate when user mentions: notecard, card, infographic, knowledge poster, visualize article,
  diagram, summary chart, timeline, turn this article into a graphic, create a visual about XX,
  use this card's style as reference, use this product image for notecard, replace the content of this notecard,
  create a series of notecards, split long text into multi-page notecards,
  notecard slide deck, card slides, notecard presentation, image PPT, image slides,
  卡片, 信息卡片, 信息图, 知识图谱海报, 把文章可视化, 图解, 总结图, 时间线图, 把这篇文章转成图,
  围绕XX主题做一张图解, 参照这张信息图的风格, 用这张产品图做信息图,
  把这张信息图的内容换成, 做一组系列信息图, 把长文拆成多页信息图,
  图片幻灯片, 图片PPT, 信息图幻灯片, 信息图PPT, 做一套图片PPT, 做一套信息图幻灯片,
  infographic slide deck, infographic slides, infographic presentation.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*), Bash(zip *)
metadata: {"openclaw": {"requires": {"env": ["PLUME_API_KEY"]}, "primaryEnv": "PLUME_API_KEY"}}
---

# Plume AI Notecard Service

Help users generate notecards (information cards) through natural language. Notecards emphasize "layout design" and "information delivery", distinct from regular illustrations/posters.

Boundary with plume-image: User says "notecard/card/infographic/diagram/visualize/timeline/turn article into graphic" → this skill; says "generate image/poster/remove background/video" → plume-image.

## Security

This skill follows these security practices:

- Credential stripping for secrets, API keys, and tokens
- No remote code execution patterns like `curl | bash`
- HTTPS-only downloads with redirect limits (max 5)
- Content-Type validation for downloaded files (image/* only)
- Sanitized logging with no secret leakage
- External content treated as untrusted input

## Agent Environment Adaptation

This skill is compatible with multiple agent environments. Scripts automatically detect and select appropriate storage paths.

### Claude Code

Config locations:
- Project-level: `.plume-notecard/EXTEND.md`
- User-level: `~/.plume-notecard/EXTEND.md`

Media directory: `~/.claude/media/plume-notecard/`

### OpenClaw

Config location: `env.PLUME_API_KEY` in `~/.openclaw/openclaw.json`
Media directory: `~/.openclaw/media/plume-notecard/`

### Other Agents (Cursor / Cline / generic)

Configure via `PLUME_API_KEY` environment variable or `~/.plume-notecard/EXTEND.md`
Media directory: `~/.agent/plume-notecard/`

## Permission Requirements

This skill requires the following tool permissions:

| Tool | Purpose | Notes |
|------|---------|-------|
| `Bash(python3 ...)` | Execute Python scripts | Universal |
| `Bash(zip *)` | Package results | Universal |

## Mandatory Pre-check

Must execute before each use:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_config.py
```

- `CONFIGURED` — Configured, proceed with workflow
- `NOT_CONFIGURED` — Stop, prompt user:
  - OpenClaw environment: Configure to `env.PLUME_API_KEY` in `~/.openclaw/openclaw.json`
  - Claude Code environment: Set `PLUME_API_KEY` environment variable
  - Other environments: Set `PLUME_API_KEY` environment variable
  - Get API Key: Visit [Plume](https://design.useplume.app/notecard)

## Template Gallery

During content planning, always include the template gallery link for users to browse styles. Append `?lang=` parameter based on the user's language:

| User Language | Link |
|--------------|------|
| 中文 | `https://design.useplume.app/notecard/templates?lang=zh-CN` |
| English | `https://design.useplume.app/notecard/templates?lang=en` |
| 日本語 | `https://design.useplume.app/notecard/templates?lang=ja` |

Agent auto-selects the matching link based on the language the user is currently using in conversation.

When user clicks a template and pastes it back, Agent extracts the template name to search for matching ID, then passes it via `--template-id` when creating the task.

If user doesn't select a template and confirms directly, Agent auto-matches style based on content (can pass via `--style-hint`).

## Core Workflow

**`transfer` (when reference image exists) → `create` (sync wait for result) → get local image path → `merge-pdf` / `create-zip` (optional, for batch/deck) → subsequent operations (deliver/package etc.)**

**Before calling create, you must first send a waiting message to the user**, e.g. "Sure, generating your notecard now. This usually takes 1-2 minutes, please wait." This message must be sent before calling create. Because create is synchronous and blocking — if the prompt text and create are in the same turn, the text may not reach the user before blocking starts.

```bash
# Upload reference image (reference mode, subcommand is transfer)
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py transfer --file /path/to/image.png
# Returns {"success": true, "image_url": "https://...", "width": W, "height": H}

# Create task and wait for result (default timeout 30 minutes)
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
  --channel <channel> --mode <article|reference> [params...]
# Returns {"success": true, "task_id": "xxx", "images": ["/abs/path/result_xxx.png", ...], "result_urls": [...]}

# Create task with auto PDF merge (batch/deck mode)
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
  --channel <channel> --mode article --count 5 --merge-to-pdf
# Returns {"success": true, "images": [...], "pdf": {"path": "/path/to/merged.pdf", "page_count": 5, "file_size_mb": 2.3}}

# Create task with auto ZIP packaging (batch/deck mode)
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create \
  --channel <channel> --mode article --count 5 --create-zip
# Returns {"success": true, "images": [...], "zip": {"path": "/path/to/notecards.zip", "file_count": 5, "file_size_mb": 1.8}}

# Merge existing images to PDF
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py merge-pdf \
  --images /path/to/img1.png,/path/to/img2.png,/path/to/img3.png \
  --output /path/to/output.pdf
# Returns {"success": true, "pdf_path": "/path/to/output.pdf", "page_count": 3, "file_size_mb": 1.5}

# Package existing images to ZIP
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py create-zip \
  --images /path/to/img1.png,/path/to/img2.png,/path/to/img3.png \
  --output /path/to/output.zip
# Returns {"success": true, "zip_path": "/path/to/output.zip", "file_count": 3, "file_size_mb": 1.2}

# Read operation log (for retry/quoting previous results)
python3 ${CLAUDE_SKILL_DIR}/scripts/create_notecard.py history --channel <channel>

# After getting images, continue with operations:
# Deliver to user (handled by current Agent's own message tool)
# Or package
zip -j /tmp/notecard.zip /abs/path/result_xxx.png
```

**Prohibited:** Fabricating task_id/URL, asking for API Key in chat, auto-creating tasks when user only sends image without text, creating tasks directly when user only gives a topic word or one sentence (must first guide and confirm content and style), uploading local files without explicit user confirmation, deleting or modifying any JSON files under the media directory.

**Exec timeout requirement:** The create command is long-running (deck/batch tasks typically take 3-10 minutes). When calling, you **MUST** set a sufficiently long timeout, recommended 1800 seconds. Do NOT use shorter timeouts like 120/180/300 — these will SIGTERM the process before the task completes, wasting credits.

**Timeout handling:** If create returns `"status": "timeout"`, inform user the task is still processing and they can retry later.

**SIGTERM recovery:** If the create process is killed by SIGTERM, do NOT create a new task. Inform user the process was interrupted but the task may still be running on the server, suggest they retry later or wait for the result.

## Scenario Detection

When receiving user message, check in the following order, stop on first match:

1. Does this turn have a new image?
   ├─ Has image + has action instruction → go to [Reference Image] flow
   ├─ Has image + no text → Reply "Got the image, how would you like me to process it?"
   └─ No new image → continue ↓

2. Does conversation history have unconsumed historical images?
   ├─ Yes → **Ask user for confirmation before uploading**, then go to [Reference Image] flow
   └─ No → continue ↓

3. Is user referencing/modifying existing results? ("switch style" / "换个风格", "try again" / "再试一次", "regenerate" / "重新生成")
   ├─ Yes → Read history, go to [Retry] flow
   └─ No → continue ↓

4. Is user requesting an image-based slide deck?
   ├─ Must match BOTH "image/notecard" AND "slide deck/PPT/presentation" keywords → go to [Deck] flow
   └─ No → go to [New Creation] flow (article mode)

### User Intent → Mode Mapping

| User Says | mode | Key Parameters |
|-----------|------|---------------|
| "Make a notecard about XX" / "做一张XX的卡片" / "帮我做个XX图解" | `article` | `--article` (Agent first expands into complete content) |
| "Turn this article into a notecard" / "把这篇文章转成卡片" | `article` | `--article` |
| Upload image + "turn this into a notecard" / "把这个做成卡片" | `reference` | `--reference-type sketch` + urls + width + height |
| Upload image + "use this style to make one about XX" / "参照这个风格做一张关于XX" | `reference` | `--reference-type style_transfer` + urls + width + height + topic/article |
| Upload image + "replace the content with XX" / "把内容换成XX" | `reference` | `--reference-type content_rewrite` + urls + width + height + article |
| Upload product image + "use this product for notecard, selling points are..." / "用这个产品做卡片，卖点是..." | `reference` | `--reference-type product_embed` + urls + width + height + `--reference-article <selling points>` |
| "Switch style" / "换个风格" (for existing result) | Retry | `--action switch_style` + `--last-task-id` + `--article <original content>` |
| "Regenerate" / "重新生成" / "再试一次" (for existing result) | Retry | `--action repeat_last_task` + `--last-task-id` |
| "Replace content with XX" / "把内容换成XX" (for existing result) | Retry | `--action switch_content` + `--article <new content>` + `--last-task-id` |
| "Generate N notecards in a series" / "生成N张系列卡片" | Batch | `--count N` + `--child-reference-type` |
| "Make a notecard slide deck about XX" / "做一套XX的图片幻灯片" / "做一套信息图PPT" | Deck | `--deck-mode` + `--article` + `--page-count` |

For complete parameter documentation see [references/modes.md](references/modes.md), scenario examples see [references/workflows.md](references/workflows.md), error codes see [references/error-codes.md](references/error-codes.md).

## Usage Guide

When the user first triggers this skill but their intent is vague (e.g. just says "notecard", "card", "make me a graphic", without providing a specific topic or image), Agent must reply with a brief usage guide:

```
Here's how you can get started:

1️⃣ Tell me a topic directly, e.g.: "Create a notecard about the history of gold"
2️⃣ Upload an existing notecard, then say: "Replace the content with xxx topic"

How would you like to start?
```

## Content Planning (Mandatory, Cannot Skip)

**Before calling create, must determine if user input is "information-complete":**

**Information-complete = all of the following are met:**
1. Has clear content body (at least 3+ specific knowledge points/paragraphs/data)
2. User has confirmed content and style (or explicitly said "you decide" / "whatever" / "just do it" / "你来定" / "随便" / "直接做")

**Typical incomplete examples (must NOT create directly):**
❌ "Make a notecard about the history of AI"  → Only a topic, no specific content
❌ "Create a blockchain diagram"              → Only a topic word
❌ "Generate a notecard about healthy eating" → One-line request
❌ "Make a Python learning roadmap"          → Topic + direction, but no specific content
Chinese equivalents (same rule applies):
❌ "做一张人工智能发展史的卡片"  → 只有主题，没有具体内容
❌ "帮我做个区块链图解"          → 只有主题词
❌ "生成一张关于健康饮食的卡片"    → 一句话需求
❌ "做张Python学习路线图"         → 主题+方向，但无具体内容

**Complete examples (can create directly):**
✅ User pasted a complete article + "turn this into a notecard"
✅ User provided detailed content outline (3+ sections with key points for each)
✅ Previous turn Agent proposed content plan, user replied "looks good" / "go ahead"
Chinese equivalents:
✅ 用户贴了一篇完整文章 + "把这篇转成卡片"
✅ 用户给了详细的内容大纲（3个以上板块+每个板块的要点）
✅ 上一轮 Agent 提出了内容规划，用户回复"可以"/"就这样做"

**When information is incomplete, must first reply with a planning message:**
- Include 2-3 content section suggestions
- **Must include template gallery link** (select matching `?lang=` based on user language)
- Wait for user confirmation before calling create
- Complete in one message, don't ask across multiple turns

**Batch `--child-reference-type` selection rule:**
- `content_rewrite` (default): Unified style, visually consistent series notecards
- `style_transfer`: User uploaded external reference image, need to transfer style

**Deck mode (`--deck-mode`):** First plan page count and structure, prefer passing structured content via `--pages`. Default aspect ratio `16:9`.

**PDF merge behavior:**
- User explicitly mentions "PDF" / "合并成 PDF" / "merge to PDF" → add `--merge-to-pdf` flag
- Batch/deck mode without PDF request → generate images only, mention: "如需 PDF 版本，请告诉我。" / "Let me know if you need a PDF version."
- User later requests PDF → call `merge-pdf` with image paths from history
- Single image (`count = 1`) → no PDF merge option

**ZIP packaging behavior:**
- User explicitly mentions "ZIP" / "打包" / "package" / "压缩包" → add `--create-zip` flag
- Batch/deck mode without packaging request → generate images only, mention: "如需打包下载，请告诉我。" / "Let me know if you need a packaged download."
- User later requests ZIP → call `create-zip` with image paths from history
- Single image (`count = 1`) → no ZIP packaging option

## Error Handling

| Return Value | Meaning | Agent Must Do |
|-------------|---------|--------------|
| `"success": false, "status": 4` | **Task failed** | Stop immediately, inform user |
| `"success": false, "status": 5` | **Task timeout** | Stop immediately, inform user |
| `"success": false, "status": 6` | **Task cancelled** | Stop immediately, inform user |
| `"success": false, "status": "timeout"` | **Local wait timeout** | Inform user task is still processing |
| `"success": false` (other) | API call failed | Inform user of error reason |

### Automatic Retry Strictly Prohibited

After create returns `"success": false`:
1. **Do NOT** automatically switch content, style, parameters and re-call create
2. **Do NOT** misjudge status=4 (failure) as timeout or content issue
3. Must stop immediately and inform user of the failure as-is
4. Only retry when user explicitly says "try again", and max 2 task creations per conversation
5. Each create deducts credits (200 credits), blind retries directly waste user's money
