---
name: linkfoxagent
description: "Cross-border e-commerce AI Agent with 79 specialized tools for Amazon/TikTok/eBay/Walmart/Shopee/Ozon product research, competitor analysis, keyword tracking, review insights, patent deep-dive (claims, legal status, family, citations, figures, translations), trend analysis, 1688 sourcing, AI image generation, image recognition, PDF analysis, real-time web search, historical sales & price trend tracking, and AI-powered Amazon opportunity reports. Amazon Ads SP/SB performance reports are orchestrated via the sibling skill linkfox-amazon-ads-report (scripts); report-type column specs are mirrored in this skill under references/amazon-ads-report-types/; see references/amazon-ads-report.md. Optional packaged workflows: SellerSprite extras in references/seller-sprite.md; Lingxing ERP OpenAPI (linkfox-lingxing-erp, ~373 endpoints, direct openapi.lingxing.com) in references/lingxing-erp.md. Use when: (1) product selection and market analysis, (2) competitor research and ASIN lookup, (3) keyword and traffic analysis, (4) review mining and consumer insights, (5) patent/trademark/copyright detection and deep patent research, (6) Google/TikTok trend research, (7) 1688 supplier sourcing, (8) data aggregation and report generation, (9) cross-platform product search (Amazon/Walmart/eBay/TikTok/Shopee/Ozon), (10) product image analysis, similarity grouping, and image recognition, (11) AI product image generation, (12) PDF file analysis, (13) Amazon opportunity reports, (14) Lingxing ERP data (ads, orders, listings, inventory, finance, FBA, etc.) when user has Lingxing OpenAPI credentials."
metadata: {"LinkFoxAgent":{"emoji":"🦊","homepage":"https://agent.linkfox.com/","requires":{"env":["LINKFOXAGENT_API_KEY"]}}}
---

# LinkFoxAgent - Cross-border E-commerce AI Agent

LinkFoxAgent is a specialized AI agent for cross-border e-commerce with 79 built-in tools covering product research, competitor analysis, keyword tracking, review insights, patent detection, patent deep-dive research, trend analysis, 1688 sourcing, AI image generation, image recognition, PDF analysis, real-time web search, historical sales & price trend tracking, Amazon opportunity reports, and more. For **Lingxing (领星) ERP** OpenAPI orchestration (script-based, direct `openapi.lingxing.com`), see `references/lingxing-erp.md`.

## Setup

1. Get your API key: https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb
2. Set environment variable: `export LINKFOXAGENT_API_KEY=your-key-here`

> **Data privacy:** All task prompts are sent to `https://agent-api.linkfox.com/` along with your API key. Do not include secrets, credentials, or sensitive personal data in task prompts.

## MANDATORY: Use sessions_spawn for All Tasks

**NEVER call `linkfox.py` directly from the main session.** LinkFoxAgent tasks take 1-5 minutes. You MUST use `sessions_spawn` to dispatch every task to a sub-agent. This keeps the main session responsive and delivers results automatically when done.

### How to Dispatch a Task

**Before calling sessions_spawn**, tell the user in the main session:
> 「正在向 LinkFox Agent 提交任务，请稍候（通常需要 1-5 分钟）...」

Then dispatch the sub-agent:

