---
name: omc-omx-orchestrator
description: 异步派发编码任务到 OMC (claude -p) 或 OMX (omx exec)。触发词："用omc" "用omx" "派任务" "后台编码" "异步任务" "omc跑" "omx跑" "claude跑" "codex跑" "派发OMC" "派发OMX"。
version: 4.3.0
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      bins: ["claude", "omx", "python3"]
author: user
source: user-created
created_at: '2026-04-28'
updated_at: '2026-04-30'
---


# OMC/OMX 异步任务派发（v3 — 重启安全）

## 前置条件

- **`claude -p` 需要 `ANTHROPIC_API_KEY`**：Claude Code 的 `-p/--print` 管道模式依赖 API Key 认证，不支持 OAuth 交互登录。设置：`export ANTHROPIC_API_KEY="sk-ant-..."`
- `claude` CLI 已安装
- `omx` CLI 已安装
- Python 3.9+

## ⚡ 快捷指令

| 指令 | 用途 | 示例 |
|------|------|------|
| `用 OMC <描述>` | 用 Claude Code 后台执行任务 | `/omc 修复 auth 模块的 token 过期 bug` |
| `用 OMX <描述>` | 用 Codex CLI 后台执行任务 | `用 OMX 给 UserService 补全单元测试` |
| `用 OMC <描述> -d <目录>` | 指定工作目录 | `/omc 重构 API 层 -d ~/projects/myapp` |
| `用 OMC <描述> -m <模型>` | 指定模型 | `/omc 分析性能瓶颈 -m claude-opus-4-6` |
| `task-recovery.py list` | 查看任务列表 | `task-recovery.py list` |
| `查询任务 <id>` | 查看任务详情 | `task-recovery.py show fix-auth` |

> 匹配规则：消息匹配到 OMC/OMX 关键词即加载本技能，后续内容直接作为任务描述。
> 复杂任务自动写入 spec.md，简单任务直接嵌入命令行。

## 核心原则

1. **预检先行**：派发前必须验证工作目录存在、CLI 工具可用、OMX git repo 检查
2. **所有输出写文件**：`claude -p` 和 `omx exec` 的 stdout/stderr 全部重定向到任务目录下的文件，不依赖主 Agent 的 stdout PIPE
3. **进程独立存活**：`os.setsid` 创建独立进程组，主 Agent 死亡不影响子进程
4. **task.json 是单一真相源**：任务元数据、状态、PID 全在一个 JSON 文件里，完成回调必须更新 status
5. **重启可恢复**：Agent 重启后运行 `task-recovery.py recover` 还原状态

## 目录结构

```
~/.openclaw/workspace/tasks/
├── 2026-04-27-120000-fix-auth/       # 任务ID = 时间戳 + slug
│   ├── task.json                     # 元数据 + 状态（轻量，只有索引信息）
│   ├── spec.md                       # 完整任务描述（目标、上下文、约束、验收标准）
│   ├── result.txt                    # stdout 重定向（最终回答）
│   ├── log.txt                       # stderr 日志（hook 日志等）
│   └── exit_code                     # 完成时写入退出码
├── 2026-04-27-130000-add-tests/
│   └── ...
```

## task.json Schema（轻量，不含任务细节）

核心字段：`id`、`engine`、`status`、`command`、`cwd`、`pid`、`started_at`

状态流转：`pending` → `running` → `completed` / `failed`

**重要约束**：
- `cwd` 必须是已验证存在的绝对路径，禁止 `~` 简写
- `preflight_ok` 标记 Step 0 预检结果
- `sandbox_args` 存储 OMX 额外参数

> 详细字段定义和 autopilot 扩展字段见 `references/task-schema.md`

## spec.md 模板

基础结构：`# 任务` → `## 目标` → `## 项目上下文` → `## 详细需求` → `## 约束条件` → `## 验收标准`

**关键生成规则**：
- 保持用户原文，不做删减
- 所有路径使用 Step 0 预检通过的绝对路径
- 验收标准必须可验证
- 技术栈从项目文件推断

