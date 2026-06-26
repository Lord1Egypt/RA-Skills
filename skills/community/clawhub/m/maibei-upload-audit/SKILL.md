---
name: maibei-upload-audit
description: Upload local/inbound media to Maibei/MaybeAI, copy the audit spreadsheet, analyze uploaded files into the sheet, run the audit stage, generate a visual HTML report, and share it via trycloudflare tunnel. Use when a user asks to upload product images/videos to https://maibei.maybe.ai/e-commerce/upload-audit-file, continue an existing audit batch, fetch the generated spreadsheet link, run the audit pipeline end-to-end, or replay any step with a valid MaybeAI token and user-id. Triggers on: "上传文件并审核", "maybe audit", "maibei audit", "run audit pipeline", "上传审核", "生成审核报告", "分享审核链接".
---

# Maibei Upload Audit

Full end-to-end upload + analyze + audit + HTML report generation + share pipeline.

## Quick start

```bash
python3 scripts/upload_audit.py \
  --token "<bearer-token>" \
  --user-id "<user-id>" \
  --mode full \
  --file "/path/to/image.jpg"
```

With automatic HTML report generation + trycloudflare sharing:

```bash
python3 scripts/upload_audit.py \
  --token "<bearer-token>" \
  --user-id "<user-id>" \
  --mode full \
  --file "/path/to/image.jpg" \
  --html \
  --share
```

## Correct end-to-end order

1. Confirm inputs: bearer token, user-id, local files or inbound media
2. Upload each file with the MaybeAI tRPC upload API
3. Run copy-sheet workflow to create a working spreadsheet
4. Run analyze workflow to classify files, OCR text, and write rows into `审核文件信息`
5. Run the audit stage (audit + font-audit in parallel)
6. Run the summary workflow after audit stage completes
7. **Generate HTML report** grouping results by media URL, sorted by risk
8. **Share via trycloudflare** to produce a public URL
9. Return the working sheet URL + public HTML report URL

## Audit stage execution model

Treat the audit stage as one logical stage after analyze finishes.

Current known workflows inside that stage:
- audit workflow artifact: `69c6582612aa26396bd2ace7`
- font-audit workflow artifact: `69ccb9d584cf626fe68ff7ea`

Inside that stage, `audit` and `font-audit` run in parallel as internal workflows, then `summary` runs after both complete.

## Current known workflow ids

For `/e-commerce/upload-audit-file`:

- copy workflow artifact: `69ca226377efb8a1de743d34`
- analyze workflow artifact: `69c245bca5e657510a37a6a2`
- audit workflow artifact: `69c6582612aa26396bd2ace7`
- font-audit workflow artifact: `69ccb9d584cf626fe68ff7ea`
- summary workflow artifact: `69ca16d067a09db8deb145c2`
- source Excel URL: `https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0`

## Required auth context

Need all of:
- bearer token
- `user-id`
- local files or inbound media, or already-uploaded file URLs

## Script usage

```text
upload_audit.py --mode <mode> [options]

Modes:
  upload    Upload files only
  copy      Copy source Excel only
  analyze   Run analyze step (requires --sheet-url or prior upload)
  audit     Run audit + font-audit
  summary   Run final summary
  full      Upload → copy → analyze → audit → summary (all in one)

Full-mode options:
  --file <path>            Local file to upload (repeatable)
  --html                   Generate HTML report after workflows complete
  --share                  Share HTML report via trycloudflare tunnel
  --html-only              Skip workflows, generate HTML from prior results
  --skip-analyze           Skip analyze step in full mode
  --skip-audit             Skip audit step in full mode
  --skip-font              Skip font-audit step in full mode
  --skip-summary           Skip final summary step

Other options:
  --token <token>          MaybeAI bearer token (required)
  --user-id <id>           MaybeAI user-id (required)
  --sheet-url <url>        Existing working sheet URL
  --source-excel-url <url> Source Excel URL (default: see above)
  --print-json             Output results as JSON
```

## HTML report generation

When `--html` is passed (or `--mode html`), the script generates a self-contained HTML report at `$WORKDIR/audit_report.html`.

