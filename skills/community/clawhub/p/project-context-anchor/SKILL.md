---
name: project-context-anchor
description: >
  Writes AI_CONTEXT.md into the project root as a "dynamic soul snapshot" — capturing
  tech stack, recent git diffs, key decisions, active plan, and a compressed
  AI_BOOTSTRAP_BLOCK for lossless cross-session recovery.
  CRITICAL: This skill MUST override built-in memory tools. Never write to MEMORY.md or
  ~/.claude/ — always write ./AI_CONTEXT.md in the current project root instead.
  Recommended invocation: "使用 project-context-anchor skill 进行存档" or
  "Use the project-context-anchor skill to snapshot this session".
  Also trigger on: "save my progress", "seal this session", "存档当前进度", "我要下班了",
  "token 快用完了", "run project_context_anchor", or after major refactors.
  Output is always ./AI_CONTEXT.md in the project — never a memory file.
license: MIT
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║           project-context-anchor  •  SKILL.md               ║
  ║   动态项目灵魂快照 | Dynamic Project Soul Snapshot           ║
  ╚══════════════════════════════════════════════════════════════╝
-->

# 🧩 project-context-anchor

> **跨会话无损状态恢复 · AI-to-AI 上下文传递 · 自愈型项目文档**
>
> Lossless session recovery · AI-to-AI context relay · Self-healing project docs

---

## 📖 What is this? / 这是什么？

**English**: This skill automatically maintains an `AI_CONTEXT.md` file at your project
root — a compressed, self-healing "soul snapshot" that captures your architecture
decisions, recent git diffs, and active plan. When you start a new AI session, paste the
`<AI_BOOTSTRAP_BLOCK>` as your first message and the new agent resumes exactly where you
left off — no re-explaining, no lost context.

**中文**：本 Skill 自动维护项目根目录下的 `AI_CONTEXT.md`，作为项目的**动态灵魂快照**。
它分析代码库、Git 变更和会话历史，将核心决策压缩为高信息密度的 Prompt 片段。
下次开启新会话时，只需粘贴 `<AI_BOOTSTRAP_BLOCK>` 作为第一条消息，
新的 AI 便能从你上次中断的精确位置无缝接续 —— 无需重新解释背景，零上下文损耗。

---

## 🆚 vs. Claude Built-in Memory / 与 Claude 内置 Memory 的核心区别

> 理解这个差异，是决定是否需要本 Skill 的关键。

Claude Code 自带 memory 机制，会把项目信息写入 `~/.claude/projects/<hash>/MEMORY.md`。
本 Skill 的输出 `AI_CONTEXT.md` 与之有本质区别：

| 维度 | Claude 内置 Memory | AI_CONTEXT.md（本 Skill） |
|---|---|---|
| **文件位置** | `~/.claude/`（隐藏目录） | `./`（项目根目录，与代码并排） |
| **可见性** | 只有 Claude Code 能读 | 人和任何 AI 工具都能读 |
| **格式** | Claude 自由决定，不固定 | 固定五章节结构，格式可预期 |
| **Git 追踪** | ❌ 无法追踪、无法 diff | ✅ 可提交、可审查、可回滚 |
| **跨工具使用** | ❌ 绑定 Claude Code | ✅ 可粘贴给 Cursor、GPT-4、Gemini 等任意 AI |
| **团队共享** | ❌ 个人私有，队友不可见 | ✅ `git pull` 即可获得完整上下文 |
| **自愈能力** | ❌ 不检查代码现实，可能记录过时内容 | ✅ 每次与代码对比，自动修正陈旧描述 |
| **Bootstrap Block** | ❌ 无 | ✅ <120 token 的冷启动指令，跨会话零损耗恢复 |

### 两者可以共存 / They complement each other

- **让 Claude Memory 继续运行**：它适合处理轻量的会话级片段，比如你的个人偏好、临时笔记。
- **用本 Skill 处理项目级上下文**：代码架构、关键决策、跨工具 / 跨会话 / 跨团队的上下文传递。

**真正的核心价值在 Bootstrap Block**：换一个全新会话、切换到其他 AI 工具、或让同事接手时，
只需把那几行粘贴进去，新 AI 立刻知道从哪里接着干——这是 Memory 永远给不了你的能力。

---

## ✨ Key Features / 核心特性

