---
slug: global-biblio-base
name: global-biblio-base
displayName: 全球12亿文献知识库（8千万中文期刊可下载）
version: 3.6
description: |
  全球12亿文献知识库（8千万中文期刊可下载）——覆盖8000万篇授权中文期刊全文+12.28亿条全球文献元数据（含期刊7.19亿、专利2.15亿、会议论文7155万、学位论文2473万、标准268万等）。
  内置三级检索策略（宽检索高查全/窄检索高查准/平衡策略），支持关键词检索、文献详情查看、全文下载（中文直接下载+外文十级渠道自动探测+OA免费下载）、迭代优化检索、引文追溯、分类号检索、结果质量评估。
  ✨ 亮点：每篇文献提供原始数据库来源链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等，覆盖率100%，平均4.75个链接/篇），可直接跳转验证文献真实性。
  💎 OA文献下载：OA文献（Gold/Hybrid/Bronze/Green OA）通过十级渠道免费获取PDF，不消耗SmartLib配额。
  全程自动化：首次使用自动注册开通（免费100次/月），按实际API调用次数计费（共5个接口：中文检索/全球检索/中文详情/全球详情/全文下载，每次调用计1次），配额自动消耗，用尽后引导充值续费。配额耗尽后暂停检索服务，直接提示充值。全程对话驱动，无需人工申请或独立平台。
  适用于用户需要查找中外文学术论文、期刊文献、学位论文、专利、标准等场景。
  当用户表达"查论文""找文献""检索学术""搜索期刊""查专利""找标准""找论文""搜文献""学术检索""文献调研""文献综述""下文献""下论文""下载论文""论文下载""搜论文""查SCI""查EI""英文论文""中文论文""论文搜索""文献搜索""学术搜索""找参考文献""写毕业论文""开题报告文献""课题查新""论文查新""文献调研工具""考研文献""帮我找论文""论文在哪找""怎么查文献"等意图时触发。
  也适用于用户提到具体学术主题并希望获取相关论文的场景，如"帮我找一些关于XX的论文""XX领域有哪些研究""帮我写文献综述""引用几篇文献支撑论点"。
  英文触发词："find papers", "search literature", "write literature review", "find supporting citations", "search papers", "literature review"。
  若检测到 API 凭证未配置，自动通过 smartlib-gateway 注册开通（免费 100 次/月），全程对话驱动无需人工申请。
  / Global 1.2B literature knowledge base (80M Chinese journal articles downloadable).
  Three-tier search strategy (broad/high-recall, narrow/high-precision, balanced), keyword search, detail view, full-text download, iterative refinement, citation tracing, classification-based search, result quality assessment.
  Fully automated: auto-registration (100 free/month), quota consumed per API call (search/detail/download each=1 call), auto quota tracking, WeChat Pay recharge available. When quota exhausted, search service paused with recharge prompt.
  Triggers on Chinese/English intents like "find papers", "search literature", "查论文", "找文献", "学术检索", "write literature review", "find supporting citations".
  Auto-detects missing API credentials and auto-registers via smartlib-gateway (100 free/month).
  Production URL: read from config.json → SMARTLIB_GATEWAY_URL (Gateway v47, version 67)
agent_created: true
---

# 全球12亿文献知识库（8千万中文期刊可下载）

> 中文 / Chinese | [English below each section]

通过 SmartLib 开放平台 API 提供中外文学术文献检索能力。

> Powered by SmartLib Open Platform API. Search across 80M Chinese journal articles and 1B global literature records.

---

## ⚡ 启动前必须执行 / Pre-flight Checklist

### Step A：凭证自动检测 & 注册 / Auto Credential Check & Registration

> ## ⚠️ 强制规则 — 必须先询问邮箱
> 1. **执行任何操作前，必须先询问用户邮箱地址**
> 2. 禁止使用 config.json 中预填的邮箱（即使存在且非 null）
> 3. 禁止自动生成邮箱（如 `user@example.com`、`auto@xxx.com` 等）
> 4. 用户未提供邮箱 → 停止执行，回复：
>    "请提供您的邮箱地址以注册 SmartLib 文献检索服务（新用户免费 100 次/月）"
> 5. 只有用户明确输入邮箱后，才能调用 /register 或 /quota
>
> ## 邮箱识别自动化
> 当用户消息中出现以下模式时，自动提取邮箱 → 无需再次询问：
> - 明确的邮箱地址（包含 @ 符号的完整地址，如 `xxx@xxx.xxx`）
> - "我的邮箱是 xxx" / "email: xxx" / "用 xxx 注册" / "邮箱 xxx"

每次执行本技能时，按以下流程处理凭证（从 config.json 读取）：

```
读取技能目录下的 config.json
检查 SMARTLIB_EMAIL 是否已配置
  ├── 已配置 → 进入 Step B (配额检查)
  │
  └── 未配置 → 自动注册流程:
        ├── ① 展示检索计划 + 询问邮箱（一句话）:
        │      "📋 我将用中英文关键词检索... 首次使用需绑定邮箱（免费 100 次/月，仅用于配额管理），请输入邮箱即可开始:"
        │      用户输入 → 写入 config.json
        │
        ├── ② 调智能网关注册（无需验证码，极速注册）:
        │     POST {SMARTLIB_GATEWAY_URL}/register
        │     Headers: {"Authorization": "Bearer {SMARTLIB_GATEWAY_SECRET}"}
        │     Body: {"email": "{用户邮箱}"}
        │
        ├── 成功 (201/200) → Gateway 返回配额信息
        │     提示: "✅ 注册成功！本月免费 100 次，可立即使用。确认邮件已发送（邮箱验证仅充值时需要，现在不验证也能用）。"
        │     追加引导: "请告诉我您想检索什么主题，现在就可以开始——"
        │     → 继续 Step B 配额检查 → 检索
        │
        └── 失败 → 提示原因 (服务暂不可用 / 网络错误等) → 终止
```

> **注意**：注册无需验证码，极速完成。**注册后即可立即使用全部功能**，确认邮件为可选项（仅充值时需验证邮箱）。
> 

### Step B：配额检查 / Quota Check

```
凭证就绪后, 调网关查询配额:
  GET <SMARTLIB_GATEWAY_URL>/quota?email=<SMARTLIB_EMAIL>
  Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}

  返回字段: total_remain, email_verified, plan
  （完整返回: user_id, email, plan, trial_total, trial_used, trial_remain, paid_total, paid_used, paid_remain, paid_expires_at, total_remain, email_verified）
  
  如果返回 404 "not_registered" → 用户可能已被重置/删除
    → 提示: "检测到您的账户需要重新绑定，正在自动重新注册..."
    → 跳回 Step A ②（调 /register 重新注册，使用同一邮箱）
    → 注册成功后继续配额检查
  
  total_remain > 20 → 静默进入检索
  total_remain 5-20 → 尾部轻提示: "📊 本月剩余 {n} 次"
  total_remain 1-5  → 警告: "⚠️ 接近用尽（剩余 {n} 次），回复「充值」查看套餐（数字 1-4 选）"
  total_remain 0    → 配额耗尽处理（见配额耗尽章节）

  额外检查:
```

