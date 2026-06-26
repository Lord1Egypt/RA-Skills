---
name: popai-presentations
description: Create presentations (PPT) using PopAI API. Use when asked to create slides, presentations, decks, or PPT content via PopAI. Supports uploading reference files (pptx/pdf/docx/images).
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"], "env":["POPAI_API_KEY"]},"primaryEnv":"POPAI_API_KEY" } }
---

# PopAI PPT Skill

Create presentations programmatically via PopAI's API. Supports optional file uploads as reference material or templates.

## Setup

1. Get API key from https://www.popai.pro
2. Store in environment: `export POPAI_API_KEY=...`

## Scripts

- `scripts/generate_ppt.py` - Generate PPT via PopAI API (upload files → create channel → SSE stream → get pptx)

## Usage Examples

```bash
# Generate PPT from topic only
python3 generate_ppt.py --query "人工智能发展趋势报告"

# With a template pptx file
python3 generate_ppt.py --query "特斯拉财报ppt" --file template.pptx

# With multiple reference files (max 5)
python3 generate_ppt.py --query "年度报告" --file template.pptx data.pdf chart.png
```

## Agent Steps

1. Get PPT topic from user
2. If user provides local files, pass them via `--file` (max 5, supports pptx/pdf/docx/images etc.)
3. Create a temp output file, then run script **in background** with `--output`:
   ```bash
   # Step 3a: Create temp file and launch in background
   OUTFILE="/tmp/popai_ppt_$(date +%s).jsonl"
   touch "$OUTFILE"
   ```
   ```bash
   # Step 3b: Run in background (run_in_background: true, timeout: 600000)
   cd /Users/Gunnar/popai-python/.claude/skills/popai-presentations && POPAI_API_KEY="$POPAI_API_KEY" python3 scripts/generate_ppt.py --query "TOPIC" [--file FILE1 FILE2 ...] --output "$OUTFILE"
   ```
   Tell user: "PPT正在生成中，预计3-5分钟..."

4. **Poll for progress** — periodically read new lines from the output file using `Read` tool or `cat "$OUTFILE"`, and show progress to user:
   - `task` events → show task status updates
   - `search` events → show "正在搜索..."
   - `summary` event → show generation summary
   - `pptx_ready` event → final result (stop polling)
   - `stream_end` → generation complete (stop polling)
   Poll every ~30 seconds until `pptx_ready` or `stream_end` appears.

5. Present final results to user:
   - Show `summary` text (from `NODE_END` event) as the generation summary
   - Show `pptx_url` as the download link: "下载PPT: <pptx_url>"
   - Show `web_url` as the site link: "在线查看/编辑: <web_url>"

## Output

**Event types (stdout, one JSON per line):**
```json
{"type": "task", "id": "1", "content": "搜索特斯拉最新财报数据", "status": "progressing"}
{"type": "search", "action": "Web Searching", "results": [{"title": "...", "url": "...", "snippet": "...", "date": "..."}]}
{"type": "tool_result", "event": "TOOL_CALLS-xxx", "action": "...", "result": "..."}
{"type": "summary", "text": "已完成特斯拉财报PPT的创建..."}
{"type": "stream_end"}
```

**Final result (`is_end: true`):**
```json
{
  "type": "pptx_ready",
  "is_end": true,
  "pptx_url": "https://popai-file-boe.s3-accelerate.amazonaws.com/.../xxx.pptx",
  "file_name": "xxx.pptx",
  "preview_images": ["https://...0.jpeg"],
  "preview_count": 10,
  "web_url": "https://www.popai.pro/agentic-pptx/<channelId>"
}
```

- `pptx_url`: .pptx文件下载链接
- `web_url`: PopAI源站链接，可在线查看和编辑
- `summary`: NODE_END事件的最终总结文本，展示给用户作为生成摘要

## Technical Notes

- **Streaming**: SSE stream; `TOOL_CALLS-pptx` event contains final .pptx download URL; `last:true` marks stream end
- **File Upload**: Presigned POST to S3 via `getPresignedPost`, supports any file type
- **Timeout**: Generation takes 3-5 minutes
