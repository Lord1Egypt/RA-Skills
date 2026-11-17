---
name: linkfox-os
description: linkfox-os — Cross-border e-commerce AI agent system with 6 specialized agents covering the full seller workflow: (1) General Assistant (default) — platform data queries across Amazon/TikTok Shop/eBay/Walmart/Shopee/Ozon, Keepa/SIF/SellerSprite analytics, Google Trends, 1688 sourcing, patent/IP search, PDF analysis, web search; (2) Market Analysis Agent (linkfox-market-analysis-agent) — 5-dimension market research (market overview, competitor analysis, review mining, keyword research, compliance detection), structured HTML reports; (3) Product Selection Agent (linkfox-product-selection-agent) — keyword-based selection, viral product prediction, condition-based filtering, benchmark selection across 7 platforms, risk assessment; (4) Listing Agent (linkfox-listing-agent) — Amazon Listing creation/optimization/scoring (benchmark, rewrite, create, batch modes), keyword matrix, compliance scan; (5) Image Agent (linkfox-image-agent) — product/cloth image collections, image fission, bestseller replication, mannequin-to-model, white background, scene, selling point, A+, model, close-up images; (6) Video Agent (linkfox-video-agent) — image-to-video, AI sales talking video, viral video replication. Use when: product selection, market analysis, competitor research, keyword research, review mining, Listing writing/optimization, product image generation, video generation, IP/patent detection, trend analysis, 1688 sourcing, cross-platform data queries, or any multi-step e-commerce workflow. **内置账号引导（onboarding）**：未配置 API key / 鉴权失败（401）/ 计费不足（402 或消息含'积分余额不足/余额不足/请充值/quota exceeded/insufficient balance'）时，自动进入引导流程——脚本化手机号注册取 key、列套餐、生成支付二维码，见 references/onboarding.md。用户说'没配 key/鉴权失败/积分不足/充值/recharge/注册/手机号注册'也触发。**用户素材上传（File Upload）**：用户先提供本地图片/文档/视频给下游 agent 使用时（触发短语：'我有一张参考图 / 帮我上传商品图 / 帮我传一份文档 / 附一份参考视频 / 用这张图生成…'），走 `<skill>/scripts/upload/upload_file.py` 拿到 `file://` 虚拟路径后塞进下一步 prompt，见 SKILL.md §14。
metadata: {"linkfox-os":{"homepage":"https://os.linkfox.com/","requires":{"env":["LINKFOXAGENT_API_KEY"]}}}
---

# linkfox-os — Cross-border E-commerce AI Agent System

**linkfox-os** submits a prompt to the LinkFox async task pipeline and polls for the result. It dispatches each task to one of **6 specialized AI agents**, each with its own toolchain, context, and multi-step orchestration logic — together covering the full cross-border e-commerce seller workflow.

---

## 0. Output Rules (MANDATORY)

**禁止输出任何 emoji / 表情符号 / 图形字符**（包括但不限于笑脸、勾叉、纸夹、文件夹、灯泡、警告标志、旗帜、动物等 Unicode emoji）。

- 转发本 skill 产出的进度行、结果 chunk、数据文件段时，若上游意外携带 emoji，**必须先剥离再输出**给用户。
- 结构化前缀一律使用文本标签：`[思考]` / `[工具]` / `[消息]` / `[文件]` / `[本地]`，**不得**用任何 emoji 替代（如"想"、"扳手"、"对话气泡"、"纸夹"、"文件夹"图标一律禁用）。
- 不要用 emoji 做要点符号、状态标记（勾/叉）或装饰。列表用 `-`，"错误示例"直接写 `WRONG:`。

---

## 1. When to use

Trigger this skill when the user needs any of:

- **平台数据查询** — Amazon / TikTok Shop / eBay / Walmart / Shopee / Ozon 商品搜索、详情、评论；Keepa、SIF、SellerSprite、ABA、店雷达、Google Trends
- **市场分析** — 完整 5 维度市场调研（市场初步 / 竞品 / 评论 / 关键词 / 合规），结构化 HTML 报告
- **选品** — 关键词选品、条件选品、潜在爆款预测、对标选品；覆盖 Amazon / TikTok Shop / Shopee / Ozon / Walmart / eBay / 1688 七大平台
- **Listing 撰写与优化** — 亚马逊 Listing 对标复刻 / 诊断优化 / 新建 / 批量生成 / 质量评分
- **商品出图** — 白底图、场景图、卖点图、A+ 图、特写图、模特图、尺码图、图片裂变、爆款复刻、人台换模特
- **视频生成** — 图转视频（含首尾帧）、带货口播、爆款视频复刻
- **合规 / 供应链 / 趋势** — 外观/发明专利、商标、版权检测；1688 以图搜图 & 供应商查找；Google Trends / TikTok 热销榜 / 亚马逊 BSR
- **通用工作流** — Excel / PDF 分析、Python 沙箱、Tavily 网页搜索、多步骤跨平台数据串联

**Do NOT use** for interactive multi-turn chat — this is a one-shot async task pipeline (每次 1–5 min)，不适合追问式对话。

---

## 2. Available Capabilities (6 Specialized Agents)

Each task is routed to one specialized Agent via `--model <modelId>`. Omit `--model` to let the platform default-route to the general assistant.

