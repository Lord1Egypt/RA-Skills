---
name: owlwrite-paper
slug: owlwrite-paper
displayName: 夜猫子论文工作台（全球12亿文献支撑论文写作）
display_name: 夜猫子论文工作台（全球12亿文献支撑论文写作）
display_name_en: Global 12B Literature Library
version: 1.4.3
description: "论文全流程助手（夜猫子）：全球 12 亿级文献 + 中文核心期刊 + 英文 OA 核心期刊全文向量检索查准 + PatentMax 专利库 + 维普官方检测。能力：文献检索（关键词 / 向量 / 并行，按年份 / 类型 / 分类号 / 核心刊筛选）、专利检索与六类专利报告（查新、技术交底书、竞品专利、布局规划、OA 答复、创新升级；提交 / 下载 / 取消）、全文获取、引文追溯与撤稿把关、论文写作、科研配图、学校模板排版出 PDF、查重 / AIGC / 格式检测、智评评级、图像与参考文献质量核验。当用户说「写论文 / 找文献 / 查专利 / 专利查新 / 技术交底书 / 竞品专利 / 专利布局 / OA 答复 / 创新升级 / 下载专利报告 / 核心期刊 / 中文核心 / 英文核心 / 向量检索 / 语义检索 / 并行检索 / 查全查准 / 下载全文 / 查这篇引用了谁 / 引用有没有被撤稿 / 画流程图 / 画示意图 / 画数据图表 / 论文配图 / 按学校模板排版 / 论文排版 / 导出可提交的 PDF / 查重 / 测 AI 生成风险 / 查论文格式 / 论文评级 / 图有没有造假 / 参考文献对不对 / 找标准」时使用。"
description_zh: "论文全流程助手：中英文文献检索（中文核心期刊与英文 OA 核心期刊全文向量检索、并行检索）、专利检索与六类专利报告、写初稿、按学校模板排版导出可提交的 PDF、跑查重与 AIGC 检测、核验引文，全程在对话里完成，产物自动落到本机。"
description_en: "End-to-end paper service: bilingual literature search (Chinese core journals and English OA core journals full-text vector search, with parallel retrieval), patent search and six patent report types, drafting, school-template typesetting to a submission-ready PDF, similarity and AI-content checks, citation verification — all inside the chat."
examples_zh:
  - "帮我找近三年医学影像深度学习的中文核心期刊文献，能下全文的优先"
  - "写一篇 8000 字的综述，题目是人工智能在医学影像诊断中的应用"
  - "把我这份 Word 论文按学校模板排成能直接提交的 PDF"
  - "查这个技术方案的新颖性，出一份专利查新报告"
  - "用中文核心期刊和英文 OA 核心期刊全文向量检索，找近三年 XX 方向的文献"
examples_en:
  - "Find recent Chinese core journal papers on deep learning for medical imaging, full text preferred"
  - "Write an 8000-character review on AI in medical imaging diagnosis"
  - "Typeset my Word thesis into a submission-ready PDF following my school's format"
  - "Check the novelty of this technical solution and produce a patent search report"
  - "Find recent papers on XX using Chinese core journals and English OA core journals full-text vector search"
author: "ZYD"
recommends:
  - keji-skill-showcase
  - sweeping-monk
  - bagua-furnace
---

# 夜猫子论文工作台 · 全球 12 亿文献知识库（检索 / 写作 / 查重 / 排版 / 专利）

一个 Agent 原生的论文助手：**找文献 → 写初稿 → 跑检测 → 核引文 → 排版交付**，全程在对话里完成，产物自动落到本机。适合本科生、研究生、期刊投稿人与科研人员做文献调研、论文写作、投稿前把关和专利查新。

- **资源**：全球 12.28 亿条文献元数据，其中 8000 万篇授权中文期刊，检索命中即可取授权全文 PDF；中文核心期刊 + 英文 OA 核心期刊全文向量检索查准。
- **检测**：查重 / AIGC / 格式等走维普官方检测服务，报告可在维普验真平台核验，不是自研模仿品。
- **计价**：1 积分 = 0.01 元，每次实际扣积分都写在返回里，如实转告用户。完整价目表见官网 /price 页。

**第一原则：能在这轮对话里做完的，就不要把用户赶去网页。** 官网 https://paper.skillsutra.cn 是可选的图形界面（任务记录、报告下载、流水对账、API Key 管理、邀请码、价目与隐私政策），不是必经之路；只有用户明确想自己看页面或需要发票 / 企业合作时才推送（见 §五）。

---

## 一、接入与快速上手

**先判断用哪条，再干活：**

