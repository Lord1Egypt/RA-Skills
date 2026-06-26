# LoongFlow Engine Mode

Follow these instructions to set up and run the LoongFlow evolutionary optimization engine.

**Model format:** Model names must use the `anthropic/` prefix (e.g., `anthropic/claude-sonnet-4-20250514`, `anthropic/deepseek-v3.2`). The actual model can be any model accessible via the configured endpoint. Requires `ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL`.

## Step 1: Check Prerequisites and Install

### 确定当前 Workspace 路径

**关键**：skill 可能安装在任意 workspace，必须动态确定当前 workspace，而不是总用 main。

> ⚠️ 注意：以下 bash 代码块是**示意伪代码**，`$0` 在 agent 执行时无效（agent 不是 shell 脚本）。
> **实际执行时，agent 应直接用 Python 查询 openclaw.json 确定 workspace**，不要照搬 `$0` 那行。

```bash
# 示意：SKILL.md 在 <workspace>/skills/loongflow/SKILL.md，向上两级即 workspace
# 实际执行时请改用下方 Python fallback，不要使用 $0

# fallback（推荐）：从 openclaw.json 查当前 agent 的 workspace
CURRENT_WORKSPACE=$(python3 -c "
import json, os
d = json.load(open('/root/.openclaw/openclaw.json'))
agents = d.get('agents', {}).get('list', [])
agent_id = os.environ.get('OPENCLAW_AGENT_ID', '')
hit = next((a for a in agents if a.get('id') == agent_id), None)
defaults = d.get('agents', {}).get('defaults', {})
print((hit or {}).get('workspace') or defaults.get('workspace', '/root/.openclaw/workspace'))
" 2>/dev/null || echo "/root/.openclaw/workspace")

LOONGFLOW_DIR="$CURRENT_WORKSPACE/.loongflow/engine"
echo "CURRENT_WORKSPACE: $CURRENT_WORKSPACE"
echo "LOONGFLOW_DIR: $LOONGFLOW_DIR"
```

### Quick check: already installed?

If `.loongflow/engine/.venv` exists and loongflow is importable, skip to Step 2:

```bash
if [ -d "$LOONGFLOW_DIR/.venv" ]; then
    "$LOONGFLOW_DIR/.venv/bin/python" -c "import loongflow; print('loongflow ok')" 2>/dev/null && echo "READY"
fi
```

If output is `loongflow ok` / `READY`, **skip directly to Step 2 (Configure the Task)**.

### Fresh install

Only run this if `.loongflow/engine/.venv` does NOT exist or loongflow is not importable:

1. **ANTHROPIC_API_KEY** is set:
   ```bash
   echo $ANTHROPIC_API_KEY | head -c 10
   ```
   If empty, tell the user:
   > LoongFlow requires an API key. Please set it:
   > `export ANTHROPIC_API_KEY="your-key-here"`

2. **ANTHROPIC_BASE_URL** is set:
   ```bash
   echo $ANTHROPIC_BASE_URL
   ```
   If empty, tell the user:
   > LoongFlow requires a base URL for the API endpoint. Please set it:
   > `export ANTHROPIC_BASE_URL="https://api.anthropic.com"` (or your custom endpoint)

3. **网络可达性检查**（百度内网环境）：
   ```bash
   curl -s --connect-timeout 5 https://github.com -o /dev/null -w "%{http_code}" || echo "UNREACHABLE"
   ```
   If unreachable, tell the user:
   > 当前环境无法访问 GitHub，请确认是否有内网镜像地址，或手动下载 LoongFlow 到 `$LOONGFLOW_DIR`。

4. **Download and install:**

```bash
# Clone if not already present
if [ ! -d "$LOONGFLOW_DIR" ]; then
    git clone https://github.com/baidu-baige/LoongFlow "$LOONGFLOW_DIR"
fi

cd "$LOONGFLOW_DIR"
git pull origin main

# Prefer uv (handles Python version automatically), fall back to pip
# NOTE: Do NOT use `source .venv/bin/activate` — use full paths to avoid shell compatibility issues
if command -v uv &> /dev/null; then
    uv venv .venv --python 3.12
    uv pip install -e . --python .venv/bin/python
else
    python3.12 -m venv .venv || python3 -m venv .venv
    .venv/bin/pip install -e .
fi

# Verify
.venv/bin/python -c "import loongflow; print('loongflow ok')"
```

**Note:** `uv venv --python 3.12` will automatically download Python 3.12 if not available on the system. This is the preferred approach.

## Step 2: Configure the Task

Create a task directory under `agents/general_agent/examples/` inside the engine dir:

```bash
TASK_SLUG="<task-slug>"  # kebab-case name from user's task
TASK_DIR="$LOONGFLOW_DIR/agents/general_agent/examples/$TASK_SLUG"
mkdir -p "$TASK_DIR"
```

### Generate task_config.yaml

Adapt the following template based on the user's task. Key fields to customize:
- `evolve.task`: The user's detailed task description
- `evolve.max_iterations`: Higher for harder problems (default: 50)
- `evolve.target_score`: The target quality threshold (default: 0.9)
- `evolve.evaluator.timeout`: Longer for complex evaluations (default: 600s)

