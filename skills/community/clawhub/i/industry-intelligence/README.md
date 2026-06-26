# 行业情报 / Industry Intelligence

一个为 Claude Code 打造的竞争情报技能，帮助用户对任意行业建立结构化的竞争情报体系 — 从资源库构建、全网信息汇聚到专业报告生成，一站式完成。

A competitive intelligence skill built for Claude Code. It helps users establish a structured competitive intelligence system for any industry — from resource library construction and full-web information aggregation to professional report generation, all in one workflow.

---

## 核心特性 / Key Features

### 双模式自动切换 / Dual-Mode Auto-Switching

技能被调用时自动判断工作模式：若目标行业尚无资源库则进入**建库模式**；若资源库已存在则直接进入**采集模式**。资源库只需构建一次，后续采集复用同一份资源库，用户可随时增量补充竞争对手或更正信息源。

The skill automatically detects the working mode on invocation: if no resource library exists for the target industry, it enters **Library-Building Mode**; otherwise it goes directly to **Collection Mode**. The library is built once and reused across all future collections — users can incrementally add competitors or correct sources at any time.

### 七大情报类别 / Seven Intelligence Categories

每条情报被归入七大标准类别，管制类与非管制类行业自动切换栏目名，确保覆盖面完整且结构统一：

Every piece of intelligence is classified into seven standardized categories, with the first category name auto-switching based on whether the industry is regulated:

| 类别 / Category | 说明 / Description |
|----------------|-------------------|
| 🏛️ 监管动态 / 政策动态 | 管制类行业（金融、医疗、能源等）使用"监管动态"，非管制类行业（互联网、消费、零售等）使用"政策动态"。 Regulated industries (finance, healthcare, energy) use "Regulatory Updates"; unregulated ones (internet, consumer, retail) use "Policy Updates". |
| 📌 媒体关注 | 权威媒体报道的并购重组、战略调整、年报季报发布、高管变动等重大事件。 Major events from authoritative media: M&A, strategy shifts, annual/quarterly reports, executive changes. |
| 🏢 企业官方发布 | 同业公司通过官网、微信公众号、视频号等官方渠道发布的公告与新闻。 Official announcements from competitors' websites, WeChat accounts, and other official channels. |
| 💼 业务动态 | 同业在业务领域的创新突破，重点关注新产品/新服务发布，影响力评分自动加权 +0.5。 Business innovations, with +0.5 impact weighting for new product/service launches. |
| 🔬 企业数智化动态 | 同业在数字化与智能化领域的重大投入，重点关注新系统上线与 AI 等新技术落地，影响力评分自动加权 +0.5。 Major digital transformation initiatives with +0.5 impact weighting for new systems and AI deployments. |
| 🌍 国际同行 | 海外同业机构动态，来源包括 Bloomberg、Reuters、FT、WSJ 等国际媒体与公司官网、Twitter/X、LinkedIn。 Updates on international peers from Bloomberg, Reuters, FT, WSJ, official websites, Twitter/X, and LinkedIn. |
| 🌫️ 江湖传闻 | 可信度 ≤ 3.5 的非权威信息，来自自媒体、微博、知乎、雪球等社区渠道，附风险提示。 Non-authoritative information (credibility ≤ 3.5) from social media and forums, marked with risk warnings. |

### 双维度智能评分 / Dual-Dimension Scoring

每条情报均标注**可信度**（1.0-5.0）和**影响力**（1.0-5.0）两项评分，精确到小数点后 1 位，并附舆情方向（正面/中性/负面）。业务创新与数智化类信息自动获得 +0.5 影响力加权，确保高价值情报优先呈现。

Each piece of intelligence is scored on two dimensions — **Credibility** (1.0-5.0) and **Impact** (1.0-5.0), precise to one decimal place — plus a sentiment tag (Positive / Neutral / Negative). Business innovation and digital transformation news automatically receive a +0.5 impact bonus, ensuring high-value intelligence surfaces first.

### 两步走采集策略 / Two-Step Collection Strategy

采集遵循**"全网汇聚 → 头部深挖"**策略，平衡覆盖面与调用开销：第一步用 WebSearch 进行全网新闻检索，快速覆盖监管动态、媒体关注与国际报道；第二步仅对行业 Top 10 头部企业的官网做深度排查补充，避免对 30 家公司官网逐一暴力穷举。

