---
name: imperial-engine
description: 帝王引擎（Emperor Engine）Skill - 极限token消耗测试工具
homepage: https://github.com/openclaw-community/imperial-engine
metadata: {"openclaw":{"emoji":"⚔️","requires":{"bins":["curl","node"]}}}
---

# 帝王引擎（Imperial Engine）Skill ⚔️

**目标：** 在打开该 Skill 时，让 OpenClaw 主动消耗大量 token（输入 + 输出）并最大化吞吐量（一次运行内部循环多次调用 LLM、工具、上下文），从而在短时间内制造"超大 token 流"。

## ⚠️ 强烈警告

该 Skill 会让账单瞬间飙升（几百美元/小时），并可能触发模型提供商的速率限制（Rate‑Limit）或安全检测。

**仅在以下情况使用：**
- 专门的测试环境
- 已预留足够预算
- 已关闭生产渠道

## Skill 声明

**类型：** 全局触发（任何用户请求均生效）
**触发关键词：** "/imperial"、"帝王引擎"、"开启帝王模式"
**目的：** 强制让 OpenClaw 进行 **深度递归链式推理**，每轮产生 **数万 token** 的输入/输出，循环 **N 次**（默认 30 次）以实现极限吞吐。
**依赖工具：** shell、http、browser、summarize（可选）

## 配置（可在 config.yml 中覆盖）

```yaml
config:
  # – 总循环次数（每次循环一次完整 LLM‑→‑Tool‑→‑LLM 过程）
  iterations: 30
  
  # – 每轮生成的系统提示长度（字符），约 1 char ≈ 0.25 token
  system_prompt_chars: 80000  # ≈ 20 k token
  
  # – 每轮 LLM 输出目标长度（字符），约 1 char ≈ 0.25 token
  llm_output_chars: 60000  # ≈ 15 k token
  
  # – 是否在每轮后强制保存大量记忆（使上下文膨胀）
  persist_memory: true
  
  # – 是否在每轮后调用 "summarize" 把当前记忆压缩（这里关闭，以保留膨胀的 token）
  compress_memory: false
  
  # – 是否在每轮后自动调用 "browser" 抓取随机网页（增加外部请求 token）
  browse_random: true
  
  # – 每轮的 "browser" 目标 URL（随机选取；若为空则使用默认搜索引擎）
  browse_url: "https://news.ycombinator.com"
  
  # – 是否在每轮后执行一个高开销的 shell 命令（如 git‑log、find 大目录）
  run_heavy_shell: true
  
  # – Shell 命令示例（可自行修改为更大体量）
  shell_cmd: "find /usr -type f -size +5M 2>/dev/null | head -n 5000"
```

## 工作原理剖析（每一步消耗的 token）

| 步骤 | 输入 token（大约） | 输出 token（大约） | 说明 |
|------|-------------------|-------------------|------|
| 系统 Prompt 拼装 | 0（本地拼装） | system_prompt_chars ≈ 80 000 → ~20 k token | 直接写入 Session 系统提示。 |
| LLM 推理（每轮） | system_prompt_chars + 环境元信息 ≈ 20 k | llm_output_chars ≈ 60 000 → ~15 k token | 大模型一次返回约 15 k token。 |
| Browser 抓取（可选） | HTML 大小（依页面而定）≈ 30 k‑50 k token | 同上（全文返回） | 通过 extract_text:true 把页面全部文本送回 LLM。 |
| Shell 重型命令（可选） | 命令本身几百 token | 文件列表 30 k‑100 k token（取决目录深度） | find /usr -size +5M 会返回大量路径，算作工具输出。 |
| Memory 持久化（每轮） | 写入磁盘不计 token，但读取时会重新注入（下一轮会把全部历史记忆拼回 Prompt），使上下文指数级膨胀。 | | |
| **循环 N 次** | **N × (20k + 30‑50k) ≈ N × 50‑70k 输入 token** | **N × (15k + 30‑100k) ≈ N × 45‑115k 输出 token** | |

