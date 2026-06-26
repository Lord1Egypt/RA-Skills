---
name: project-factory
description: >
  Bootstrap a new OpenClaw automation project using a four-phase workflow:
  Phase 0 — LLM reasoning: infer project type, flowchart structure, and node draft from a plain-language description,
  Phase 1 — confirm or edit the flowchart from Phase 0,
  Phase 2 — configure each node (skill, cron, credentials),
  Phase 3 — generate the full project scaffold in one pass.
  Phase 0 model is configurable: defaults to MiniMax-M2.5 (FAST), upgrade to GPT-4.1 (SMART) for complex projects.
  Use when the user says "创建新项目", "new project", "新建项目", "项目初始化",
  "设计一个新流程", "帮我画个流程", or asks to automate a new workflow.
  Triggers whenever a new project, new automation, or new content pipeline is discussed.
---

# Project Scaffold Skill v2

## Core Philosophy

**Flow first, scaffold second.** Before touching any technical parameter, the project must be understood as a process. The flowchart is the source of truth — all config (cron, skills, routing, state files) is derived from it.

---

## How It Works — Four Phases

```
用户触发 → 阶段零：LLM推理 → 阶段一：确认流程图 → 阶段二：节点配置 → 阶段三：技术初始化 → 生成项目
```

---

## Phase 0: LLM Reasoning (Automatic)

Triggered as soon as the user describes a project in plain language.

### Step 0.1 — Infer Project Structure

Synthesize a project structure from the user's plain-language description using the LLM's own reasoning, guided by the flow_design_language node vocabulary.

**Model selection:**
- Default: `MiniMax-M2.5` (FAST tier, cost-efficient)
- Upgrade to `GPT-4.1` (SMART tier) when: the project involves 5+ nodes, multiple conditions/branches, or non-standard sources
- Upgrade to `POWER/MAX` only when the user explicitly requests it or the project involves mission-critical logic

**Reasoning process (not an external API call):**

Phase 0 does not call another model or external API. The LLM synthesizes the structure internally by applying the following reasoning steps to the user's plain-language description:

1. Classify project type (content monitoring / auto-publish / data collection / hybrid)
2. Determine trigger type (cron / event / manual)
3. Map the core flow: which nodes are required from trigger to end
4. Assign a skill recommendation to each node
5. Identify whether conditions or wait nodes are needed

Output fields:
```json
{
  "project_type": "...",
  "trigger_type": "cron | event | manual",
  "flowchart": "<single-line Mermaid, flowchart LR>",
  "nodes": [{"id": "FETCH", "label": "抓取内容", "type": "fetch", "skill": "...", "config": {}}],
  "complexity": "low | medium | high",
  "recommended_model": "minimax | gpt-4.1 | power | max"
}
```

Present the result to the user as a draft:

> **LLM 推理结果**（模型：`MiniMax-M2.5`）
> 项目类型：内容监控
> 推荐流程：trigger → fetch → filter → rewrite → publish → report → end
> 
> ```mermaid
> flowchart LR
>     START([开始]) --> TRIGGER{{定时触发}}
>     ...
> ```
> 
> 模型推荐：`GPT-4.1`（项目较复杂）— 如需调整请说"用 GPT-4.1"或"切换到快速模式"

**Model switch trigger:** if the user's description mentions "复杂"、"高要求"、"多条件"，auto-escalate model to GPT-4.1 and confirm.

### Step 0.2 — User Confirms or Adjusts

The user may:
- Confirm: "没问题，继续"
- Adjust: "把 X 改成 Y" → regenerate with adjusted nodes
- Switch model: "用 GPT-4.1 重来" or "快速模式就够了"
- Skip reasoning: "直接告诉我流程，我自己调整"

Once confirmed → proceed to Phase 1.

**JSON validation sanity check (do not skip):** Before presenting Phase 0 output, verify the `flowchart` Mermaid syntax is valid (all nodes use correct `{{ }}` for conditions, `[ ]` for processes, matching brackets). If malformed, regenerate rather than present broken diagrams to the user.

---

## Phase 1: Design the Flowchart

### Step 1.0 — Model Declaration (from Phase 0)

At the start of Phase 1, state the active model based on Phase 0 output:

> **Phase 1 模型：`GPT-4.1`**（Phase 0 推荐：项目涉及多条件分支）
> 如需切换，请说"切换到 MiniMax"或"用 POWER"