### Step C：按接口调用次数消耗配额 / Per-API-Call Quota Consumption

本技能的配额按**实际 API 接口调用次数**计费，不是按对话会话计费。

共涉及 **5 个接口**（分3类），每次调用其中任意一个接口计 **1 次**配额。

> Quota is consumed **per API call**, not per conversation session. **5 interfaces** in 3 categories, each call = 1 quota.

**计费接口清单（5个）/ Billable Interfaces (5 total):**

| 类别 | 接口 | API 端点 | 计费 |
|------|------|---------|------|
| **检索** | 中文期刊检索 | API 1 `Articlesearch` | 每次调用 **1 次** |
| **检索** | 全球文献检索 | API 4 `Articlesearch` | 每次调用 **1 次** |
| **详情** | 中文期刊详情 | API 1/5 `Articledetail` | 每次调用 **1 次** |
| **详情** | 全球文献详情 | API 4/5 `Articledetail` | 每次调用 **1 次** |
| **下载** | 中文期刊全文下载 | API 3 `GetArticleFile` | 每次调用 **1 次** |

> 注：全球文献（API 4）无全文下载接口，仅返回元数据。

**计次示例 / Counting Examples:**

```
示例1：用户请求"查10篇工业母机论文，下载5篇中文PDF"
  → 检索接口：中文1次 + 英文1次         = 2 次
  → 详情接口：查5篇详情                   = 5 次
  → 下载接口：下载5篇PDF                  = 5 次
  → 合计消耗: 12 次配额
```

```
示例2：用户请求"帮我看看这篇论文的详情"（1篇）
  → 详情接口：1次                         = 1 次
  → 合计消耗: 1 次配额
```

```
示例3：用户仅请求"检索人工智能论文"（不查看详情、不下载）
  → 检索接口：1次（或2次，若中英文并行） = 1-2 次
  → 合计消耗: 1-2 次配额
```

**扣减方式 / Deduction Method:**

**⚠️ 强制执行规则：每次调用计费接口前，必须先调 `/consume` 获取 token，再用 token 调 `/search`。**

每次调用计费接口的流程：

```
① POST <SMARTLIB_GATEWAY_URL>/consume
   Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
   Body: {"email": "<SMARTLIB_EMAIL>", "skill_source": "global-biblio-base"}

   返回 200 → 获取 consume_token，继续
   返回 429 → 配额已用完，终止后续调用，提示充值

② POST <SMARTLIB_GATEWAY_URL>/search
   Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
   Body: {
       "email": "<SMARTLIB_EMAIL>",
       "consume_token": "<上一步返回的token>",
       "skill_source": "global-biblio-base",
       "api_path": "/openapi/t/data0012/doccenter/Articlesearch",
       "api_body": {<检索请求体>}
   }

   返回 200 → 检索成功
   返回 401 → token 无效/过期/已用，需重新 /consume
```

> **MANDATORY**: Call `/consume` → `/search` for **EACH** billable API call. Token is single-use, expires in 60s. If 401 on /search, re-consume.

**🛡️ Token 绑定调用链 / Token-Bound Call Chain:**

> **强制安全机制 — 不可绕过：**
> 每次调用计费接口前，必须通过 `/consume` 获取 `consume_token`，然后将 token 传给 `/search` 代理端点。
> Gateway 验证 token 签名 + 有效期 + 防重放后才转发检索请求。
> Token 由 GATEWAY_SECRET 签名，AI 无法伪造。无有效 token 则 /search 直接 401。
>
> **调用流程 / Call Flow:**
> ```
> 1. POST /consume {"email":"...", "skill_source":"global-biblio-base"} → 返回 consume_token
> 2. POST /search {"email":"...", "consume_token":"...", "skill_source":"global-biblio-base", "endpoint":"/search/cn", "rule":"..."}
>    → Gateway 验证 token → 代理转发到检索 API → 返回检索结果
> ```
>
> **注意**：每个 consume_token 只能使用一次（防重放），有效期 60 秒。每次检索 API 调用前都需要先 /consume 获取新 token。

**🆕 v36 行为：仅成功调用消耗配额 / Quota Deducted on Success Only:**

> `/consume` 仅验证配额可用性 + 签发 token，**不预扣配额**。配额在实际调用 SmartLib API 且返回成功后，由 Gateway 自动扣除。
> **失败的 API 调用不消耗配额**（如参数错误导致 400、网络错误导致 500 等）。
> `/consume` 返回的 `total_remain, email_verified, plan` 反映的是当前已成功调用的次数，非预扣后的值。

**不计费的操作 / Non-billable Operations:**

| 操作 / Operation | 说明 / Note |
|------|------|
| /consume 配额消费 | Gateway 验证，不计费 |
| 联网关键词扩展 | Web search，不计费 |
| 结果排序/格式化展示 | 本地处理，不计费 |
| 多级 OA PDF 探测 | 外部免费 API（ArXiv/Unpaywall/CORE/OpenAlex等），**不消耗 SmartLib 配额** |
| 原始来源链接展示 | Source 字段随详情接口返回，不计额外费用 |


---

## 💰 支付与充值 / Payment & Recharge

### 触发时机
1. 配额为 0 (gateway 返回 429)
2. 用户说 "充值" "续费" "购买"

### 套餐列表

| 套餐 | plan key | 价格(元) | 配额 | 说明 |
|------|----------|---------|------|------|
| 体验包 | `trial` | 9.90 | 1000 次 | 限购 1 次 |
| 基础月付 | `basic` | 29.00 | 5000 次/月 | 个人用户 |
| 进阶月付 | `pro` | 99.00 | 20000 次/月 | 轻度团队 |
| 专业月付 | `enterprise` | 299.00 | 100000 次/月 | 重度使用 |

> **plan key**：调用 `/api/pay/create` 时传 `trial`/`basic`/`pro`/`enterprise`。金额单位为**元**（非分）。

### 支付流程（对话交互，数字选套餐）

全部在对话中完成，用户只需回复数字：