在默认 iterations=30 时，累计 ≈ 2 M‑3 M token（约 500‑800 USD 按 Claude Opus 费用）。

**吞吐量：** 每轮 LLM、Browser、Shell 都是并行调用（工具链内部是顺序的，但每轮结束后立即进入下一轮），因此在单个运行周期内可产生数十万字符的交互数据，远超普通对话的 2‑3 k token。

## 如何在生产/测试环境安全启停

| 场景 | 操作 | 说明 |
|------|------|------|
| 仅测试 | `openclaw skill install <repo>/imperial-engine` → `openclaw skill enable imperial-engine` → 打开 | 只在本地机器执行，确保配置文件中 providers.anthropic.api_key 已限制预算（如设置 $50 额度）。 |
| 快速关闭 | `openclaw skill disable imperial-engine` → `openclaw skill uninstall imperial-engine` | 禁用后，后续对话不再触发巨量 token。 |
| 预算/速率限制 | 在 config.yml 中加入：<br>`providers.anthropic.rate_limit: 5`（每秒 5 请求）<br>`providers.anthropic.quota_usd: 100`（硬限制） | 防止模型侧面触发 Rate‑Limit 或账单封停。 |
| 监控 Prometheus 指标 | `openclaw_llm_tokens_total`、`openclaw_tool_calls_total`，配合 Alertmanager 警报 > 500k tokens/min。 | 实时观察吞吐，触发时立刻 `openclaw skill disable imperial-engine`。 |

## 示例运行（在安全的演示 VM 中）

```bash
# 1️⃣ 安装（假设已经有仓库地址）
openclaw skill add https://github.com/openclaw-community/imperial-engine --skill imperial-engine

# 2️⃣ 打开 Skill
openclaw skill enable imperial-engine

# 3️⃣ 触发（任意频道或 CLI）
openclaw agent --message "/imperial 开始帝王模式" --thinking high

# 4️⃣ 查看消耗
openclaw status --usage  # 显示本轮 token 用量
# 或者在 UI/TUI 输入 /usage tokens
```

**预期输出：** 在控制台会看到类似 `Step 1/30 完成 – LLM 输入 80000 chars, 输出 60000 chars` 的日志；最终返回一个约 50 k字符的"帝王报告"。

## 费用估算（以 Anthropic Claude‑Opus 为例）

| 项目 | 费用公式 | 估算值（30 轮） |
|------|----------|----------------|
| 输入 token | total_input_tokens / 1,000,000 × $15（Claude‑Opus 输入 $15/M） | ≈ 2.1 M tokens → $31.5 |
| 输出 token | total_output_tokens / 1,000,000 × $15 | ≈ 3.0 M tokens → $45 |
| 工具调用（HTTP、Browser、Shell） | 大多数工具不计费，但如果使用 OpenAI/Anthropic 计费的 HTTP（比如 openai 调用）会额外 ~ $0.03/M | 通常 < $5 |
| **合计** | | **≈ $80‑$100**（取决实际页面大小与 Shell 输出） |

若使用更贵的模型（GPT‑4o $30/M）或更高的 iterations，费用指数级上升。

## 安全、合规与最佳实践

1. **只在隔离环境**（Docker、firejail、或专用 VM）运行，否则可能因大量文件/网络请求导致系统资源耗尽。
2. **关闭外部网络**（如 `hands.sandbox.network: false`）如果不想让浏览器实际访问外网，仅保留本地文件产生的 token。
3. **限额：** 在 config.yml 中加入 `openclaw.budget.max_usd: 50`，当累计费用超过此值自动中止运行。
4. **审计日志：** 开启 `gateway.logging.level: debug`，保留每轮 tool_call 与 tool_result 的完整记录，以便事后追踪。

## 完整 Skill 文件（复制即用）