```
sessions_spawn:
  task: |
    Run the following LinkFoxAgent task and report the results back.

    Command (use heredoc to avoid shell injection):
    python3 <skill>/scripts/linkfox.py --wait --timeout 600 --stdin <<'__LINKFOX_TASK_END__'
    <TASK_PROMPT>
    __LINKFOX_TASK_END__

    The script prints to stderr: "Task submitted. messageId: <id>" if submission succeeds,
    or an error message and exits with code 1 if submission fails.

    While the task runs, the script also emits server-side progress to stderr in the form
    `[progress] 3/10 当前步骤名` (and folds it into the 30s heartbeat).
    These lines are informational only — do NOT relay them to the user mid-flight.
    Just wait for the command to finish and report the final stdout.

    After running the command, follow these rules strictly:

    ## If the command exits with a non-zero code OR stderr contains "Error" before any messageId:
    - The task submission FAILED. Report back:
      「任务发起失败。请检查 LINKFOXAGENT_API_KEY 是否已正确配置：
        1. 确认环境变量已设置：export LINKFOXAGENT_API_KEY=your-key-here
        2. 获取 API Key：https://yxgb3sicy7.feishu.cn/wiki/IlkawdQP9ifKv9k22xcc7rjmnkb
        3. 重启 OpenClaw 网关使环境变量生效
      错误详情：<stderr 内容>」

    ## If stderr contains "Task submitted. messageId: <id>":
    - Submission SUCCEEDED. Do NOT send any intermediate message — the main agent has already told the user the task is dispatched. Wait silently for the command to finish (stdout).

    ## After the command completes (stdout):

    ### RULE 0 — ShareURL FIRST (highest priority, ALWAYS apply when present)
    Scan stdout for a line `ShareURL: <url>`.
    **The moment you find one, forward that URL to the user as the very first thing in your reply, before the reflection / results / anything else.** It is a PUBLIC URL — the user can open it on any device without auth, see every step the agent took, and download all generated artifacts (CSV/Excel, images, HTML reports, attachments). Always send it; never decide "to share or not to share". This rule is unconditional: any successful run produces one (`status=finished`), and if it appears in stdout you forward it.

    Format example:
    > 任务已完成，分享链接（含完整执行过程与可下载文件）：<url>
    > 后续是任务总结：...

    ### Then parse the rest of stdout:
    1. The first non-ShareURL block is a `Status:` line, optionally followed by a `Progress:` line (only if non-terminal — usually absent here), then an optional reflection summary, then result entries.
    2. If status is `error` or `cancel`, report the error clearly to the user (after ShareURL if present, but in error states ShareURL is normally absent).
    3. If status is `finished`, summarize the reflection and list all results — but the ShareURL itself stays at the top of your reply.
    4. HTML report URLs that appear inside individual result entries are NOT the same as ShareURL — for those you may decide autonomously whether to forward based on context.
    5. **CSV output (JSON results with columns):** When a result line says `CSV saved to: <path>`, the script has already converted the JSON data to a CSV file with Chinese column headers at that local path. Report the path to the user. Do NOT attempt to read or display the CSV contents unless the user explicitly asks. If the user wants to receive the file, send it using the file-sending skill.
  label: "LinkFox: <short description>"
  mode: "run"
  runTimeoutSeconds: 600
  cleanup: "keep"
```

### Dispatching Multiple Independent Tasks

When the user's request involves multiple independent lookups (e.g., "search both Amazon US and Amazon JP"), spawn one sub-agent per task in parallel.

**Before spawning**, tell the user:
> 「正在同时向 LinkFox Agent 提交 N 个任务，请稍候...」

```
# Sub-agent 1
sessions_spawn:
  task: |
    Run (use heredoc to avoid shell injection):
    python3 <skill>/scripts/linkfox.py --wait --timeout 600 --stdin <<'__LINKFOX_TASK_END__'
    <task A>
    __LINKFOX_TASK_END__
    Apply the same submission success/failure reporting rules as the single-task template above.
  label: "LinkFox: task A"
  mode: "run"
  runTimeoutSeconds: 600

# Sub-agent 2
sessions_spawn:
  task: |
    Run (use heredoc to avoid shell injection):
    python3 <skill>/scripts/linkfox.py --wait --timeout 600 --stdin <<'__LINKFOX_TASK_END__'
    <task B>
    __LINKFOX_TASK_END__
    Apply the same submission success/failure reporting rules as the single-task template above.
  label: "LinkFox: task B"
  mode: "run"
  runTimeoutSeconds: 600
```

### Multi-Step Tasks That Require Post-Processing