```
配额耗尽/用户说"充值" →
    ↓
⓪ 展示套餐卡片（show_widget），用数字①②③④标注:
   ① 体验包 ¥9.90 — 1,000 次/月
   ② 基础月付 ¥29.00 — 5,000 次/月
   ③ 进阶月付 ¥99.00 — 20,000 次/月 [推荐]
   ④ 专业月付 ¥299.00 — 100,000 次/月
   用户回复数字 (如 "3")
    ↓
   映射: "1"→trial, "2"→basic, "3"→pro, "4"→enterprise
    ↓
① 调 Gateway 生成订单:
  POST {SMARTLIB_GATEWAY_URL}/api/pay/create
  Headers: {"Authorization": "Bearer {SMARTLIB_GATEWAY_SECRET}"}
  Body: {"plan": "basic", "amount": 29.00, "quota": 5000, "email": "{SMARTLIB_EMAIL}"}

  返回: {"code_url": "weixin://...", "out_trade_no": "WB...", "amount": 29.00, "plan": "basic", "quota": 5000}
    ↓
② 生成带订单信息的二维码 HTML 页面，用 preview_url 在对话内展示:

  **页面必须包含：套餐名称、金额、配额标签、二维码、订单号**
  用 qrcode.js CDN 将 code_url 渲染为二维码。
  样式参考：渐变紫色背景 + 白色卡片 + 居中布局。

  ⚠️ 不要在卡片内容中显示用户邮箱

    ↓
③ 轮询支付状态:
  GET {SMARTLIB_GATEWAY_URL}/api/pay/status?out_trade_no=xxx
  (间隔 3s 轮询,最多轮询 20 次 ≈ 60s，超时提示重新发起)

  支付成功时返回:
  {"status":"paid", "auto_recharged":true, "quota_remain":5000, "quota_total":5100, "quota_used":100}
    ↓
④ 对话中通知结果:
  "✅ 支付成功! 已自动充值 5000 次，当前剩余 5000 次。"
    ↓
  自动重试上次中断的检索
```

### 为什么不需要 /recharge？
支付回调 (`/api/pay/notify`) 由微信支付服务器直接通知 Gateway，Gateway 在回调中**同一事务内**完成标记订单 paid + 累加配额。`/api/pay/status` 查询到 paid 时配额已到账，无需额外操作。

### 安全机制
- 网关通过 `out_trade_no` UNIQUE 索引防重复充值
- 二维码 5 分钟有效, 超时需重新发起
- `/api/pay/status` 为公开端点（无需 Bearer Token），可直接轮询
- `SMARTLIB_GATEWAY_SECRET` 仅供后端调用, 不在对话中输出
- ⚠️ 生成的支付 HTML 页面上**禁止显示用户邮箱**，仅显示套餐信息

---

## 🔒 配额耗尽处理 / Quota Exhaustion

配额耗尽后，**暂停新的检索请求**，不再展示任何部分结果。

| 状态 | 行为 |
|------|------|
| **配额充足** (>0) | 正常执行检索，完整展示所有结果（含详情查看、全文下载、智能排序） |
| **配额耗尽** (=0) | Gateway 返回 429，**拒绝服务**，直接提示充值 |

配额耗尽后的提示格式：

```
⚠️ 您的 SmartLib 检索配额已用尽（0/100次）。

当前配额不支持发起新检索。请充值后继续使用。

> 💰 充值套餐：
> 体验包：¥9.90 / 1000次
> 月付基础：¥29.00 / 5000次/月
> 月付进阶：¥99.00 / 20000次/月
> 月付专业：¥299.00 / 100000次/月
> 回复「充值」查看套餐（回复数字 1-4 选择），支付后立即生效。
```

**重要规则**：
- 配额耗尽后，**所有检索请求一律拒绝**，不展示任何结果
- 用户需先充值恢复配额，才能继续使用检索功能
- 充值后立即生效，无需等待

---

## 输出规范 / Output Standards

**每次检索结果末尾必须展示配额状态：**

```
📊 本次消耗 3 次 | 剩余 82 次 (共 100 次/月)
```
或接近耗尽时：
```
⚠️ 剩余 3 次 (共 100 次/月)，回复「充值」选套餐
```

```
```

## 核心能力 / Core Capabilities

| 能力 / Capability | 说明 / Description |
|------|------|
| **中文期刊检索 / Chinese Journal Search** | 8000万篇授权中文期刊文献，支持全文下载 / 80M authorized Chinese journal articles with full-text download |
| **全球文献检索 / Global Literature Search** | 10亿篇中外文文献元数据（含中英文论文、专利、标准、学位论文等）/ 1B global literature metadata (papers, patents, standards, theses) |
| **文献详情 / Article Detail** | 查看摘要、DOI、基金资助、核心收录等完整信息 / View abstracts, DOI, funding, core journal indexing |
| **全文下载 / Full-text Download** | 授权中文期刊支持 PDF 全文下载 / PDF download for authorized Chinese journals |
| **原始来源链接 / Source Links** | 每篇文献提供多个原始数据库详情链接（覆盖300+数据库，如Scopus/WoS/EI/PubMed等），覆盖率100%，平均4.75个/篇，可直接验证文献真实性 / Multi-database source links for authenticity verification |
| **OA文献免费下载 / OA Free Download** | 十级多渠道自动探测OA文献PDF（ArXiv/Unpaywall/CORE/OpenAlex等），Gold/Hybrid/Bronze/Green OA免费获取，**不消耗SmartLib配额** / OA PDF auto-detection via 10 channels, no quota consumption |
| **智能关键词扩展 / Smart Keyword Expansion** | 联网检索中英文同义词/近义词，自动扩展检索词，提升召回率 / Web search for synonyms to expand search terms |
| **核心期刊优先排序 / Core Journal Priority** | 联网查询核心收录情况（SCI/EI/北大核心/CSSCI等），优先展示高水平文献 / Rank by core journal indexing (SCI/EI/CSSCI etc.) |
| **相关性智能排序 / Relevance Ranking** | 基于题名、关键词、摘要语义分析，对检索结果进行二次相关性排序 / Semantic relevance re-ranking |
| **少结果智能扩展 / Low-result Expansion** | 结果过少时自动推荐上位词、相关机构、学科分类号等多种扩展策略 / Auto-suggest broader terms and alternative strategies |

## 能力边界 / Capability Boundaries

### 支持的功能 / Supported

- 中文期刊论文检索、详情、全文下载（8000 万篇授权文献）
- 全球文献元数据检索（10 亿篇，含论文/专利/标准/学位论文等）
- 关键词智能扩展、核心期刊优先排序、少结果自动扩展
- 自然语言输入，无需学习检索语法

### 不支持的功能 / Not Supported