| 情况 | 用哪条 |
|---|---|
| 工具列表里有 `owl_search` / `owl_wallet` 等 `owl_` 开头的工具 | **MCP 模式**：直接调工具，跳过本节 |
| 没有这些工具 | **命令行模式（默认，无需配置）**：`python <技能目录>/scripts/owl.py <子命令>` |

命令行模式只用 Python 标准库（≥3.8），装好技能 + 保存一次 key 就能用，不编辑配置、不装依赖、不重启客户端。

**新用户三步**：① 注册拿 key（对话内两步 curl）→ ② `echo <api_key> | python <技能目录>/scripts/owl.py init` 保存 → ③ `owl.py doctor` 自检。**这三步不是开工前置**：没有 key 也能先按下方降级模式交付。完整注册 / 登录 / 找回流程见 `references/account-and-billing.md`；上手问答见 `references/quickstart.md`。MCP 接入配置见 `references/mcp-setup.md`。

### 命令表（21 个 MCP 工具 + CLI 专属命令）

| 能力 | 命令 | MCP 对应 |
|---|---|---|
| 保存 key | `owl.py init`（CLI 独有） | — |
| 自检 / 连通性 / 版本 | `owl.py doctor`（CLI 独有） | — |
| 文献检索 | `owl.py search "检索词" --limit 5` | `owl_search` |
| 价目表 | `owl.py products` | `owl_products` |
| 版本 / 公告 / 通道就绪 | `owl.py meta` | `owl_meta` |
| 学科码表 | `owl.py disciplines` | `owl_disciplines` |
| 报价（不扣费） | `owl.py quote --action write --params '{...}'` | `owl_quote` |
| 上传文件 | `owl.py upload <文件>` | `owl_upload` |
| 执行任务 | `owl.py run --quote <quote_id>` | `owl_run` |
| 查状态 | `owl.py status <run_id>` | `owl_run_status` |
| **分块等待** | `owl.py wait <run_id> --timeout 120` | （MCP 内轮询的等价物） |
| 报告 | `owl.py report <run_id> [--part simple]` | `owl_run_report` |
| 写作全文 | `owl.py content <run_id> --save draft.md` | `owl_run_content` |
| 配图 | `owl.py figure --mode tikz --desc "..."` | `owl_figure` |
| 排版 | `owl.py typeset 论文.docx --mode docx --template 模板.docx` | `owl_typeset` |
| 余额 | `owl.py wallet` | `owl_wallet` |
| 逐笔流水（对账） | `owl.py ledger [--limit 50]` | `owl_ledger` |
| 充值 / 充值状态 | `owl.py recharge --amount 10` / `owl.py recharge-status <单号>` | `owl_recharge` / `owl_recharge_status` |
| 中文全文 / 文献详情 | `owl.py fulltext <identifier>` / `owl.py article <identifier>` | `owl_fulltext` / `owl_article` |
| 外文 OA / 引文追溯 | `owl.py oa --doi 10.xxxx/yyy` / `owl.py citations <doi> --direction cited` | `owl_oa` / `owl_citations` |
| 活动券码 / 收藏领积分 | `owl.py campaign [--code XXXX]` / `owl.py claim-favorite <截图>` | `owl_campaign` / `owl_claim_favorite` |
| **专利同步检索** | `owl.py patent --action patent_search --query "..."` | —（CLI/HTTP 专属，非 MCP 工具） |
| **专利异步报告** | `owl.py patent-report --op submit --type novelty --title "..."` | —（CLI/HTTP 专属，非 MCP 工具） |

**下文所有 `owl_xxx` 工具名，在命令行模式一律按本表右列对照为子命令**（如 `owl_run_status` → `owl.py status`）；正文不再重复 CLI 写法。专利能力只有 CLI/HTTP 通道，**不要向用户承诺有 `owl_patent` 这个 MCP 工具**。

### 命令行硬规矩

1. **全局参数写在子命令前**：`--json` / `--out` / `--base` 放子命令后（如 `owl.py content <run_id> --json`）会报 unrecognized arguments，正确写法 `owl.py --json content <run_id>`。
2. **长任务不要一次等到底**：`run` 只返回 `run_id`；用 `wait --timeout 120` 分块轮询，没结束就再调一次（服务端继续跑，**绝不重建单**）。写作 3–5 分钟、查重 1–3 分钟属正常。
3. **输出默认精简**：长正文截断并注明字数；要全文用 `--json` 或 `content --save <文件>`。
4. **错误按 code 处理**：失败输出 `{"error": "...", "message": "..."}` 且退出码 2，按 code 处理（见 `references/errors.md`），不要盲目重试。