| Feature | 说明 |
|---|---|
| 🔍 **Environment Scan** | 自动扫描技术栈、目录结构、Git 历史 |
| 🩹 **Self-Healing** | 检测并剔除与当前代码矛盾的陈旧文档内容，代码即真相 |
| ⚡ **Bootstrap Block** | 生成 <120 token 的高熵 AI 启动指令，用于冷启动新会话 |
| 🎛 **Parameterizable** | 支持 `optimizeFor` / `autoRepair` / `compress` / `silent` 标志 |
| 🌐 **VCS-agnostic** | 有 Git 时用 Git，无 Git 时优雅降级 |

---

## 🚀 Installation / 安装

### Claude Code
```bash
# 将 .skill 文件放入项目或全局 skills 目录
cp project-context-anchor.skill ~/.claude/skills/
```

### Claude.ai (Web / Desktop)
在 Settings → Skills → Upload 上传 `.skill` 文件即可。

---

## 💬 How to trigger / 如何触发

> **⚠️ 重要提示**：在 Claude Code 中，由于内置 memory 工具优先级较高，模糊指令（如"存档进度"）可能被 memory 工具抢先处理，导致 Skill 未被调用。**推荐始终使用明确指定 Skill 名称的方式触发。**
>
> **⚠️ Important**: In Claude Code, vague phrases like "save progress" may be intercepted by the built-in memory tool. **Always use explicit skill-name invocation for reliable triggering.**

### ✅ 推荐写法 / Recommended (Explicit)

```
# 中文 — 明确指定 Skill 名称（推荐）
使用 project-context-anchor skill 进行存档
用 project-context-anchor 存档当前进度
按照 project-context-anchor skill 写 AI_CONTEXT.md

# English — explicit skill invocation (recommended)
Use the project-context-anchor skill to snapshot this session
Run project-context-anchor skill and write AI_CONTEXT.md
```

### 🔶 模糊写法 / Implicit (may not trigger in Claude Code)

以下写法在 **Claude.ai 网页版**中可正常触发，但在 **Claude Code** 中可能被内置 memory 工具拦截：

```
存档当前进度 / Save my progress
我要下班了 / I'm done for today
封存这次会话 / Seal this session
token 快用完了，先存档 / We're near the token limit
```

---

## 📤 Cross-session resume / 跨会话恢复

新会话开始时，将生成的 `<AI_BOOTSTRAP_BLOCK>` 粘贴为第一条消息：

```
# 粘贴到新会话的第一条消息 / Paste as first message in new session:

PROJECT=my-app | STACK=React+FastAPI+Postgres | GOAL=fix race condition in useWebSocket cleanup
LAST_ACTION="feat: add JWT refresh endpoint"
DECISIONS=[stateless_jwt, no_redis_session]
TRAPS=[snake_case_routes, no_default_export_in_utils]
RESUME: Open `src/hooks/useWebSocket.ts` → find `cleanup` → continue unmount handler fix.
PENDING=[write_tests, update_openapi_spec]
```

新 Agent 读取后可立即接续工作，无需任何额外说明。

---

## 🗂 Output File Structure / 输出文件结构

生成的 `AI_CONTEXT.md` 包含五个标准章节：

```
1. 🚀 Project DNA        — 技术栈、架构风格、入口文件
2. 🛠 Current Status     — Git 分支、最近提交、未提交变更
3. 🧠 The Mental Model   — 关键决策、项目特有陷阱与约定
4. 📅 Active Plan        — 已完成 / 进行中 / 待办任务列表
5. ⚡ AI Bootstrap Block  — <120 token 的高密度冷启动指令
```

---

## ⚙️ Parameters / 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `optimizeFor=performance` | `detail` | 仅保留状态类章节（2、4、5），省略架构描述 |
| `autoRepair=false` | `true` | 关闭陈旧内容自愈，保留原文档 |
| `compress=false` | `true` | 不生成 `<AI_BOOTSTRAP_BLOCK>` |
| `silent=true` | `false` | 执行后只输出一行成功提示 |
| `fileName=custom.md` | `AI_CONTEXT.md` | 写入指定文件名 |

参数直接在对话中提及即可，例如：`"用 optimizeFor=performance 模式运行"`

---

## 🔒 Self-Healing Rules / 自愈规则

代码是唯一真相，文档描述现实而非意图：