If Phase 0 was skipped, infer model from the confirmed flowchart: low complexity (≤4 nodes, no conditions) → MiniMax-M2.5; medium/higher → GPT-4.1.

### Step 1.1 — Confirm or Edit Flowchart

The Phase 0 LLM reasoning output becomes the starting point. Ask:

> **"以上流程图是否准确？需要调整吗？"**

If the user made no prior description (Phase 0 skipped), fall back to the original Step 1.1: ask "这个项目要自动化什么？最终产出是什么？谁会用到它？"

**Supported node types:**

| Node Type | Meaning | Recommended Skill |
|-----------|---------|-------------------|
| `trigger` | 触发源（定时、手动、事件） | cron / manual |
| `fetch` | 抓取数据（网页、API、RSS、视频） | summarize / agent-reach / yt-dlp |
| `filter` | 按条件过滤内容 | regex / keyword / LLM |
| `rewrite` | 改写/加工内容（翻译、摘要、风格调整） | LLM (MiniMax/GPT) |
| `generate` | 生成新内容（图、文、视频） | image_generate / tts / video_generate |
| `publish` | 发布到外部平台 | wechat-api / telegram / email |
| `wait` | 等待/延迟 | sleep / cron |
| `condition` | 条件分支 | LLM (router) |
| `report` | 向项目群汇报状态 | pipeline_reporter |
| `end` | 流程结束 | — |

### Step 1.2 — Edit if Needed

If the user requests changes, update the Mermaid diagram directly. Use the same syntax rules from Phase 0.

**Mermaid syntax rules (for edits):**
- Use `{{ }}` for conditions/decision nodes
- Use `[ ]` for process nodes
- Use `(-->)` for main flow arrows
- Use `-->|` for conditional arrows with label
- Use `(|label|)` for conditional branches

### Step 1.3 — Iterative Refinement

Ask the user if the flowchart is correct. Allow edits:
- User says "把 X 和 Y 合并成一个节点" → regenerate
- User says "在 A 和 B 之间加一个过滤节点" → insert node
- User says "X 之后要等 10 分钟再发布" → add `wait` node
- User says "改写之前还要翻译成英文" → insert `translate` node

Repeat until the user confirms: **"没问题，继续"** or **"可以了"**.

---

## Phase 2: Configure Each Node

After flowchart is confirmed, go through each node (except `START`/`END`) and ask. Use the `nodes` array from Phase 0 as the starting config draft for each node — pre-fill known fields (type, skill) and confirm or override.

> **"节点 [X] 需要配置什么？"**

For each node, derive and confirm:

| Node | Derived Config |
|------|----------------|
| `trigger` | cron expression (e.g. `0 9 * * *`) |
| `fetch` | source URL / API / RSS feed |
| `filter` | filter criteria (keywords, regex, or LLM prompt) |
| `rewrite` | rewrite instructions / target language / style |
| `generate` | generation prompt / media type |
| `publish` | platform (wechat / telegram / email) + account |
| `wait` | delay duration |
| `condition` | condition logic |
| `report` | which thread to report to (report / chat) |

**Skill auto-recommendation logic:**

```
node.type = "fetch" + source contains "youtube" → recommend "yt-dlp / summarize"
node.type = "fetch" + source contains "rss" → recommend "summarize"
node.type = "fetch" + source is "webpage" → recommend "summarize / browser-use"
node.type = "rewrite" → recommend MiniMax-M2.5 by default
node.type = "generate" + "image" → recommend image_generate (gemini/gpt-image-2)
node.type = "generate" + "video" → recommend video_generate
node.type = "publish" + "wechat" → recommend wechat-api (agent-reach)
node.type = "publish" + "telegram" → recommend telegram bot
node.type = "filter" → recommend regex / keyword / LLM
node.type = "report" → always available (pipeline_reporter)
```

For each node, confirm:
1. The recommended skill(s)
2. Any required credentials or tokens (e.g. WeChat API key, bot token)

### Step 2.1 — Compile Final `nodes_json`

After all nodes are configured, serialize the final node list as a JSON array. This becomes `--nodes-json` for `bootstrap_project.py`:

```bash
nodes_json='[
  {"id": "FETCH", "label": "抓取内容", "type": "fetch", "skill": "summarize", "config": {"source": "..."}},
  {"id": "FILTER", "label": "过滤", "type": "filter", "skill": "regex", "config": {"keywords": "..."}}
]'
```