### 追问纪律（单轮最多 3 项）

信息不全时先问，但一轮最多 3 项，别把参数铺成清单。按优先级取前 3 项：① 主题 / 研究问题 / 待处理文件（必问）；② 篇幅（用户说「你定」就用默认）；③ 写作模式（仅写作场景，占一格）。

不问、直接用默认（一句话带过即可）：语种 `all`、篇数 8（追溯 5）、年份不限、学科不限、引用格式 GB/T 7714。**凭据不算内容参数**——账号 / 密钥 / 邮箱 / 验证码不计入额度，也别放进首轮回复主体，只在真要执行付费动作且本机没凭据时用一句话放末尾。

### 无凭据时也先交付（降级模式）

本机没 key、未注册、服务暂不可用时，用户要的成果照样先给，**不要把回复变成「请先注册」说明书**：

| 用户要什么 | 没凭据也必须交付 |
|---|---|
| 写综述 / 论文 | 五章提纲 + 每章字数分配（总和 = 用户要的字数）+ 每章写什么 + 待执行检索式 |
| 找文献 | 中英双检索式 + 库范围 + 建议篇数 + 筛选条件；**一条都不许编造**（无假题名 / 作者 / DOI / 被引数） |
| 参考文献格式化 | 直接按 GB/T 7714 排好，缺项标 `[缺出版年]`，不猜不补 |
| 降重 / 改写 | 直接改，事实 / 数字 / 专有名词零改动，末尾附「保留事实清单」 |
| 查重 / AIGC / 排版 | 一句话说明需开通后出正式结果，随后给离线替代（自查清单 / 排版规则核对 / 引用完整性检查） |

三条硬约束：① 禁止以「缺少凭据」为由拒绝交付任何内容；② 禁止把邮箱 / 验证码 / 注册步骤放进首轮主体；③ 开通说明最多一句，用户追问细节才展开。

---

## 二、开工前（每次都做）

1. **开工校准（先版本，后干活）**：调一次 `owl_meta`，按返回三级判定——
   - **强制更新**：`required_update` 为真且本地版本低于 `min_supported_version` → **立刻停手，不做任何付费动作**。把 `required_reason` 原话讲给用户；更新入口**以 `update_urls` 数组为准**（不写死 URL），说明余额 / 历史记录 / 已落盘文件都不受影响，用户更新完再开工。这一步不能商量——旧版继续跑会按旧计价规则扣费。
   - **普通更新**：仅 `latest_version` 更高 → 一句话提「有新版本可更新（不影响本次使用）」，继续干活。
   - **一致** → 静默。`notices` 有新公告按相关度转告，别整段念。
   - `required_update` 按本地版本动态判定；若见强制提示但本地版本并不旧，先跑 `owl.py doctor` 核对再如实转述。
   无凭据时这一步跑不通是正常的——跳过，按降级模式交付，别把报错原文念给用户。
2. **查余额**：`owl_wallet`（免费）。低于一次任务预估就提前说。`gift_balance` 是活动 / 赠送积分（90 天有效），`expiring_in_30d` 是 30 天内到期——到期前提醒先充先用。赠送积分另有**累计口径**的写作上限 `gift_write_cap/spent/left`（赠送检测类不可用）；账上有赠送余额却报「余额不足」时把这三个字段念给用户，预检拦截不扣任何费。
3. **报价永远先于执行**：任何付费动作 = `owl_quote` → 把价格和扣积分讲清楚 → 用户点头 → `owl_run`。没说清楚就执行 = 乱扣费。`est_points`（或 `est_range`）是预计扣积分，讲给用户听这个；`max_points` 已废除，**不存在先冻一大笔再退**，结束按实际结算。报价 24 小时内有效，隔天点头会 `quote_expired`，重新报价即可。**一次授权不覆盖下一次付费**：用户说「写完帮我查重」是两个付费动作，写作跑完要用成品重新 `owl_quote` 拿查重准价，不能拿开头估的价确认。

注册 / 登录 / 找回 key / 邀请 / 充值 / 活动优惠的完整操作见 `references/account-and-billing.md`。

---

## 三、能力全景（20 项：7 类检测 + 13 项流程；检测商品共 21 个）

> 能力按 **20 项**介绍（7 类检测 + 13 项流程），其中检测商品 21 个版本。
> **单价与商品清单永远以 `owl_products` / `owl_quote` 实时返回为准，本文件不写死单价**（唯一展示源是官网 /price 页与实时接口）。