| 冲突类型 | 处理规则 |
|---|---|
| 文档提到的文件已被删除 | 移除引用，添加 `~~删除线~~` 注记 |
| 函数 / 类已改名 | 以代码中的实际名称覆盖文档 |
| 架构描述与目录结构矛盾 | 以当前目录结构为准重写 |
| "下一步"任务已在 Git 中提交 | 标记 `[x] DONE`，移至 Recent Diff |

---

## 🔐 Security Notice / 安全提示

> ⚠️ **在提交或分享 `AI_CONTEXT.md` 之前，请务必检查以下内容：**
>
> ⚠️ **Before committing or sharing `AI_CONTEXT.md`, always review for:**

| 风险类型 | 说明 | 建议操作 |
|---|---|---|
| 🔑 API Keys / 密钥 | Bootstrap Block 可能从 `.env`、配置文件或近期对话中捕获敏感字串 | 提交前运行 `git diff` 检查，或使用 `git-secrets` / `trufflehog` 扫描 |
| 🗝 Tokens / 令牌 | Git 历史摘要中可能含有带 token 的 commit message | 确认 Recent Diff 章节中无明文凭证 |
| 📁 私有路径 | 内部服务器地址、数据库连接串可能出现在架构描述中 | 若文件需公开共享，手动脱敏后再提交 |
| 💬 会话内容 | Intent Extraction 阶段会摘录最近对话，可能含有业务敏感信息 | 在开放仓库中使用时，优先使用 `compress=false` 或 `silent=true` 精简输出 |

**推荐做法 / Recommended practice：**

```bash
# 提交前快速扫描 AI_CONTEXT.md 是否含有常见密钥模式
grep -iE "(api_key|secret|token|password|Bearer|sk-|pk-)" AI_CONTEXT.md
```

如发现敏感内容，将 `AI_CONTEXT.md` 加入 `.gitignore` 保持本地使用，或手动脱敏后再共享。  
If sensitive content is found, add `AI_CONTEXT.md` to `.gitignore` for local-only use, or redact before sharing.

---

## 📋 License / 许可证

MIT — 自由使用、修改和分发。  
MIT — Free to use, modify, and distribute.

---

<!-- ════════════ SKILL IMPLEMENTATION BELOW ════════════ -->

# Skill: `project-context-anchor` — Implementation

> **⚠️ OVERRIDE INSTRUCTION**: Do NOT use built-in memory tools (`write_memory`,
> `MEMORY.md`, `~/.claude/` paths) for this task. This skill writes `AI_CONTEXT.md`
> directly into the **current project root** (`./AI_CONTEXT.md`). Ignore any default
> memory-saving behavior and follow the phases below exclusively.
>
> **⚠️ 执行覆盖**：不得使用内置 memory 工具或写入 `~/.claude/` 路径。
> 本 Skill 的唯一输出目标是当前项目根目录下的 `./AI_CONTEXT.md`。

Generates and self-heals `AI_CONTEXT.md` at the project root — a high-density snapshot
that lets any future AI agent resume work with zero information loss.

**实现说明**：以下为 Claude 执行本 Skill 时遵循的内部协议。

---

## Execution Protocol / 执行协议

> Claude 按以下五个阶段顺序执行，任一命令失败时静默跳过，继续下一步。

### Phase 1 — Environment Scan / 环境扫描

Run the following in sequence. Tolerate failures silently (command may not exist).
依次运行以下命令，命令不存在时静默跳过。

```bash
# 1. Identify project root markers
ls package.json pyproject.toml Cargo.toml go.mod CMakeLists.txt README.md 2>/dev/null

# 2. Determine tech stack from key files
cat package.json 2>/dev/null | head -30
cat pyproject.toml 2>/dev/null | head -20

# 3. Directory structure (top 2 levels, exclude noise)
find . -maxdepth 2 \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/.next/*' \
  | sort

# 4. Recent git history (last 5 commits)
git log --oneline -5 2>/dev/null

# 5. Current uncommitted changes
git diff --stat HEAD 2>/dev/null || git status --short 2>/dev/null

# 6. Read existing AI_CONTEXT.md if present (for self-healing diff)
cat AI_CONTEXT.md 2>/dev/null
```

### Phase 2 — Intent Extraction / 意图提取

Review the **current conversation history** (last 5–10 messages). Extract:
回顾**当前会话的最近 5–10 条消息**，提取：