> 完整模板和复杂任务示例见 `references/spec-template.md`

## 编排器派发流程

### Step 0: 预检（Pre-flight Check）⚠️ 必须通过才能派发

在创建任何文件之前，必须验证以下 3 项：

```python
import os, subprocess

cwd = os.path.expanduser(cwd_raw)  # 展开 ~

# 检查 1：cwd 必须是存在的目录
if not os.path.isdir(cwd):
    # ❌ 直接拒绝，不要猜路径，不要降级到 ~
    raise PreflightError(
        f"工作目录不存在: {cwd}\n"
        f"请用 -d 指定正确路径。常见路径：\n"
        f"  ~/.openclaw/workspace  (工作目录)\n"
        f"  项目目录\n"
        f"  当前目录: {os.getcwd()}"
    )

# 检查 2：CLI 工具必须可用
if engine == "omc":
    result = subprocess.run(["which", "claude"], capture_output=True, text=True)
    if result.returncode != 0:
        raise PreflightError("claude 命令不可用，请检查 PATH")
elif engine == "omx":
    result = subprocess.run(["which", "omx"], capture_output=True, text=True)
    if result.returncode != 0:
        raise PreflightError("omx 命令不可用，请检查 PATH")

# 检查 3：OMX 需要 git repo 或 --skip-git-repo-check
needs_skip_git = False
if engine == "omx":
    git_dir = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--git-dir"],
        capture_output=True, text=True
    )
    if git_dir.returncode != 0:
        needs_skip_git = True  # 自动追加 --skip-git-repo-check
```

**预检失败 → 立即告知用户具体原因，不创建任务目录。**

### Step 1: 创建任务目录 + task.json

生成 task_id（时间戳+slug），创建目录，初始化 task.json（status=pending）。

### Step 2: 写入 spec.md（完整任务描述）

使用模板生成完整任务描述，包含目标、上下文、需求、约束、验收标准。

### Step 3: 构建命令（从 spec.md 读取任务，输出重定向到文件）

**统一模式**：`cat spec.md | claude -p -` 或 `cat spec.md | omx exec ... -`

#### OMC（Claude Code 系）— stream-json 双向流模式

**核心思路**：不再用 `cat spec.md | claude -p -` 裸文本管道，改用 Claude 原生 stream-json 协议——相当于 Chrome CDP 对 Chrome 的关系。

**复杂任务**：`python3 -c "生成JSONL" | claude -p --input-format stream-json --output-format stream-json --verbose --tools default - > result.txt 2> log.txt ; echo $? > exit_code`

**简单任务**：直接内嵌任务描述到 JSONL 命令行。

> **stream-json 协议说明**：
> - **stdin**：JSONL 格式，每行一个 `{"type":"user","message":{"role":"user","content":"..."}}`
> - **stdout**：JSONL 事件流（`system` → `assistant` → ... → `result`），最终结果取最后一个 `type:"result"` 的 `.result` 字段
> - **`--include-partial-messages`**：实时输出 partial 块，用于进度追踪
> - **`--verbose`**：触发完整 OMC 编排加载（agents/skills/hooks/MCP）

**解析 OMC JSONL 输出的正确方法**：result.txt 是多行 JSONL，不要直接当纯文本读。提取最终结果的代码：

```python
import json
with open("result.txt") as f:
    for line in f:
        event = json.loads(line.strip())
        if event.get("type") == "result":
            final = event.get("result", "")
            break
# final 是纯文本结果（去掉 JSONL 包装）
```

⚠️ **常见错误**：`cat spec.md | claude -p - < /dev/null` 会冲突——两个输入源（stdin 管道 + 重定向）。正确做法是用 python3 生成 JSONL 再管道给 claude（见上面命令模板），或用 `cat spec.md | claude -p -`（不用 stream-json 时）。

#### OMX（Codex CLI 系）