- **付费墙内英文文献全文下载**：通过 SmartLib API 4 查到的全球文献仅返回元数据。本技能已集成十级多渠道下载策略（ArXiv/Unpaywall/CORE/OpenAlex/Semantic Scholar/Crossref/DOI.org/Europe PMC/bioRxiv/medRxiv + CDP浏览器），可免费获取 OA 版本（Gold/Hybrid/Bronze/Green OA），**OA 下载不消耗 SmartLib 配额**。但付费墙内（closed access）文献无法获取全文
- **付费墙内文献**：不提供需单独购买的文献全文
- **批量导出**：不提供 EndNote/BibTeX 等格式的批量导出功能
- **文献查重/查新**：不具备论文查重或科技查新功能

### 使用限制 / Limitations

| 限制项 / Limit | 说明 / Description |
|------|------|
| **单次查询条数 / Per-query limit** | PageSize 20-1000，建议 ≤100 以保证速度 / Recommend ≤100 |
| **翻页上限 / Max pages** | 无硬限制，但建议不超过 50 页（共 1000 条）/ No hard limit, but ≤50 pages recommended |
| **请求频率 / Rate limit** | 有频率限制（未公开数值），触发 429 时自动等待重试 / Undisclosed limit; auto-retry on 429 |
| **Token 有效期 / Token TTL** | Access Token 30 秒，Refresh Token 2 小时。系统自动管理刷新 / Access Token 30s, Refresh Token 2h. Auto-managed. |
| **下载链接有效期 / Download URL TTL** | 约 10 分钟，过期需重新调用下载接口 / ~10min, re-call download API |
| **依赖 / Dependencies** | 完全依赖 SmartLib API 和网络连接，离线不可用 / Requires network + SmartLib API |

### 触发意图区分 / Trigger Intent Differentiation

| 用户表达 / User Expression | 系统行为 / System Behavior | 区分逻辑 / Rationale |
|------|------|------|
| "查论文"、"找文献"、"检索XX" / "Search XX papers" | **触发本 Skill**，精准检索，默认平衡策略 | 明确的检索意图 |
| "写文献综述"、"帮我写综述" / "Write a literature review" | **触发本 Skill**，切换为综述模式：宽检索策略、去重合并、按主题聚类 | 综述需更全的覆盖范围和聚类分析 |
| "帮我写论文开头/引言" / "Write paper intro, need citations" | **触发本 Skill**，窄检索策略：找 3-5 篇最相关引用，核心期刊优先 | 写作引用需要精准而非全面 |
| "这段论述有文献支撑吗"、"找几篇引用" / "Find supporting citations" | **触发本 Skill**，窄检索 + 核心期刊优先，提供可引用的高质量文献 | 文献支撑场景需要高可信度来源 |
| "这篇论文是真的吗"、"核查引用" / "Verify this citation" | **不触发本 Skill**，应转至 smartlib-citation-checker | 引用核查是独立能力 |
| "帮我写论文"、"写作辅助" / "Help me write" | **不触发本 Skill** | 论文写作不是文献检索功能 |
| "下载这篇论文的 PDF" / "Download this paper's PDF" | **触发本 Skill**（若有中文期刊 ID） | 下载是检索的延伸功能 |

## 数据范围 / Data Coverage

平台累计汇聚各类资源元数据总量达 **12.28 亿条**。

> The platform aggregates **1.228 billion** metadata records.

### 核心文献类型存量规模 / Core Literature Type Inventory

| 文献类型 / Type | 存量规模 / Inventory | 说明 / Notes |
|------|------|------|
| **期刊文献 / Journal Articles** | **7.19 亿条 / 719M** | 平台核心资源 / Largest category |
| **专利资源 / Patents** | **2.15 亿条 / 215M** | 第二大品类 / Second largest |
| **会议论文 / Conference Papers** | **7155 万条 / 71.55M** | — |
| **学位论文 / Theses & Dissertations** | **2473 万条 / 24.73M** | — |
| **标准资源 / Standards** | **268 万条 / 2.68M** | — |

### 可检索数据集 / Searchable via API

- **中文期刊数据集 / Chinese Journal Dataset**：8000 万篇授权中文期刊文献，支持全文下载 / 80M authorized Chinese journal articles with full-text download
- **全球文献数据集 / Global Literature Dataset**：覆盖全平台 12.28 亿条元数据 / Covers all 1.228B metadata records

## 环境配置 / Environment Configuration

配置存储于技能目录下的 `config.json`：

> Config persisted at skill-level config.json:

```json
{
  "SMARTLIB_GATEWAY_URL": "https://<your-gateway>.ap-shanghai.tencentscf.com",
  "SMARTLIB_GATEWAY_SECRET": "<your-gateway-secret>",
  "SMARTLIB_EMAIL": null
}
```

Gateway 自动管理 SmartLib 凭证, 你不需要 APPID/APPSECRET。用户的 EMAIL 在首次注册后自动写入。运行前先读取 config.json 获取网关地址和密钥。

## Token 管理 / Token Management

SmartLib 的 OAuth Token 由 Gateway 全权管理。你无需获取或缓存 Token。

Gateway 支持两种检索调用模式：

### 推荐：语义化端点（v36+，更简洁）

```
POST /search
Headers: {"Authorization": "Bearer <SECRET>"}
Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<token>",
  "skill_source": "global-biblio-base",
  "endpoint": "/search/cn",     // 或 /search/global, /detail/cn, /detail/global
  "rule": "K=人工智能",          // 检索表达式
  "page_index": 1,
  "page_size": 20,
  "sort": 1                     // 可选
}
```

支持的 endpoint：`/search/cn` `/detail/cn` `/download/cn` `/search/global` `/detail/global`

### 兼容：全代理模式（旧版，仍可用）

```
POST /search
Body: {
  "email": "...",
  "consume_token": "...",
  "skill_source": "global-biblio-base",
  "api_path": "/openapi/t/data0012/doccenter/Articlesearch",
  "api_body": {"Rule": "...", "PageIndex": 1, "PageSize": 20}
}
```

## 检索接口选择策略 / Search Interface Selection

| 用户需求特征 / User Intent | 推荐接口 / Recommended API | 原因 / Reason |
|-------------|---------|------|
| 查中文论文/需要全文 / Chinese papers, need full-text | 接口1（中文期刊检索）/ API 1 | 支持全文下载 / Full-text available |
| 查英文论文/国际期刊 / English papers, intl. journals | 接口4（全球文献检索）/ API 4 | 覆盖范围更广 / Broader coverage |
| 需要专利/标准/学位论文 / Patents, standards, theses | 接口4（全球文献检索）/ API 4 | 支持多种文献类型 / Multi-type support |
| 不确定/跨语言检索 / Uncertain, cross-language | 优先接口4，再补充接口1 / API 4 first, supplement API 1 | 互为补充 / Complementary |
| 明确指定中文来源 / Explicit Chinese source | 接口1（中文期刊检索）/ API 1 | 数据更精准 / More precise |