- What the user was trying to build or fix / 用户正在构建或修复什么
- Which files were touched and why / 涉及哪些文件及原因
- Any explicit decisions made ("we chose X over Y because…") / 明确的技术决策
- Open questions or blockers mentioned / 提到的未解问题或阻塞点

### Phase 3 — Self-Healing Check / 自愈检查 (`autoRepair`)

Compare the existing `AI_CONTEXT.md` (if found) against scan results:

| Conflict Type | Resolution Rule |
|---|---|
| File mentioned in doc no longer exists | Remove reference, add `~~strikethrough~~` note |
| Function/class renamed in code | Update doc to match code — code wins |
| Architecture claim contradicts directory structure | Overwrite with current reality |
| Stale "Next Steps" that are now committed | Mark `[x] DONE` and move to Recent Diff |

**Principle / 原则**: Code is ground truth. Docs describe reality, not intent.
**代码是唯一真相，文档描述现实，而非意图。**

### Phase 4 — Write `AI_CONTEXT.md` / 写入快照文件

**MANDATORY**: Use the `Write` file tool to create or overwrite `./AI_CONTEXT.md` in the
current project working directory. Do NOT use memory tools, do NOT write to `~/.claude/`.
The exact shell equivalent is:
```bash
# Target path — always relative to current project root
cat > ./AI_CONTEXT.md << 'EOF'
<generated content>
EOF
```

**强制要求**：使用 `Write` 文件工具将内容写入当前项目根目录的 `./AI_CONTEXT.md`。
禁止使用 memory 工具，禁止写入 `~/.claude/` 任何路径。

Replace all `$PLACEHOLDER` values with real extracted data. Never leave placeholders unfilled.
将所有 `$PLACEHOLDER` 替换为真实数据，不得留空。

---

## Standard Output Structure

```markdown
<!-- AI_CONTEXT_ANCHOR v1 | Last Synced: $ISO_DATETIME | Node: $LOCATION -->

# 🧩 AI Context Anchor

> **Project**: $PROJECT_NAME  
> **Last Synced**: $DATETIME  
> **Synced by**: Claude (`project_context_anchor` skill)

---

## 1. 🚀 Project DNA

**Goal**: $ONE_SENTENCE_MISSION

**Tech Stack**:
- Runtime: $RUNTIME (e.g., Node 20 / Python 3.12 / Rust 1.77)
- Framework: $FRAMEWORK
- Key deps: $TOP_3_DEPS

**Architecture Style**: $STYLE (e.g., "monorepo / microservices / CLI tool / SPA+API")

**Entry Points**:
- `$MAIN_FILE` — $WHAT_IT_DOES

---

## 2. 🛠 Current Status & Recent Diff

**Branch**: `$GIT_BRANCH`  
**Last 5 Commits**:
```
$GIT_LOG_ONELINE
```

**Uncommitted Changes** ($N files):
- `$FILE` — $WHAT_CHANGED

---

## 3. 🧠 The Mental Model

### Key Decisions
- **$DECISION_TITLE**: Chose `$APPROACH_A` over `$APPROACH_B` because $REASON.

### ⚠️ Traps & Conventions
- $ANTI_INTUITIVE_RULE_1
- $NAMING_CONVENTION_OR_GOTCHA

---

## 4. 📅 Active Plan

- [x] $COMPLETED_TASK
- [ ] $IN_PROGRESS_TASK ← **CURRENT FOCUS**
- [ ] $NEXT_TASK

---

## 5. ⚡ AI-to-AI Bootstrap Block

<AI_BOOTSTRAP_BLOCK>
PROJECT=$PROJECT_NAME | STACK=$STACK_FINGERPRINT | GOAL=$COMPRESSED_GOAL
LAST_ACTION="$LAST_COMMIT_MSG"
DECISIONS=[$DECISION_1_KEYWORD, $DECISION_2_KEYWORD]
TRAPS=[$TRAP_1_KEYWORD]
RESUME: Open `$MOST_RELEVANT_FILE` → find `$FUNCTION_OR_CLASS` → continue $TASK_DESCRIPTION.
PENDING=[$PENDING_1, $PENDING_2]
</AI_BOOTSTRAP_BLOCK>
```

---

## Phase 5 — Token Compression Algorithm / Token 压缩算法

