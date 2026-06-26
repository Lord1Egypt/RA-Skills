---
name: openclaw-plus
description: Multi-capability dev skill for chained workflows involving Python execution, package management, git, HTTP requests, file operations, process management, sub-agents, or webhook notifications. Use when the task combines two or more of these — or when any single one requires disciplined error handling.
license: Complete terms in LICENSE.txt
---

# OpenClaw+ 🚀

A modular super-skill for development and automation workflows. Chain capabilities together or use them individually.

## Capabilities

| Capability | Use for |
|---|---|
| `run_python` | Execute Python code or scripts |
| `install_package` | Install pip/system packages |
| `git_status` / `git_commit` | Version control operations |
| `http_request` | Fetch URLs or call APIs (GET, POST, PUT, DELETE) |
| `file_ops` | Read, write, move, copy, delete, diff files |
| `process` | Start, monitor, and stop background processes |
| `sub_agent` | Delegate tasks to a spawned agent |
| `notify` | Send webhook notifications (Slack, Discord, ntfy, custom) |

---

## Core Capabilities

### 1. Python Execution (`run_python`)

```python
# Simple execution
run_python("print('Hello, world!')")

# Multi-line with packages
run_python("""
import pandas as pd
df = pd.read_csv('data.csv')
print(df.describe())
""")
```

**Notes:**
- Use absolute paths for files
- For scripts >50 lines, write to a `.py` file first then execute
- Capture both stdout and stderr

---

### 2. Package Installation (`install_package`)

```bash
install_package("pandas")                    # single
install_package("numpy==1.24.0")             # pinned version
install_package("requests beautifulsoup4")   # multiple
install_package("-r requirements.txt")       # from file
```

**Implementation:** `pip install <package> --break-system-packages`

Always check if a package is already installed before installing. Handle version conflicts explicitly.

---

### 3. Git Operations (`git_status`, `git_commit`)

```bash
git_status()                                         # check current state
git_status("/path/to/repo")                          # specific directory
git_commit("feat: add data pipeline")                # commit staged files
git_commit("fix: resolve parsing error", stage_all=True)  # stage all + commit
```

**Conventional commit types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Keep first line under 50 characters. Always run `git_status()` before committing. Configure `user.email` and `user.name` if git commit fails with identity errors.

---

### 4. HTTP Requests (`http_request`)

Unified capability for both URL fetching and API calls.

```python
# GET request
data = http_request("https://api.example.com/users")

# POST with JSON body
result = http_request(
    "https://api.example.com/create",
    method="POST",
    json={"name": "Alice", "role": "admin"}
)

# With authentication
data = http_request(
    "https://api.example.com/protected",
    headers={"Authorization": "Bearer TOKEN"}
)

# GraphQL
result = http_request(
    "https://api.example.com/graphql",
    method="POST",
    json={"query": "{ users { id name } }"}
)
```

**Notes:**
- Default timeout: 30s — always set explicitly for slow endpoints
- Call `response.raise_for_status()` before parsing
- Handle rate limiting with exponential backoff for retries

---

### 5. File Operations (`file_ops`)

Read, write, move, copy, delete, and diff files without shelling out manually.

```python
# Read
content = file_ops("read", "data/report.txt")
data = file_ops("read", "config.json", parse_json=True)

# Write
file_ops("write", "output/results.txt", content="Analysis complete.")
file_ops("write", "data/config.json", content={"key": "value"}, as_json=True)

# Append
file_ops("append", "logs/run.log", content="[2026-05-28] Step complete\n")

# Copy / Move
file_ops("copy", "report.txt", dest="archive/report_v1.txt")
file_ops("move", "temp_output.csv", dest="final/output.csv")

# Delete
file_ops("delete", "temp/scratch.txt")
file_ops("delete", "temp/", recursive=True)  # delete directory

# Diff
diff = file_ops("diff", "old_config.json", "new_config.json")

# List directory
entries = file_ops("list", "data/", pattern="*.csv")
```

**Best practices:**
- Always check if a file exists before reading or deleting
- Use absolute paths in scripts to avoid working-directory surprises
- Prefer `append` over `write` for log files to avoid overwriting
- Clean up temp files at the end of workflows

---

### 6. Process Management (`process`)

Start background processes, check their status, tail output, and stop them.