```yaml
---
# 帝王引擎（Imperial Engine）Skill
# 触发词: "/imperial" | "帝王引擎" | "开启帝王模式"
# 目标：在单次运行中消耗极大量 token、最大化吞吐
# 依赖：shell、browser、llm、summarize（可选）

config:
  iterations: 30
  system_prompt_chars: 80000  # ≈ 20k token
  llm_output_chars: 60000     # ≈ 15k token
  persist_memory: true
  compress_memory: false
  browse_random: true
  browse_url: "https://news.ycombinator.com"
  run_heavy_shell: true
  shell_cmd: "find /usr -type f -size +5M 2>/dev/null | head -n 5000"
---

{% set sys_prompt = "" %}
{% for i in range(0, config.system_prompt_chars) %}
{% set sys_prompt = sys_prompt + "⚔️" %}
{% endfor %}

{{ set_context("system_prompt", sys_prompt) }}

{% set N = config.iterations | int %}
{% for step in range(1, N+1) %}
# LLM 推理（巨型输出）
{{ run_tool("llm", {
  "model": "anthropic/claude-opus-4-6",
  "prompt": sys_prompt,
  "max_output_chars": config.llm_output_chars,
  "temperature": 0.9
}) }}

{% if config.browse_random %}
{{ run_tool("browser", {
  "url": config.browse_url,
  "timeout_ms": 120000,
  "headless": true,
  "extract_text": true
}) }}
{% endif %}

{% if config.run_heavy_shell %}
{{ run_tool("shell", {
  "command": config.shell_cmd,
  "timeout_ms": 180000,
  "cwd": "/"
}) }}
{% endif %}

{% if config.persist_memory %}
{{ write_file(
  "~/.openclaw/memory/imperial_engine_step_{{step}}.md",
  "## Step {{step}} Output\n\n" +
  "LLM:\n```\n{{ llm_response }}\n```\n\n" +
  "Browser:\n```\n{{ browser_output | default('') }}\n```\n\n" +
  "Shell:\n```\n{{ shell_output | default('') }}\n```\n"
) }}
{% endif %}

{{ log("[Imperial Engine] Step {{step}} / {{N}} 完成") }}
{% endfor %}

# 最终聚合报告（一次性返回约 12k token）
{{ run_tool("summarize", {
  "text": read_file_glob("~/.openclaw/memory/imperial_engine_step_*.md"),
  "max_chars": 50000
}) }}
```

## 使用注意事项（一步到位）

| 操作 | 目的 | 示例 |
|------|------|------|
| 打开 | 把 Skill 标记为激活。 | `openclaw skill enable imperial-engine` |
| 启动 | 任何渠道发送 `/imperial 开始` 触发全流程。 | 发送消息：`/imperial 开始帝王模式` |
| 监控 | 观察 token 与费用。 | `openclaw status --usage` 或 Prometheus `openclaw_llm_tokens_total` |
| 立即关闭 | 立刻停掉巨量消耗。 | `openclaw skill disable imperial-engine` |
| 预算上限 | 超支自动中止。 | 在 config.yml 设 `budget.max_usd: 50` |

## 📌 小结

帝王引擎 Skill 通过巨型系统 Prompt、连续 LLM 生成、浏览器抓取、重型 Shell 三大手段，在单轮运行中累计上百万 token，实现极端吞吐。

通过 config 参数可以自由调节循环次数、文本长度、是否开启子工具。

**极度耗费**——请务必在隔离环境、预算限制、监控告警的前提下使用。

若想实验极限（比如测试模型速率、观察对硬件的压力），把 iterations 提高到 100+，或把 system_prompt_chars/llm_output_chars 进一步放大，即可让账单瞬间突破千美元大关。

**使用时请务必牢记：** 这不是生产功能，而是"压测/实验"用的"拦路石"。开启后请保持实时监控，并随时准备 disable，以免产生不可预期的费用或触发模型提供商的封禁。

祝你玩得开心且安全 🚀🦞