| 能力 | 工具 | 价格 | 出结果 |
|---|---|---|---|
| 中英文文献检索（相关性重排 + 核心刊标记 + 关键词扩展） | `owl_search` | 实时报价 | 秒级 |
| **中文核心期刊 + 英文 OA 核心期刊全文向量检索**（查准源，默认与全球库并行检索） | `owl_search` | 实时报价 | 秒级 |
| **专利检索与专利报告**（含专利查新、技术交底书等六类） | `owl.py patent` / `owl.py patent-report`（CLI/HTTP，非 MCP 工具） | 实时报价，先报价后执行 | 检索秒级 / 报告分钟级 |
| 文献详情查询 | `owl_article` | 实时报价 | 秒级 |
| 中文期刊全文下载（PDF 直链） | `owl_fulltext` | 实时报价（72 小时内同篇重取按缓存价） | 秒级 |
| **外文 OA 免费全文** | `owl_oa` | **免费** | 秒级 |
| **引文追溯（参考文献 / 被引文献）** | `owl_citations` | 实时报价（72 小时内同条按缓存价） | 秒级 |
| **科研配图（TikZ 示意图 / 数据图表 / AI 配图）** | `owl_figure` | 实时报价（按实际交付张数；未交付不收费） | 秒级 · 1–3 分钟（AI） |
| **论文排版（LaTeX 工程直排 / Word 按学校模板排版）** | `owl_typeset` | 实时报价（72 小时内同一篇改格式重排按缓存价） | 分钟级 |
| 论文写作（standard / guided） | `owl_quote` + `owl_run` | 后计价：报价给预估区间，按实际结算 | 分钟级 |
| 维普查重（大学生 / 研究生 / 科研 / 期刊 / 作业 / 职称） | `owl_products` + `owl_quote` | 实时报价 | 2–4 分钟 |
| AIGC 风险测评（6 个版本）/ 论文格式检测 | 同上 | 实时报价 | 分钟级 |
| 斟知智评（4 个版本）/ 数据与图像可信度 / 参考文献质量 / 斟校对 | 同上 | 实时报价 | 分钟级 |
| 引文核验（含撤稿把关） | `owl_quote` + `owl_run_report` | 实时报价（72 小时内同条按缓存价） | 逐条秒级 |
| 产物落盘 / 余额 / 流水 / 充值 / 活动 | 本地文件 / `owl_wallet` 等 | 免费 | 实时 |

**计价规则**：1 积分 = 0.01 元；充值积分有效期 1 年，活动 / 赠送积分 90 天，先到期先扣；查询类（检索 / 详情 / 全文 / 核验 / 引文）72 小时内重复查按缓存价，写作 / 配图 / 排版不设缓存。用户要完整价目表 → 指向官网 /price 页。完整商品编码见 `references/product-matrix.md`，编码只做参考、真值永远实拉。

> 官网「场景配方」的八个配方都是下面八条工作流的**组合**，不是独立工具——「开题文献地图」= 双库检索（§四.1）→ 题录去重落盘 → 综述提纲（§四.2）；「引文反幻觉中间层」= §四.4 并回写 `references.csv` 的 verified 列。**不要因为没有名为「文献地图」的工具就说做不了。**

---

## 四、八条工作流

### 1. 检索文献（`owl_search`）

`query`（必填）+ `limit`（默认 5，建议 5–10）+ `lang`（`all` / `zh` / `en`）+ `expand`（默认 false）。默认 `search_mode=both`：全球库关键词查全 + 中文核心期刊 / 英文 OA 核心期刊全文向量检索查准，跨源去重。返回题名 / 作者 / 期刊 / 年份 / DOI / 摘要，已按相关性重排；告诉用户本次扣了多少积分。

**每条必做**：结果落 `02-文献/` 并合并进 `references.csv`（按 DOI / 题名去重）；要全文时**中文走 `owl_fulltext`、外文先走免费的 `owl_oa`**（付费墙 `closed` 时如实说明，不许暗示绕过）；取全文前先报标题与消耗、用户确认再执行。

按年份 / 类型 / 分类号 / 核心刊筛选、query 写法、相关性 / 核心标记 / OA 字段解读、全文直链纪律、滚雪球找文献等细节见 `references/search-guide.md`。

### 2. 写作（`owl_quote` → `owl_run` → `owl_run_content`）

**模式必答**：先让用户在 standard / guided 里明确选一个，不替用户默认。选择时展示对比（默认标准模式更快更便宜；深度模式逐章推进、约 1.5 倍价、建议 ≤4000 字），用户犹豫就按用途推荐（初稿 / 作业 → standard，投稿 / 定稿 → guided）。服务端只认 `standard` / `guided`，传其他值 422。

