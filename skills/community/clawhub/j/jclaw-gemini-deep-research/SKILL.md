---
name: deep-research-via-gemini-cli
description: "Execute Gemini Deep Research using the gemini-deep-research MCP extension for the Gemini CLI. Use when user wants deep, comprehensive research on a topic — market analysis, industry research, geopolitical analysis, investment research, or any complex multi-source inquiry. Triggers on: deep research X, 帮我研究 X, gemini deep research X, research X thoroughly, 研究一下 X, do a deep search on X, 深度研究 X. Requires: (1) gemini CLI installed (`npm install -g @google/gemini-cli`), (2) gemini-deep-research extension installed, (3) a paid Google AI API key configured via `gemini extensions config gemini-deep-research`. See references/setup-guide.md for setup instructions."
---

# Gemini Deep Research

Executes a full Deep Research workflow via the `gemini-deep-research` MCP extension, with background polling and automatic report saving. The workflow is non-blocking — the agent sets up the task and exits immediately while a background script handles polling.

---

## Prerequisites

See `references/setup-guide.md`. If any prerequisite is missing, inform the user and stop.

---

## Scripts

Three scripts in `<skill>/scripts/`:

| Script | Role |
|--------|------|
| `start-research.js` | Calls `research_start`, outputs JSON with research ID |
| `poll-research.js` | Polls `research_status` every 5 min until done/timeout |
| `save-report.js` | Calls `research_save_report` once status is `completed` |

All scripts read/write `task.json` in the task's temp directory.

---

## Workflow

### Step 1 — Pre-Flight Confirmation (one message, all parameters)

Write in the user's current session language.

```
请确认 Deep Research 参数：

① 研究主题：[用户描述]
   （将原样发给 Gemini，请确保表述清晰具体）

② 报告格式：
   - Comprehensive Research Report（推荐，最全面）
   - Executive Brief（精简版，1-2页）
   - Technical Deep Dive（技术深度分析）

③ 保存位置：~/ObsidianVault/Default/DeepResearch/
   （默认文件名：YYYYMMDD-<slug>.md，可自定义路径）

④ 轮询最大时长：40 分钟（5 分钟 × 8 次），超时后通知您手动处理

直接回复修改项，或"确认"以默认参数启动。
```

### Step 2 — Create Task Temp Directory

```bash
mkdir -p /tmp/gemini-deep-research/<YYMMDD-HHmm>_<sanitized-topic>/
```

Write `task.json`:

```json
{
  "input": "研究主题",
  "format": "Comprehensive Research Report",
  "outputPath": "/home/node/ObsidianVault/Default/DeepResearch/<YYYYMMDD>-<slug>.md",
  "pollIntervalSeconds": 300,
  "maxPolls": 8,
  "createdAt": "<ISO timestamp>"
}
```

### Step 3 — Start Research

**方法 A：使用 start-research.js（优先尝试）**

```bash
node <skill>/scripts/start-research.js /tmp/gemini-deep-research/<task-dir>/
```

Parse stdout JSON for `{ status: "started", researchId: "v1_..." }`. If `status: "error"`, inform the user and abort.

**⚠️ 已知问题：start-research.js 可能超时（MCP server 60s timeout bug）**

如果方法 A 失败，使用 **方法 B（Shell Pipe 直连 MCP）**，这是经过验证可用的方式：

```bash
export GEMINI_DEEP_RESEARCH_API_KEY=$(cat ~/.gemini/extensions/gemini-deep-research/.env | grep API_KEY | cut -d= -f2)
TASK_DIR="/tmp/gemini-deep-research/<task-dir>"
TOPIC=$(python3 -c "import json; print(json.load(open('$TASK_DIR/task.json'))['input'])")

# 直接通过 shell pipe 与 MCP server 交互
(echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"gemini-dr","version":"1.0"}}}'
 sleep 1
 echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"research_start\",\"arguments\":{\"input\":\"$TOPIC\",\"report_format\":\"Comprehensive Research Report\"}}}"
) | timeout 120 node ~/.gemini/extensions/gemini-deep-research/dist/index.js 2>/dev/null | grep -v "MCP server running" | tail -1 > "$TASK_DIR/start-output.json"

# 提取 research ID
python3 -c "
import json
data = json.load(open('$TASK_DIR/start-output.json'))
text = data['result']['content'][0]['text']
# 提取 ID
import re
match = re.search(r'ID:\s*(v1_[a-zA-Z0-9]+)', text)
if match:
    task = json.load(open('$TASK_DIR/task.json'))
    task['researchId'] = match.group(1)
    json.dump(task, open('$TASK_DIR/task.json','w'), indent=2)
    print(f'Research ID: {match.group(1)}')
else:
    print(f'Failed to extract ID from: {text[:200]}')
"
```