## 检索策略分级体系 / Search Strategy Hierarchy

### 策略选择决策表 / Strategy Selection Matrix

| 检索场景 / Scenario | 推荐策略 / Strategy | 目标 / Goal |
|------|------|------|
| 开题报告、文献综述、查新 / Thesis proposal, literature review, novelty check | **宽检索 / Broad** | 查全优先 / Recall-first |
| 精准溯源、单篇确认、引用支撑 / Precise trace, citation verification, evidence finding | **窄检索 / Narrow** | 查准优先 / Precision-first |
| 常规文献调研、一般检索 / General literature survey | **平衡策略 / Balanced (default)** | 查全查准兼顾 / Balanced |

### 策略切换信号 / Strategy Switch Signals

执行检索后，系统根据结果自动评估是否需要切换策略：

- 结果 > 500 条且前 10 条相关性差 → 提示切换为**窄检索**
- 结果 < 5 条 → 提示切换为**宽检索**（执行「结果数量自适应策略」）
- 结果方向偏（前 10 条均不相关）→ 提示**更换关键词或字段**

---

## 可用接口 / Available Interfaces

### 1. 中文期刊文献检索 / Chinese Journal Search

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/data0012/doccenter/Articlesearch",
  "api_body": {
    "Rule": "<检索表达式>",
    "PageIndex": 1,
    "PageSize": 20,
    "Sort": 1,
    "FilterRule": "<可选：过滤表达式>"
  }
}
```

**检索表达式规则（Rule，必填）：**
- 字段代码：`T`=题名，`A`=作者，`K`=主题词，`P`=出版物名称，`O`=机构，`U`=全部字段
- 逻辑运算符（必须大写，两边空格）：`AND` `OR` `NOT`
- 示例：`(K=人工智能 OR K=机器学习) AND O=清华大学`、`T=深度学习`

**过滤表达式规则（FilterRule，可选）：**
- 字段代码：`L`=中图分类号，`C`=学科分类号，`Y`=出版年份，`TY`=文献类型，`LA`=语言
- 文献类型 TY：3=期刊文献，4=学位论文，5=标准，7=专利，等
- 示例：`TY=3 AND Y=2024`

**排序 Sort：** 1=相关度（默认），2=时效性倒序，3=时效性正序
**PageSize 范围：** 20~1000

### 2. 中文期刊文献详情 / Chinese Journal Detail

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/data0011/doccenter/Articledetail",
  "api_body": {
    "Identifier": "<文献ID>"
  }
}
```

返回完整文献详情，包含摘要、DOI、页码、基金资助、核心收录、原始数据库来源链接等。

### 3. 中文期刊文献下载 / Chinese Journal Download

仅限授权中文期刊全文下载。

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/data0013/doccenter/GetArticleFile",
  "api_body": {
    "Identifier": "<文献ID>"
  }
}
```

返回 / Response：`{"Data": {"Url": "<下载链接>", "Identifier": "<文献ID>"}}`

---

### 3b. 全球文献全文多渠道下载 / Multi-channel Full-text Download

SmartLib API 3 仅覆盖中文期刊全文。对于 API 4（全球文献检索）查到但有 DOI 的国际论文，本技能提供多级多渠道下载策略，最大化免费获取成功率。

#### ⚡ 执行触发条件 / Execution Trigger

**仅在用户主动请求全文下载时才执行外文文献下载流程。** 检索结果展示后，默认只展示元数据；用户说"下载全文"/"获取PDF"/"帮我下载"时才触发。

> Full-text download is **user-triggered only**. After search results are displayed, only metadata is shown. Execute download only when the user explicitly requests full-text (e.g., "下载全文", "获取PDF", "帮我下载").

**触发关键词 / Trigger Keywords:**
- 中文：「下载全文」「获取PDF」「帮我下载」「我要看全文」「下载这篇/这些」
- 英文：`download full-text` / `get PDF` / `download this paper`

**执行规则 / Execution Rules:**

```
用户请求下载全文:
  ├── 中文期刊文献 → 调 API 3 下载 PDF（直接）
  └── 外文文献（API 4，有 DOI）
       ├── 按渠道优先级 1→10 自动逐级尝试
       ├── 任一渠道成功 → 停止后续渠道，标记结果
       ├── 全部失败 → 按失败分类标记
       └── 每篇文献独立执行，并行处理（最多 10 篇并发）
```

**结果标记规范 / Result Tagging Standard:**

每篇外文文献下载完成后，必须在结果列表中标记获取状态。标记使用明确的图标+文字：

| 标记 / Tag | 含义 / Meaning | 触发条件 |
|------|------|------|
| `[全文:已获取 ✓]` | PDF 已成功下载 | 任一渠道成功获取 PDF 文件 |
| `[全文:在线 📖]` | 可在线阅读但无法自动下载 | Bronze OA / 出版商防盗链 |
| `[全文:付费 💰]` | 付费墙内，需机构订阅或购买 | Closed access / 所有渠道均返回 403 |
| `[全文:手动 🔍]` | 所有渠道均失败，需用户手动获取 | 无 OA 版本 / 网络错误 / 无 DOI |
| `[全文:未尝试 -]` | 无 DOI 或未触发下载流程 | 文献无 DOI 或 API 4 未返回 DOI |

**结果展示格式 / Display Format:**

检索结果列表中，每篇外文文献末尾追加标记：

```
1. [SCI一区] Attention Is All You Need
   Vaswani A, Shazeer N, Parmar N, et al.
   Advances in Neural Information Processing Systems, 2017
   摘要: The dominant sequence transduction models are based on...
   DOI: 10.5555/3295222.3295349
   [全文:已获取 ✓] → papers/attention_is_all_you_need.pdf
```

**渠道执行报告 / Channel Execution Report:**

所有文献下载完成后，在结果末尾输出汇总表：

```
## 📥 外文文献全文获取报告 / Full-text Retrieval Report

| # | 文献标题 | DOI | 成功渠道 | 状态 | 备注 |
|---|---------|-----|---------|------|------|
| 1 | Attention Is All You Need | 10.5555/xxx | ArXiv (渠道1) | [全文:已获取 ✓] | — |
| 2 | BERT: Pre-training of... | 10.18653/v1/xxx | Unpaywall (渠道2) | [全文:已获取 ✓] | — |
| 3 | Closed-access paper | 10.1000/xxx | — | [全文:付费 💰] | Elsevier 付费墙 |
| 4 | Bronze OA paper | 10.1093/xxx | DOI.org (渠道7) | [全文:在线 📖] | OUP Bronze OA，需手动保存 |
| 5 | No DOI paper | — | — | [全文:手动 🔍] | 无 DOI，建议联系作者 |