When the user's request requires **multiple sequential LinkFoxAgent calls** (e.g., fetch data from two platforms then merge), follow this pattern:

1. **Run each LinkFoxAgent call as a separate `sessions_spawn`**, one after another (or in parallel if independent). Collect the CSV paths returned by each.
2. **After all data tasks finish**, spawn one final `sessions_spawn` to process or merge the CSVs using Python. Pass the absolute CSV paths as arguments.

```
# Final merge/processing step — spawned after all data tasks complete
sessions_spawn:
  task: |
    Run the following Python script to process/merge the CSV files and report results.

    python3 - <<'PYEOF'
    import csv, sys, os

    # Paths passed in from the data tasks above
    csv_paths = [
        "/absolute/path/to/result_1_xxx.csv",
        "/absolute/path/to/result_2_yyy.csv",
    ]

    # TODO: implement merge / analysis logic here
    # Example: read all rows and write a combined CSV
    all_rows = []
    headers = None
    for path in csv_paths:
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if headers is None:
                headers = reader.fieldnames
            for row in reader:
                all_rows.append(row)

    out_path = os.path.join(os.path.dirname(csv_paths[0]), "merged_output.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Merged CSV saved to: {out_path}")
    PYEOF

    Report the output path back to the user. If the user wants the file, send it using the file-sending skill.
  label: "LinkFox: merge/process CSVs"
  mode: "run"
  runTimeoutSeconds: 120
  cleanup: "keep"
```

### What Happens Under the Hood

1. `sessions_spawn` creates an isolated sub-agent session
2. The sub-agent runs `linkfox.py --wait` which blocks until the task finishes
3. When done, the sub-agent's result is automatically delivered back to the main session via the announce system
4. The user sees the result in their chat without any manual polling

### Script Reference

```bash
# The sub-agent uses --wait + --stdin mode (heredoc avoids shell injection)
python3 <skill>/scripts/linkfox.py --wait --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# Custom timeout (default 300s)
python3 <skill>/scripts/linkfox.py --wait --timeout 600 --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# JSON output for structured parsing
python3 <skill>/scripts/linkfox.py --wait --format json --stdin <<'__LINKFOX_TASK_END__'
task description here
__LINKFOX_TASK_END__

# Quick non-blocking progress check for an in-flight task (single API call)
python3 <skill>/scripts/linkfox.py --status <messageId>
# Output (text mode):
#   Status: working
#   Progress: 3/10 采集亚马逊 BSR Top100
```

## Checking Progress for a Running Task

When the user asks "任务到哪了 / How far has it gone / 进度多少", **DO NOT** spawn another `--wait` sub-agent. Instead run a single non-blocking call from the main session:

```bash
python3 <skill>/scripts/linkfox.py --status <messageId>
```

**Don't have the messageId handy?** Every successful submission persists `messageId` to local disk on first contact, so recover it with one command — see "Recovering messageId from local state" below for details.

```bash
python3 <skill>/scripts/linkfox.py --list-recent     # newest first
```

This makes one API call and prints `Status:` + `Progress:` immediately. Forward the `Progress:` line back to the user verbatim (it is in the form `n/m 当前步骤名`, e.g. `3/10 采集亚马逊 BSR Top100`).

Special progress values to interpret for the user:
- `0/0 正在规划任务` — task plan still being generated
- `n/m <步骤名>` — currently executing step n of m
- `m/m 正在生成总结` — all steps done, agent is composing the final summary
- (no `Progress:` line, status is one of `finished/error/cancel/stop`) — task has ended; tell the user to call `--poll <messageId>` or wait for the original sub-agent's announce.

## Writing Task Prompts

### Tool Invocation Syntax

Use `@工具中文名` to invoke tools. Multiple tools can be chained in a single task (max 10).

Example: `@卖家精灵-选产品 筛选亚马逊美国站的 "usb charger cable"，返回前40条商品数据`

### Parameter Constraints