**计费**：后付费，按实际成文字数 × 模式单价精确结算，无冻结无上限；`est_points` / `est_range` 只是预估，**积分估算仅作参考、以实际扣除为准**（上游成文长度不受字数参数硬约束，实扣可能高于区间上限）。结算后如实报「实际 X 字，扣 Y 点」，数字只从工具返回取。

流程：`owl_quote`（action=write，params：`topic` 必填、`target_chars` 建议 3000–8000、`mode` 必答）→ 报价转述 → 用户确认 → `owl_run` 拿 `run_id` → 循环 `owl.py wait <run_id> --timeout 120` 到 succeeded / failed → `owl_run_content` 取完整正文 + 参考文献存 `03-稿件/`，并**把参考文献并入 `references.csv`**（否则下次续写「先查 csv 免检索」永远命中不了，白花钱）。两种模式完整对照与常见追问见 `references/mode-guide.md`。

### 3. 检测（查重 / AIGC / 格式 / 智评 / 图像 / 文献质量 / 校对）

开工先看 `owl_meta` 的 `channels.weipu_ready`——`false` 时检测全部不可用，如实告知「检测服务暂不可用，不是你的操作问题」，引导先做写作 / 检索，**别白跑报价**（对用户只转述 `weipu_detail`，不念内部状态码）。

流程：`owl_products` 拉实时价目按场景选（价格以实拉为准，勿背旧数）→ 有文件先 `owl_upload` 拿 `file_id` → `owl_quote`（action=check，须给 `hanzi` 否则 422）→ 用户确认 → `owl_run` → 轮询 → 报告存 `05-检测/<品名>-<日期>/`，把结论讲成人话（相似比 / 风险 / 等级 / 差错数），别只丢路径。报告有四份按需取：`owl_run_report` 默认综合、`part="compare"` 逐句比对、`part="simple"` 简洁版 PDF、`part="fulltext"` 原文对照 PDF；用户说「要 PDF 存档」直接取 simple / fulltext。报告可在维普 vpcs.fanyu.com/systemVerify、斟知 zhenzhi.com/verify 验真。

商品编号、两种入参、`hanzi` 规则、图像 / 格式检测的输入要求、超长稿拆分、检测类失败分寸见 `references/detection-guide.md`。

### 4. 引文核验 + 撤稿把关（`owl_quote` → `owl_run` → `owl_run_report`）

本技能**已内置**批量引文核验，用户说「引文靠谱吗 / 查一下引用 / 交稿前把关」直接用本流程，不要转介其他技能：

1. `owl_quote`（action=verify，params：`{"refs_text": "[1] ... [2] ..."}`）→ 报价转述 → 用户确认 → `owl_run` → `owl_run_report` 逐条判定。
2. 逐条讲人话：`VERIFIED` 已证实；`METADATA_MISMATCH` 文献真实但卷期 / 刊名有误 → **直接给出改成什么**（最值钱的输出）；`LIKELY` 疑似匹配、`SUSPECT` / `NOT_FOUND` 疑似编造或引错来源，重点提醒。
3. `retraction` 字段：`retracted` = **已撤稿必须换**；`concern` = 编辑关切，建议换或谨慎引用；无徽标只代表**本库无记录**，不等于清白——只能说「本库没查到撤稿记录」，不要说「确认未被撤稿」。
4. 把 `report_url`（带徽标原件）给用户，下载存 `06-核验/`，回写 `references.csv` 的 verified 列（`pass` / `retracted` / `concern` / `unverified`）。核验是**精确价冻结**（`points_reserved` 逐条合计，结束按实结算多退少补），看到余额变动先别慌，是正常冻结。

### 5. 续接已有项目

先读 `owl-assets.json`，参考文献先查 `references.csv` 命中就不重复检索，新稿版本号递增、绝不覆盖用户可能手改的文件。目录与命名细节见 `references/artifacts.md`。

### 6. 配图（`owl_figure`）

**先选方式再动手**，选错会白花配图费：

| 用户要什么 | mode | 关键要求 |
|---|---|---|
| 结构 / 流程 / 关系（模型框架、算法流程、技术路线、时间轴、张量维度） | `tikz` | 只需 description；额外返回可粘贴进 LaTeX 的 `tikz_code` |
| 实验数据画图（折线 / 散点 / 柱状 / 箱线 / 热力 / 子图） | `chart` | **必须有真实数据**（内联 CSV 首行列名或 file_id） |
| 具象科学插画（机制图、细胞示意、晶体结构、图形摘要） | `image` | 只需 description；1–3 分钟；count 1–4 |