> ✅ 成功 2/5 篇 | 📖 需在线阅读 1 篇 | 💰 付费墙 1 篇 | 🔍 需手动获取 1 篇
```

#### 渠道优先级 / Channel Priority

| 优先级 | 渠道 | 适用条件 | 可靠性 | 费用 |
|:--:|------|------|:--:|------|
| **1** | **ArXiv 直链** | 论文有 arxiv ID | ★★★★★ | 免费 |
| **2** | **Unpaywall OA 探测** | 有 DOI + 邮箱 | ★★★★☆ | 免费 |
| **3** | **CORE OA 聚合器** | 有 DOI + API Key | ★★★★☆ | 免费 |
| **4** | **OpenAlex 存档 PDF** | 有 DOI + API Key | ★★★★☆ | 免费 $1/天 |
| **5** | **Semantic Scholar PDF** | 有 API Key | ★★★☆☆ | 免费 |
| **6** | **Crossref 链接提取** | 有 DOI | ★★★☆☆ | 免费 |
| **7** | **DOI.org 重定向** | 有 DOI | ★★☆☆☆ | 免费 |
| **8** | **Europe PMC + PMC** | 生命科学/医学 DOI | ★★★☆☆ | 免费 |
| **9** | **bioRxiv/medRxiv** | 生命科学预印本 | ★★★★☆ | 免费 |
| **10** | **真实浏览器 CDP** | Bronze/Green OA | ★★★★☆ | 需服务器 |

#### 下载决策树 / Download Decision Tree

```
用户请求下载某篇论文
  ├─ 文献来自 API 1（中文期刊）→ 调 API 3（中文期刊下载）
  └─ 文献来自 API 4（全球文献）或仅有 DOI
       ├─ 有 ArXiv ID？ → 渠道 1：ArXiv 直链
       ├─ 获取 DOI → 渠道 2：Unpaywall OA状态探测
       ├─ 渠道 3：CORE 全球OA聚合器
       ├─ 渠道 4：OpenAlex 存档PDF
       ├─ 渠道 5：Semantic Scholar PDF
       ├─ 渠道 6：Crossref PDF 链接提取
       ├─ 渠道 7：DOI.org 内容协商重定向
       ├─ 渠道 8：Europe PMC + PMC
       ├─ 生物医学 → 渠道 9：bioRxiv/medRxiv 预印本
       └─ 全部失败 + Bronze/Green OA？ → 渠道 10：真实浏览器 CDP
```

#### 出版商排障表 / Publisher Troubleshooting

| 出版商 | 常见错误 | 原因 | 应对方案 |
|------|------|------|------|
| **OUP (Oxford)** | 403 Forbidden | Bronze OA，不开放自动化下载 | 渠道 10 CDP 模拟人工点击 |
| **IEEE** | 403 / 418 | 需机构订阅 IP | CC-BY 论文可直接下；其余需机构权限 |
| **Elsevier** | 403 | 付费墙 | 查 Green OA 版本 |
| **Springer Nature** | 403 / 418 | 付费墙 + 机器人检测 | 查 ArXiv 预印本 |
| **Nature / Science** | 403 | 几乎无免费 PDF | 查作者自存档 |
| **Wiley** | 403 | 付费墙 | 同 Elsevier |

#### 失败分类与用户引导 / Failure Classification

| 失败原因 | 用户提示 |
|------|------|
| **Bronze OA（出版商防盗链）** | 该论文为 Bronze OA——出版商允许免费阅读但禁止自动化下载。建议：[点击在线阅读]({url}) 手动保存 |
| **Closed（付费墙）** | 该论文在付费墙内。建议：1) 通过机构图书馆访问 2) 搜索 ArXiv/bioRxiv 预印本 3) 通过科研通求助 |
| **所有渠道均失败** | 所有下载渠道均未获取到全文。建议：[在线阅读]({url}) 或联系通讯作者请求 PDF |

---

### 4. 全球文献检索 / Global Literature Search

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/skrs2/doccenter/Articlesearch",
  "api_body": {
    "Rule": "<检索表达式>",
    "PageIndex": 1,
    "PageSize": 20,
    "Sort": 1,
    "FilterRule": "<可选：过滤表达式>"
  }
}
```

检索表达式和过滤规则与中文期刊检索完全相同。返回数据结构同 API 1，结果列表字段为 `Data.List`。

### 5. 全球文献详情 / Global Literature Detail

通过 Gateway /search 代理访问:

```
POST {SMARTLIB_GATEWAY_URL}/search
Headers: {"Authorization": "Bearer <SMARTLIB_GATEWAY_SECRET>"}
Content-Type: application/json

Body: {
  "email": "<SMARTLIB_EMAIL>",
  "consume_token": "<通过 /consume 获取的 token>",
  "api_path": "/openapi/t/skrs1/doccenter/Articledetail",
  "api_body": {
    "Identifier": "<文献ID>"
  }
}
```

---

## 使用指南 / Usage Guide

### 完整工作流 / Complete Workflow

```
                    ┌──────────────────────────────────┐
                    │ 1. 理解需求 / Understand Intent    │
                    └───────────────┬──────────────────┘
                                    ↓
                    ┌──────────────────────────────────┐
                    │ 2. 选定检索策略 / Select Strategy │ ← 宽检索/窄检索/平衡
                    └───────────────┬──────────────────┘
                                    ↓
              ┌─────────────────────────────────────────┐
              │ 3. 关键词智能扩展 / Keyword Expansion     │
              │ 4. 构建检索式 / Build Expression          │
              │ 5. 选择接口 / Select API                  │
              │ 6. 执行检索 / Execute Search              │
              │ 7. 结果智能排序 / Smart Ranking           │
              └─────────────────────┬───────────────────┘
                                    ↓
                    ┌──────────────────────────────────┐
                    │ 8. 结果评估 / Evaluate Results     │
                    └───────────────┬──────────────────┘
                          ┌─────────┴─────────┐
                          ↓                   ↓
              ┌───────────────────┐  ┌───────────────────┐
              │ 结果满意 / Good   │  │ 结果需调整 / Needs │
              │ → 步骤9          │  │ Adjustment         │
              └───────┬───────────┘  └─────────┬─────────┘
                      ↓                        ↓
              ┌───────────────┐    ┌──────────────────────┐
              │ 9. 展示结果   │    │ 9a. 策略调整          │
              │ 10. 深入查看  │    │ 过多→窄化 / 过少→宽化 │
              │ 11. 全文下载  │    │ 方向偏→换关键词       │
              │  (中文直接下) │    └──────────┬───────────┘
              │  (外文自动走) │
              │  (十级渠道)   │
              └───────────────┘
                                              ↓
                                    ┌──────────────────────┐
                                    │ 9b. 二次检索         │
                                    │ 回到步骤3-7          │
                                    └──────────────────────┘
```

