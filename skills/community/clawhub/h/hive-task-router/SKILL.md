---
name: Hive Task Router
slug: hive-task-router
version: 1.0.0
description: Intelligent task routing system that identifies task types (web/code/data/doc/chat) and routes to optimal models with appropriate execution mode (subagent/main session). Supports any AI model provider via environment variables.
author: qiongcao
requires:
  - openclaw-cli
  - bash
os:
  - darwin
  - linux
  - windows-wsl
tags:
  - routing
  - task-management
  - subagent
  - productivity
  - multi-provider
---

# Hive Task Router

**Smart task distribution system for OpenClaw** — Automatically routes tasks to optimal models and execution modes based on task type recognition.

**Universal Model Support** — Works with any AI model provider (Bailian, OpenAI, Anthropic, etc.) via environment variable configuration.

---

## When to Use

### Automatic Trigger Rules (For AI Agents)

**Use this skill automatically when the user's message contains ANY of these patterns:**

| Trigger Pattern | Keywords | Action |
|----------------|----------|--------|
| **Code tasks** | 代码、编程、脚本、函数、nodejs、react、vue、typescript、javascript、html、css、前端、后端、api、接口、调试、bug、优化、重构 | Run `router.sh` → Execute with `code` model + subagent |
| **Web research** | 搜索、查找、调研、研究、github、项目、趋势、报告、分析、对比、评测、最新、2026、新闻、动态 | Run `router.sh` → Execute with `web` model + subagent |
| **Data tasks** | 数据、分析、统计、图表、可视化、excel、csv、json、处理、转换 | Run `router.sh` → Execute with `data` model + subagent |
| **Documentation** | 文档、说明、教程、指南、手册、readme、wiki、注释、文档化 | Run `router.sh` → Execute with `doc` model + subagent |
| **Batch tasks** | 多个、批量、同时、并行、一起 | Run `router.sh` for each → Execute in parallel |

**Do NOT use this skill when:**
- Simple chat/conversation (你好、谢谢、安排、计划、汇报、总结)
- Quick questions (what is, how to, explain)
- Tasks already in progress
- User explicitly says "don't use subagent" or "just answer directly"

### Manual Trigger (For Users)

**Users can explicitly trigger this skill by:**
- Running `router.sh "task description"` directly
- Saying "use hive router" or "analyze this task"
- Asking "which model should I use for this task"

### Decision Flow for AI Agents

```
Receive user message
    ↓
Contains specific trigger keywords? (code/web/data/doc/batch)
    ↓
YES → Run router.sh to analyze
    ↓
Get recommended model + execution mode
    ↓
Execute with recommended configuration
    ↓
Report result to user
    ↓
NO → Check for vague task keywords? (任务、帮忙、处理、搞定、完成)
    ↓
YES → Ask clarifying question (see "Vague Task Handling")
    ↓
User clarifies → Re-analyze with new info
    ↓
NO → Handle directly (no routing needed)
```

### Vague Task Handling

**When user message is vague** (e.g., "做个任务", "帮忙处理一下", "搞定这件事"):

**Step 1: Acknowledge and ask**
```
好的主人，请问是什么类型的任务？

💻 写代码/脚本？
   - 例如："写个 Python 脚本"、"开发一个 API"

🔍 搜索调研？
   - 例如："搜索最新趋势"、"调研竞品"

📊 数据处理？
   - 例如："分析 Excel 数据"、"转换 JSON 格式"

📄 写文档？
   - 例如："写 API 文档"、"编写教程"

💬 还是只是聊天？
   - 例如："今天有什么安排"、"帮我总结一下"

或者您直接告诉我具体内容，我来判断！
```

**Step 2: User clarifies**
```
User: "写个脚本处理数据"
  ↓
Now contains: "脚本" (code) + "数据" (data)
  ↓
Priority: code > data
  ↓
Execute with: qwen3-coder-plus + subagent
```

**Vague Keywords (trigger clarification):**
- 任务、帮忙、处理、搞定、完成、做一下、弄一下
- 这个、那个、一件事、一个东西

**Specific Keywords (trigger automatic routing):**
- code: 脚本、代码、编程、函数、nodejs、react...
- web: 搜索、调研、分析、趋势、报告、对比...
- data: 数据、统计、图表、excel、csv、json...
- doc: 文档、教程、指南、readme、wiki...