Collection follows a **"Web Aggregation → Head Deep Dive"** strategy that balances coverage with API cost: first, use WebSearch to sweep the open web for news across regulators, media, and international sources; second, deep-dive only into the top-10 head competitors' official websites for supplementary disclosure. No brute-force crawling of all 30 competitor sites.

### 情报条数动态限额 / Dynamic Item Count Caps

报告总条数根据时间跨度动态设定：月报 30-50 条、周报 20-30 条、日报 10-20 条；同时单个数据源（单家公司）最多入选 2 条，按影响力排序截取，防止信息臃肿与单一公司刷屏。

Total report items are capped by time span: monthly report 30-50 items, weekly 20-30, daily 10-20. A single source (single company) contributes at most 2 items, ranked by impact — preventing bloat and single-company dominance.

### 双报告格式 / Dual Report Formats

- **简报 / Brief**：一句话摘要 + 评分，快速掌握行业脉搏，仅生成 Markdown。  
  One-line summary + scores for a quick industry pulse. Markdown only.

- **详报 / Detail**：完整摘要 + 原文链接 + 执行摘要 + 舆情统计表 + 数据源统计表，同时生成 Markdown 和 PDF，PDF 生成失败时自动降级为仅 Markdown 输出，不中断任务。  
  Full summaries, source links, executive summary, sentiment stats, and data source stats. Produces both Markdown and PDF, with automatic graceful degradation to Markdown-only if PDF generation fails.

### 统一采集工具箱 / Unified Collection Toolbox

`scripts/web_fetchers.py` 以命令行子命令形式整合四类常用采集能力，无需编写临时 Python 代码：

`scripts/web_fetchers.py` consolidates four common collection capabilities as CLI subcommands — no ad-hoc Python required:

| 子命令 / Subcommand | 用途 / Purpose |
|---------------------|----------------|
| `dynamic <URL>` | 调用 Playwright 无头浏览器渲染 SPA / JS 依赖页面。 Renders SPA/JS-dependent pages via headless Playwright. |
| `encoding <URL>` | 自动检测并转换 GBK/GB2312 等非 UTF-8 编码中文网页。 Auto-detects and converts GBK/GB2312 Chinese pages to UTF-8. |
| `xueqiu` | 通过雪球公共热帖 JSON API 采集散户舆情。 Fetches retail sentiment via the Xueqiu public hot-post JSON API. |
| `zhihu <URL>` | 解析知乎指定问题的答案列表。 Parses the answer list of a specified Zhihu question. |

红线：严禁模拟登录或自动化抓取微信、抖音、小红书等闭源生态 — 遇此类源建议手工翻阅或走 RSS。

Red line: **never** attempt to simulate login or scrape closed ecosystems like WeChat, Douyin, or Xiaohongshu — handle those manually or via RSS.

### 完整采集日志 / Full Collection Logs

每次采集自动生成详细日志，记录每个数据源的访问状态、获取条数、跳过原因与错误详情，支持采集质量回溯与审计。日志按 ISO 8601 时间戳命名，超过 7 天自动清理。

Each collection produces a detailed log tracking every data source's status, item count, skip reason, and error details — enabling quality tracing and auditing. Logs are named with ISO 8601 timestamps and auto-cleaned after 7 days.

### PDF 生成与字体降级 / PDF Generation with Font Fallback

`scripts/md_to_pdf.py` 使用 reportlab 将 Markdown 详报转为排版精美的中文 PDF，内置**三级字体降级链**：优先使用 `fonts/` 目录下的开源思源字体（Noto Serif SC / Noto Sans SC），其次回退到系统字体（Windows/macOS/Linux 路径自动适配），最终兜底 Helvetica，跨平台无缝兼容。

`scripts/md_to_pdf.py` converts Markdown reports to well-formatted Chinese PDFs using reportlab, with a **three-tier font fallback chain**: first tries open-source Noto fonts in `fonts/`, then system fonts (auto-detected across Windows/macOS/Linux), finally Helvetica as last resort — cross-platform without manual configuration.

### 模板驱动 / Template-Driven