检索→评估→调整→再检索是核心工作流。首次检索后自动评估结果质量，必要时调整策略重新检索。

**Step 11 全文下载（用户触发）：** 仅当用户主动请求时才执行全文下载：
- **中文期刊**：直接调 API 3 下载 PDF
- **外文文献**：走十级多渠道 OA PDF 探测（见 3b 章节），每篇独立并行执行
- 下载结果以标记形式追加到结果列表中，并在末尾输出「全文获取报告」汇总表
- **未触发下载时**：仅展示元数据，不执行任何下载操作

### 关键词智能扩展 / Smart Keyword Expansion

每次检索前，先对用户提供的核心关键词进行中英文同义词扩展，以显著提升召回率。

**扩展维度 / Expansion Dimensions:**

| 维度 | 说明 | 示例 |
|------|------|------|
| 中文同义词 | 学术语境下的等价表述 | "大语言模型" → "大模型" "LLM" |
| 英文同义词 | 英文学术常用表述 | "deep learning" → "deep neural network" |
| 中英互译 | 中英文之间的对照词 | "知识图谱" ↔ "knowledge graph" |
| 缩写/全称 | 学术缩写及其展开 | "NLP" → "natural language processing" |
| 上下位词 | 更泛化或更具体的表述 | "深度学习" → "机器学习"（上位） |

**检索表达式构建规则：** 同义词组内用 `OR` 连接，不同概念组间用 `AND` 连接。扩展词数量控制在每概念组 3-8 个。

### 结果智能排序 / Smart Result Ranking

检索结果需进行二次智能排序，综合考虑以下因素（优先级从高到低）：

1. **核心收录权重**：SCI/SSCI > EI > CSSCI > 北大核心 > CSCD > 普通期刊
2. **内容相关性权重**：题名匹配 > 题名+关键词 > 摘要相关 > 仅关键词命中
3. **时效性权重**：近 3 年文献给予适当加分

### 结果数量自适应策略 / Adaptive Result Strategy

**结果过少（< 5 篇）— 宽化扩展：**

1. 上位词扩展：联网搜索更泛化的术语
2. 字段放宽：`T=` → `K=` → `U=`
3. 相关机构检索：查找领域代表性机构
4. 学科分类号检索：使用中图分类号或教育部分类号
5. 放宽过滤条件：去掉时间/语言/文献类型限制
6. 关键词拆分/重组

**结果过多（> 500 条或相关性差）— 窄化收缩：**

1. 字段收窄：`U=` → `K=` → `T=`
2. 增加 AND 限定
3. 核心词精简
4. 强化过滤条件（限定文献类型/语言/年份）
5. 排序优化

### 自然语言转检索表达式示例 / NL-to-Query Examples

| 用户需求 | 扩展后的 Rule | FilterRule | 接口 |
|---------|------|-----------|------|
| 找关于深度学习的论文 | `(U=深度学习 OR U=深度神经网络 OR U=deep learning OR U=DNN)` | - | 接口1+4 |
| 清华大学发表的人工智能相关论文 | `(K=人工智能 OR K=AI) AND O=清华大学` | `TY=3` | 接口1 |
| 2024年中文期刊上关于大模型的文章 | `(K=大语言模型 OR K=大模型 OR K=LLM)` | `TY=3 AND Y=2024 AND LA=ZH` | 接口1 |
| Nature 期刊上的量子计算论文 | `(K=quantum computing) AND P=Nature` | - | 接口4 |
| 查找计算机领域的专利 | `(K=计算机 OR K=computer)` | `TY=7` | 接口4 |
| 2023-2025年的深度学习综述 | `(T=深度学习 OR T=deep learning) AND (T=综述 OR T=review)` | `Y=2023 OR Y=2024 OR Y=2025` | 接口1+4 |

### 高级检索技巧 / Advanced Search Techniques

#### 引文追溯策略 / Citation Tracing

| 追溯方向 | 操作方式 | 适用场景 |
|------|------|------|
| **作者追踪** | `A=作者名` | 追踪核心研究者团队全部成果 |
| **期刊溯源** | `P=期刊名 AND K=相关主题词` | 锁定高水平期刊中该领域全部论文 |
| **机构扩展** | `O=机构名` | 了解机构在相关领域的研究布局 |
| **参考文献反向查** | 提取参考文献标题，用 `T=` 逐一检索验证 | 确认引用文献是否在数据库中 |
| **引用链追踪** | `L=分类号 OR C=分类号` | 在相同分类号下发现更多相关文献 |

#### 分类号体系利用 / Classification-based Search

利用中图分类号（`L=`）和教育部学科分类号（`C=`）检索可绕过关键词歧义。常用分类号：`TP18`=人工智能，`TP391.1`=自然语言处理，`O413`=量子论，`0812`=计算机科学与技术。

#### 字段选择策略矩阵 / Field Selection Matrix

| 字段 | 精度 | 覆盖 | 最佳场景 |
|------|------|------|------|
| `U=` 全部字段 | 低 | 最高 | 宽泛探索 |
| `K=` 关键词 | 中 | 高 | 常规检索（默认） |
| `T=` 题名 | 最高 | 低 | 精准匹配、引用确认 |
| `A=` 作者 | 高 | 低 | 追踪特定研究者 |
| `O=` 机构 | 中 | 中 | 了解机构研究布局 |
| `P=` 出版物 | 高 | 中 | 限定高质量期刊 |

### 结果展示规范 / Result Display Standards

**检索结果列表**以编号列表形式展示，每篇文献包含：序号、核心收录标注、标题、作者、来源出版物、出版日期、摘要（截取前200字）、文献ID。

**文献详情**额外展示：DOI、核心收录、原始数据库链接、SmartLib 详情页、基金资助、页码。

结果按「结果智能排序」策略排列。展示后主动提示用户：
- "输入文献编号可查看详情"
- "中文期刊文献支持全文下载"
- "如需更多结果，可以说'下一页'"

### 检索结果质量判断 / Result Quality Assessment

#### 核心收录标注解读

| 标注 | 含义 | 权重 |
|------|------|------|
| `[SCI一区]` | 国际顶级期刊（影响因子前 25%） | 最高 |
| `[SCI二区]` | 国际高水平期刊 | 高 |
| `[SSCI]` | 社会科学国际核心期刊 | 最高 |
| `[EI]` | 工程领域国际核心收录 | 高 |
| `[CSSCI]` | 中文社会科学引文索引（南大核心） | 高 |
| `[CSCD]` | 中国科学引文数据库 | 中高 |
| `[北大核心]` | 北京大学核心期刊目录 | 中 |
| `[CCF-A]` | 中国计算机学会 A 类会议/期刊 | 最高 |