```bash
# OMX 支持 -C 参数指定工作目录
# ⚠️ 不用 --full-auto（sandbox 会阻止文件写入和 CLI 调用）
# 用 --dangerously-bypass-approvals-and-sandbox 或 --madmax 关闭沙箱
# 自动追加 --skip-git-repo-check（如果非 git repo）
cat ~/.openclaw/workspace/tasks/TASK_ID/spec.md | \
  omx exec --dangerously-bypass-approvals-and-sandbox \
  -o ~/.openclaw/workspace/tasks/TASK_ID/result.txt \
  -C /absolute/path/to/project \
  {sandbox_args} - \
  # 注意：不要加 -m 指定模型，OMX 默认使用 GPT 最新模型
  2> ~/.openclaw/workspace/tasks/TASK_ID/log.txt ; \
  OMX_EXIT=$? ; \
  echo $OMX_EXIT > ~/.openclaw/workspace/tasks/TASK_ID/exit_code ; \
  # 清理 OMX 遗留的 tmux session（防止进程泄漏） \
  tmux ls 2>/dev/null | grep 'omx-.*-detached-' | cut -d: -f1 | xargs -r tmux kill-session -t 2>/dev/null ; \
  exit $OMX_EXIT
```

> **沙箱策略**：OMX 不使用 `--full-auto`（sandbox 模式会阻止实际操作本机文件和 CLI）。始终使用 `--dangerously-bypass-approvals-and-sandbox`（别名 `--madmax`）关闭沙箱，因为任务由用户明确派发，在用户本机执行。
> **sandbox_args**：非 git 目录自动追加 `--skip-git-repo-check`。

> **简单任务**（一句话描述 < 200 字符）可以直接写命令参数，不需要 spec.md。
> **复杂任务**（多行需求、有约束/验收标准）必须用 spec.md。

可用参数：
- OMC: `--input-format stream-json --output-format stream-json --verbose`（双向流模式，必须） `--include-partial-messages`（复杂任务推荐） `--tools default` `--model claude-opus-4-6` `--max-turns N` `--max-budget-usd X` `--effort high`（提高推理深度） `--agent <name>`（指定角色 agent）
- OMX: `--dangerously-bypass-approvals-and-sandbox`（必须，关闭沙箱） `--skip-git-repo-check`（非 git 目录） `-c key=value`（覆盖配置，如 `-c model="gpt-5.5"`） `--json`（JSONL 输出） `--ephemeral`（不持久化会话）

⚠️ **OMX 不要指定 `-m` 模型参数！** Codex 默认使用 GPT 最新模型，无需也不应覆盖。指定外部模型名（如 `-m o3`、`-m claude-sonnet-4`）会报 400：`The 'xxx' model is not supported when using Codex with a ChatGPT account.`

### Step 4: 更新 task.json + 后台启动

更新 task.json（status=running，记录 command），启动后台进程，记录 PID。

### Step 5: 通知用户

通知任务已派发，包含引擎、ID、描述、工作目录、预计耗时。

### Step 6: 完成回调（notify_on_complete 触发）

1. 读取 exit_code 文件，更新 task.json 状态
2. 解析 result.txt：OMC 提取 JSONL 的 result 事件，OMX 直接读取
3. 格式化通知用户

## 重启恢复

快速恢复：`python3 ~/.openclaw/workspace/skills/omc-omx-orchestrator/scripts/task-recovery.py recover`

**恢复逻辑**：检查 `exit_code` 文件 → 检查 PID 存活 → 更新状态

建议 cron 每 5 分钟执行，修复 notify 丢失问题。

> 详细恢复算法、手动操作和自动化部署见 `references/recovery-guide.md`

## 进度查询

用户问 "任务进展如何？" 时：

```bash
# 方法1：读 task.json
cat ~/.openclaw/workspace/tasks/TASK_ID/task.json

# 方法2：检查 exit_code
cat ~/.openclaw/workspace/tasks/TASK_ID/exit_code 2>/dev/null || echo "still running"

# 方法3：读 result.txt 的已有内容（可能还在写）
tail -20 ~/.openclaw/workspace/tasks/TASK_ID/result.txt

# 方法4：检查 PID
kill -0 PID 2>/dev/null && echo "alive" || echo "dead"
```