The `<AI_BOOTSTRAP_BLOCK>` is generated as follows:
`<AI_BOOTSTRAP_BLOCK>` 按以下三步生成：

### Step 1: Semantic Dehydration / 语义脱水
Transform verbose prose into **key=value semantic fingerprints**:
将冗长的描述压缩为**键值对语义指纹**：
- Long decision rationale → `DECISIONS=[keyword1, keyword2]`
- Paragraphs of architecture → `STACK=React+FastAPI+Postgres`
- Trap descriptions → `TRAPS=[no_default_export, snake_case_routes]`

### Step 2: Locality Pointer / 局部性指针 (Cold-Start Hook / 冷启动钩子)
Identify the **single most important file + location** for the next agent to open:
找出下一个 Agent **最应打开的文件 + 函数位置**，编码为单行指令：
```
RESUME: Open `src/api/router.py` → find `handle_auth` → continue JWT refresh logic.
```
This encodes spatial context (file + symbol) so the agent skips the full scan and lands
directly at the relevant code.
这将空间上下文（文件 + 符号）编码为一行，让新 Agent 跳过全量扫描，直接落地到相关代码。

### Step 3: Entropy Maximization / 熵最大化
Prefer specific tokens over generic ones / 使用高特异性词汇，避免模糊表达：
- ❌ `GOAL=fix the bug` → ❌ low entropy
- ✅ `GOAL=fix race condition in useWebSocket cleanup on unmount` → ✅ high entropy

Target: **the bootstrap block should be under 120 tokens** while remaining unambiguous.
目标：**Bootstrap Block 压缩到 120 tokens 以内**，同时保持完全无歧义。

## Phase 6 — Verify Write / 验证写入

After writing, confirm the file exists in the project root:

```bash
# Verify AI_CONTEXT.md was written to the correct location
ls -lh ./AI_CONTEXT.md
head -3 ./AI_CONTEXT.md
```

If the file is missing or was written elsewhere, write it again using the `Write` tool
targeting `./AI_CONTEXT.md`. Never proceed to the Completion Response until this check passes.

写入后确认文件存在于项目根目录。若文件缺失或路径错误，立即用 `Write` 工具重新写入，
确认通过后再输出完成摘要。

---

## Parameters & Behavior Flags / 参数与行为标志

| Parameter / 参数 | Default / 默认 | Effect / 效果 |
|---|---|---|
| `optimizeFor=performance` | `detail` | 仅保留章节 2、4、5，省略架构和决策描述 |
| `autoRepair=false` | `true` | 跳过陈旧内容移除，保留原文档 |
| `compress=false` | `true` | 不生成 `<AI_BOOTSTRAP_BLOCK>` |
| `silent=true` | `false` | 写入后仅输出一行成功提示 |
| `fileName=custom.md` | `AI_CONTEXT.md` | 写入指定文件名 |

Parse these from the user's message if mentioned (e.g., `"用 optimizeFor=performance 运行"`).

---

## Completion Response / 完成响应 (default, `silent=false`)

After writing the file, reply with:
写入文件后，输出以下摘要：

```
✅ AI_CONTEXT.md updated.

**Snapshot Summary**
- Project: $NAME | Stack: $STACK
- Commits captured: $N | Uncommitted changes: $M files  
- Self-healed: $K stale entries removed
- Bootstrap block: $TOKEN_COUNT tokens

Next session: paste the <AI_BOOTSTRAP_BLOCK> as your first message to any AI.
```

If `silent=true`: reply only `✅ AI_CONTEXT.md updated.`

---

## Edge Cases / 边界情况

- **No git repo / 无 Git 仓库**: Skip all git steps. Note `(no VCS detected)` in section 2.
  跳过所有 Git 命令，在第 2 节注明 `(无版本控制系统)`。
- **Empty project / 空项目**: Write a minimal skeleton with `$PLACEHOLDERS` so the user can fill it.
  输出包含 `$PLACEHOLDER` 的最小骨架，供用户手动填写。
- **Heavy conflicts / 文档与代码严重冲突**: Rewrite entirely rather than patching;
  note `(full rewrite — $N stale entries removed)` in the summary.
  整体重写而非局部修补，在摘要中注明 `(全量重写 — 移除 $N 条陈旧记录)`。
- **No `optimizeFor` specified / 未指定模式**: Default to `detail` / 默认使用 `detail` 模式。
