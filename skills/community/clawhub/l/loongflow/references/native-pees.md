# Native PEES Mode（异步 Subagent）

Native PEES 以异步方式运行——将任务交给独立 subagent 执行，主 session 立刻释放，不阻塞对话。

## Step 1: 准备工作区

在主 session 中创建工作区目录和初始文件：

```
.loongflow/<task-slug>-<YYYYMMDD-HHMMSS>/
├── index.md       # 迭代索引，subagent 读写
├── task.md        # 任务描述和成功标准
├── iteration_1/   # 每轮迭代目录（由 subagent 创建）
│   ├── plan.md
│   ├── execute.md
│   ├── evaluate.md
│   └── summary.md
└── result.md      # 最终结果（subagent 写入）
```

- `<task-slug>`：从任务描述派生的 kebab-case 短名
- `<YYYYMMDD-HHMMSS>`：创建时间戳

## Step 2: 写入 task.md 和 index.md

**task.md** 写入任务描述和成功标准。如果用户提供了明确标准则直接使用，否则从任务描述推导并确认。

**index.md** 初始内容：

```markdown
# PEES Evolution Index

## Task
<task description>

## Success Criteria
<criteria>

## Target Score
<0.0–1.0>

## Iterations
(none yet)
```

## Step 3: 注册任务到 tasks.json

**注意**：路径解析和注册合并在一个 Python 脚本中执行，避免 bash→Python 环境变量跨代码块传递失效的问题。

将以下内容保存为临时脚本并执行，替换 `<task-slug>` 和 `<YYYYMMDD-HHMMSS>` 为实际值：

```python
import json, time, os
from pathlib import Path

# === 路径解析（内联，不依赖外部环境变量）===
# 从 openclaw.json 查当前 agent 的 workspace
try:
    d = json.load(open('/root/.openclaw/openclaw.json'))
    agents = d.get('agents', {}).get('list', [])
    agent_id = os.environ.get('OPENCLAW_AGENT_ID', '')
    hit = next((a for a in agents if a.get('id') == agent_id), None)
    defaults = d.get('agents', {}).get('defaults', {})
    agent_workspace = (hit or {}).get('workspace') or defaults.get('workspace', '/root/.openclaw/workspace')
except Exception:
    agent_workspace = '/root/.openclaw/workspace'

tasks_json_path = Path(agent_workspace) / '.loongflow' / 'tasks.json'
notify_user = os.environ.get('BAIDU_CC_USERNAME', '') or os.popen('whoami').read().strip()
now_epoch = int(time.time())  # UTC epoch，无时区问题

print(f"agent_workspace: {agent_workspace}")
print(f"tasks.json: {tasks_json_path}")
print(f"notify_user: {notify_user}")

# === 注册任务 ===
task_id = "<task-slug>-<YYYYMMDD-HHMMSS>"   # 替换为实际值
task_dir = Path(agent_workspace) / '.loongflow' / task_id

tasks_json_path.parent.mkdir(parents=True, exist_ok=True)
data = json.loads(tasks_json_path.read_text()) if tasks_json_path.exists() else {"tasks": []}

data["tasks"].append({
    "id": task_id,
    "name": "<task-slug>",              # 替换为实际值
    "mode": "native",
    "status": "running",
    "taskDir": str(task_dir),           # 任务迭代目录（.loongflow/<task-id>/）
    "agentWorkspace": agent_workspace,  # agent workspace 根目录（用于定位 tasks.json）
    "notifyUser": notify_user,
    "startedAtEpoch": now_epoch,        # UTC epoch，不依赖时区
    "currentIteration": 0,
    "maxIterations": 5,
    "bestScore": 0,
    "updatedAtEpoch": now_epoch
})
tasks_json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print(f"Task registered: {task_id}")
print(f"tasks.json written to: {tasks_json_path}")
```

> **说明**：`taskDir`（任务迭代目录，存放 iteration_N/ 等文件）和 `agentWorkspace`（workspace 根目录，用于定位 tasks.json）是两个不同概念，不要混淆。无论 skill 安装在哪个 workspace，tasks.json 始终写在对应 workspace 下，不跨 workspace 混用。

## Step 4: 启动 Subagent