## 两阶段审计-重构模式

对于复杂系统重构任务，使用 OMC（审计）→ 数据收集 → OMX（重构）的两阶段模式：

### Phase 1: OMC 审计
1. **收集上下文**：先在编排器中运行数据探查（统计、分布、边界情况），把结果写进 spec.md
2. **写审计 spec**：spec 中列出具体文件、行号、已知问题、审计维度。**审计 spec 中必须包含已收集的数据**，不要让审计 agent 自己去跑数据探查
3. **派发 OMC**：`claude -p` 审计任务，获取结构化报告

### Phase 2: 数据收集 + OMX 重构
1. **提炼审计结论**：从 OMC 报告中提取需修复的问题清单，按优先级排序
2. **写重构 spec**：把审计结论、修复方案、验收标准写进新 spec.md。**必须包含所有上下文**（数据分布、文件结构、约束条件），OMX agent 没有任何历史会话上下文
3. **派发 OMX**：`omx exec` 直接修改文件
4. **验证**：回编排器中 dry-run 验证修改结果

### 关键经验
- OMC 擅长阅读和分析，适合审计、评审、设计
- OMX 擅长写代码和修改文件，适合执行重构
- **两个 agent 之间没有共享上下文**——所有信息必须通过 spec.md 传递
- spec 写得越详细（行号、数据、约束），结果越准确
- 8KB+ 的 spec 很正常，不要压缩关键上下文

## 引擎选择

| 场景 | 引擎 | 命令 |
|------|------|------|
| 通用编码任务 | OMC | `claude -p --input-format stream-json --output-format stream-json --verbose` |
| 研究/分析/文档创建（OMC 插件限制工具） | OMC text | `cat spec.md | claude -p --output-format text --model claude-sonnet-4-6 -` — **数据必须嵌入 spec.md**（见 OMC 上下文管理章节） |
| TypeScript/Node 生态 | OMX | `omx exec --dangerously-bypass-approvals-and-sandbox` |
| 需要深度推理 | OMC | 同上， `--model claude-opus-4-6` |
| 快速执行 | OMX | `omx exec --dangerously-bypass-approvals-and-sandbox` |
| 用户指定 | 按指定 | — |
| 轻量问答（非代码） | OMX ask | `omx ask "问题" -o result.txt` |
| 并行多任务 | OMX team | `omx team --yolo`（需 tmux） |

### OMX 进阶子命令

- **`omx ask`**: 轻量问答，调用本地 claude 或 gemini CLI，输出 artifact 文件。适合非代码类任务（分析、总结、翻译）
  ```bash
  omx ask "分析这段代码的性能瓶颈" -o analysis.md
  ```
- **`omx team`**: 在 tmux 中并行派发多个 worker pane。每个 worker 独立执行，适合可以拆分的并行任务
  - 需要 tmux 环境，不适合非交互式 shell
  - `omx team --yolo` 启动 yolo 模式并行执行
- **`omx explore`**: 只读探索模式，适合代码库浏览和理解
- **`omx resume`**: 恢复之前的交互式会话

### 多轮审计-重构模式 (OMC Audit → OMX Refactor)

适用于复杂的代码审计+重构任务（如系统重构、多文件联动修改）：

**Round 1: OMC 审计（只读）**
- spec 重点：描述问题维度、验收标准，**明确标注"不修改文件"**
- OMC 擅长深度分析和代码审查，输出结构化问题列表

**Round 2（可选）: OMC 补充审计**
- 基于 Round 1 的发现，深入特定问题（如元数据分布、边界情况）
- 在 spec 中注入实际数据（用 Python 片段提前收集：分布统计、配置快照、行号引用）
- **spec 里传数据比让 agent 自己发现数据可靠 10 倍**