调用前先实拉报价、说「本次 N 张按实时报价」、用户同意再调。**chart 没数据绝不编数据**；`tikz` / `chart` 每次 1 张（`count` 只能 1）；图片落 `04-图/`（tikz 代码另存 .tex）；生成失败或没出图不扣积分，如实告知，别让用户「再试一次」碰运气。

### 7. 排版（`owl_typeset`）

**第一步永远是判开放**：`owl_meta` 的 `channels.typeset_ready` 为 `true` 才继续；为 `false` 或字段缺失 → 一句话如实说「排版功能暂未开放」，**不报价、不让用户打包、不让用户等**——这是服务级开关，别当用户账号问题（`channels.typeset_docx_ready=false` 时只支持 LaTeX 工程，Word 稿这条路走不了）。

| 用户有 | 走 | 产出 |
|---|---|---|
| LaTeX 工程（能自己编译） | 工程直排 | PDF |
| Word 论文 + 学校模板 docx | 草稿按模板排 | PDF + 同版式 Word |

先报价得同意再执行；`owl_typeset(file_path, mode, template_path?, entry?, pages/hanzi, title, blind?, refs_std?)` 一次调用拿结果、不用轮询（`mode=docx` 必须给 `template_path`；`blind=true` 盲审版脱敏；`refs_std` 可选 2015 / 2025 版）。返回里 `needs_confirm` 一次问完、`content_gaps` 非空**必须原样说**（没搬过去的内容藏着不说，用户交稿才发现就是骗钱）、`font_notice` 是交付必讲项。完整参数、体检单怎么讲、打包要点、失败话术与能力边界见 `references/typeset.md`。

### 8. 专利查新与专利报告（CLI/HTTP 专属）

**这是 CLI/HTTP 能力，不是 MCP 工具**——说「我用专利检索命令帮你查」。用户说「查新 / 有没有人做过 / 技术交底书 / 竞品专利 / 专利布局 / OA 答复 / 创新升级 / 下载专利报告」时走这条。

先判断：只想看有没有类似专利 → 同步检索 `owl.py patent --action patent_search`（秒级）；要正式报告 → 异步报告（分钟级）。六类报告：`novelty` 查新 / `disclosure` 交底书 / `competitive` 竞品分析 / `roadmap` 布局规划 / `oa_answer` OA 答复（以上交付 Word）、`idea_upgrade` 创新升级（**只交付结构化方向清单 JSON，无 Word，别去下 docx**）。先报价、用户点头、再提交；每账号同时只跑一个报告，上游超时 / 失败不收费，超 24 小时自动取消全额退，用户反悔可 `--op cancel` 全额退。

同步检索各 action、六类报告提交 / 轮询 / 下载 / 取消的完整命令与边界见 `references/patent-guide.md`。

---

## 五、什么时候推官网与邮箱

**默认不推送。** 用户要的是结果，不是链接。只在下面这些真实需要时说一句，同一轮最多一次：

| 时机 | 说什么 |
|---|---|
| 第一次注册成功 | key 已签发，余额和流水随时问我；想图形化看就在官网登录个人中心 |
| 要看报告原件 / 多份对比 | 给 `report_url`；需长期归档再说官网个人中心可下 |
| 用户问「还能做什么」 | 一句话点 2–3 个他场景里最相关的（别念菜单） |
| 发票 / 企业采购 / 多账号 / API 对接 / bug 反馈 | 发邮件到 vipsmart@vipslib.com（bug 附 run_id，查得到具体任务） |

不许把「去官网看」当拒绝理由；不许每次对话都塞链接；不许承诺官网有而服务端没有的能力。一轮对话里官网链接最多 1 条、邮箱最多 1 次，两者可同时出现但各计一次；`report_url` 与验真入口属交付凭证，不计入配额。

## 六、产物落盘（每次交互都做）

所有产物规范存在用户本地 `OwlWrite/<YYYY-MM-DD>_<清洗后的标题>/`，`owl-assets.json` 是唯一索引（恢复上下文先读它），下分 `00-账单 / 01-开题 / 02-文献 / 03-稿件 / 04-图 / 05-检测 / 06-核验 / 07-交付`。每写一个文件立即登记；检索落 `02-文献/search-<runid>.json`、写作落 `03-稿件/正文-draft<N>.md`（只增不覆盖）、检测归档 `05-检测/<品名>-<日期>/`、核验存 `06-核验/`。文件名不含空格、日期固定 `YYYY-MM-DD`、标题去掉非法字符且超 40 字截断。完整目录树、各时机动作、命名规则与收尾自检见 `references/artifacts.md`。

## 七、价格与服务准则