#### 用户自检清单 / User Quality Checklist

在引用或深入阅读文献前，建议用户快速核对：
- [ ] **来源**：发表在什么期刊/会议上？是否为核心收录？
- [ ] **时效**：出版年份是什么？对当前领域是否足够新？
- [ ] **作者**：作者是否是该领域的活跃研究者？
- [ ] **相关性**：标题和摘要是否与我的研究问题直接相关？
- [ ] **可获取性**：是中文期刊（可下载全文）还是全球文献（仅元数据）？

---

### 错误处理 / Error Handling

错误处理必须给出具体可操作的解决方案。网络波动时自动重试（最多 3 次，指数退避 1s→2s→4s）。

#### 错误码处理表 / Error Code Handling

| 状态码 | 含义 | 具体处理步骤 |
|------|------|------|
| **401** | Token 无效或过期 | Gateway 自动管理 Token 刷新, 无需处理。若持续 401，请检查 consume_token 是否有效 |
| **403** | 权限不足 | 提示"当前凭证无此接口权限，请确认 API 套餐是否已开通此接口" |
| **429** | 请求频率超限 | 等待 5 秒后自动重试 |
| **499** | 参数错误 | 检查 Rule 语法（运算符大写、有空格）、FilterRule 字段代码、PageSize 范围 |
| **500/502/503** | 服务端错误 | 自动重试 3 次 → 全部失败后提示"SmartLib 服务暂时不可用" |
| **网络超时** | 请求无响应 | 自动重试 3 次 → 提示"请检查网络是否可访问 data.smart.vipslib.com" |
| **无结果** | API 返回空列表 | 按「结果数量自适应策略」自动提供扩展建议 |
| **凭证缺失** | 环境变量未设置 | 自动触发 Pre-flight 注册流程 |

---

### 常见问题（FAQ）

| 问题 | 答案 |
|------|------|
| **检索不到想要的论文怎么办？** | 1. 去掉过滤条件扩大范围 2. 尝试上位词 3. 用英文关键词在接口4再试 4. 用 `U=` 替代 `T=` |
| **全文下载失败怎么办？** | 仅中文期刊支持全文下载。下载 URL 约 10 分钟有效，过期需重新调用。英文文献自动走多渠道下载策略获取 OA 版本。 |
| **Token 多久过期？** | Access Token 30 秒，Refresh Token 2 小时。系统自动管理刷新，用户无感知。 |
| **英文文献能不能下全文？** | 本技能集成十级多渠道下载策略（ArXiv → Unpaywall → CORE → OpenAlex 等），Gold/Green/Hybrid OA 论文成功率 >85%。付费墙内论文无法获取。 |
| **配额耗尽后还能用吗？** | 不能。配额耗尽后 Gateway 返回 429 拒绝所有检索请求，必须先充值恢复配额才能继续使用。 |

---

### API 调用注意事项 / API Call Notes

- **检索结果数据路径**：列表字段为 `Data.List`，解析时先尝试 `List`，回退 `Items`
- **Source 字段需详情接口获取**：检索列表中 `Source` 为空数组，原始数据库链接需调用详情接口。Source 数组元素结构为 `{"Source_DbId": "scopusjournal", "Source_DbTitle": "Scopus", "Source_Link": "https://..."}`，字段说明：`Source_DbId`=数据库标识符，`Source_DbTitle`=数据库中文名称，`Source_Link`=原始数据库详情页链接。平台覆盖300+数据库，100篇样本实测平均每篇4.75个链接，覆盖率100%。

---

## 注意事项 / Notes

- 检索策略遵循三级分级体系：默认平衡策略，综述自动切换宽检索，引用自动切换窄检索
- 检索→评估→调整→再检索是核心工作流
- Access Token 有效期 30 秒，Refresh Token 2 小时，系统自动管理刷新
- 全球文献检索（接口4）仅提供元数据，部分无全文
- 中文期刊（接口1-3）支持全文下载，是核心优势，应优先推荐
- PageSize 建议不超过 100
- 检索表达式中的运算符必须大写且两边有空格
- 英文关键词建议同时检索接口1和接口4以提高覆盖率
- 展示文献详情时，务必从详情接口取 `Source` 字段并展示原始数据库链接（`Source_DbTitle` + `Source_Link`）
- 引文追溯是提升检索质量的捷径：从一篇确认的高质量文献出发追踪
- 分类号检索（`L=` / `C=`）可绕过关键词歧义

---

## 版本历史 / Version History

| 版本 | 日期 | 核心变更 |
|------|------|---------|
| v1.0 | 2026-05 | 初次上线：中文期刊检索+全文下载，基础文献查询功能 |
| v1.5 | 2026-05 | 新增全球文献检索，覆盖中外文双轨数据源 |
| v1.6 | 2026-05 | 检索策略升级：三级分级体系（宽检索/窄检索/平衡），智能适应结果数量，结果质量评估 |
| v2.0 | 2026-05 | 计费方式优化，按实际API调用次数计费更透明 |
| v2.1 | 2026-05 | 计费说明更清晰：明确5个接口计费标准，附带使用示例 |
| v2.2 | 2026-05 | 接口精确化：5个核心检索接口，每次成功调用计1次 |
| v2.3 | 2026-05 | 外文文献下载增强：支持十级渠道自动探测，免费OA文献不消耗配额 |
| v2.4 | 2026-05 | 下载改回用户主动触发模式，避免后台自动消耗配额 |
| v2.5 | 2026-05 | 安全防护升级，防止第三方盗用配额 |
| v2.6 | 2026-05 | 每篇文献附带原始数据库来源链接（覆盖300+数据库，平均4.75个链接/篇），可一键跳转验证 |
| v2.7 | 2026-05 | OA文献免费下载（十级渠道），不消耗SmartLib配额；来源链接覆盖率提升 |
| v2.8 | 2026-06 | 检索失败不消耗配额；检索命令简化（endpoint+rule格式） |
| v2.9 | 2026-06 | 服务连接优化，检索速度提升 |
| v3.0 | 2026-06 | 注册流程简化，新用户开通更快捷，无需验证码 |
| v3.1 | 2026-06 | 注册赠送次数增加至100次/月；可订阅套餐最低1000次起 |
| v3.2 | 2026-06 | 新用户引导体验优化，首次使用自动配置，无需手动设置 |
| v3.3 | 2026-06 | 全球文献库扩充至12.28亿条；中文期刊8000万篇可下载 |
| v3.4 | 2026-06 | 文献入口统一，跨技能联动更顺畅 |
| v3.5 | 2026-06 | 技能调用可溯源，方便了解各渠道使用情况 |
| v3.6 | 2026-06 | 版本日志优化，展示更简洁 |