### Step 4 — Write Background Poll Script

**⚠️ 使用 Shell Pipe 方式（经过验证可用）**

Write `<task-dir>/poll.sh`:

```bash
#!/bin/bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$TASK_DIR"

[[ -f done.flag ]] && echo "Already complete." && exit 0

RESEARCH_ID=$(python3 -c "import json; print(json.load(open('task.json'))['researchId'])")
OUTPUT_PATH=$(python3 -c "import json; print(json.load(open('task.json'))['outputPath'])")
GEMINI_EXT="$HOME/.gemini/extensions/gemini-deep-research"
CHAT_ID="INJECT_CHAT_ID"  # ← Agent: replace with current Discord channel ID (from inbound_meta.chat_id)

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a poll.log; }

# Direct message to user — no agent processing, used for errors/timeouts
notify_user() {
  local message="$1"
  openclaw message send --channel discord --target "$CHAT_ID" -m "$message" 2>/dev/null || log "WARNING: notification failed"
}

# Trigger agent to execute next workflow step — used on success for skill chaining
trigger_agent() {
  local message="$1"
  openclaw agent --channel discord --message "$message" --deliver --timeout 600 2>/dev/null || {
    log "WARNING: agent trigger failed, falling back to direct message"
    notify_user "$message"
  }
}

# 使用 shell pipe 方式调用 MCP（避免 Node spawn 超时问题）
poll_status() {
  (echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"poll","version":"1.0"}}}'
   sleep 0.5
   echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"research_status\",\"arguments\":{\"id\":\"$RESEARCH_ID\"}}}"
  ) | timeout 60 node "$GEMINI_EXT/dist/index.js" 2>/dev/null | grep -v "MCP server running" | tail -1
}

POLL_COUNT=0
MAX_POLLS=8
INTERVAL=300

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))
  [[ $POLL_COUNT -gt $MAX_POLLS ]] && { log "TIMEOUT"; notify_user "❌ Deep Research 超时。"; exit 1; }

  log "[Poll $POLL_COUNT/$MAX_POLLS] Checking status..."
  RESULT=$(poll_status) || true
  echo "$RESULT" >> poll.log

  # 解析 status 和 report
  STATUS=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    text = d['result']['content'][0]['text']
    obj = json.loads(text)
    print(obj.get('status', 'unknown'))
except: print('parse_error')" 2>/dev/null)

  log "Status: $STATUS"

  if [[ "$STATUS" == "completed" ]]; then
    log "Completed! Extracting report..."
    # 从完整 response 中提取报告文本
    echo "$RESULT" | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
text = d['result']['content'][0]['text']
obj = json.loads(text)
report = obj.get('outputs', [{}])[0].get('text', '')
if report:
    with open('$OUTPUT_PATH', 'w') as f: f.write(report)
    print(f'Saved: {len(report)} chars')
else:
    print('No report found')
" >> poll.log 2>&1

    if [[ -s "$OUTPUT_PATH" ]]; then
      SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
      log "Report saved: $OUTPUT_PATH ($SIZE)"
      touch done.flag
      notify_user "✅ Deep Research 完成！报告已保存（$SIZE），共 $POLL_COUNT 轮。"
      # Trigger agent to chain the next workflow step (e.g., NotebookLM)
      # Pass all parameters the downstream skill needs
      TOPIC=$(python3 -c "import json; print(json.load(open('task.json'))['input'])" 2>/dev/null || echo "Deep Research")
      trigger_agent "✅ Deep Research 完成。请启动 NotebookLM 工作流，参数如下：
- 报告路径：$OUTPUT_PATH
- Notebook 名称：$TOPIC
- 产出类型：Audio Overview (播客)
- 格式：deep_dive
- 长度：default
- 语言：zh-CN
请创建 notebook、上传报告、生成播客。"
    else
      log "WARNING: Output file empty or missing"
      notify_user "⚠️ Deep Research 完成但报告保存失败。请手动检查。"
    fi
    exit 0
  fi

  [[ "$STATUS" == "failed" ]] && { log "Failed"; notify_user "❌ Deep Research 失败。"; exit 1; }

  log "Still in_progress. Sleeping ${INTERVAL}s..."
  sleep "$INTERVAL"
done
```