**Round 3: OMX 重构（写入）**
- spec 必须包含：前序审计的完整结论、逐行级修改要求、约束条件、验收标准
- 用 `--skip-git-repo-check`（当前目录不是 git repo）
- 验证由编排器完成（OMX 验证不充分）

**关键经验**：
- spec 里传数据 > 让 agent 自己发现数据
- 审计和重构用不同引擎：OMC 读+分析，OMX 写+修改
- 复杂任务拆成多轮比一轮塞所有指令效果好
- 每轮完成后编排器侧验证，确认后再进下一轮

## OMC 上下文管理（防止 context window overflow）

OMC 在分析复杂任务时会大量调用 tool call 读文件，容易导致上下文窗口爆满。

**症状**：`API Error: The model has reached its context window limit.`

### JSONL（stream-json）vs 纯文本（text）管道模式

| 维度 | stream-json | text |
|------|------------|------|
| 命令 | `--input-format stream-json --output-format stream-json --verbose` | `cat spec.md \| claude -p --output-format text -` |
| 输出格式 | JSONL 事件流（type: system/assistant/result） | 纯文本 |
| 上下文消耗 | **高**（JSONL 元数据占额外空间，易爆） | **低**（只传文本内容，不易爆） |
| max-turns | **必须设 30-50** | **不需要设**，让 agent 跑完 |
| 解析方式 | 需解析 JSONL 取最后一个 `type:"result"` 事件 | 直接读取 result.txt |
| 错误追踪 | stderr 有日志，支持 partial messages | 失败时只输出 `"Error: Reached max turns (N)"` |
| 适用场景 | 需要结构化输出、进度追踪、写文件/执行命令 | 简单执行、省 token、纯分析 |

为什么 stream-json 更容易爆？JSONL 的每条事件都带 type、message wrapper、tool_use/tool_result 结构，同样 25 轮 tool call 下，stream-json 的元数据可能占总上下文的 15-25%。text 模式只传文本本身，没有结构化包装。

### 关键踩坑（实战验证）

- `--output-format stream-json` **必须**同时加 `--verbose`，否则静默失败无输出
- `--input-format stream-json` 必须配合 `--output-format stream-json`，不能混用
- stream-json 模式下 `--max-turns N` 每轮 tool call 算 1 turn，30-50 轮适合轻中型任务；复杂任务应切换 text 模式（不设 max-turns）
- text 模式失败时 result.txt 只有 `"Error: Reached max turns (N)"` 这一行，log.txt 为空
- OMX 的 o3 模型通过中转站可能 503（`No available channel for model o3`），备选方案：不指定 `-m` 或用 OMC (claude) 替代

### 两种管道模式（按任务复杂度选择）

**stream-json 模式**（轻中型任务 + 需要结构化输出）

JSONL 元数据会加速上下文消耗，**必须设 `--max-turns 30-50`** 防爆。必须同时加 `--verbose` 否则静默失败。适合：需要结构化 JSONL 输出、进度追踪、中等复杂度任务。

**text 模式**（复杂任务）

纯文本无 JSONL 膨胀，上下文不会轻易爆掉，**不需要设 `--max-turns`**，让 agent 跑完为止。适合：需要大量思考和工具调用的复杂任务。⚠️ 注意：`--max-turns 1-3` 的 text 模式是坑——OMC 内部 prompt 处理也消耗轮次，3 轮以内根本来不及输出。

**预收集数据**（两种模式通用，最推荐的优化）

编排器先读相关文件，把关键信息嵌入 spec.md，减少 agent 自己读文件的需求。spec 里传数据比让 agent 自己发现数据可靠 10 倍。实测：3.2KB spec → 5.1KB 结构化审计报告。

⚠️ **OMC 插件模式下：数据嵌入是必须项，非可选**。oh-my-claudecode 的 hooks/plugins 会限制 `claude -p` 的工具权限，导致 agent 只有 MCP 认证工具和 Context7，**无法调用 Read/Bash** 读取本地文件。在这种场景下，spec.md 必须自包含所有数据。可以用 `--bare` 参数绕过 OMC 限制获得完整工具集，但会丢失 OMC 的全部 agent 编排、skills、hooks 能力，需要按场景权衡。