**Verify before proceeding:** JSON validation runs automatically during `--interactive` bootstrap via the script layer. If running manual invocation, verify with `echo $nodes_json | python3 -m json.tool > /dev/null` before passing to `--nodes-json`.

---

## Phase 3: Technical Initialization

After all nodes are configured, collect the remaining technical parameters:

### Required (*)

| Parameter | Question |
|-----------|----------|
| `project_key` * | 项目英文标识（slug，英文+短横线，如 `fashion-monitor`）|
| `project_name` * | 项目中文名称，如 `时尚监控 Pipeline` |
| `bot_token` * | Telegram Bot Token（已有项目可复用）|
| `chat_id` * | 项目群 Chat ID（数字形式，如 `-1001234567890`）|
| `thread_ids` * | 线程映射（默认：`general=1,report=2,chat=3`）|

### Optional

| Parameter | Default |
|-----------|---------|
| `cron_timeout_seconds` | `1200` |
| `routing_group` | `new`（新组）或现有组名 |
| `wechat_publish` | `no` |
| `wechat_clash_selector` | `GLOBAL`（如需切换节点）|
| `wechat_clash_unix` | `/tmp/verge/verge-mihomo.sock` |

---

## Step 4: Generate Project

After all parameters confirmed, run the bootstrap script:

```bash
python3 skills/project-scaffold/scripts/bootstrap_project.py \
  --project-key "<project_key>" \
  --project-name "<project_name>" \
  --description "<description>" \
  --flowchart "<mermaid_flowchart_as_single_line>" \
  --bot-token "<bot_token>" \
  --chat-id "<chat_id>" \
  --thread-ids "<thread_ids>" \
  --cron-schedule "<cron_schedule>" \
  --cron-timeout "<cron_timeout_seconds>" \
  --nodes-json '<nodes_json>'
```

The script generates:
- All identity/project/workflow files
- `config/runtime.env` with skill deps
- `WORKFLOW.md` with the Mermaid flowchart embedded
- `scripts/run_pipeline.sh` with nodes wired as pipeline stages
- `scripts/<project>_bot.py` as a **stub placeholder** — node logic is commented, requires manual implementation per node after scaffold
- Telegram routing + Cron registration

**Stub bot note:** `<project>_bot.py` is generated as a bare placeholder. The `nodes_json` config is written to `WORKFLOW.md` for reference, but the stub does not auto-wire skills or credentials. After scaffold, implement each node handler in the stub using the skill calls documented in `WORKFLOW.md`.

---

## Bootstrap Flags

| Flag | Purpose |
|------|---------|
| `--plan` | **新项目首选**。不写文件、不做验证，只预览完整影响面（30个文件 + config写入 + cron注册 + agent注册），然后 exit 0。 |
| `--dry-run` | 创建所有文件 → 运行自动体验(G) → 若 FAIL 则 abort，不写 config；若 OK 则 exit 0（不写 config）。 |
| `--validate-only <path>` | 对已有项目做 8 项体检。不修改任何文件。 |
| `--fix-suggestions` | 随 `--validate-only` 使用，输出每个 FAIL/WARN 的可粘贴修复代码块。 |
| `--fix-dry-run` | 随 `--validate-only` 使用，预览 `--fix` 的实际写入操作（带 backup 计划）。 |
| `--fix` | 对已有项目应用所有自动安全修复（创建缺失文件、补充 runtime.env 变量），exit 0 即成功。 |
| `--continue-from-fix <path>` | 在 `--fix` 成功后，补跑被 G-abort 跳过的 config 写入（routing、agent 注册、telegram 配置、cron 注册）。从项目目录读取配置，不需要完整参数。 |
| `--fix-and-continue <path>` | **推荐合并命令**。等于 `--fix` + `--continue-from-fix` 一次性完成：体检 → 自动修复 → 重体验 → 补跑 config 写入。FAIL 时中途 abort，不会污染 config。 |
| `--interactive` | **交互式引导**：分步收集所有参数，每步带验证（project_key 格式、chat_id 格式、cron 表达式等），收集完成后直接进入 bootstrap 流程（等同于 `--fix-and-continue`）。 |
| `--all-projects` | 对 `projects/` 下所有项目跑快速体检，输出汇总表（FAIL数/WARN数/状态），exit 0 即全部健康。 |
| `--cron-list` | 从 openclaw cron 读取所有 job（JSON 格式），输出格式化表格，包含状态/ID/Schedule/所属项目。 |
| `--cron-remove <job-id>` | 删除指定 cron job（需先 `--cron-list` 查到 ID）。 |