```python
# Start a background process
pid = process("start", "python3 server.py", cwd="/app", capture_output=True)

# Start and get a handle
job = process("start", "npm run build", env={"NODE_ENV": "production"})

# Check status
status = process("status", pid)
# Returns: { "pid": 1234, "running": True, "exit_code": None }

# Tail output
logs = process("logs", pid, lines=50)

# Wait for completion (blocks)
result = process("wait", pid, timeout=120)
# Returns: { "exit_code": 0, "stdout": "...", "stderr": "..." }

# Kill
process("kill", pid)
process("kill", pid, signal="SIGTERM")  # graceful shutdown
```

**Common patterns:**

```python
# Start a server, wait for it to be ready, then run tests
server_pid = process("start", "./start_server.sh")
time.sleep(2)  # brief startup wait

result = process("wait", test_pid, timeout=60)
if result["exit_code"] != 0:
    logs = process("logs", test_pid)
    print(f"Tests failed:\n{logs}")
finally:
    process("kill", server_pid)
```

**Notes:**
- Always kill background processes when done — don't leave orphans
- Use `process("wait", pid, timeout=N)` rather than `time.sleep` for predictable completion
- Check `exit_code` after `wait` — a `0` is success, anything else needs handling
- Redirect stdout/stderr to files for long-running processes

---

### 7. Sub-Agents (`sub_agent`)

Delegate a task to a spawned agent and get the result back. Use when a task is large enough to benefit from parallel work or clean separation of concerns.

```python
# Spawn an agent with a specific task
result = sub_agent(
    task="Analyze the CSV at data/sales.csv and return a JSON summary with total revenue, top 5 products, and monthly breakdown.",
    context={"file": "data/sales.csv"}
)

# Spawn multiple agents in parallel
results = sub_agent(
    tasks=[
        "Summarize the Q1 report at reports/q1.pdf",
        "Summarize the Q2 report at reports/q2.pdf",
        "Summarize the Q3 report at reports/q3.pdf"
    ],
    parallel=True
)

# Agent with specific tools/skills
result = sub_agent(
    task="Generate a bar chart of monthly revenue from data/revenue.json and save it as charts/revenue.png",
    skills=["run_python", "file_ops"]
)
```

**When to use sub-agents:**
- Tasks that can be parallelized (summarizing multiple documents, processing batches)
- Isolating a complex sub-task so failures don't cascade
- Tasks that need a fresh context window (e.g., processing a large file)
- Delegating specialized work (one agent for data, one for formatting)

**When NOT to use sub-agents:**
- Simple sequential steps that take seconds — overhead isn't worth it
- When shared state between steps is required — sub-agents don't share memory
- When you need tight control over each intermediate result

**Notes:**
- Always give the sub-agent a clear, self-contained task — include all context it needs
- Specify expected output format explicitly (e.g., "return JSON with these fields")
- Handle the case where a sub-agent returns an error or unexpected format
- For parallel agents, define how to merge/reconcile their outputs

---

### 8. Webhook Notifications (`notify`)

Send notifications when a workflow step completes, fails, or needs attention.

```python
# Slack
notify(
    "slack",
    webhook_url=os.environ["SLACK_WEBHOOK"],
    message="✅ Data pipeline complete. 4,821 records processed.",
    channel="#data-alerts"
)

# Discord
notify(
    "discord",
    webhook_url=os.environ["DISCORD_WEBHOOK"],
    message="Build failed on main branch.",
    username="OpenClaw Bot",
    embed={
        "title": "Build Failure",
        "description": "Step 3 exited with code 1",
        "color": 0xFF0000
    }
)

# ntfy (self-hosted push notifications)
notify(
    "ntfy",
    topic="my-agent-alerts",
    message="Scraping job finished: 320 products saved.",
    priority="default",
    tags=["white_check_mark"]
)

# Generic webhook (any HTTP endpoint)
notify(
    "webhook",
    url="https://hooks.example.com/alert",
    payload={"event": "pipeline_complete", "records": 4821, "status": "ok"},
    headers={"X-Secret": os.environ["WEBHOOK_SECRET"]}
)
```

**Best practices:**
- Always store webhook URLs in environment variables — never hardcode
- Send notifications at meaningful checkpoints: job start, completion, and on failure
- Include actionable context in the message: what ran, how many records, what failed
- For failure notifications, include the error message and the step that failed
- Use `notify` at the end of long workflows so the user doesn't have to watch