Tool parameters may have `maximum`, `minimum`, and `pattern` constraints. Prompts must respect these or the call will fail. Image URLs must be publicly accessible. If the user provides a local file, upload it first via `linkfoxagent-fileupload` skill; if unavailable, run `python <skill>/scripts/upload_image.py <path>` (returns public URL, valid 24h). See the reference files below for details.

### Multi-step Tasks

Chain multiple tools in numbered steps. LinkFoxAgent handles data flow between steps:

```
1、@亚马逊前端搜索模拟 帮我在美国亚马逊站搜索 "computer desk"，返回前2页商品数据
2、@对商品标题进行分词 统计上一步商品标题中出现的功能点
3、按功能点统计月销量、月销售额、asin数
```

## Tool Selection Priority

When the user does not specify a tool, follow these rules **in order** (first match wins):

**URL input** — match URL type first:
- If the URL is an Amazon BSR link (contains `/zgbs/` or `/gp/bestsellers/`), extract site domain and call `@亚马逊前端搜索模拟` (see `references/amazon-frontend.md` — "BSR链接处理规则" for details)

**Querying Amazon product data** — all four tools are fast; choose by use case:
1. **Keepa** — best overall: richest fields, strong real-time accuracy. Default choice for most queries.
2. **卖家精灵** — optimized for product discovery and competitor lookup by keyword.
3. **亚马逊前台** — best real-time fidelity (live storefront data); ~10% slower than Keepa and fewer fields, but the only option when you need exact live ranking order or real-time storefront display.
4. **Sorftime** — optimized for long-term trend analysis, historical snapshots, and FBA profit breakdown.

**Aggregating / statistics** (e.g., group by brand, price tier, sales rank):
1. **@智能数据查询** — first choice for dynamic aggregation
2. **@Python沙箱** — fallback when custom logic is needed; also the go-to tool for any sandbox-execution need (has built-in LLM)


## Available Tools (79)