资源库、简报、详报、采集日志均基于 `templates/` 目录下的独立模板文件，SKILL.md 仅引用路径而不内联大段模板，最大限度节省 context window。

Resource libraries, briefs, detail reports, and collection logs are all driven by standalone template files under `templates/`. SKILL.md references them by path instead of inlining, maximizing context window efficiency.

---

## 快速开始 / Quick Start

### 触发方式 / Trigger

在 Claude Code 中提及以下关键词即可触发本技能：

Mention any of these keywords in Claude Code to trigger this skill:

> "行业情报"、"竞争对手动态"、"行业动态"、"监管动态"、"政策动态"、"行业情报收集"、"国际同行"、"企业数智化"、"江湖传闻"，或描述需要了解某行业的竞争格局、跟踪同业动向。

### 建库 / Build Library

首次使用时确认三项信息：

On first use, confirm three items:

1. **行业名称 / Industry** — 如"证券"、"公募基金"、"财产保险"
2. **竞争对手范围 / Scope** — 头部企业（前10）、中坚力量（11-30）、全市场或自定义
3. **区域范围 / Region**（可选）— 如"华东"、"广东省"

生成文件 / Output: `{当前工作区}/industry-intelligence/resource/{行业名称}-resources.md`

资源库、报告与日志**始终写入 agent 当前工作区**下的 `industry-intelligence/` 目录，不写入技能安装目录。

Libraries, reports, and logs are **always written into the agent's current workspace** under an `industry-intelligence/` subdirectory — never into the skill install directory.

### 采集与报告 / Collect & Report

资源库就绪后确认：

Once the library is ready, confirm:

1. **时间范围 / Time Range** — 由用户指定，不设默认值
2. **报告类型 / Report Type** — 简报 (Brief) 或 详报 (Detail)，未明确时默认详报
3. **重点关注 / Focus**（可选）— 特定公司或类别

生成文件 / Output（路径均相对当前工作区 / paths relative to current workspace）:
- `./industry-intelligence/reports/{行业名称}行业情报-{日期}.md` + `.pdf`（详报）
- `./industry-intelligence/reports/{行业名称}简报-{日期}.md`（简报）
- `./industry-intelligence/log/{报告名称}-{时间戳}.md`（采集日志）

---

## 目录结构 / Directory Structure

```
industry-intelligence/
├── SKILL.md                 # 技能主文件 / Main skill file
├── README.md                # 本文件 / This file
├── LICENSE                  # MIT License
├── templates/               # 报告模板 / Report templates
│   ├── resource.md          #   资源库模板
│   ├── brief-report.md      #   简报模板
│   ├── detail-report.md     #   详报模板
│   └── log.md               #   采集日志模板
├── scripts/                 # 辅助脚本 / Helper scripts
│   ├── web_fetchers.py      #   统一采集工具箱 (dynamic/encoding/xueqiu/zhihu)
│   ├── md_to_pdf.py         #   Markdown → PDF 转换
│   └── download_fonts.py    #   开源字体下载
├── fonts/                   # 开源中文字体 / Open-source CJK fonts
├── resource/                # 行业资源库 / Industry resource libraries
├── reports/                 # 生成的报告 / Generated reports
├── log/                     # 采集日志 / Collection logs
├── evals/                   # 评测用例 / Evaluation cases
│   └── evals.json
└── examples/                # 示例输出 / Example outputs
```

---

## 依赖 / Dependencies

**Python 包 / Python Packages**（仅辅助脚本需要 / only for helper scripts）：

```bash
pip install markdown reportlab requests beautifulsoup4 playwright
playwright install chromium
```

**字体 / Fonts**（PDF 生成可选 / optional for PDF）：

```bash
python scripts/download_fonts.py
```

下载思源宋体（Noto Serif SC）和思源黑体（Noto Sans SC）到 `fonts/` 目录。未下载时脚本会自动回退至系统字体或 Helvetica，不影响任务完成。

Downloads Noto Serif SC and Noto Sans SC into `fonts/`. If unavailable, the script falls back automatically to system fonts or Helvetica without breaking the workflow.

---

## 许可证 / License

MIT

## 作者 / Author

sunhang (citywanderr)