**Ideal scenarios:**
- Handling multiple concurrent tasks
- Technical development requiring code-specialized models
- Research tasks needing web search capabilities
- Mixed workloads with varying complexity
- Multi-provider environments (Bailian + OpenAI + Anthropic)

---

## Quick Reference

### Task Type Recognition Keywords

| Type | Keywords (Chinese) | Keywords (English) | Priority |
|------|-------------------|-------------------|----------|
| **web** 🔍 | 搜索、查找、调研、研究、github、项目、趋势、报告、分析、对比、评测、最新、2026、新闻、动态 | search, research, github, project, trend, report, analysis, comparison, latest, news | 1 (Highest) |
| **code** 💻 | 代码、编程、脚本、函数、nodejs、react、vue、typescript、javascript、html、css、前端、后端、api、接口、调试、bug、优化、重构 | code, programming, script, function, nodejs, react, vue, typescript, javascript, html, css, frontend, backend, api, debug, bug, optimize, refactor | 2 |
| **data** 📊 | 数据、分析、统计、图表、可视化、excel、csv、json、处理、转换 | data, analysis, statistics, chart, visualization, excel, csv, json, processing, conversion | 3 |
| **doc** 📄 | 文档、说明、教程、指南、手册、readme、wiki、注释、文档化 | documentation, guide, tutorial, manual, readme, wiki, comment, document | 4 |
| **chat** 💬 | 你好、谢谢、再见、今天、明天、安排、计划、汇报、总结、提醒、备忘 | hello, thanks, goodbye, today, tomorrow, plan, schedule, summary, reminder, memo | 5 (Default) |

### Model Selection Rules

**Note:** Model IDs are configurable via environment variables. Replace `provider/` with your actual model provider (e.g., `bailian/`, `openai/`, `anthropic/`).

| Task Type | Default Model | Environment Variable | Reason |
|-----------|--------------|---------------------|--------|
| **code** | `provider/qwen3-coder-plus` | `HIVE_MODEL_CODE` | Specialized in code generation and debugging |
| **web** | `provider/qwen3-max` | `HIVE_MODEL_WEB` | Strong search and reasoning capabilities |
| **data** | `provider/qwen3-coder-plus` | `HIVE_MODEL_DATA` | Code-based data processing |
| **doc** | `provider/qwen3.5-plus` | `HIVE_MODEL_DOC` | Good text generation, cost-effective |
| **chat** | `provider/qwen3.5-plus` | `HIVE_MODEL_CHAT` | Best for casual conversation, cost-effective |

### Model Configuration Examples

**Bailian (通义千问):**
```bash
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
export HIVE_MODEL_DOC="bailian/qwen3.5-plus"
export HIVE_MODEL_DATA="bailian/qwen3-coder-plus"
```

### Model Validation Modes

**Automatic Model Detection (Recommended):**

```bash
# Auto-detect available models from OpenClaw
export HIVE_VALIDATE_MODEL=auto
```

**First run:** Detects models and caches configuration  
**Subsequent runs:** Uses cached config (24h TTL)  
**Benefit:** No manual configuration needed!

**Manual Validation Modes:**

| Mode | Environment Variable | Behavior | Use Case |
|------|---------------------|----------|----------|
| **Auto (Recommended)** | `export HIVE_VALIDATE_MODEL=auto` | Auto-detect + cache 24h | **Best for most users** |
| **Cache** | `export HIVE_VALIDATE_MODEL=cache` | Validate once, cache 24h | Manual config, stable |
| **Always** | `export HIVE_VALIDATE_MODEL=1` | Validate every execution | Debugging, changes |
| **Never** | `export HIVE_VALIDATE_MODEL=0` | Skip validation | Production, known config |

**Cache Configuration:**
```bash
# Cache directory (default: ~/.hive-task-router)
export HIVE_CACHE_DIR="$HOME/.hive-task-router"

# Cache TTL in seconds (default: 86400 = 24 hours)
export HIVE_CACHE_TTL=86400
```