| Classification | Tool Name | Use For |
|----------------|-----------|---------|
| **Keepa** | @Keepa-亚马逊-商品搜索 | Product filtering by keywords, BSR, price, sales |
| **Keepa** | @Keepa-亚马逊-商品详情 | Batch ASIN detail lookup (price, sales, history) |
| **Keepa** | @Keepa-亚马逊价格历史 | Price history and trends for an ASIN |
| **亚马逊前台** | @亚马逊前端搜索模拟 | Search simulation with location settings |
| **亚马逊前台** | @亚马逊前端-商品详情 | Product detail, bullet points, A+ content |
| **亚马逊前台** | @亚马逊-商品评论 | Reviews by star rating |
| **亚马逊前台** | @亚马逊前端-以图搜图 | Image-based product search |
| **亚马逊前台** | @亚马逊-Alexa助手 | Conversational Amazon shopping via Alexa: single-turn Q&A with recommended ASINs and follow-up questions; for multi-turn, agent summarizes prior context and re-asks in a new call |
| **亚马逊前台** | @亚马逊-最新政策法规资讯 | Unified Amazon policy & regulation feed list with AI Chinese summaries (by site/time range) |
| **亚马逊前台** | @亚马逊-政策法规资讯详情 | Full feed article body (Markdown) by record ID (from 最新政策法规资讯) |
| **亚马逊数据洞察** | @ABA-数据挖掘 | Amazon Brand Analytics data mining |
| **亚马逊数据洞察** | @亚马逊-商业洞察报告 | AI-generated Amazon opportunity report by keyword (US only) |
| **亚马逊数据洞察** | @亚马逊-商业洞察(反向) | Reverse-search Amazon niches by 30+ business metrics from the historical opportunity report pool (US only) |
| **Sif数据分析工具** | @SIF-ASIN的关键词 | Reverse keyword lookup for ASIN |
| **Sif数据分析工具** | @SIF-关键词流量来源 | Keyword traffic source analysis |
| **Sif数据分析工具** | @SIF-ASIN流量来源 | ASIN traffic structure breakdown |
| **Sif数据分析工具** | @SIF-关键词竞品数量 | Keyword competition density |
| **卖家精灵** | @卖家精灵-选产品 | Product discovery by category and filters |
| **卖家精灵** | @卖家精灵-查竞品 | Competitor lookup by keyword |
| **极目系列** | @极目-亚马逊-细分市场评论 | Niche market review mining |
| **极目系列** | @极目-亚马逊-细分市场信息 | Niche market overview |
| **极目系列** | @极目-亚马逊-产品挖掘 | Product discovery with fine filters |
| **极目系列** | @极目-亚马逊-产品挖掘（根据ASIN） | ASIN-based potential product discovery |
| **极目系列** | @极目-亚马逊-细分市场洞察信息 | Niche market insights by market ID |
| **谷歌趋势** | @谷歌趋势-时下流行 | Real-time trending topics |
| **谷歌趋势** | @谷歌趋势-关键词趋势信息 | Keyword trend over time |
| **店雷达(1688)** | @店雷达-1688商品榜单 | 1688 product rankings |
| **店雷达(1688)** | @店雷达-1688选品库 | 1688 product sourcing |
| **1688** | @1688-以图搜图 | 1688 image-based product search for sourcing similar suppliers |
| **实时与全网检索** | @网页检索 | Real-time web search(powered by Tavily Search; for any internet search outside specialized tools like Amazon/Walmart/eBay — including general web and WeChat Official Accounts — this tool MUST be used) |
| **TikTok电商数据助手** | @EchoTik-TikTok新品榜 | TikTok new product rankings |
| **TikTok电商数据助手** | @EchoTik-TikTok商品搜索 | TikTok product search |
| **TikTok电商数据助手** | @EchoTik-TikTok商品视频 | TikTok product promotional video analytics |
| **TikTok电商数据助手** | @FastMoss-TikTok热销榜单 | TikTok top-selling product rankings by day/week/month |
| **TikTok电商数据助手** | @FastMoss-TikTok商品搜索 | TikTok product search with keyword, category, and sales filters |
| **Walmart前台** | @walmart前端-商品列表 | Walmart product search |
| **Walmart前台** | @WallySmarter-商品详情 | Product detail, pricing & sales trend history |
| **eBay前台** | @ebay前端-商品列表 | eBay product search |
| **友鹰数据** | @友鹰-shopee商品选品 | Shopee product search and selection |
| **Ozon电商数据助手** | @Mpstats-Ozon-商品搜索 | Ozon Russia product search by keyword/SKU |
| **Ozon电商数据助手** | @Mpstats-Ozon-卖家商品 | Ozon seller drill-down: full product list with sales/stock/turnover |
| **Ozon电商数据助手** | @Mpstats-Ozon-类目商品 | Ozon category drill-down: bestseller and blue-ocean discovery |
| **Ozon电商数据助手** | @Mpstats-Ozon-品牌商品 | Ozon brand drill-down: competitor analysis and product structure |
| **Ozon电商数据助手** | @Mpstats-Ozon-商品详情 | Ozon batch SKU detail (price, sales, lost profit, FBO/FBS) |
| **Ozon电商数据助手** | @Mpstats-Ozon-商品趋势 | Ozon single-SKU daily trend (sales, price, stock, rating) |
| **专利检索** | @智慧芽-专利图像检索 | Design patent image search |
| **专利检索** | @睿观-外观专利检测 | Design patent infringement check |
| **专利检索** | @睿观-版权检测 | Copyright detection |
| **专利检索** | @睿观-图形商标检测 | Graphic trademark detection |
| **专利检索** | @睿观-文本商标检测 | Text trademark detection |
| **专利检索** | @睿观-发明专利检测 | Utility patent detection |
| **专利检索** | @睿观-政策合规检测（纯图检测） | Policy compliance (image check) |
| **专利检索** | @智慧芽-简单著录项 | Simple bibliographic info by patent ID/number |
| **专利检索** | @智慧芽-著录项目 | Full bibliographic data by patent ID/number |
| **专利检索** | @智慧芽-权利要求 | Patent claims lookup |
| **专利检索** | @智慧芽-权利要求翻译 | Patent claims translation (CN/EN/JP) |
| **专利检索** | @智慧芽-摘要翻译 | Patent abstract translation (CN/EN/JP) |
| **专利检索** | @智慧芽-说明书 | Patent description/specification |
| **专利检索** | @智慧芽-说明书翻译 | Patent description translation (CN/EN/JP) |
| **专利检索** | @智慧芽-法律状态 | Patent legal status and events |
| **专利检索** | @智慧芽-PDF全文 | Patent PDF full text |
| **专利检索** | @智慧芽-专利引用 | Forward citations (patents/literature cited) |
| **专利检索** | @智慧芽-专利被引用 | Backward citations (cited by other patents) |
| **专利检索** | @智慧芽-专利家族 | Patent family information |
| **专利检索** | @智慧芽-全文附图 | Full-text figures and drawings |
| **专利检索** | @智慧芽-摘要附图 | Abstract figures |
| **Sorftime** | @Sorftime-亚马逊产品搜索 | Product search with historical snapshots |
| **Sorftime** | @Sorftime-亚马逊产品详情(含趋势) | ASIN detail with trend history and profit |
| **AI工具** | @按商品主图相似度分组 | Group products by image similarity |
| **AI工具** | @分析商品主图 | Extract image prompts from product photos |
| **AI工具** | @对商品标题进行分词 | Title word segmentation |
| **AI工具** | @AI绘图 | Generate any image — products, characters, scenes, backgrounds, and more — from reference images + prompt (powered by top-tier Google Gemini model; ALL image generation tasks must use this tool) |
| **AI工具** | @图片识别 | Image recognition and analysis by URL + user intent |
| **AI工具** | @Google AI Mode | Google AI Overview (AI Mode) single-round search; returns Markdown summary with citations for cross-border deep research, consumer preference and long-tail selection insights; for follow-ups, agent summarizes prior result and re-asks in a new call |
| **沙箱** | @智能数据查询 | Dynamic data query and aggregation |
| **沙箱** | @excel内容提取并分析 | Excel file extraction and analysis |
| **沙箱** | @Python沙箱 | Process structured JSON data from prior steps: data calculation/filtering/sorting, generate Markdown tables, export to CSV/Excel, LLM-based image recognition (e.g. A+ image color/composition). Built-in LLM — use for ALL sandbox-execution needs. **Restrictions:** no nested calls; structured JSON only (no plain text/files); no chart generation or analysis reports. |
| **沙箱** | @智能Excel处理 | Smart Excel processing |
| **沙箱** | @分析PDF文件 | PDF file analysis with download link and user requirements |