```yaml
# workspace_path is relative to the engine dir (.loongflow/engine/)
workspace_path: "agents/general_agent/examples/<task-slug>/output"

llm_config:
  model: "anthropic/deepseek-v3.2"    # Must use anthropic/ prefix. Any model name after the slash.
  # url and api_key can also be set via ANTHROPIC_BASE_URL and ANTHROPIC_API_KEY env vars
  # url: "https://api.anthropic.com"
  # api_key: "your-key"

planners:
  general_planner:
    permission_mode: "acceptEdits"
    max_turns: 100

executors:
  general_executor:
    permission_mode: "acceptEdits"
    max_turns: 100

summarizers:
  general_summarizer:
    permission_mode: "acceptEdits"
    max_turns: 100

evolve:
  task: |
    <INSERT USER'S TASK DESCRIPTION HERE>
  planner_name: "general_planner"
  executor_name: "general_executor"
  summary_name: "general_summarizer"
  max_iterations: 100
  target_score: 1.0
  concurrency: 1
  evaluator:
    timeout: 1800
    agent:
      permission_mode: "acceptEdits"
      max_turns: 100
  database:
    storage_type: "in_memory"
    num_islands: 1
    population_size: 50
    checkpoint_interval: 5
    sampling_weight_power: 2
```

### Copy User Files

If the user has source code, data files, or evaluation scripts relevant to the task, copy them into the task directory:

```bash
# Copy user's files if provided
cp -r <user-files> "$TASK_DIR/"
```

If the user provides a custom evaluation script, save it as `eval_program.py` in the task directory. It must implement:

```python
def evaluate(solution_path: str) -> dict:
    return {
        "status": "success",
        "score": 0.0,  # 0.0 to 1.0
        "summary": "Description of evaluation result",
        "metrics": {},
        "artifacts": {}
    }
```

## Step 3: Launch Evolution

```bash
cd "$LOONGFLOW_DIR"
# Use full python path — do NOT use `source .venv/bin/activate`
PYTHONPATH=$PYTHONPATH:./src .venv/bin/python agents/general_agent/general_evolve_agent.py \
  --config "agents/general_agent/examples/$TASK_SLUG/task_config.yaml" \
  > "agents/general_agent/examples/$TASK_SLUG/run.log" 2>&1 &
echo $! > "agents/general_agent/examples/$TASK_SLUG/.run.pid"
echo "Started PID: $(cat agents/general_agent/examples/$TASK_SLUG/.run.pid)"
sleep 3
tail -20 "agents/general_agent/examples/$TASK_SLUG/run.log"
```

Tell the user:
> LoongFlow evolution started in background for task `<task-slug>`.
> PID: `<pid>`, Log: `<log-path>`

## Step 4: 注册任务 + 设置监控

### 注册到 tasks.json

**注意**：路径解析和注册合并在一个 Python 脚本中执行，避免 bash→Python 环境变量跨代码块传递失效的问题。

将以下脚本保存后执行，替换 `<task-slug>` 为实际值：

```python
import json, time, os
from pathlib import Path

# === 路径解析（内联，不依赖外部环境变量）===
try:
    d = json.load(open('/root/.openclaw/openclaw.json'))
    agents = d.get('agents', {}).get('list', [])
    agent_id = os.environ.get('OPENCLAW_AGENT_ID', '')
    hit = next((a for a in agents if a.get('id') == agent_id), None)
    defaults = d.get('agents', {}).get('defaults', {})
    agent_workspace = (hit or {}).get('workspace') or defaults.get('workspace', '/root/.openclaw/workspace')
except Exception:
    agent_workspace = '/root/.openclaw/workspace'

task_slug = "<task-slug>"   # 替换为实际值
loongflow_dir = str(Path(agent_workspace) / '.loongflow' / 'engine')
tasks_json_path = Path(agent_workspace) / '.loongflow' / 'tasks.json'
notify_user = os.environ.get('BAIDU_CC_USERNAME', '') or os.popen('whoami').read().strip()
now_epoch = int(time.time())  # UTC epoch，无时区问题

print(f"agent_workspace: {agent_workspace}")
print(f"loongflow_dir: {loongflow_dir}")
print(f"tasks.json: {tasks_json_path}")
print(f"notify_user: {notify_user}")

# === 注册任务 ===
tasks_json_path.parent.mkdir(parents=True, exist_ok=True)
data = json.loads(tasks_json_path.read_text()) if tasks_json_path.exists() else {"tasks": []}

data["tasks"].append({
    "id": task_slug,
    "name": task_slug,
    "mode": "engine",
    "status": "running",
    "agentWorkspace": agent_workspace,
    "notifyUser": notify_user,
    "pidFile": f"{loongflow_dir}/agents/general_agent/examples/{task_slug}/.run.pid",
    "logFile": f"{loongflow_dir}/agents/general_agent/examples/{task_slug}/run.log",
    "startedAtEpoch": now_epoch,        # UTC epoch，不依赖时区
    "maxIterations": 50,
    "updatedAtEpoch": now_epoch
})
tasks_json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print(f"Task registered: {task_slug}")
print(f"tasks.json written to: {tasks_json_path}")
```

### 确保监控 Cron 存在

**必须读取 `references/monitoring.md` 并按其指令操作**——cron 命令统一维护在那里，不要在此处内联。

执行步骤：
1. 先检查是否已有 loongflow 监控 cron（命令见 monitoring.md "检查是否已存在" 一节）
2. 若 **FOUND**：跳过，不重复创建
3. 若 **MISSING**：执行 monitoring.md "创建监控 Cron" 一节中的 `openclaw cron add` 命令

> 所有任务共用同一个监控 cron，cron message 包含完整的摘要生成逻辑，每 10 分钟向用户推送有实质内容的进度摘要（分数趋势、本轮策略、关键发现）。

### On Completion

When evolution finishes, report to the user:
- **Best score** achieved
- **Iteration count**: total iterations completed
- **Final solution content** (the regex, code, etc.)

### Stopping a Task

```bash
PID=$(cat "$LOONGFLOW_DIR/agents/general_agent/examples/<task-slug>/.run.pid")
kill $PID
```