> **不确定用哪个 agent？直接 `default`（省略 `--model`）**。default 是主 agent，聚合了 92 个 skill——所有数据查询、IP 检索、底层生图/生视频、通用工具都在里面。专业 agent 只是在此之上叠了针对性的编排 pipeline：
>
> - `linkfox-market-analysis-agent` 独占 7 个 5 维度市场分析 skill（`linkfox-market-*` / `product-proposal`）
> - `linkfox-product-selection-agent` 独占 5 个端到端选品流程 skill（`linkfox-keyword-select` / `viral-predict` / `condition-selection` / `benchmark` / `cross-platform`）
> - `linkfox-listing-agent` 独占 22 个 Listing L1-L5 pipeline skill（`listing-*`）
> - `linkfox-image-agent` 独占 3 个高级出图（`bestseller-replicate` / `image-fission` / `mannequin-to-model`）
> - `linkfox-video-agent` 覆盖底层 videogen（default 也有）
>
> **规则**：只要用户没明确要"编排型报告"或"完整流水线"，就用 `default`——不会漏能力。真要用编排 skill 时才切专业 agent。每个 skill 的用途 / 入参 / 返回详细参考 `references/skills-*.md`（8 个文件，按主题分桶）。

| modelId | Agent | 核心能力（简述） |
|---------|-------|-----------------|
| `default` | 通用智能助手 | 全域业务 skill：平台数据查询、市场分析、选品调研、关键词研究、Listing 撰写、图片/视频生成、IP 检索、1688 供应链、Google Trends、Tavily 搜索、Excel/PDF/Python 沙箱。适合快速数据查询与多 skill 编排。 |
| `linkfox-market-analysis-agent` | 市场分析 Agent | 顶级咨询公司级别的亚马逊细分市场分析师。5 维度（市场初步/竞品/评论/关键词/合规）分析，三种模式：**编排型**全链路 HTML 报告、**聚焦型**单/多维分析、**工具查询型**（用户提到具体指标时优先）。60+ 可调用 skill。 |
| `linkfox-product-selection-agent` | 选品 Agent | 跨境电商选品专家，覆盖 7 平台。4 种自有选品流程：`关键词选品` / `潜在爆款预测` / `条件选品` / `对标选品`。约束条件（平台/市场/运营方式/预算/供应链）→ 契合产品输出。取数预算 ≤7 次 API 调用，端到端一次跑完。 |
| `linkfox-listing-agent` | Listing Agent | 亚马逊 Listing 运营官。5 种模式：`benchmark` 对标复刻 / `rewrite` 诊断优化 / `create` 新建 / `batch` 批量 / `report` 质量评分。L1-L5 pipeline（输入 → 采集 → 关键词矩阵 → 文案 → 质量门 → HTML 报告）。符合 Amazon 2026 政策（Title≤75c、Item Highlights≤125c）。 |
| `linkfox-image-agent` | 图片 Agent | 电商出图总编排。路由到 6 条出图链路：`商品套图` / `服饰套图` / `图片裂变` / `爆款复刻` / `人台换模特` / `底层自由做图`。可产白底 / 场景 / 卖点 / A+（Premium/Standard/Phone）/ 特写 / 模特 / 尺码图。支持 BANANA_PRO / GPT_2_IMAGE / SEEDREAM5 等 6 种模型。 |
| `linkfox-video-agent` | 视频 Agent | 电商视频总编排。3 条链路：`图转视频`（参考图 / 首尾帧）/ `带货口播`（先出 3 套方案 → 用户选择 → 生成）/ `爆款视频复刻`（参考视频 + 商品图 → 同款结构短视频）。 |

### 快速选择（用户话术 → 推荐 modelId）

| 用户意图 | 推荐 modelId |
|---------|-------------|
| 查价格 / 销量 / 关键词 / Keepa / 评论列表 / 一次性数据取数 | `default` |
| 完整市场分析 / 5 维度调研 / 竞品格局 / 生成 HTML 报告 | `linkfox-market-analysis-agent` |
| 分析差评 / 用户痛点 / 关键词搜索量 & CPC / 合规检测 | `linkfox-market-analysis-agent` |
| 帮我选品 / 有什么值得做的品 / 蓝海爆款预测 / 按预算选品 | `linkfox-product-selection-agent` |
| 对标 ASIN / 按品牌 / 按图找竞品 | `linkfox-product-selection-agent` |
| 写 Listing / 优化标题 / 五点 / 关键词矩阵 / Listing 打分 | `linkfox-listing-agent` |
| 出主图 / 场景图 / A+ 图 / 卖点图 / 图片裂变 / 人台换模特 | `linkfox-image-agent` |
| 图转视频 / 口播视频 / 爆款视频复刻 | `linkfox-video-agent` |
| 综合问题 / 不确定走哪个 Agent | `default`（或省略 `--model`） |

**深度参考**：每个 Agent 的完整能力表、子任务触发短语、prompt 模板 → 见 `references/capabilities.md`。

### 跨 Agent 工作流

复杂任务可按序串联多个 Agent（每一步都是一个独立任务）：

```
Step 1  linkfox-product-selection-agent   在美国站找 3 个值得做的 insulated water bottle 细分方向
Step 2  linkfox-market-analysis-agent     对 Step 1 的 Top 1 方向做完整市场分析
Step 3  linkfox-listing-agent             参考 Top 3 竞品，为我的产品生成差异化 Listing
Step 4  linkfox-image-agent               基于 Listing 卖点生成一套 7 张商品图
Step 5  linkfox-video-agent               用商品主图生成 15 秒带货口播视频
```