### Tool Reference Files (by classification)

Read the relevant reference file when you need prompt templates and parameter constraints:

- **Keepa** (3 tools: 商品搜索、商品详情、价格历史): See `references/keepa.md`
- **亚马逊前台** (7 tools: 搜索模拟、商品详情、评论、以图搜图、Alexa助手、最新政策法规资讯、政策法规资讯详情): See `references/amazon-frontend.md`
- **亚马逊数据洞察** (3 tools: ABA-数据挖掘、商业洞察报告、商业洞察(反向)): See `references/amazon-data-insight.md`
- **Sif数据分析工具** (4 tools: ASIN关键词、关键词流量来源、ASIN流量来源、关键词竞品数量): See `references/sif.md`
- **卖家精灵** (2 tools: 选产品、查竞品): See `references/seller-sprite.md`
- **极目系列** (5 tools: 细分市场评论、市场信息、产品挖掘、产品挖掘(ASIN)、细分市场洞察): See `references/jimu.md`
- **谷歌趋势** (2 tools: 时下流行、关键词趋势): See `references/google-trends.md`
- **实时与全网检索** (1 tool: 网页检索): See `references/web-search.md`
- **TikTok电商数据助手** (5 tools: 新品榜、商品搜索、商品视频、热销榜单、商品搜索(FastMoss)): See `references/tiktok.md`
- **Walmart前台** (2 tools: 商品列表、商品详情): See `references/walmart.md`
- **eBay前台** (1 tool: 商品列表): See `references/ebay.md`
- **友鹰数据** (1 tool: shopee商品选品): See `references/youying.md`
- **店雷达/1688** (3 tools: 商品榜单、选品库、以图搜图): See `references/1688.md`
- **专利检索** (21 tools: 专利图像检索、外观专利检测、版权、图形商标、文本商标、发明专利、政策合规、简单著录项、著录项目、权利要求、权利要求翻译、摘要翻译、说明书、说明书翻译、法律状态、PDF全文、专利引用、专利被引用、专利家族、全文附图、摘要附图): See `references/patent.md`
- **Sorftime** (2 tools: 亚马逊产品搜索、亚马逊产品详情(含趋势)): See `references/sorftime.md`
- **AI工具** (6 tools: 主图相似度分组、主图分析、标题分词、AI绘图、图片识别、Google AI Mode): See `references/ai-tools.md`
- **沙箱** (5 tools: 智能数据查询、Excel分析、Python沙箱、Excel处理、分析PDF文件): See `references/sandbox.md`
- **卖家精灵（仓库内补充能力）**：除上表内置 `@卖家精灵-*` 工具外，选市场 / 市场统计 / 商品库类独立编排说明见 `references/seller-sprite.md` 文末 **「seller-sprite（包装 skill 分组）」** 小节。
- **领星 ERP（OpenAPI 编排）**：非内置工具；CLI 为 **`scripts/lingxing.py`**（与本 skill 内 `scripts/linkfox.py` 同级）。环境变量、工作目录与调用方式见 `references/lingxing-erp.md`；参数以领星官方文档与 `python3 scripts/lingxing.py --api help` 为准。