### Step 5 — Launch Background Process

```bash
cd /tmp/gemini-deep-research/<task-dir>/
nohup bash poll.sh > /dev/null 2>&1 &
echo "Background PID: $!"
```

### Step 6 — Notify User

> "🔬 Deep Research 已启动\n\n主题：[topic]\n格式：[format]\n预计完成：2–15 分钟（视主题复杂度而定）\n\n轮询后台运行，完成后我会通知您。如超时（40 分钟）未完成，我会告知并提供手动检查方法。"

### Step 7 — Completion

When the user asks "is it done?" or when notified by a new session:

```bash
# Check done.flag or task.json status
cat /tmp/gemini-deep-research/<task-dir>/task.json
```

**On success:**
> "✅ Deep Research 完成！\n\n主题：[topic]\n报告：[outputPath]\n轮询次数：N\n\n已保存到 ObsidianVault，可在 `DeepResearch/` 目录找到。"

**On timeout:**
> "⏰ Deep Research 超时\n\n主题：[topic]\nResearch ID：`v1_...`\n\n该 ID 在 Google 侧仍可能已完成。可手动保存：\n\`\`\`bash\nnode <skill>/scripts/save-report.js /tmp/gemini-deep-research/<task-dir>/\n\`\`\`\n\n或前往 https://notebooklm.google.com/ 查看。"

**On failure:**
> "❌ Deep Research 失败\n\n原因：[error message]\n\n请检查 API Key 配置（`gemini extensions config gemini-deep-research`）或查询 [references/setup-guide.md](references/setup-guide.md)。"

---

## Report Formats

| Format | Description |
|--------|-------------|
| `Comprehensive Research Report` | Full multi-section report with analysis and citations (default) |
| `Executive Brief` | Condensed summary for decision-makers |
| `Technical Deep Dive` | Detailed technical analysis |

---

## File Naming

Default pattern: `YYYYMMDD-<slug>.md`

- `YYYYMMDD` = today's date
- `<slug>` = lowercase, spaces→hyphens, strip special chars
- Example: `20260325-iran-hormuz-strait-market-impact.md`

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|-----------|
| `API key not found` | Key not configured | Guide to `references/setup-guide.md` step 4 |
| `429 Too Many Requests` | Free-tier key / quota exceeded | Requires paid key |
| Research timed out | Took > 40 min | Check `task.json`, manually save if completed server-side |
| MCP server spawn failed | Extension path wrong | Verify `~/.gemini/extensions/gemini-deep-research/` exists |

---

## Temp Directory Structure

```
/tmp/gemini-deep-research/
  <YYMMDD-HHmm>_<topic>/
    task.json       ← task parameters + research ID
    progress.json    ← poll count, last poll time
    poll.log        ← each poll attempt log (包含完整 MCP response)
    error.log       ← errors
    done.flag       ← created on success
    <report>.md     ← saved report
```

---

## Lessons Learned (2026-03-27)

### 已知问题与解决方案

1. **`start-research.js` MCP 超时**：脚本中 `sendCommand` 的超时设为 60s，初始化时 MCP server 启动可能超过 60s。**解决方案**：使用 Shell Pipe 方式（Step 3 方法 B），直接 `(echo init; sleep 1; echo tool_call) | timeout 120 node dist/index.js`。

2. **报告提取失败**：`outputs[0].text` 是正确的 JSON 路径，但完整的 MCP response 包含 escaped newlines，导致简单的 grep 匹配失败。**解决方案**：将完整 MCP response append 到 `poll.log`，然后用 Python `json.loads` 逐行解析。

3. **API Key 需要显式导出**：脚本运行时可能没有 `.env` 中的 `GEMINI_DEEP_RESEARCH_API_KEY`。**解决方案**：在脚本中显式 `export` 或通过 `.env` 文件读取。

4. **MCP server via Node spawn 不稳定**：在子进程中 spawn MCP server 有时会 hang。Shell pipe 方式更可靠，因为 stdin/stdout 直接对接。