**Validation Behavior:**
- ✅ Checks if model IDs contain `provider/` placeholder
- ✅ Warns if placeholder detected
- ✅ Caches validation result (configurable TTL)
- ✅ Non-blocking (warnings only, doesn't stop execution)

**OpenAI:**
```bash
export HIVE_MODEL_CODE="openai/gpt-4"
export HIVE_MODEL_WEB="openai/gpt-4-turbo"
export HIVE_MODEL_CHAT="openai/gpt-3.5-turbo"
export HIVE_MODEL_DOC="openai/gpt-3.5-turbo"
export HIVE_MODEL_DATA="openai/gpt-4"
```

**Anthropic (Claude):**
```bash
export HIVE_MODEL_CODE="anthropic/claude-3-5-sonnet"
export HIVE_MODEL_WEB="anthropic/claude-3-opus"
export HIVE_MODEL_CHAT="anthropic/claude-3-haiku"
export HIVE_MODEL_DOC="anthropic/claude-3-haiku"
export HIVE_MODEL_DATA="anthropic/claude-3-5-sonnet"
```

**Mixed Providers:**
```bash
# Use best model for each task type
export HIVE_MODEL_CODE="anthropic/claude-3-5-sonnet"  # Best for code
export HIVE_MODEL_WEB="openai/gpt-4-turbo"           # Best for search
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"        # Cost-effective
```

### Execution Mode Rules

| Task Type | Execution Mode | Reason |
|-----------|---------------|--------|
| **chat** | Main Session | Quick response, no need for isolation |
| **code/web/data/doc** | Subagent | Long-running tasks, parallel execution, session isolation |

**Priority Rule:** When multiple keywords match, use the highest priority type (web > code > data > doc > chat).

---

## Usage

### For AI Agents (Automatic Integration)

**When installed as an OpenClaw Skill**, the agent will automatically use this skill when:

1. **User message contains task keywords** (code/web/data/doc/batch)
2. **Task is long-running** (not a simple Q&A)
3. **Multiple tasks** need parallel execution

**Agent Decision Example:**
```
User: "帮我写一个 Python 脚本处理 Excel 数据"
  ↓
Agent checks: Contains "脚本" (code) + "数据" (data)
  ↓
Priority: code > data
  ↓
Agent executes:
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-coder-plus \
  --task "帮我写一个 Python 脚本处理 Excel 数据"
```

**Configuration for Agents:**
Add to agent's `AGENTS.md` or `SOUL.md`:
```markdown
## Hive Task Router Integration

When receiving tasks:
1. Check if message contains task keywords (see SKILL.md)
2. If yes → Use hive-task-router skill
3. If no → Handle directly
```

---

### Method 1: Router Script (Recommended)

The router script automatically analyzes tasks and outputs recommended execution commands.

```bash
# Basic usage
bash router.sh "帮我写一个 Node.js 脚本"

# Analyze research task
bash router.sh "搜索 2026 年最新的前端趋势"

# Analyze data task
bash router.sh "分析这个 JSON 数据并生成图表"
```

**Output format:**
```
================================
蜂巢智能任务分发系统 - 路由分析
================================

任务描述：帮我写一个 Node.js 脚本
任务类型：code
推荐模型：bailian/qwen3-coder-plus
执行方式：subagent

📦 代码任务 - 使用 qwen3-coder-plus 模型
   适合：Node.js、前端代码、脚本编写

================================
推荐执行命令:
================================

openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-coder-plus \
  --task "帮我写一个 Node.js 脚本"
```

### Method 2: Manual Commands

#### Code Tasks
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-coder-plus \
  --task "帮我写一个 Express API 服务"
```

#### Web Research Tasks
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-max-2026-01-23 \
  --task "调研 5 个 React UI 库"
```

#### Chat Tasks (Main Session)
```bash
openclaw agent \
  --session-id agent:main:chat \
  --model bailian/qwen3.5-plus \
  --message "今天有什么安排"
```

#### Data Processing Tasks
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-coder-plus \
  --task "处理这个 CSV 文件并生成统计报告"
```

#### Documentation Tasks
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3.5-plus \
  --task "为这个项目编写 README 文档"
```

### Method 3: Parallel Execution

For batch tasks, use parallel subagents:

```bash
# Spawn multiple subagents concurrently
openclaw sessions spawn --mode run --runtime subagent --model bailian/qwen3-max-2026-01-23 --task "调研项目 A" &
openclaw sessions spawn --mode run --runtime subagent --model bailian/qwen3-max-2026-01-23 --task "调研项目 B" &
openclaw sessions spawn --mode run --runtime subagent --model bailian/qwen3-max-2026-01-23 --task "调研项目 C" &

# Wait for all to complete
wait

# Then collect and summarize results
```

---

## Examples

### Example 1: Code Development Task

**User Input:**
```
帮我写一个 Node.js 文件处理脚本，支持读取 CSV 和 JSON 格式
```

**Router Analysis:**
- **Matched Keywords:** Node.js, 脚本，文件处理
- **Task Type:** code
- **Recommended Model:** bailian/qwen3-coder-plus
- **Execution Mode:** subagent

**Execution Command:**
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-coder-plus \
  --task "帮我写一个 Node.js 文件处理脚本，支持读取 CSV 和 JSON 格式"
```

---

### Example 2: Web Research Task

**User Input:**
```
搜索 2026 年最新的前端趋势，包括 React、Vue、Svelte 的对比
```

**Router Analysis:**
- **Matched Keywords:** 搜索，2026, 趋势，对比
- **Task Type:** web (Priority 1)
- **Recommended Model:** bailian/qwen3-max-2026-01-23
- **Execution Mode:** subagent

**Execution Command:**
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-max-2026-01-23 \
  --task "搜索 2026 年最新的前端趋势，包括 React、Vue、Svelte 的对比"
```

---

### Example 3: Daily Chat Task

**User Input:**
```
今天有什么安排？帮我总结一下昨天的工作
```

**Router Analysis:**
- **Matched Keywords:** 今天，安排，总结
- **Task Type:** chat
- **Recommended Model:** bailian/qwen3.5-plus
- **Execution Mode:** main_session

**Execution Command:**
```bash
openclaw agent \
  --session-id agent:main:chat \
  --model bailian/qwen3.5-plus \
  --message "今天有什么安排？帮我总结一下昨天的工作"
```

---

### Example 4: Data Analysis Task

**User Input:**
```
分析这个销售数据 Excel 文件，生成可视化图表和统计报告
```

**Router Analysis:**
- **Matched Keywords:** 分析，数据，Excel, 图表，统计
- **Task Type:** data
- **Recommended Model:** bailian/qwen3-coder-plus
- **Execution Mode:** subagent

**Execution Command:**
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3-coder-plus \
  --task "分析这个销售数据 Excel 文件，生成可视化图表和统计报告"
```

---

### Example 5: Documentation Task

**User Input:**
```
为这个 Python 项目编写完整的 API 文档和使用教程
```

**Router Analysis:**
- **Matched Keywords:** 文档，教程
- **Task Type:** doc
- **Recommended Model:** bailian/qwen3.5-plus
- **Execution Mode:** subagent

**Execution Command:**
```bash
openclaw sessions spawn \
  --mode run \
  --runtime subagent \
  --model bailian/qwen3.5-plus \
  --task "为这个 Python 项目编写完整的 API 文档和使用教程"
```

---

### Example 6: Mixed Task Batch (Parallel)

**User Input (Multiple Tasks):**
```
1. 写个脚本处理 JSON 数据
2. 搜索最新 AI 工具
3. 今天有什么安排
```

**Router Analysis:**
- Task 1: code → qwen3-coder-plus + subagent
- Task 2: web → qwen3-max-2026-01-23 + subagent
- Task 3: chat → qwen3.5-plus + main_session

**Parallel Execution:**
```bash
# Task 1 & 2 run in parallel subagents
openclaw sessions spawn --mode run --runtime subagent --model bailian/qwen3-coder-plus --task "写个脚本处理 JSON 数据" &
openclaw sessions spawn --mode run --runtime subagent --model bailian/qwen3-max-2026-01-23 --task "搜索最新 AI 工具" &

# Task 3 runs in main session (non-blocking)
openclaw agent --session-id agent:main:chat --model bailian/qwen3.5-plus --message "今天有什么安排"

# Wait for subagents
wait
```

**Performance:** 3x faster than sequential execution

---

## Installation

### Install via ClawHub

```bash
clawhub install qiongcao/hive-task-router
```

### Manual Installation

1. Clone or download this skill folder
2. Copy to your OpenClaw skills directory:
   ```bash
   cp -r hive-task-router ~/.openclaw/workspace/skills/
   ```
3. Make router script executable:
   ```bash
   chmod +x ~/.openclaw/workspace/skills/hive-task-router/router.sh
   ```
4. Configure models for your provider:
   ```bash
   export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
   export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
   export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
   ```

---

## Configuration

### Prerequisites

- OpenClaw CLI installed
- Bash shell available
- Models configured (adjust for your provider):
  - Code model (e.g., `bailian/qwen3-coder-plus`)
  - Web model (e.g., `bailian/qwen3-max-2026-01-23`)
  - Chat model (e.g., `bailian/qwen3.5-plus`)

### Environment Variables

Optional environment variables for customization:

```bash
# Model overrides (required)
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
export HIVE_MODEL_DOC="bailian/qwen3.5-plus"
export HIVE_MODEL_DATA="bailian/qwen3-coder-plus"

# Optional: custom session IDs
export HIVE_SESSION_CODE="custom:code:session"
export HIVE_SESSION_WEB="custom:web:session"
export HIVE_SESSION_CHAT="custom:chat:session"

# Optional: concurrency limit
export HIVE_MAX_CONCURRENT=10
```

### Verify Setup

```bash
# Check models
openclaw models list | grep bailian

# Test router script
bash router.sh "测试任务"

# Verify environment variables
echo $HIVE_MODEL_CODE
echo $HIVE_MODEL_WEB
```

---

## Troubleshooting

### Issue 1: Router script not found

```bash
# Make sure script is executable
chmod +x router.sh

# Run with full path
bash /path/to/router.sh "task"
```

### Issue 2: Model not available

```bash
# Check available models
openclaw models list

# Update environment variables with available models
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
```

### Issue 3: Task type misidentified

```bash
# Add more specific keywords to router.sh
# Edit CODE_KEYWORDS, WEB_KEYWORDS, etc.
```

### Issue 4: Wrong model used

```bash
# Verify environment variables are set
echo $HIVE_MODEL_CODE
echo $HIVE_MODEL_WEB

# Set them explicitly before running router.sh
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
bash router.sh "task"
```

---

## Best Practices

1. **Task Distribution Principles**
   - ✅ Short tasks → Main session
   - ✅ Long tasks → Subagent
   - ✅ Batch tasks → Multiple parallel subagents
   - ✅ Fixed types → Session isolation + specialized models

2. **Model Selection**
   - Use code-specialized models for programming tasks
   - Use reasoning models for research tasks
   - Use cost-effective models for chat tasks
   - Mix providers for best-in-class results

3. **Concurrency Control**
   - Recommended max concurrent subagents: **5-10**
   - For 10+ tasks → Execute in batches
   - Monitor API quota usage

4. **Environment Management**
   - Set environment variables in `.bashrc` or `.zshrc`
   - Use different configs for different projects
   - Document your model choices

---

## Performance

| Metric | Traditional | Hive Router | Improvement |
|--------|-------------|-------------|-------------|
| 3 project research | ~180s | ~60s | **3x** ⚡ |
| Model utilization | Single model | Multi-model | Flexible |
| Task routing | Manual | Automatic | Intelligent |
| Multi-provider | Manual switching | Auto config | Seamless |

---

## Provider Compatibility

| Provider | Status | Notes |
|----------|--------|-------|
| **Bailian (通义千问)** | ✅ Tested | Default configuration |
| **OpenAI (GPT)** | ✅ Compatible | Set HIVE_MODEL_* variables |
| **Anthropic (Claude)** | ✅ Compatible | Set HIVE_MODEL_* variables |
| **Google (Gemini)** | ✅ Compatible | Set HIVE_MODEL_* variables |
| **Other OpenAI-compatible** | ✅ Compatible | Use provider/ prefix |

---

## License

MIT License - Feel free to use and modify.

---

*Author: qiongcao*  
*Version: 1.0.0*  
*Last Updated: 2026-03-12*  
*Universal Model Support: Yes*
