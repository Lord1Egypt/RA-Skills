---
name: polling-best-practices
description: Best practices for automating long-running, asynchronous tasks via cron-style polling. Use when the user wants to monitor a background CLI command or API call that does not return an immediate result — such as waiting for a report to generate, a podcast to be created, a deep research job to complete, or any task with a clear completion condition. Triggers on requests like "monitor X until done", "poll for Y", "wait for Z to complete in the background", "run X in the background and notify me when ready", "long-running task automation", "async task monitor". This skill is NOT for tasks requiring real-time interaction, complex LLM judgment during execution, or streaming output. It is a guidance-only skill — it does not install scripts or tools; the agent applies these principles manually based on the guidance here. A template polling script is provided in the scripts/ directory for convenience.
---

# Polling Best Practices

A guidance-style skill for automating long-running, asynchronous tasks using a **cron-compatible polling pattern**. When a task cannot complete synchronously (e.g., a CLI command that triggers a background job and returns a job ID), this skill guides the agent through: (1) deciding whether polling is appropriate, (2) pre-flight confirmation with the user, (3) setting up a task directory, (4) writing the polling script, (5) launching the background job, and (6) monitoring it to completion or timeout.

**Language:** All confirmation messages to the user should be written in the user's current session language (check the session language — if the user is writing in Chinese, reply in Chinese; if in English, reply in English).

---

## 1. Suitability Checklist

Before proceeding, the agent must answer:

### ✅ Suitable for Polling — if ALL of the following are true:

- [ ] The target command/API returns **immediately** with a **process ID, job ID, artifact ID, or similar handle**
- [ ] There is a **clear, machine-parseable completion condition** (e.g., a JSON/TOML field, a status string, an exit code, a file appearing)
- [ ] The condition can be **checked by re-running the same command** or a lightweight query command
- [ ] The wait time is **predictable** (typically 1–15 minutes)
- [ ] No **real-time user interaction** is needed during execution

### ❌ NOT Suitable — if ANY of the following are true:

- [ ] The task requires **complex LLM judgment** to determine if it's "done" (e.g., "is this output good enough?")
- [ ] The task requires **streaming or real-time output** to be shown to the user
- [ ] The task outcome **changes during polling** based on intermediate results
- [ ] The completion condition is **ambiguous or subjective**
- [ ] The user wants to **stop or redirect the task mid-execution**

If the task is NOT suitable for polling, inform the user and propose an alternative approach (e.g., run synchronously, use a sub-agent with polling only for the final wait, etc.).

---

## 2. Post-Poll Actions (轮询后行为)

After polling completes (success, failure, or timeout), one or more actions may be needed. **Always define these before writing the poll script.**

### Category A — Notify (通知)

| Action | Command | When to Use |
|--------|---------|-------------|
| **Direct notify user** | `openclaw message send --channel discord --target "$CHAT_ID" -m "msg"` | Failure, timeout, simple completion. No agent processing needed. |
| **Trigger agent** | `openclaw agent --channel discord --message "msg" --deliver --timeout 600` | Success requiring next workflow step. Agent receives instructions and executes downstream skill. |

**Rules:**
- **Failure/timeout** → always `notify_user` (direct). Never trigger agent on failure.
- **Success, no chaining** → `notify_user` (direct). Simple "task done" message.
- **Success, needs chaining** → `trigger_agent` with all parameters the next step needs.

### Category B — Artifact (产物处理)

| Action | Code Pattern | When to Use |
|--------|-------------|-------------|
| **Download** | `nlm download audio $ID --id $ART_ID -o $PATH` | External service generated a file; bring it local. |
| **Verify** | `[[ -s "$output_path" ]]` | Confirm file exists and is non-empty before declaring success. |
| **Move/Copy** | `cp "$temp_path" "$final_path"` | User specified a destination; move from temp to final location. |

### Category C — Cleanup (清理)

| Action | Code Pattern | When to Use |
|--------|-------------|-------------|
| **Keep temp folder** | (default) | For debugging, resume, or manual inspection. |
| **Delete temp folder** | `rm -rf "$TASK_DIR"` | Only if user explicitly requested cleanup. Never auto-delete. |

### Decision Matrix

| Scenario | Notify | Artifact | Cleanup |
|----------|--------|----------|---------|
| Simple task done, no output file | `notify_user` | — | Keep |
| File generated, user wants it | `notify_user` | Verify + Move | Keep |
| Chaining to next skill | `trigger_agent` | — (next skill handles) | Keep |
| Timeout | `notify_user` with error details | — | Keep (for debug) |
| Failure | `notify_user` with error details | — | Keep (for debug) |

---

## 3. Pre-Flight Confirmation (One-Time, All Parameters)

Before starting any polling task, **ask the user to confirm all parameters in a single message**. This avoids back-and-forth and sets clear expectations.

**Confirm in the user's current session language.** Include the post-poll actions in the confirmation.