**Failure notification pattern:**
```python
try:
    run_pipeline()
    notify("slack", webhook_url=SLACK_URL, message="✅ Pipeline complete")
except Exception as e:
    notify("slack", webhook_url=SLACK_URL, message=f"❌ Pipeline failed: {e}")
    raise
```

---

## Workflow Patterns

### Data Pipeline with Notification
```python
install_package("pandas requests")
data = http_request("https://api.example.com/dataset")
file_ops("write", "raw_data.json", content=data, as_json=True)
run_python("""
import pandas as pd, json
df = pd.read_json('raw_data.json')
df.dropna().to_csv('clean_data.csv', index=False)
print(f"Processed {len(df)} records")
""")
git_commit("feat: add cleaned dataset", stage_all=True)
notify("slack", webhook_url=os.environ["SLACK_WEBHOOK"], message="✅ Pipeline done")
```

### Parallel Document Processing
```python
# Delegate each document to a sub-agent in parallel
reports = ["q1.pdf", "q2.pdf", "q3.pdf", "q4.pdf"]
summaries = sub_agent(
    tasks=[f"Summarize reports/{r} and return JSON with key_findings and total_revenue" for r in reports],
    parallel=True
)
file_ops("write", "output/annual_summary.json", content=summaries, as_json=True)
notify("slack", webhook_url=os.environ["SLACK_WEBHOOK"], message="Annual summaries ready")
```

### Background Service + Tests
```python
server = process("start", "python3 -m app.server", cwd="/app")
time.sleep(2)
try:
    result = process("wait",
        process("start", "pytest tests/integration/", capture_output=True),
        timeout=120
    )
    status = "✅ All tests passed" if result["exit_code"] == 0 else "❌ Tests failed"
finally:
    process("kill", server)
    notify("slack", webhook_url=os.environ["SLACK_WEBHOOK"], message=status)
```

### File Batch Processing with Sub-Agent
```python
csv_files = file_ops("list", "data/incoming/", pattern="*.csv")
results = sub_agent(
    tasks=[f"Validate and clean data/incoming/{f}, save to data/processed/{f}" for f in csv_files],
    parallel=True,
    skills=["file_ops", "run_python"]
)
file_ops("write", "data/processing_report.json", content=results, as_json=True)
git_commit("chore: process incoming CSV batch", stage_all=True)
```

---

## Error Handling

Always handle errors at each step — don't let a mid-workflow failure leave things in a broken state.

```python
# File operations
if not file_ops("exists", "data/input.csv"):
    raise FileNotFoundError("data/input.csv not found — aborting")

# Process management
result = process("wait", pid, timeout=60)
if result["exit_code"] != 0:
    logs = process("logs", pid)
    notify("slack", webhook_url=SLACK_URL, message=f"❌ Process failed:\n{logs[-500:]}")
    raise RuntimeError(f"Process exited {result['exit_code']}")

# Sub-agent results
for i, result in enumerate(sub_agent_results):
    if result.get("error"):
        print(f"Sub-agent {i} failed: {result['error']}")

# HTTP requests
response = http_request(url)
if response.status_code != 200:
    raise RuntimeError(f"API returned {response.status_code}: {response.text}")

# Git — nothing to commit
status = git_status()
if "nothing to commit" not in status:
    git_commit("chore: update output files", stage_all=True)
```

---

## Security

- **Credentials:** Always use environment variables. Never hardcode API keys, tokens, or webhook URLs.
- **File paths:** Validate paths before file operations. Don't allow user input to construct paths directly.
- **Processes:** Avoid passing unsanitized user input to `process("start", ...)`.
- **Sub-agents:** Don't pass secrets in the task string — inject them via environment variables instead.
- **Webhooks:** Use HTTPS endpoints only. Validate with a shared secret where the service supports it.

---

## Quick Reference

```python
run_python(code)
install_package("name" or "-r requirements.txt")
git_status() / git_commit("message", stage_all=True)
http_request(url, method="GET", json={}, headers={})
file_ops("read|write|append|copy|move|delete|diff|list|exists", path, ...)
process("start|status|logs|wait|kill", pid_or_cmd, ...)
sub_agent(task="...", parallel=False, skills=[...])
notify("slack|discord|ntfy|webhook", webhook_url="...", message="...")
```