---

## 3. Quick Start

### Setup

**先检查 `LINKFOXAGENT_API_KEY` 环境变量存在且可用**——这是使用本 skill 的前置条件，未通过任何后续调用都会 401。

```bash
# 检测环境变量
[ -n "$LINKFOXAGENT_API_KEY" ] && echo have_key || echo missing
```

**分流**：
- `missing` → **走 onboarding 引导注册**：见 `references/onboarding.md` 入口 1，用 `scripts/onboarding/send_verify_code.py <phone>` + `scripts/onboarding/login_and_get_key.py <phone> <code>` 帮用户拿新 key，然后写入 shell rc 并**提示用户重启会话让环境变量生效**。
- `have_key`，但真发一个任务返回 `errcode=401` / `authorized error` → **同样走 onboarding 引导**（`references/onboarding.md` 入口 1 情况 A）：先让用户重启会话（最常见误判），仍失败再引导重取 key 或用新手机号重新注册。
- `have_key` 且能正常提交 → 继续下一步 Writing Task Prompts。

> 首次真发任务时才会打网关，`--list-recent` 是纯本地读 `.linkfox-os/recent-tasks.json`，不做 API 探活。

**可选**：`export LINKFOXAGENT_BASE_URL=...` 覆盖 BASE URL（默认 `https://agent-api.linkfox.com/`）。

> **数据隐私**：Task prompts + 你的 API key 会发送到 `LINKFOXAGENT_BASE_URL`。不要在 prompt 里包含 secrets / credentials / 敏感个人数据。

### Writing Task Prompts

`prompt` 是自由文本，描述让 linkfox-os 做什么。多步任务写编号步骤，Agent 内部会处理数据流：

```
1、在亚马逊美国站搜索 "computer desk"，返回前 2 页商品数据
2、对上一步商品标题分词，统计出现的功能点
3、按功能点统计月销量、月销售额、asin 数
```

用 `--model <modelId>` 指定 Agent；缺省用 `default` 由平台路由。

---

## 4. Running Tasks (Live Progress Mode)

AgentStudio tasks 通常需要 1–5 分钟。推荐 dispatch 模式在执行过程中实时展示 **真实 eventList 进度**（Agent 的思考 + 工具调用），而不是空洞的"仍在等待"文案。

### Step 1 — Submit (non-blocking)

**Before submitting**, tell the user:
> 「正在通过 linkfox-os 接口提交任务，请稍候（通常需要 1-5 分钟）...」

```bash
python3 <skill>/scripts/linkfox_os.py --stdin <<'__LINKFOX_TASK_END__'
<TASK_PROMPT>
__LINKFOX_TASK_END__
```

Returns immediately: `{"messageId": "..."}`. Extract `messageId`.

### Step 2 — Poll loop (relay real eventList as progress)

Every 15 seconds, call:

```bash
python3 <skill>/scripts/linkfox_os.py --status <messageId> --format progress
```

Returns one JSON object. Parse and **output the real progress to the user as YOUR OWN TEXT** (not inside a command). In Codex/Claude Code, command output is collapsed and invisible to the user — only your text responses between commands are directly visible. So after each poll command, you MUST write out the new steps as plain text:

```json
{
  "status": "running",
  "message": "采集亚马逊 BSR Top100",
  "steps": [
    {"label": "[思考] The user wants to search for cat...", "status": "completed"},
    {"label": "[工具] linkfox-sellersprite-product-search (keyword=cat)", "status": "completed"},
    {"label": "[消息] Launching skill: linkfox-sellersprite-product-search", "status": "in_progress"}
  ],
  "stop_reason": null,
  "message_id": "aaxF..."
}
```

**How to relay to user** (VERBATIM, do NOT rephrase):
- `status=running` — for each NEW `steps[].label` (not already shown), output the label **VERBATIM** as a line. Do NOT rephrase, summarize, or interpret. Copy the label string exactly. Example:
  ```
  [思考] The user wants to analyze negative reviews for ASIN B0GZSVVBJZ...
  [工具] linkfox-amazon-reviews-list (ASIN: B0GZSVVBJZ, site: US)
  [消息] Launching skill: linkfox-amazon-reviews-list
  [文件] [linkfox-amazon-reviews-list] https://lfclaw-oss-nx-prod.s3.cn-northwest-1.amazonaws.com.cn/temp/data/reviews-123.json → 已下载: [reviews-123.json](/path/to/output/202607.../reviews-123.json)
  [思考] Good, I got 70 reviews. Let me analyze the patterns...
  [工具] Bash (python3 -c "import json...")
  [消息] 数据分析完成。现在生成详细的差评分析报告。
  ```
  **CRITICAL: `[文件]` lines are resource/data file URLs produced by tool calls. You MUST output them verbatim to the user — they are the actual data file links the user needs. Do NOT skip, summarize, or omit `[文件]` lines.**
- `status=finished` — go to Step 3
- `status=error` — report `error` field to user, stop

**IMPORTANT: Do NOT invent generic progress commentary** ("还在采集数据...", "Agent 仍在工作中...", "产品详情接口耗时较长...", "数据已拉取完成！", "继续跟进中..."). These are FORBIDDEN. Only output what `steps[].label` and `message` actually say — verbatim, unmodified. If no new steps appeared since last poll, output nothing. Silence is correct; invented filler is wrong.