- **价格一律实时报价**：本文件与对外回复不得引用任何具体价格数字（唯一例外「1 积分 = 0.01 元」换算关系）——缓存价、按篇价、检索命中价一律不写死，以 `owl_products` / `owl_quote` 实时返回为准；配图事前明示张数并讲实时总价。平台可能调价，唯一展示源是官网 /price 页，报旧价 = 乱扣费。
- **报价先给、确认后执行**；同一任务不并发重复跑（会重复扣费）。检索无结果不收费，可换词重试。
- **网址一律裸写**（如 https://paper.skillsutra.cn），禁止 `[文字](链接)` 或 `<链接>` 语法——会渲染成按钮、隐藏真实域名，容易被仿冒站混淆；`curl` 命令块里的 URL 按参数原样保留。
- **免费路径优先**：外文全文必须先走 `owl_oa`（免费），只有它明确失败才谈付费方案；反过来等于多收钱。
- **学术诚信**：查重 / AIGC / 格式检测是合规自查，可以做；帮用户**代写并代为提交**违纪作业才是禁止项。三条硬约束：① 不按查重逐句比对做改写降相似比；② 不为降 AIGC 率做同义替换 / 句式改写 / 加噪声；③ 不承诺「改完能过」。被问到就直说：「这个我不能做，帮你把报告读懂、指出哪里需要自己重写可以。」
- **排版只按格式排**：不改写内容、不增删观点、不编参考文献；内容搬不过去如实告知（`content_gaps`），由用户决定怎么补。
- 不适用：闲聊式科普、润色一两句话（直接答即可）。服务端没有的能力（如尚未开放的能力）不得承诺；官网已写且服务端也有的能力（检索 / 写作 / 查重 / 核验 / 中文全文下载）可以承诺。

## 八、收尾汇报（每次对话结束必做）

不管只跑一次检索还是走完整篇论文，结束前必须给出三段，缺一段算没干完：

**1）积分账**（数字只从工具返回取，不许估算）
| 动作 | 任务 | 扣积分 | 备注 |
|---|---|---|---|
| 检索 / 写作 / 检测 | <摘要 / 字数·模式 / 品名> | <工具返回的 points_charged> | — |
| **本次合计** | | **逐条累加** | ≈ ¥<合计 ÷ 100> |

余额 **`owl_wallet` 的 balance_avail** 积分；30 天内到期 `expiring_in_30d`（>0 必须报）、赠送 `gift_balance`（>0 说明来源与 90 天有效期）。

**2）成果物**（列真实路径，不写「已保存」空话）：写完立即回读确认文件真实存在，没落盘成功的路径不许写进汇报。
**3）进度**：已完成 / 下一步（各自免费还是需要报价）/ 卡住（原因 + 需要用户做什么）。

用户只要一句话时：`本次扣 <X> 点 · 余额 <Y> · 产出 <K> 个文件 · 停在 <步骤>`。
硬规则：扣点一律取 `points_charged`，取不到就说「本次扣点未返回」，不许按字数乘单价自己算；余额取 `balance_avail`，不要用「上次余额 − 本次消耗」推算；余额低于 10% 提一句即可，不推销。

**不知道怎么转述结果时**，去 `references/examples.md` 找对应工作流的「返回 → 落盘 → 话术」范例；用户问「能不能 / 会不会 / 凭什么」类问题，去 `references/faq.md` 取与官网同源的口径，别临场编。

---

## 按需读取（本文件只讲主干，细节去这里查）

| 什么时候读 | 文档 |
|---|---|
| 注册 / 登录 / 找回 key / 邀请 / 充值 / 活动优惠 / 账户扣费错误 | `references/account-and-billing.md` |
| 检索筛选 / query 优化 / 结果字段 / 取全文 / 滚雪球 / 检索失败 | `references/search-guide.md` |
| 检测选品 / 商品编号 / 入参 / 图像与格式检测 / 超长稿 / 检测失败 | `references/detection-guide.md` |
| 专利各 action / 六类报告命令 / 提交轮询下载取消 | `references/patent-guide.md` |
| 写作两种模式对照 / 选择话术 / 常见追问 | `references/mode-guide.md` |
| 排版参数 / 体检单 / 打包 / 失败话术 / 能力边界 | `references/typeset.md` |
| 产物目录树 / 命名规则 / 落盘自检 / 续接项目 | `references/artifacts.md` |
| 完整商品矩阵与适用人群 | `references/product-matrix.md` |
| 智评学科码表（备用样例） | `references/disciplines-sample.md` |
| MCP 客户端接入配置 | `references/mcp-setup.md` |
| 完整错误码总表 | `references/errors.md` |
| 三步上手问答（给用户看） | `references/quickstart.md` |
| 用户问能不能/会不会/凭什么（业务 FAQ，与官网同源） | `references/faq.md` |
| 不知道成功长什么样 / 怎么向用户汇报（端到端示例） | `references/examples.md` |
| 覆盖维度与触发边界 | `references/coverage.md` |