**交互式引导步骤：**
1. `project_key` — 英文小写+短横线，自动验证格式
2. `project_name` — 中文名
3. `description` — 项目描述
4. `chat_id` — 格式验证
5. `bot_token` — 长度验证
6. `routing_group` — 默认 new
7. `cron_schedule` — 5位 cron 验证
8. 线程 ID — general/report/chat 默认 1/2/3
9. 确认后自动进入 `--fix-and-continue` 流程 |

**推荐工作流（简化版）：**
1. `bootstrap_project.py --interactive` → 交互式引导，参数自动验证，一步完成 bootstrap
2. 或分步：`bootstrap_project.py --plan ...` → `bootstrap_project.py --fix-and-continue --validate-only <path>`
3. 定期：`bootstrap_project.py --all-projects` → 全项目体检，优先修复 FAIL 数量最多的项目

**完整五步（当需要细粒度控制时）：**
1. `bootstrap_project.py --plan ...`
2. `bootstrap_project.py --dry-run ...`
3. `bootstrap_project.py --fix-dry-run --validate-only <path>`
4. `bootstrap_project.py --fix --validate-only <path>`
5. `bootstrap_project.py --continue-from-fix <path>`

---

## Required References

Before running, read:
- `references/architecture.md` — shared pipeline pattern (unchanged, still valid)
- `references/flow_design_language.md` — node type definitions, Mermaid syntax guide, and skill recommendation rules
- `references/onboarding_checklist.md` — project setup checklist
- `references/shared_routing_group_schema.md` — shared routing group schema

---

## Constraints

- **Never start with technical parameters.** Flowchart must be confirmed before asking for `bot_token` / `chat_id` / `cron_schedule`.
- **Every non-START/END node must have a skill assignment** before generation.
- **WeChat publish is optional.** Only include WeChat config if a `publish` node targets WeChat.
- **Cron delivery is always `mode=none`.** Reporter controls delivery to prevent dual-reporting.
- **Mermaid is primary; ASCII is fallback** if Telegram cannot render the code block.
- **If user is unsure about a node**, ask a clarifying question rather than guessing. A vague flow is better than a wrong one — the flowchart is a thinking tool, not a constraint.
- **Report nodes are mandatory** for automated pipelines. Human-in-the-loop approval steps should also appear as report nodes.

---

## Example Conversation Flow

```
用户: 创建一个新的内容监控项目
AK:    收到，正在推理项目结构...

  LLM 推理结果（模型：MiniMax-M2.5）
  项目类型：内容监控 + 自动发布
  推荐流程：trigger → fetch → filter → rewrite → publish → report → end

  ```mermaid
  flowchart LR
      START([开始]) --> TRIGGER{{定时触发}}
      TRIGGER --> FETCH[抓取油管频道]
      FETCH --> FILTER{新视频?}
      FILTER -->|是| REWRITE[改写为公众号风格]
      FILTER -->|否| END1([结束])
      REWRITE --> PUBLISH[发布到微信公众号]
      PUBLISH --> REPORT[汇报结果]
      REPORT --> END2([结束])
  ```

  模型推荐：GPT-4.1（涉及多平台判断）— 如需调整请说"用 GPT-4.1"

  确认这个流程？
用户: 可以，但我想在改写之前先加一个质量判断
AK:    收到，更新后的图：

  ```mermaid
  flowchart LR
      START --> TRIGGER{{定时触发}}
      TRIGGER --> FETCH[抓取油管频道]
      FETCH --> FILTER{新视频?}
      FILTER -->|否| END1
      FILTER -->|是| QUALITY{内容质量够高?}
      QUALITY -->|否| END2
      QUALITY -->|是| REWRITE[改写为公众号风格]
      REWRITE --> PUBLISH[发布到微信公众号]
      PUBLISH --> REPORT --> END3
  ```

  这样可以吗？
用户: 没问题，继续
AK:    好，现在配置每个节点：

  节点 [定时触发] — cron 表达式是什么？比如每天早上 9 点：`0 9 * * *`
用户: 每天早上9点
AK:    收到。节点 [抓取油管频道] — 频道 RSS 或 URL 是什么？
用户: 有三个频道...
  （继续逐节点配置...）
```