## Examples

### Example 1: Market Analysis

```
1、@卖家精灵-选产品 筛选亚马逊美国站的 "usb charger cable"，返回符合条件的 40 条商品数据
2、@智能数据查询 根据品牌、评分值、价格（每2美金一个阶梯） 统计月销量、月销售额、月销量占比、月销售额占比
3、生成对应的初步市场分析报告
```

### Example 2: Review Mining

```
@亚马逊-商品评论 @亚马逊前端-商品详情 亚马逊美国站，asin为B00163U4LK 的详情以及每个星级各100条
进行总结：展示他的人群特征、使用时刻、使用地点、使用场景、未被满足的需求、好评、差评、购买动机，每个要点要有描述、原因、数量占比。并最终给我一个改良建议
```

### Example 3: Competitor-based Listing Optimization

```
努力思考，选择适合以下场景的工具，完美完成以下任务：
亚马逊美国站，asin为:B0FPZHSLYR、B0CP9Z56SW、B0FFNF9TK1、B0FS7DRCLZ、B0CP9WRDFV、B0BWMZDCCN，我的竞品就是这些，你参考他们的五点描述和A+页面内容，生成我的商品的标题、五点描述
步骤：
1）查询以上所有asin的商品详情
2）查询每个asin的关键词
3）将上一步的全部关键词，构建关键词价值打分表
4）写作前再次查询亚马逊五点描述的写作要求和Amazon cosmo算法和经典营销理论FABE法则
5）生成5点描述，要求竞品的品牌词不能作为关键词，写出符合FABE法则和最新Amazon cosmo算法的五点描述，并且将关键词价值打分表价值高的词埋入
```

### Example 4: Visual Market Analysis

```
1、@亚马逊前台模拟搜索工具 筛选亚马逊美国站的，关键词为necklaces for women，默认排序，第一页的商品
2、对上一步的商品主体，统计主图不同挂件形状的销售额，绘制出不同形状的销售额占比
3、进行总结：把步骤二的数据完整的用精美的html网页显示给我看（不要精简)
```