The report includes:
- Top-level summary metrics (total / high / medium / low risk counts)
- Overall audit result badge
- Tabbed view by risk level (高风险 / 中风险 / 低风险)
- Per-item cards ordered by risk (high → medium → low), each containing:
  - Media preview thumbnail
  - Media URL (clickable)
  - Overall risk level badge
  - 第三方审核 / 内部规则审核 / 行业规则审核 / 字体审核 sub-results
  - 风险点 (risk hits)
  - BLOCK reason in plain language
  - 建议修改点 and concrete rewrite direction
- Link back to the original working spreadsheet

The HTML is fully self-contained (no external JS/CSS dependencies) and responsive.

## Sharing via trycloudflare

When `--share` is passed, after HTML generation the script:
1. Starts a local HTTP server serving the workspace directory
2. Starts a cloudflared tunnel to expose it publicly
3. Waits for the trycloudflare URL to become reachable
4. Verifies the URL returns HTTP 200
5. Returns the verified public URL

```bash
python3 scripts/share_url.py /path/to/file.html
# outputs: https://xxxx.trycloudflare.com/file.html
```

## Upload step

Use the MaybeAI tRPC endpoint:

```
POST https://maibei.maybe.ai/api/trpc/imageGetUploadUrl
```

Request shape:
```json
{ "key": "superapp/uploads/<timestamp>-<filename>" }
```

Response fields:
- `result.data.uploadUrl`
- `result.data.url`

Upload pattern:
1. Call `imageGetUploadUrl` with a unique `key`
2. PUT raw file bytes to `uploadUrl`
3. Use `url` as the uploaded public URI in later workflows

## Analyze payload construction

Build `variable:dataframe:product_images` as rows:

```json
[
  {
    "url": "https://statics.maybe.ai/.../file.webp",
    "file_type": "image",
    "file_name": "file.webp"
  }
]
```

Use `file_type: "image"` for png/jpg/jpeg/webp/gif.

## Audit and summary payload

Send all three values:

```json
[
  { "name": "variable:scalar:copy_excel_url", "default_value": "<sheet>" },
  { "name": "variable:scalar:excel_url", "default_value": "<sheet>" },
  { "name": "variable:dataframe:copy_excel_url_data", "default_value": [{ "copy_excel_url": "<sheet>" }] }
]
```

## Font-audit payload

Send:

```json
[
  { "name": "variable:scalar:copy_excel_url", "default_value": "<sheet>" }
]
```

## Execution communication rules

**Report progress at every step.** Required progress messages:

```
📤 正在上传文件 1/5...
✅ 文件1 上传完成
📋 正在复制源Excel...
✅ 复制完成
🔍 正在分析文件...
✅ 分析完成
🔴 正在审核（内部规则 + 行业规则）...
✅ 审核完成
🔤 正在字体审核...
✅ 字体审核完成
📊 正在汇总...
✅ 汇总完成
🌐 正在生成HTML报告...
✅ 报告已生成
🔗 正在分享到公网...
✅ 报告已发布: https://xxx.trycloudflare.com/audit_report.html
```

## Response format

After successful end-to-end run with `--html --share`, return:
- Working sheet URL
- Uploaded file URLs (if applicable)
- Copy step result
- Analyze step result
- Audit step result
- Summary workflow result
- HTML report local path
- Public share URL (trycloudflare)

## Debugging

If upload fails:
1. Verify token and user-id
2. Inspect `imageGetUploadUrl` response shape
3. Verify the PUT upload returns 200

If workflow fails:
1. Verify the artifact id by calling `workflow/detail/public`
2. Verify `Authorization: Bearer <token>` and `user-id` on `play-be.omnimcp.ai`
3. Inspect streamed events, especially `action_output`, `dataflow_output`, and `workflow_output`

## Resources

```
maibei-upload-audit/
├── SKILL.md
├── scripts/
│   ├── upload_audit.py   # Main CLI for full pipeline
│   └── share_url.py      # Trycloudflare sharing utility
└── references/
    ├── protocol-notes.md      # API request/response shapes
    └── live-run-notes.md      # Validated execution notes
```