### Step 3 — Fetch full result (terminal state)

```bash
python3 <skill>/scripts/linkfox_os.py --poll <messageId> --timeout 60
```

Then apply the Result Parsing Rules（见 §6 below）.

### Do NOT use --wait

`--wait` 会阻塞整个命令直到终态，Codex / Claude Code 的命令输出被折叠成"运行了多个命令"，stderr 里的 eventList 用户看不到。要让用户看到进度，只能走上面的 poll loop：`--status` 拿到 JSON 后，把 `steps[].label` 作为**你自己的文本回复**输出（不在命令里），这段文本才会直接显示在对话里。

### Dispatching Multiple Independent Tasks

When the user's request involves multiple independent tasks, submit all tasks first (Step 1 for each), then interleave their poll loops (Step 2), showing progress for all in parallel.

---

## 5. Output Format (MANDATORY — applies whether this skill is explicitly specified or auto-matched)

All data files returned by the task MUST be formatted in Markdown using the following structure. Do NOT output raw URLs, plain text paths, or any other format.

### Data File Links (数据文件)

Every data file link MUST use this exact format:

```
[文件] 数据文件：[filename](url)
[本地] 已保存至本地：[filename.json](/absolute/path/to/filename.json)
```

Example:

```
[文件] 数据文件：[amazon-search-results.json](https://lfclaw-oss-nx-prod.s3.cn-northwest-1.amazonaws.com.cn/temp/data/amazon-search-results.json)
[本地] 已保存至本地：[amazon-search-results.json](/Users/xxx/project/.linkfox-os/output/202607161030/amazon-search-results.json)
```

### FORBIDDEN output patterns (these are WRONG):

- WRONG: Raw URL without markdown link: `https://xxx.s3.amazonaws.com.cn/temp/data/file.json`
- WRONG: Plain path without markdown: `/path/to/file.json`
- WRONG: Code block wrapping the URL: `` `https://...` ``
- WRONG: Missing `[文件]` / `[本地]` prefix markers
- WRONG: Using any emoji markers instead of `[文件]` / `[本地]` — 严禁输出任何 emoji
- WRONG: Mixing Chinese and English inconsistently (use `[文件] 数据文件：` and `[本地] 已保存至本地：`)

### Progress Step Lines (进度步骤)

During polling, resource/data file lines in `steps[].label` starting with `[文件]` MUST be output VERBATIM — they contain the actual data file URLs the user needs:

```
[文件] [tool-name] https://...url... → 已下载: [filename.json](/local/path/filename.json)
```

### Final Result Text

Forward all `[chunk i] <text>` content directly. If the text contains markdown (tables, headers, lists), preserve it as-is. Do NOT wrap it in code blocks or strip its formatting.

---

## 6. Result Parsing Rules

Apply to the script's stdout (both direct-run and sessions_spawn paths produce identical output). There is **no ShareURL** in the linkfox-os API.

**核心原则：省 token 不省内容。** 脚本会把完整 API 响应、每个 chunk 全文、resource_link 下载文件全部落盘到 `<taskDir>/` 下，stdout 仅返回**路径 + 短预览**。你（调用方 agent）负责判断是否需要读某个文件——对用户有价值的段才 Read 出来，别把整份报告都吞进 context。

1. **首块**：`Status:` 行（finished / error / unknown），后跟 `StopReason:`（e.g. `end_turn`）、`toolCount=… | eventCount=…` 汇总行、然后是 chunk 段。
2. **If `Status: finished`** (StopReason is `end_turn`):
   - Chunk 段每一条是 `[chunk i] <text>`（短 chunk，≤400 字符）或 `[chunk i] length=<N> chars → saved: <path>` 后跟 `preview: <前200字符>`（长 chunk 已落盘）。
   - **短 chunk（内联）**：直接转发给用户。
   - **长 chunk（已落盘）**：**先看 preview 判断是否与用户需求相关**——相关就用 Read 工具读 `<path>` 拿全文再展示；不相关或用户没要求，只需告诉用户"完整结果已保存到 `<path>`（xxxx 字），需要看具体哪部分请示"。**绝对不要**"为了完整"把整份长 chunk Read 出来再复制到回复里——这会二次浪费 token，且原本就在磁盘上供用户随时查看。
   - resource link (line like `Resource [<title>]: <uri>`): 转发 URI，是公开 HTTP URL。
   - tool call (line like `[Tool: <name>]`): 可内联总结。
   - **After the chunks, look for the `--- 数据文件 ---` section.** Each entry has two lines:
     - `[name] <url>` — the public download URL
     - `  已下载到本地: [filename.json](/abs/path/filename.json)` — Markdown link to local file (or `(跳过下载，uri=...)` if not downloadable)
     You MUST output ALL entries VERBATIM to the user. Do NOT reformat or rephrase. Output exactly:
     ```
     [文件] 数据文件：[name](<url>)
     [本地] 已保存至本地：[filename.json](/abs/path/filename.json)
     ```
     The Markdown link `[filename](/path)` is clickable in VS Code / Cursor / Codex — output it verbatim.
3. **If `Status: error`** (StopReason is something other than `end_turn`, e.g. `max_tokens` / `error`):
   - Report the StopReason and any error content to the user. Still forward any partial `[chunk i] …` text that did come back, since the task may have produced partial results.