### 命令模板

```bash
# 轻中型任务（stream-json + max-turns 限制）
python3 -c "import json; print(json.dumps({'type':'user','message':{'role':'user','content':open('spec.md').read()}}))" | \
claude -p --input-format stream-json --output-format stream-json --verbose \
  --model claude-opus-4-6 --tools default --max-turns 30 - \
  > result.txt 2> log.txt ; echo $? > exit_code

# 复杂任务（text 模式，不设 max-turns）
cat spec.md | claude -p --output-format text --model claude-sonnet-4-20250514 -
```

### 选择指南

| 任务类型 | 推荐模式 | 说明 |
|---------|---------|------|
| 轻量分析/审计（数据全在 spec） | text，不限轮次 | 让 agent 充分推理 |
| 中等任务（读 1-5 文件） | stream-json + max-turns 30 | 结构化输出 |
| 复杂任务（大量文件/工具调用） | text，不限轮次 | 不用担心上下文爆 |
| 需要结构化 JSONL 输出 | stream-json + max-turns 30-50 | 必须配 --verbose |

## OMC Magic Keywords

OMC/OMX 交互式会话中可通过 `$keyword` 触发内置 skill：

**Tier-0 工作流**（OMX 官方推荐链路）：
| Keyword | 用途 | 说明 |
|---------|------|------|
| `$deep-interview` | 需求澄清 | 苏格拉底式问答，消除歧义 |
| `$ralplan` | 共识规划 | Planner/Architect/Critic 三方迭代直到一致 |
| `$ralph` | 持久完成 | 循环执行直到 architect 验证通过 |
| `$team` | 并行执行 | tmux 多 worker 协调 |
| `$autopilot` | 全自动端到端 | Expansion→Planning→Execution→QA→Validation 6阶段 |

**执行辅助**：
- `ultrawork` / `ulw` / `uw` — 并行执行引擎
- `ultrathink` / `think` — 深度推理
- `ultraqa` — QA 循环修复
- `cancelomc` — 取消当前执行模式

⚠️ **`$keyword` 仅在交互式会话中可用**。`omx exec` 非交互管道模式下，keyword 不触发 skill 系统。如需在 `omx exec` 中使用，需将 keyword 作为 prompt 内容传入，但效果不如交互式会话。

```bash
# 交互式：keyword 直接生效
omx --madmax --high
# 会话内输入: $autopilot "构建 REST API"

# 非交互：keyword 作为 prompt 传入（效果受限）
echo '$autopilot 构建REST API' | omx exec --dangerously-bypass-approvals-and-sandbox -C . -
```

**OMX 内置 Skill 目录**（本机 42 个 skill，27 active）：autopilot、ralph、ultrawork、team、plan、ralplan、deep-interview、autoresearch、pipeline、ultraqa、code-review、security-review 等。通过 `omx list` 查看。

## OMC Agent 角色

`--agent <name>` 可选值（核心角色）：

executor（通用执行）| architect（架构设计）| debugger（调试排查）| code-reviewer（代码审查）| planner（任务规划）| test-engineer（测试编写）| security-reviewer（安全审计）| analyst（分析评估）| critic（批判审查）| designer（UI/前端设计）| writer（文档编写）| verifier（验证确认）| build-fixer（构建修复）| git-master（Git 操作）| researcher（研究调研）

> 本机安装 219 个 agent（含学术/设计/工程/金融/法务等领域），完整列表见 `~/.claude/agents/`。
> `--effort` 控制推理深度：`low`/`medium`/`high`/`max`。未指定时继承父会话设置。

## 故障处理