Example (Chinese):

```
启动前请确认以下参数：

① 轮询对象
  - 任务：[简短描述]
  - 状态查询命令：[具体命令]
  - 成功判定条件：[例如输出包含 "status": "completed"]

② 轮询频率：每 [X] 分钟一次（默认：5 分钟）
③ 最长持续时间：最多 [Y] 次轮询 = [Z] 分钟（默认：40 分钟 / 8 次）

④ 完成后动作：
  - [ ] 通知用户（默认：是）
  - [ ] 下载产物 → 保存到 [路径]
  - [ ] 触发下一步工作流（说明：...）
  - [ ] 清理临时文件夹

⑤ 失败/超时时动作：
  - [ ] 通知用户（默认：是）

直接回复修改项，或"确认"以默认参数启动。
```

**Do not begin polling until the user confirms.** If triggered by an upstream skill (agent mode), skip confirmation and use the parameters from the trigger message.

---

## 4. Temp Folder Structure

Every polling task gets its own temp folder. This makes the task self-contained, resumable, and easy to inspect or clean up later.

```
/tmp/<category>/                          ← category: e.g., notebooklm, deep-research, generic
  <YYMMDD-HHmm>_<sanitized-task-name>/  ← timestamped per-task folder
    task.json          ← task metadata, all parameters, AND post-poll actions
    progress.json      ← current polling state (poll count, last check time, handles)
    poll.log           ← log of every poll attempt (timestamp + result)
    error.log          ← errors encountered
    done.flag          ← empty file, created on successful completion
    <output files>     ← any downloaded/generated artifacts
```

**Naming rules:**
- Category folder: lowercase, hyphenated, descriptive of the task type (e.g., `notebooklm-audio`, `deep-research`, `generic-async`)
- Task subfolder: `YYMMDD-HHmm` + `_` + sanitized task name (spaces→hyphens, max 40 chars, strip special chars)

**If a category folder doesn't exist yet**, create it. If a task subfolder already exists (e.g., from a previous attempt), ask the user: **"Resume the previous task or start fresh?"**

### `task.json` schema

Include post-poll actions in the task config so the script knows what to do on completion:

```json
{
  "category": "notebooklm-audio",
  "task_name": "example-notebook-audio",
  "poll_command": "nlm studio status <notebook_id>",
  "parse_rule": {
    "type": "json",
    "path": ".[0].status",
    "success_value": "completed",
    "failure_value": "failed"
  },
  "on_complete_command": "nlm download audio <notebook_id> --id <artifact_id> -o <output_path>",
  "verify_output": true,
  "poll_interval_seconds": 300,
  "max_polls": 8,
  "output_path": "/path/to/output.m4a",
  "temp_dir": "/tmp/notebooklm-audio/260325-1400_example-audio",
  "created_at": "2026-03-25T22:00:00Z",
  "user_confirmed": true,

  "post_poll": {
    "on_success": {
      "notify_user": true,
      "download": false,
      "download_path": null,
      "trigger_agent": false,
      "agent_message": null
    },
    "on_failure": {
      "notify_user": true
    },
    "on_timeout": {
      "notify_user": true
    }
  }
}
```

### `progress.json` schema

```json
{
  "poll_count": 3,
  "last_poll_at": "2026-03-25T22:15:00Z",
  "last_poll_result": "in_progress",
  "artifact_id": "abc123...",
  "current_handle": "..."
}
```

---

## 5. Writing the Polling Script

Write the script to the task's temp folder (`<temp_dir>/poll.sh`). The script must be **self-contained** — no external dependencies beyond standard Unix tools and the specific CLI tools for the task.

**Required properties:**
- `set -euo pipefail` at the top
- Check for `done.flag` at start — if it exists, exit 0 immediately (already done)
- On any error (auth expired, command failed, timeout), **log to `error.log`** and save progress before exiting
- Save `progress.json` after every poll attempt
- Append every poll result to `poll.log` (timestamp + truncated output)
- **Never delete the temp folder** — the user decides when to clean up
- `CHAT_ID` must be injected by the agent at script generation time

### Script Template