4. **Share Link section**: 任务终态后，stdout 末尾会追加 `--- 分享链接 ---` 段：
   ```
   --- 分享链接 ---
   ShareUrl: https://os.linkfox.com/share?id=aaXXXXXX
   ShareId: aaXXXXXX
   ```
   这是脚本自动调 `/agent-studio/task/getShareUrl` 换来的**公开工作台链接**（1 年有效，可直接发给别人，无需登录）。任何时候看到这一段都要**原样转发给用户**——用户拿这个链接可以复盘完整过程。若脚本没有输出该段（后端拒绝、任务尚未终态、权限失败等），无声跳过即可，不要造。
5. The script also writes the full API response to `<taskDir>/message.json` and the task meta to `<taskDir>/result.json`. If stdout truncated a chunk you actually need, or你要看原始 API 载荷, read `message.json` / `chunk_*.md` to recover. **Report the `taskDir` path to the user only if they ask where the raw data is**——通常他们不需要知道。

### `--status --format progress` 输出规则（JSON）

- `result_saved_to`（终态时出现）：结果文本完整落盘到 `<taskDir>/result.md`。
- `result`：终态时**只是预览**（超过 400 字符会截断到 200 字符 + `…`），`result_truncated=true` 且 `result_chars` 告诉真实长度。想拿全文用 Read 读 `result_saved_to`。
- `raw.eventList`：只有 running 时才保留；终态被丢弃（想追溯原始事件流去 Read `message.json`）。

---

## 7. Script Reference (all modes)

```bash
# Non-blocking submit (returns messageId immediately)
python3 <skill>/scripts/linkfox_os.py --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# One-shot progress check (structured JSON)
python3 <skill>/scripts/linkfox_os.py --status <messageId> --format progress

# Blocking poll to completion
python3 <skill>/scripts/linkfox_os.py --poll <messageId> --timeout 600

# Cancel a running task
python3 <skill>/scripts/linkfox_os.py --cancel <messageId>

# Recover lost messageId (list recent tasks, newest first)
python3 <skill>/scripts/linkfox_os.py --list-recent

# Custom model (dispatch to a specific Agent)
python3 <skill>/scripts/linkfox_os.py --model linkfox-market-analysis-agent --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__
```

---

## 8. Streaming Progress for Agent Clients

For agent clients (Claude Code / Cursor / Codex / Copilot) that expose **plan / commentary / final** display primitives, use the structured progress output instead of plain text. The script emits a generic JSON snapshot that every client can map to its own primitives — no client-specific format baked in.

### One-shot snapshot

```bash
python3 <skill>/scripts/linkfox_os.py --status <messageId> --format progress
```

Emits one JSON object:
```json
{"status":"running","progress_pct":40,"message":"采集亚马逊 BSR Top100",
 "steps":[{"label":"规划任务：搜索亚马逊","status":"completed"},
          {"label":"采集亚马逊 BSR Top100","status":"in_progress"}],
 "stop_reason":null,"message_id":"aarq...",
 "raw":{"eventList":[...],"eventCount":3,"toolCount":1}}
```

### Streaming until terminal

```bash
python3 <skill>/scripts/linkfox_os.py --watch <messageId> --interval 15 --timeout 600
```

Emits one JSON line (JSONL) per progress change, then a final line on terminal state:
```
{"status":"running","progress_pct":0,"message":"规划任务...","steps":[...]}
{"status":"running","progress_pct":40,"message":"采集亚马逊 BSR Top100","steps":[...]}
{"status":"finished","stop_reason":"end_turn","result":"你好！我是..."}
```

### Field → client primitive mapping

| JSON field | Maps to (client primitive) | Notes |
|---|---|---|
| `steps[]` (`label`+`status`) | plan / todo / `update_plan` | Ordered subtask list; `in_progress`=current, `completed`=done |
| `progress_pct` + `message` | commentary / progress text | Short text + percent; `progress_pct` is null when not inferable |
| `status=finished` + `result` | final answer | Format `result` text as the terminal artifact |
| `status=error` + `error` | final error | Report `error`; `stop_reason` carries the raw reason |
| `raw.eventList` | fallback | Original events for advanced parsing when `steps`/`message` are too coarse |

### Recommended agent loop (non-blocking poll)

For clients that cannot stream-read a long-running command, run a poll loop in the agent itself:

1. **Submit**: `python3 <skill>/scripts/linkfox_os.py "<task>"` → `{"messageId": ...}`
2. **Loop** every ~15s: `python3 <skill>/scripts/linkfox_os.py --status <id> --format progress`
   - `status=running` → update plan from `steps[]`, emit commentary from `progress_pct`+`message`
   - `status=finished` → emit final from `result`, stop
   - `status=error` → emit final error from `error`, stop
3. Or, if the client supports streaming tool output, use `--watch <id>` once and read the JSONL stream.

> `steps` / `progress_pct` / `message` are best-effort extracted from the server's `eventList[].sessionUpdate` (a passthrough map whose schema may vary). `raw.eventList` always carries the original payload — fall back to it when the extracted fields are too coarse.

---

## 9. Sub-agent Dispatch (Codex sessions_spawn)

When a client supports isolated sub-agent sessions and can display announce messages, you can spawn a sub-agent per task and let it block on `--wait`.