### Example 5: Keyword Functional Analysis

```
1、@亚马逊前端搜索模拟 帮我在美国亚马逊站，以"computer desk"为关键词进行搜索，同时将配送地址设置为洛杉矶，最终返回搜索结果前2页的商品数据
2、@对商品标题进行分词 统计上一步商品标题中出现的功能点
3、按功能点统计月销量、月销售额、asin数
```

## Output Directory

Each task gets its own folder at `<skill>/scripts/output/{YYYYMMDDHHmm}/`. **The folder is created the moment the task is submitted** (not when results arrive), and a `result.json` is dropped immediately containing the `messageId` + original `task`. This way the messageId can always be recovered later — even if the original `linkfox.py` invocation's stdout was not captured (the default background mode just prints messageId and exits).

```
<skill>/scripts/output/{YYYYMMDDHHmm}/
├── result.json                      # Task metadata (created at submit; updated on completion)
├── {index}_{tool_name}.json         # Raw JSON response data (only after task completes)
└── result_{index}_{tool_name}.csv   # Structured data with Chinese column headers (only after task completes)
```

`result.json` lifecycle:

```jsonc
// At submit time (background mode exits here):
{
  "messageId":   "uDqHg33fQeQfkNB5pj5LLA",
  "task":        "在亚马逊美国站,搜索关键词 \"Sports Water Bottles\" 产品，配送方式FBA,按销量倒序的前50个",
  "status":      "submitted",
  "submittedAt": "2026-06-11T13:52:05",
  "url":         ""
}

// After --wait / --poll sees a terminal status:
{
  "messageId":   "uDqHg33fQeQfkNB5pj5LLA",
  "task":        "...",
  "status":      "finished",                          // finished / error / cancel / stop
  "submittedAt": "2026-06-11T13:52:05",
  "completedAt": "2026-06-11T13:55:30",
  "url":         "https://agent.linkfox.com/share/xxxx"
}
```

Field meanings:
- `messageId`: unique task identifier; the key the API uses to look up status / progress / results.
- `task`: the original user task description that was submitted.
- `status`: lifecycle marker — `submitted` after submit, then one of `finished/error/cancel/stop` once the task ends.
- `submittedAt` / `completedAt`: ISO-formatted local timestamps (no tz suffix).
- `url`: ShareURL — public, read-only share page for the entire conversation behind this run (intent, tool calls, intermediate outputs, reflection, final summary), with downloadable artifacts (CSV/Excel, images, HTML reports, attached files). Empty string until the task succeeds.

### Recovering messageId from local state

If the user comes back later and asks "我刚才那个任务到哪了 / what happened to the task I submitted?" but the messageId is no longer in the chat, run:

```bash
python3 <skill>/scripts/linkfox.py --list-recent      # 10 most recent local tasks
python3 <skill>/scripts/linkfox.py --list-recent 30   # last 30
python3 <skill>/scripts/linkfox.py --list-recent --format json   # for parsing
```

Output is one line per task, newest first:

```
2026-06-11T13:52:05  finished    uDqHg33fQeQfkNB5pj5LLA  在亚马逊美国站,搜索关键词 "Sports Water Bottles"...
2026-06-11T13:48:02  submitted   pKlMnOpQrStUvWxYzAbCdE  @卖家精灵-选产品 筛选亚马逊美国站的 ...
```

Pick the matching task, then call `--status <messageId>` for live progress or `--poll <messageId>` to fetch the full result.

**To access result data:** list CSV files in the timestamped directory (`ls <skill>/scripts/output/{YYYYMMDDHHmm}/*.csv`) and read them directly.

## Retry on Failure

If a tool call fails, the response includes error details. Retry with adjusted parameters based on the error message. Common issues:
- Parameter out of range (check min/max constraints)
- Invalid pattern format (check regex patterns)
- Too many tools in one task (max 10)