```bash
#!/bin/bash
set -euo pipefail

# ─── Config ────────────────────────────────────────────────────────────────
TASK_DIR="/tmp/category/YYMMDD-HHmm_taskname"
cd "$TASK_DIR"

[[ -f done.flag ]] && echo "Already complete." && exit 0

CHAT_ID="INJECT_CHAT_ID"  # ← Agent: replace with Discord channel ID
POLL_COUNT=$(grep '"poll_count"' progress.json 2>/dev/null | sed 's/[^0-9]//g') || POLL_COUNT=0
MAX_POLLS=8
INTERVAL=300

# ─── Helpers ───────────────────────────────────────────────────────────────

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a poll.log; }

notify_user() {
  local message="$1"
  openclaw message send --channel discord --target "$CHAT_ID" -m "$message" 2>/dev/null || log "WARNING: notification failed"
}

trigger_agent() {
  local message="$1"
  openclaw agent --channel discord --message "$message" --deliver --timeout 600 2>/dev/null || {
    log "WARNING: agent trigger failed, falling back to direct message"
    notify_user "$message"
  }
}

# ─── Main Loop ─────────────────────────────────────────────────────────────

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))

  if [[ $POLL_COUNT -gt $MAX_POLLS ]]; then
    echo "[$(date)] TIMEOUT after $MAX_POLLS polls" >> error.log
    notify_user "❌ 任务超时（已达最大轮询次数 $MAX_POLLS）。"
    exit 1
  fi

  log "[Poll $POLL_COUNT/$MAX_POLLS] Checking..."
  RESULT=$(<your_poll_command> 2>&1) || true
  echo "$RESULT" >> poll.log

  # Parse status — adapt to your command's output
  STATUS=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('status', 'unknown'))
except: print('parse_error')
" 2>/dev/null)

  log "Status: $STATUS"

  # ── Success ──────────────────────────────────────────────────────────────
  if [[ "$STATUS" == "completed" ]]; then
    touch done.flag

    # (B1) Download artifact if needed
    # <your_download_command> >> poll.log 2>&1 || true

    # (B2) Verify output if needed
    # [[ -s "$OUTPUT_PATH" ]] || { notify_user "⚠️ 产物文件为空"; exit 1; }

    # (A) Notify
    notify_user "✅ 任务完成！共 $POLL_COUNT 轮轮询。"

    # (A) Trigger agent for chaining (uncomment if needed)
    # trigger_agent "✅ 任务完成。产物已就绪。请启动下一步：..."

    log "Done."
    exit 0
  fi

  # ── Failure ──────────────────────────────────────────────────────────────
  if [[ "$STATUS" == "failed" ]]; then
    echo "[$(date)] FAILED" >> error.log
    notify_user "❌ 任务失败。"
    exit 1
  fi

  # ── Still in progress ────────────────────────────────────────────────────
  sed -i "s/\"poll_count\": [0-9]*/\"poll_count\": $POLL_COUNT/" progress.json
  log "Still in_progress. Sleeping ${INTERVAL}s..."
  sleep "$INTERVAL"
done
```

---

## 6. Launching and Monitoring

### Start the background job

1. First, run the **trigger command** (e.g., `nlm audio create <notebook_id>`) to start the background task and capture its ID/handle.
2. Save the returned ID to `progress.json` and `task.json`.
3. Then launch the polling script as a background process.

```bash
# In the task's temp dir:
nohup bash poll.sh > /dev/null 2>&1 &
echo "Polling started in background (PID: $!)"
```

**The polling script should outlive the OpenClaw session.** The agent should not need to stay alive for polling to continue.

### Monitoring strategy

- **Do not poll from within the OpenClaw session** (sub-agents or exec loops waste resources and complicate recovery).
- If OpenClaw receives a user message asking "is it done yet?", the agent can check `done.flag` or `poll.log` in the temp folder to answer without starting a new poll.
- If a new session starts and the user asks to check on a task, read `progress.json` to determine current status.

---

## 7. Timeout and Error Handling

| Situation | Action |
|-----------|--------|
| Max polls reached (timeout) | Log to `error.log`, notify user with details, do NOT delete temp folder |
| Auth expired | Log to `error.log`, notify user to re-authenticate, exit |
| Download/generation failed | Log to `error.log`, notify user, exit |
| Temp folder already exists (duplicate start) | Ask user: resume or restart |

**After timeout/failure:** Do not auto-retry. Tell the user the task did not complete and present options:
1. Re-run with the same parameters
2. Adjust parameters and re-run
3. Clean up the temp folder

---

## 8. Template-Ready Tasks (Frequent Patterns)

If the same type of task is performed frequently (e.g., NotebookLM audio generation, Gemini Deep Research status checks), extract the polling logic into a **reusable script template** stored in a category-level folder:

```
/tmp/notebooklm-audio/
  poll-template.sh        ← reusable template for this category
  /260325-1400_task1/    ← individual task folders use the template
  /260326-0915_task2/
```

The per-task `poll.sh` either copies from the template or is generated from it, keeping the per-task folder minimal.

---

## 9. Summary Checklist

Before launching a polling task, confirm ALL of:

- [ ] Task is suitable for polling (all suitability ✅)
- [ ] User confirmed all parameters in one message (or triggered by upstream skill)
- [ ] Post-poll actions defined: notify, download, trigger_agent, cleanup
- [ ] Temp folder created with correct `task.json` and `progress.json`
- [ ] Trigger command run, ID/handle captured
- [ ] `CHAT_ID` injected into poll script
- [ ] `poll.sh` written and tested for syntax (`bash -n`)
- [ ] Background process started with `nohup`
- [ ] User informed: task started, how to check status, what happens on completion