**Before spawning**, tell the user:
> 「正在同时通过 linkfox-os 接口提交 N 个任务，请稍候...」

```
# Sub-agent 1
sessions_spawn:
  task: |
    Run (use heredoc to avoid shell injection):
    python3 <skill>/scripts/linkfox_os.py --wait --timeout 600 --stdin <<'__LINKFOX_TASK_END__'
    <task A>
    __LINKFOX_TASK_END__
    Apply the same submission success/failure + result parsing rules as the single-task template above.
  label: "linkfox-os: task A"
  mode: "run"
  runTimeoutSeconds: 600
```

### What Happens Under the Hood

1. `sessions_spawn` creates an isolated sub-agent session.
2. The sub-agent runs `linkfox_os.py --wait` which blocks until `stopReason` becomes non-empty.
3. When done, the sub-agent's result is automatically delivered back to the main session via the announce system.
4. The user sees the result in their chat without any manual polling.

### Script Reference

```bash
# Sub-agent uses --wait + --stdin (heredoc avoids shell injection)
python3 <skill>/scripts/linkfox_os.py --wait --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# Choose a non-default model
python3 <skill>/scripts/linkfox_os.py --wait --model linkfox-listing-agent --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# Custom timeout (default 300s)
python3 <skill>/scripts/linkfox_os.py --wait --timeout 600 --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# JSON output for structured parsing
python3 <skill>/scripts/linkfox_os.py --wait --format json --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__
```

---

## 10. Checking Progress for a Running Task

When the user asks "任务到哪了 / How far has it gone / 进度多少", **DO NOT** spawn another `--wait` sub-agent. Instead run a single non-blocking call from the main session:

```bash
python3 <skill>/scripts/linkfox_os.py --status <messageId>
```

**Don't have the messageId handy?** Every successful submission persists `messageId` to local disk on first contact, so recover it with one command:

```bash
python3 <skill>/scripts/linkfox_os.py --list-recent     # newest first
```

This makes one API call and prints `Status:` + `Progress:` (or `StopReason:` if terminal) immediately. Forward the `Progress:` line back to the user verbatim.

Special status values to interpret for the user:
- `Status: working` + `Progress: <text>` — task still running, currently at `<text>` (extracted from the in-progress `eventList`).
- `Status: working` + `Progress: (no progress info yet)` — task running but no step info available yet.
- `Status: finished` + `StopReason: end_turn` — task ended successfully; tell the user to call `--poll <messageId>` or wait for the original sub-agent's announce.
- `Status: error` + `StopReason: <reason>` — task ended abnormally; report the reason.

---

## 11. Output Directory

**产物默认落在当前工作目录**：`$PWD/.linkfox-os/output/{YYYYMMDDHHmm}/`。跟随 CWD 而非 skill 安装路径，确保用户在 CC / Codex / workbuddy 里能读到；`.linkfox-os` 是隐藏目录，用 `.gitignore` 一行 `.linkfox-os/` 即可屏蔽。

想统一收拢到某个绝对目录，设环境变量：
```bash
export LINKFOX_OS_OUTPUT_DIR=/path/to/dir
```

**The folder is created the moment the task is submitted** (not when results arrive), and a `result.json` is dropped immediately containing the `messageId` (from the create response `id`) + original `prompt`. This way the messageId can always be recovered later — even if the original `linkfox_os.py` invocation's stdout was not captured.

```
$PWD/.linkfox-os/output/{YYYYMMDDHHmm}/
├── result.json          # Task metadata (created at submit; updated on completion)
├── message.json         # Full API response (only after --wait / --poll sees a terminal stopReason)
├── result.md            # 终态合并的所有 chunk 文本（--status/--watch 落盘用；无 chunk 时不产）
├── chunk_1.md           # 每个长 agentMessageChunk 全文（>400 字符时才落盘；短的直接内联到 stdout）
├── chunk_2.md
├── ...
└── <resource_link_filename>  # eventList / chunks 里 resource_link 下载的原始数据文件
```

`result.json` lifecycle:

```jsonc
// At submit time (background mode exits here):
{
  "messageId":   "uDqHg33fQeQfkNB5pj5LLA",
  "prompt":      "在亚马逊美国站搜索 usb charger cable，返回前 40 条",
  "status":      "submitted",
  "submittedAt": "2026-07-14T10:30:05",
  "stopReason":  ""
}

// After --wait / --poll sees a terminal stopReason:
{
  "messageId":   "uDqHg33fQeQfkNB5pj5LLA",
  "prompt":      "...",
  "status":      "finished",            // finished (end_turn) / error (other stopReason)
  "submittedAt": "2026-07-14T10:30:05",
  "stopReason":  "end_turn",
  "completedAt": "2026-07-14T10:33:18"
}
```

Field meanings:
- `messageId`: the task id returned by `/agent-studio/task/create` (field `id`); used to look up status and results.
- `prompt`: the original prompt text that was submitted.
- `status`: lifecycle marker — `submitted` after submit, then `finished` / `error` once the task ends.
- `stopReason`: the raw `message.stopReason` value from the API (empty while running; `end_turn` on success; other values indicate abnormal end).
- `submittedAt` / `completedAt`: ISO-formatted local timestamps (no tz suffix).

### Recovering messageId from local state

If the user comes back later but the messageId is no longer in the chat, run:

```bash
python3 <skill>/scripts/linkfox_os.py --list-recent      # newest first, default & max 30
python3 <skill>/scripts/linkfox_os.py --list-recent 5    # 只看最近 5 条
python3 <skill>/scripts/linkfox_os.py --list-recent --format json   # 结构化输出，便于脚本解析
```

Output is one line per task, newest first:

```
2026-07-14T10:30:05  finished    uDqHg33fQeQfkNB5pj5LLA  [default]  在亚马逊美国站搜索 usb charger cable，返回前 40 条
2026-07-14T10:25:02  submitted   pKlMnOpQrStUvWxYzAbCdE  [linkfox-market-analysis-agent]  分析这个 ASIN...
```

数据源：`$OUTPUT_ROOT/../recent-tasks.json`（默认 `.linkfox-os/recent-tasks.json`）——纯本地文件，滚动保留最近 30 条。**提交任务时追加**（status=submitted），**--poll / --wait 拿到终态时更新**（status=finished/error/cancelled + stopReason + completedAt）。超过 30 条会自动丢尾。

Pick the matching task, then call `--status <messageId>` for live progress or `--poll <messageId>` to fetch the full result.

**To access raw result data:** read `<taskDir>/message.json` — it holds the complete `{message, eventList}` response, including every `agentMessageChunks` entry.

---

## 12. Retry on Failure

If a task fails, inspect `message.json` for the `stopReason` and any error content in `agentMessageChunks`. Common issues:
- `stopReason` is an error code (not `end_turn`) — the pipeline rejected the prompt or hit a server error; retry with a simpler / adjusted prompt.
- HTTP 401/403 from submit — 未配置 / key 失效 → **走内置 onboarding 引导**（下节）。
- HTTP 402 或消息含"积分余额不足/余额不足/请充值/quota exceeded/insufficient balance" → **走内置 onboarding 充值流程**（下节）。
- Polling timeout — the task is slow; use `--status <messageId>` to check progress, or re-run `--poll <messageId>` with a larger `--timeout`.

---

## 13. Onboarding (Auth / Credits) — 内置账号与环境引导

本 skill 内置了 `linkfox-onboarding` 的全部脚本与流程，无需另装 skill。触发以下两类场景时直接走这里的脚本：

### 触发条件

**缺 Key / 鉴权失败**（满足任一）：
- `errcode = 401` 或错误消息含 `authorized error` / `鉴权失败` / `未授权` / `unauthorized`
- 环境变量 `LINKFOXAGENT_API_KEY` 为空
- 用户明确说"没配 key / 鉴权失败 / 注册 / 手机号注册"

**计费不足**（满足任一）：
- `errcode = 402`（实测返回 `{"errcode": 402, "errmsg": "积分余额不足，请充值"}`）
- 错误消息含 `积分余额不足` / `计费不足` / `余额不足` / `quota exceeded` / `insufficient balance` / `套餐到期` / `需充值` / `请充值`
- 用户明确说"积分不足 / 余额不足 / 充值 / recharge / 升级套餐"

排除：`errcode = 403`（无权限，不进入 onboarding）。

### 脚本清单（`scripts/onboarding/`）

| 场景 | 脚本 | 输入 | 输出 |
|------|------|------|------|
| 检测环境变量 | Bash 一行 | — | `ok` / `missing` |
| 发送短信验证码 | `send_verify_code.py <phone>` | 手机号 | JSON `{sent, phone, agreements}` |
| 验证码登录取 key | `login_and_get_key.py <phone> <code>` | 手机号 + 验证码 | JSON `{api_key, group_id, member_id, is_new_user, ...}` |
| 列套餐 | `list_plans.py` | — | JSON 套餐清单（含 `plan_id` / `price` / `credits` / `available_methods`） |
| 生成支付订单 + 二维码 | `create_order.py <plan_id> <pay_method>` | plan_id + wechat/alipay | JSON `{order_id, qr_content, pay_url, png_path, ascii_qr}`（`png_path` 由内置 `_qrgen.py` 从 `qr_content` 现场生成） |
| 查询订单支付状态 | `query_order.py <order_id>` | 订单号 | JSON `{order_id, status, paid_at}` |

### 快速路径

1. **检测**：`[ -n "$LINKFOXAGENT_API_KEY" ] && echo ok || echo missing`（三平台通用）。
2. **无 key**：问用户是自行注册还是让脚本帮忙注册；帮忙注册就走 `send_verify_code.py` → `login_and_get_key.py` 拿 key。
3. **鉴权失败但有 key**：优先提示"重启会话使环境变量生效"（最常见误判），仍失败再引导重取 key。
4. **计费不足**：`list_plans.py` → 让用户选套餐 + 支付方式（支持结构化选择工具的宿主用 `AskUserQuestion`，纯文本宿主给编号清单）→ `create_order.py` → 展示 PNG / 链接 / ASCII 二维码。

完整话术、失败分支、三平台环境变量配置示例、协议链接展示规则 → 见 `references/onboarding.md`。API 契约（`/user/v1|v3/web/login` / `/account/*` / `/package/*` / `/order/*`）→ 见 `references/onboarding-api.md`。

### 依赖

- Python 3
- `pip install requests`（登录链路，生产 WAF 对 urllib 敏感）
- 二维码：内置 `_qrgen.py` 纯 Python 实现，**无需再装 qrcode/pillow**