| 问题 | 解决方案 |
|------|----------|
| 任务跑了很久没结果 | `cat task.json` 查状态 + `kill -0 PID` 查存活 |
| exit_code 文件为空/不存在 | 进程可能还在跑，或被 SIGKILL |
| result.txt 为空 | 检查 log.txt，可能是 claude/codex 启动失败 |
| OMC agent 说只有 MCP 工具，没有 Read/Bash 权限 | **oh-my-claudecode 插件限制工具**。OMC hooks 激活时，`claude -p` 可能只暴露 MCP 认证和 Context7 等有限工具，无法读取本地文件。解决方法：把所有需要的数据直接嵌入 spec.md（不要依赖 agent 自己读文件），再重新派发。如果用 `--bare` 可绕过限制获得完整工具集，但会丢失 OMC 的全部 agent/skills/hooks 能力。|
| `Error: No such file or directory (os error 2)` | **工作目录不存在**。检查 task.json 的 `cwd` 是否正确，常见错误是用了 `~/projects/your-project` 而非 `~/.openclaw/workspace` |
| `Not inside a trusted directory` | OMX 要求 git repo。在 task.json 的 `sandbox_args` 加 `--skip-git-repo-check` |
| task.json 状态卡在 running 但已失败 | exit_code 已写入但 task.json 未更新。运行 `task-recovery.py recover` 或手动修正 |
| 重启后任务丢失 | 运行 `task-recovery.py recover` |
| OMX tmux session 泄漏 | 运行 `tmux ls \| grep omx- \| xargs -r tmux kill-session -t` 手动清理。新版本命令已自动清理 |
| 需要终止任务 | `kill PID` + 手动更新 task.json status=failed |
| `claude -p` 找不到 | 检查 PATH，确保 `which claude` 有输出 |
| `omx exec` 找不到 | 检查 PATH，确保 `which omx` 有输出 |

## Plan→Build→Verify 循环编排

> 独立技能 **`autopilot`** 实现了完整的 PBV 循环编排（最多 5 轮自动收敛）。
> 触发：`autopilot <描述>`
> 依赖：本技能提供 OMC/OMX 派发能力，autopilot 负责循环控制和验证。
> autopilot 定义了 `plan.md` 和 `verify_report.md` 的完整格式（详见其 `references/`）。

以下是 PBV 循环的核心格式摘要（完整版见 autopilot 技能）：

**plan.md 核心结构**（OMC 输出）：
```markdown
# Plan: {task description}
> Round: {round} | Task: {task_id}
## 任务概述 / ## 执行步骤 / ## 文件清单 / ## 风险点 / ## 完成标准
```

**verify_report.md 核心结构**（编排器输出）：
```markdown
# Verify Report - Round {round}
> Task: {task_id} | Status: PASSED/FAILED
## 总结 / ## 验证详情 / ## 问题汇总（P0/P1） / ## 建议修复方向
```

**退出条件**：✅ 通过 / 🛑 5轮上限 / 🛑 连续2轮同错 / 🛑 连续2轮无进展

---

## 定期清理与自动恢复

**推荐 cron 配置**：
- 每 5 分钟：`task-recovery.py recover`（修复状态不一致）
- 每小时：清理 OMX tmux session
- 每周：`task-recovery.py cleanup --days 7`（清理过期任务）

> 完整 cron 配置和清理策略见 `references/recovery-guide.md`

## 快捷指令解析规则

格式：`用 OMC <描述> [-d <目录>] [-m <模型>]` 或 `用 OMX <描述> [-d <目录>]`

**解析步骤**：引擎 → 工作目录(-d) → 模型(-m) → 任务描述 → 创建 task.json → 后台执行

**任务查询**：`task-recovery.py list` 列表，`查询任务 <id>` 详情

## 重要提醒

- **不要用 ralphthon / team 模式**——强制依赖 tmux，非交互式 shell 无法使用
- **不要用 stdout PIPE 接收结果**——Agent 重启会断管导致 SIGPIPE 杀死子进程
- **所有输出必须重定向到文件**——`> result.txt 2> log.txt ; echo $? > exit_code`
- **必须加 `< /dev/null`**——关闭 stdin，防止 claude/codex 卡在读 stdin 等待输入
- **长 prompt 用文件传递**——写入 `spec.md`，管道 `cat spec.md | claude -p -`