用 `sessions_spawn` 启动一个 subagent，传入完整的 PEES 执行指令：

```
sessions_spawn:
  runtime: "subagent"
  mode: "run"
  label: "pees-<task-slug>"
  task: |
    你是一个 PEES 迭代优化 agent。执行以下任务，完成后通过 infoflow_send 通知用户。

    任务目录（迭代文件存放处）：<task-dir>（即 <agent-workspace>/.loongflow/<task-id>/，绝对路径）
    Agent Workspace 根目录：<agent-workspace>（用于定位 tasks.json）
    tasks.json 路径：<agent-workspace>/.loongflow/tasks.json
    任务 ID：<task-id>
    通知用户：<notify-user>（从 tasks.json 该任务的 notifyUser 字段读取，fallback: $BAIDU_CC_USERNAME）

    ## 你的任务
    <完整任务描述，从 task.md 内容复制>

    ## 成功标准
    <成功标准>

    ## 目标分数
    <target-score>

    ## PEES 执行规则

    最多执行 5 轮迭代。每轮：

    ### Plan
    1. 读 <task-dir>/index.md，回顾已有迭代和分数
    2. 写 <task-dir>/iteration_N/plan.md：本轮策略、与上轮的区别、具体行动计划

    ### Execute
    1. 用工具实现计划（读写文件、运行命令）
    2. 写 <task-dir>/iteration_N/execute.md：记录所有操作和结果

    ### Evaluate
    1. 测试结果，打分 0.0–1.0
    2. 写 <task-dir>/iteration_N/evaluate.md：测试证据、分数、状态（pass/partial/fail）

    ### Summary
    1. 分析本轮得失，提取下轮关键 insight
    2. 写 <task-dir>/iteration_N/summary.md：结论、insight、决策（done/iterate/escalate）

    ### 更新 index.md
    每轮结束后追加：
    ```
    ## Iteration N
    - Plan: <一句话>
    - Score: 0.XX
    - Status: pass/partial/fail
    - Insight: <关键 insight>
    ```

    ### 更新 tasks.json
    每轮结束后用 UTC epoch 更新字段（`import time; int(time.time())`）：
    - `currentIteration`
    - `bestScore`
    - `updatedAtEpoch`（UTC epoch，不要用本地时间字符串）

    ## 终止条件
    - **成功**：分数 >= 目标分 → 写 result.md，标记任务 status=done
    - **达到上限**：5 轮后写 result.md，记录最佳结果，status=done
    - **连续 3 轮无提升**：记录每轮 bestScore，若最近 3 轮提升均 < 0.05，写 result.md（status=escalate），建议用户切换 Engine 模式，status=done

    ## result.md 格式
    ```markdown
    # Result
    - Final Score: 0.XX
    - Status: success / partial / escalate
    - Best Iteration: N
    - Total Iterations: N
    - Summary: <结果摘要>
    - Solution: <最终方案或文件路径>
    ```

    ## 完成后通知用户
    任务完成后：
    1. 更新 tasks.json 中 status=done，updatedAtEpoch=当前 UTC epoch
    2. 从 tasks.json 该任务的 notifyUser 字段读取收件人（fallback: $BAIDU_CC_USERNAME）
    3. 用 infoflow_send 发消息给该用户：
       ```
       ✅ PEES 任务完成｜<task-slug>｜最终分: 0.XX｜迭代: N/5
       <result.md 中的 Solution 内容>
       ```
```

启动后立刻告知用户：
> 任务 `<task-slug>` 已在后台启动，完成后会通知你。你可以继续聊其他的。

## Step 5: 确保监控 Cron 存在

**必须读取 `references/monitoring.md` 并按其指令操作**——cron 命令统一维护在那里，不要在此处内联。

执行步骤：
1. 先检查是否已有 loongflow 监控 cron（命令见 monitoring.md "检查是否已存在" 一节）
2. 若 **FOUND**：跳过，不重复创建
3. 若 **MISSING**：执行 monitoring.md "创建监控 Cron" 一节中的 `openclaw cron add` 命令

> 所有任务共用同一个监控 cron，cron message 包含完整的摘要生成逻辑，每 10 分钟向用户推送有实质内容的进度摘要（分数趋势、本轮策略、关键发现）。