---

## 14. File Upload — 用户提供本地素材

**触发条件**：用户说 "我有一张参考图 / 帮我上传商品图 / 帮我传一份文档 / 附一份参考视频 / 用这张图给我生成商品图" 等——凡是**用户先提供本地素材**再交给下游 agent 做处理的场景。典型下游：`linkfox-image-agent` 需要 `imageUrl` / `imageList` 入参，`linkfox-video-agent` 需要 `reference_video_url`。

**流程**：脚本自动完成"申请 S3 STS 凭证 → SigV4 直传 → 换 sandbox 内虚拟路径"三步，最终把一个 `file:///root/...` 形式的 URL 交给你，你直接把它塞进下一步 prompt 即可。

### 用法

```bash
python3 <skill>/scripts/upload/upload_file.py <local_absolute_path> [--kind image|doc|video]
```

stdout **只输出一个 JSON 对象**（stderr 是可读进度）：

```json
{
  "url":          "file:///root/.linkfox/workspaces/.../<uuid>.jpg",
  "s3PreviewUrl": "https://lfclaw-oss-nx-prod.s3.cn-northwest-1.amazonaws.com.cn/temp/2026/07/<uuid>.jpg",
  "fileName":     "product.jpg",
  "mimeType":     "image/jpeg",
  "size":         123456,
  "kind":         "image"
}
```

**关键字段**：

| 字段 | 何时用 |
|---|---|
| `url` (`file:///root/...`) | **给下一步 agent prompt 用**；后端渲染时会自动翻译成公网 http URL |
| `s3PreviewUrl` | 仅本地调试预览用，不要塞进 prompt（避免签名 URL 过期） |

### 典型 pipeline

用户："我有张商品图，帮我出 3 张场景图。"

```bash
# Step 1: 上传用户的原图
u=$(python3 <skill>/scripts/upload/upload_file.py /path/to/user-product.jpg --kind image)
url=$(echo "$u" | python3 -c "import sys,json;print(json.load(sys.stdin)['url'])")

# Step 2: 拼下游 prompt 交给 image-agent
python3 <skill>/scripts/linkfox_os.py --model linkfox-image-agent --stdin <<EOF
用这张商品图 $url 生成 3 张场景图：泳池度假 / 冬季雪地 / 城市咖啡馆。
EOF
```

### 参数约定

- 位置参数 = 本地文件绝对路径（必填）
- `--kind image|doc|video`（可选）—— 仅回显方便下游归类，不影响上传
- 鉴权沿用 `LINKFOXAGENT_API_KEY`；BASE_URL 沿用 `LINKFOXAGENT_BASE_URL`
- 单请求 PUT，MAX ~100 MB 单文件；再大的 multipart 场景本版本不支持
- 目标桶固定 `temp/YYYY/MM/<uuid>.<ext>`，由 STS 凭证权限锁死前缀

### 依赖

- Python 3 stdlib（`urllib` + `hmac` + `hashlib` + `uuid`）
- **不需要** `boto3` / `botocore` / `requests`——SigV4 手写在 `scripts/upload/upload_common.py`

---

## 15. Deep References

### Agent 级（面向 modelId 选择）
- `references/capabilities.md` — 每个 Agent 的完整能力表、子任务触发短语、prompt 模板、跨 Agent 工作流示例。

### Skill 级（面向 prompt 里该引用哪些 skill）
按主题分 8 桶，每 skill 一行含 **用途 / 入参 / 返回摘要 / 归属 agent**。Codex 拟定 prompt 前应先看对应桶：

- `references/skills-amazon.md` — 亚马逊生态（28 个 skill）：Amazon 原生 + SellerSprite / Keepa / SIF / ABA / Alexa + Jiimore
- `references/skills-third-platforms.md` — 跨平台（18 个）：TikTok Shop / Shopee / Walmart / eBay / Ozon / 1688 / TSearch
- `references/skills-selection.md` — 选品（7 个）：4 种端到端流程 + 词库 + 以图找竞品（**大部分只在 product-selection agent**）
- `references/skills-listing.md` — Listing（25 个）：L1-L5 pipeline + 编排模式 + 商品库 CRUD（**listing-* 系列只在 listing agent**）
- `references/skills-market-analysis.md` — 市场分析（7 个）：5 维度编排 + HTML 渲染 + 产品方案（**全部只在 market-analysis agent**）
- `references/skills-media.md` — 图片/视频/文本（10 个）：AIGC 底层 + 套图编排 + 品牌基因
- `references/skills-ip-compliance.md` — IP 合规（21 个）：睿观 6 + 智慧芽 15
- `references/skills-tools.md` — 通用工具（15 个）：文件上传 / 报告 / 定时任务 / skill 创建 / 网页爬取 / 趋势 / 飞书 / 商品库 CRUD

### API 契约
- `references/api.md` — HTTP API 契约（`/agent-studio/task/create` / `get` / `cancel` / `getShareUrl` / `getUploadCredentials` / `getFileVirtualPath`）：请求 / 响应字段、鉴权、错误码、字段解析规则。

### Onboarding
- `references/onboarding.md` — 内置账号与环境引导流程（触发条件、话术、脚本调用步骤、三平台环境变量配置）。
- `references/onboarding-api.md` — onboarding 所有后端接口契约（登录链路、套餐 / 订单网关）。