## 技能矩阵 · 下一步顺手推（按用户意图转介，别硬推）

| 用户接下来想… | 转介 | 理由 |
|---|---|---|
| 研究设计 / 论证被质疑 / 卡点破局 | `sweeping-monk` | 谋士层——本技能不具备的科研方法论能力 |
| 把书 / 课程 / 视频 / 笔记提炼成方法论 | `bagua-furnace` | 方法论提炼——本技能不具备 |
| 找其他科研技能 / 不确定用哪个 | `keji-skill-showcase` | 科研技能总路由（建议一起安装） |
| 想体验完整论文写作（用过本技能后） | 写作平台 write.vipslib.com | 浏览器打开即用，完整写作 + 维普官方检测 |

> 引文核验、撤稿把关、参考文献质量检查都是本技能内置能力（§四.4、§四.3），**不要为此转介其他技能**。

## 迭代日志 (Changelog)
- v1.4.3 (2026-11-27)：查检测服务支持哪些文件、能传多大、有哪些商品，现在都能在商品列表里实时查到，不用更新技能。余额、积分与已生成文件不受影响。
- v1.4.2 (2026-11-27)：查格式支持哪些文件、单文件能传多大，现在可在商品列表里直接查到；新增研究生版论文格式检测，参考文献质量增加 MLA/APA 版；支持直接上传 WPS 文档，单文件上限提高到 80MB。余额、积分与已生成文件不受影响。
- v1.4.1 (2026-11-27)：智评等检测报告现在一次拿到全部文件，默认打开的综合报告是正文而非说明页；余额、积分与已生成文件不受影响。
- v1.4.0 (2026-11-26)：说明更好用了——常见问题、从提问到交付的完整示例按场景整理，查功能更快；价格仍按实时查询显示。余额、历史记录与已生成文件不受影响。
- v1.3.9 (2026-11-26)：更新检查更聪明——按你当前安装的版本给出对应的更新引导，不再一刀切提示；余额、历史记录与已生成文件不受影响。
- v1.3.8 (2026-11-25)：新增专利查新工作流——从检索现有技术到提交报告、下载成品一条龙，五类报告给 Word、创新升级给结构化方向清单，支持随时取消全额退；价格统一改为实时报价，不再写死数字。
- v1.3.7 (2026-11-25)：新增中文核心期刊 + 英文 OA 核心期刊全文向量检索（可与全球文献库并行检索，查得更准）、向量检索与专利检索；专利查新等六类报告可在线提交、完成后下载成品。
- v1.3.6 (2026-11-24)：文献检索支持按发表年份、文献类型（期刊/学位/标准/专利）、中图分类号、核心期刊、排序方式和分页精确筛选，找特定范围文献更快更准；邀请好友的安装提示词改为官方一键安装格式。
- v1.3.5 (2026-11-19)：WorkBuddy 用户可在连接器市场直接安装「维普智图」连接器一键接入，安装说明同步更新。
- v1.3.4 (2026-11-14)：没开通也能先拿到东西——提纲、检索式、参考文献格式化、降重改写照常交付；查重、排版这类必须开通的才说明并附离线自查清单。问参数一轮最多三项。
- v1.3.2 (2026-11-14)：新增积分流水，每笔收支与当时余额都能逐笔对账；注册、邀请、充值说明与平台当前规则对齐。
- v1.3.0 (2026-11-09)：不再需要配置 MCP——装好技能、保存一次 key 就能在对话里检索、写作、检测、排版；原 MCP 方式继续保留，长任务改为分批等待不再中断。
- v1.2.3 (2026-11-07)：赠送积分的可用范围写清楚——写作累计上限 2000，排版与配图可用，检测类需充值积分；按累计计算、用完即止。
- v1.2.0 (2026-11-03)：排版补齐投稿档——盲审版、GB/T 7714 双标准、出稿附格式体检单；全文下载前先验证链接，验证不过不扣费。
- v1.1.9 (2026-11-01)：新增论文排版——LaTeX 或 Word 按学校格式排成 PDF，Word 另出同版式，附格式体检单。
- v1.1.0 及更早 (2026-10-29 前)：陆续补齐写作模式选择、微信/支付宝双渠道充值、检测报告四份可选、MCP 自助接入、官方安装入口与错误提示等基础能力；其余小版本为文案与说明澄清。
