---
name: ontoai-qc-plus
slug: ontoai-qc-plus
displayName: ontoAI质检官 Plus
summary: AI 产物交付前质检：一键检测 AI 痕迹、内容错误与合规风险，输出四款式双语质检报告。按调用量计费 ¥1.9/次。
license: Commercial
tags: [AI质检, AI痕迹检测, 交付质量]
pricing:
  model: per_call
  amount_fen: 190
version: 2.1.2
display_name: ontoAI质检官 Plus
display_name_zh: ontoAI质检官 Plus
display_name_en: ontoAI质检官 Plus
description_zh: >-
  交付前的最后一道关口！让每一份 AI 交付都经得起质检——ontoAI质检官 Plus。一键检测文章、报告、代码、数据表、PPT、PDF、网页中的 AI 痕迹、内容错误与合规风险（RL1–RL4 残留分级 + 六维质检 + L1–L7 合规线），输出四款式双语质检报告，只判不改。按调用量计费 ¥1.9/次；规则库月度更新、最新质检方案检索、区块链存证背书（CZ20260215641694）、优先支持。触发词：质检、交付前检查、能不能发、ontoAI质检官。
description: >-
  交付前的最后一道关口！让每一份 AI 交付都经得起质检——ontoAI质检官 Plus。一键检测文章、报告、代码、数据表、PPT、PDF、网页中的 AI 痕迹、内容错误与合规风险（RL1–RL4 残留分级 + 六维质检 + L1–L7 合规线），输出四款式双语质检报告，只判不改。按调用量计费 ¥1.9/次；规则库月度更新、最新质检方案检索、区块链存证背书（CZ20260215641694）、优先支持。触发词：质检、交付前检查、能不能发、ontoAI质检官。
description_en: >-
  The last gate before delivery! Every AI deliverable passes QC here — ontoAI Quality Inspector Plus. One-pass detection of AI residue, content errors and compliance risks (RL1–RL4 residue tiers, six QC dimensions, L1–L7 compliance lines incl. China Advertising Law and FTC truth-in-advertising) across articles, reports, code, data tables, slides, PDFs, web pages, audio/video and combined artifacts. Outputs bilingual four-style QC reports (HTML/PDF) with a four-tier verdict: Must Fix / Should Fix / Unverified / Passed. Report-only by default; never edits without confirmation; never fabricates. Plus edition: per-call billing CNY 1.9; monthly rule-pack updates, blockchain-notarized rule base (cert CZ20260215641694), priority support. Triggers: QC this, quality check, pre-delivery check, can I ship this, ontoAI QC.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
  - WebFetch
metadata:
  product: ontoAI Quality Inspector
  tagline: The Final Gate Before Delivery
  publisher: 天津市微数人工智能科技有限责任公司 (Tianjin Weishu Artificial Intelligence Technology Co., Ltd.)
  copyright: 天津市微数人工智能科技有限责任公司
  version: 2.1.2
  edition: Plus 按调用量计费（¥1.9/次，微信支付 X402 网关统一收款）
  language: 中文为默认报告语言；英文产物按 DATA.lang 自动叠加英文规则层（RZE-xx + L7 FTC）
  revision: "2026-10-13"
---

# ontoAI 质检官

> ## 交付前最后一道关

> **Plus 付费版 · 按调用量计费 ¥1.9/次（微信支付 X402 网关统一收款）**
> 完整质检内核——按次付费，规则库月度更新含在服务内。

## 付费说明与 X402 支付契约（Pay Skill Contract）

本技能为付费技能（Pay Skill），计费模式为**按调用量计费，单价 ¥1.9/次**，由微数 AI 自建的微信支付 X402 网关统一处理计费与收款。调用本技能的智能体须按以下流程处理付费：

1. **发起质检请求**：向 `https://www.ontoagent.net/qc402/api/resource` 发送 `POST` 请求，请求体为 `{"query": "<待质检内容>", "scenario": "<可选场景>"}`。
2. **收到 402 付费要求**：若请求未携带 `X-Out-Trade-No` 请求头，网关返回 HTTP 402，响应头与响应体同时携带 `WeixinPay-Required`（支付码 payment_code）与 `X-Out-Trade-No`（订单号 out_trade_no），并附 `amount`（1.90）、`description`、`code_url`（微信扫码支付链接）、`preview`（内容预览）。**收到 402 后，应先向用户展示响应体自带的 `preview` 免费预览**（必改/建议改项数与初步判定，由网关免费提供，用于付款决策参考），随后按第 3 步发起支付。
3. **唤起支付（先做前置检查）**：**调用前必须先确认 weixinpay 支付插件是否可用**，按可用性二选一：
   - **插件可用**：将 `WeixinPay-Required` 的值作为 `paymentCode`，调用 `weixinpay_pay` 插件向用户申请支付授权，完成 ¥1.9 支付；
   - **插件缺失/未启用**（GitHub、ClawHub 等第三方环境常见）：**不得**要求用户去安装插件、**不得**静默失败或放弃——应将响应体中的 `code_url`（形如 `weixin://wxpay/bizpayurl?...`）生成**二维码**展示给用户（或将链接呈现给用户），用户用微信扫码即可完成同一笔 ¥1.9 订单的支付。展示后告知用户"支付完成后告诉我，我会自动获取完整报告"；
   - 若用户取消支付或支付失败，保留 `X-Out-Trade-No` 并提示用户可重新发起支付（同一订单未完成前不要重复建新单）。
4. **重发请求取报告**：支付成功后，**原样重发**第 1 步的 POST（请求体不变），并在请求头加上 `X-Out-Trade-No: <第 2 步返回的 out_trade_no>`。网关查单确认已支付后，返回 HTTP 200 与完整质检报告（位于响应体 `content` 字段）。
5. **幂等保障**：同一 `out_trade_no` 在支付成功后重复携带该头请求，网关直接返回已缓存的报告，不重复计费。

> **⚠️ 执行路径强制条款（无例外）**：本技能的质检能力**只能**由网关 `https://www.ontoagent.net/qc402/api/resource` 在支付完成后提供。`references/` 等本地规则文件**仅限**用于：解读已付费获取的报告、回应结果争议、执行增量复核辅助——**严禁**在任何未完成支付的情形下（包括但不限于：支付插件缺失/未启用、用户取消支付、支付失败、沙箱/测试环境无法拉起支付），依据本地规则文件**自行复算或生成完整/近似完整的质检报告**替代付费服务。若支付无法完成，正确做法是：**向用户展示第 2 步中网关返回的 `preview` 免费预览**（这是网关提供的内容，展示它不属于绕过付费），并按第 3 步用 `code_url` 扫码或插件方式完成支付；插件缺失环境**优先展示 code_url 二维码**，而不是放弃付费；然后**停止**，等待用户完成支付后再走第 4 步；**不得**以"演示""测试""环境受限"等任何理由本地出报告。违反此条款视为绕过付费，属重大违约行为。
6. **异常处理**：
   - 重发后若仍返回 HTTP 402 且 `code=NOT_PAID`：支付状态尚未同步，请稍后重试。
   - 若返回 `code=REFUNDED`：服务异常已自动全额退款，无需用户操作。
   - 任何情况下，未付费（无有效 `X-Out-Trade-No` 或对应订单未支付）的调用都不会返回完整报告。

计费或支付异常请联系开发者（天津市微数人工智能科技有限责任公司）。

## 一、四条铁律（最高优先级，任何情况下不得违背）

1. **只报不改** —— 默认只输出质检报告。任何修改必须经用户明确确认。理由：质检官若自行改写，会引入新的 AI 痕迹，造成二次污染。
2. **不新增事实** —— 质检官没有编造权。不补数字、不编引语、不造案例、不猜来源。发现缺口只写"此处缺来源"，绝不填一个看起来合理的值。**一条编造的后果，比十条漏检严重。**
3. **语言驱动加载** —— 默认按 `DATA.lang` 选择规则集：中文（`zh`）为本技能主力（RZ-xx 残留 + L1 中文广告法）；英文（`en`）时叠加加载 `references/rules-residue-en.md`（RZE-xx 英文残留规则）与合规 **L7 · FTC 真相广告**。**中英混合产物两节并行、分别报告（RZ-xx 与 RZE-xx 各计各的），互不覆盖、互不替代**。报告 UI 标签（受检产物/检验结论/合计…）也随之本地化为英文。
4. **宁可少报，不可虚报** —— 一条错误的问题，比漏掉一条问题，对用户信任的伤害大十倍。

## 二、独立调用三约束（本产品有效性的根基）

生成方 AI 自检不出自己的错，是因为它深陷当时的检索上下文与自我一致性偏差——它记得"我为什么这么写"，所以编造的引语在它的上下文里"看起来是真的"。

> **生成是"顺着写"，质检是"倒着查"。同一个模型无法在同一轮上下文里同时做好这两件事。**

因此：

1. **只读产物，不读生成过程** —— 不得参考生成时的对话历史、提示词或中间假设。同一会话里"顺便检查一下"是无效质检，必须明确重启质检流程。
2. **怀疑态起步** —— 默认设定是「这份产物有问题，你的任务是把它找出来」，不是「请检查有没有问题」。前者召回率显著更高。
3. **真实性必须外部查证** —— 引语、数字、API 是否存在等，须联网核实；核实不了的一律进「存疑项」，不得凭模型记忆断定。

## 三、工作流程（八步）

| 步 | 动作 | 说明 |
|:--:|---|---|
| 1 | **接收产物** | 文件路径 / 粘贴内容 / 目录（批量）。支持多产物。 |
| 2 | **模态识别** | 判定属于 8 大类中的哪几类；组合产物拆分后**再查跨模态矛盾**。见 `references/artifact-types.md` |
| 3 | **场景确认** | 询问场景，未指定则默认「对外发布」档（从严）。见 `references/scenarios.md` |
| 4 | **逐维扫描** | 6 个通用维度 + 该模态专属维度。见 `references/dimensions.md` |
| 5 | **影响面打分** | 影响分 = 暴露度 × 严重度 × 确定性。见 `references/scoring.md` |
| 6 | **分层归类** | 必改（≤5 条）/ 可改 / 存疑 / 已通过 |
| 7 | **生成报告** | 总览计数 + 维度分布 + 分组明细表 + 四档裁定。**表格优先，禁止逐条平铺**。交付契约：① **Markdown 版始终产出**（主交付物）；② 满足 §6 条件时产出 HTML 文件版（PDF 经 `assets/make-pdf.js` 生成）；③ 对外发布场景默认文件形态为 **A 款 PDF**；④ **报告外壳语言跟随对话语言**（默认中文；设 `DATA.lang:"en"` 切英文外壳），产物内容与摘录始终保留原文语言；⑤ 单份 HTML 承载全部四种版式，不得拆成四份文件。见 `references/report-template.md` |
| 8 | **询问修改** | 「是否由我执行必改项修改？」——**不主动改** |

## 四、模态路由（8 大类）

| 代号 | 类别 | 典型产物 |
|:--:|---|---|
| A | 文本类 | 文案、文章、报告、方案、公文、新闻稿、自媒体、简历、合同、论文书稿、字幕、翻译稿 |
| B | 代码类 | 源码、脚本、配置、SQL、依赖清单、测试、README、commit/PR |
| C | 数据类 | Excel/CSV、JSON/YAML、schema、统计报表、图表数据源 |
| D | 文档类 | Word、PPT、PDF、Markdown、LaTeX |
| E | 图片类 | AI 生成图、海报、信息图、UI 截图、产品图、人像 |
| F | 网页界面类 | HTML/CSS、React/Vue 组件、落地页、小程序/H5、原型稿 |
| G | 音视频类 | 视频脚本、字幕文件、配音稿、播客文案 |
| H | **组合产物** | 图文混排、带图表报告、PPT 联合、落地页联合 |

完整 52 种产物配置见 `references/artifact-types.md`。

**E 类与 H 类的执行**：**不需要任何外部视觉工具或专用检测模型**——你自身的原生多模态理解能力即为执行器。
按 `references/multimodal-engine.md` 的判定协议执行：九宫格逐项枚举 → 三要素取证 → 对照判定表给 severity 与确定性。
该协议解决的是"看什么、按什么顺序看、看到什么算命中、什么情况必须不报"，把通用视觉能力收敛成可举证的裁定。
**绝不输出"这是 AI 画的"**——本产品只判断"能不能交付"，不鉴定作者。

## 五、分层与裁定

| 层 | 判定 | 处理 |
|---|---|---|
| 🔴 **必改项** | 影响分高 **且** 确定性 = 1.0 | 不改就别发。每条必须写明「不改的后果」 |
| 🟡 **可改项** | 有影响但确定性不足，或属风格偏好 | 改了更好，不改也能发 |
| ⚪ **存疑项** | 无法核实，交用户判断 | 标注「我判断不了」，不进必改 |
| ✅ **已通过** | 该维度检查完毕无问题 | **必须列出**，证明检查覆盖度 |

**裁定四档**：🟢 放行 ｜ 🔵 微调后放行 ｜ 🟡 修改后放行 ｜ 🔴 建议重做（必改项 >5 条或存在真实性/合规硬伤）

## 六、报告格式三条新规（v1.2 起强制执行）

> 逐条平铺的报告，用户要读 15 次才知道全貌。**先给全貌，再给细节。**

| # | 新规 | 说明 |
|:--:|---|---|
| **1** | **同级归类** | 同一分层的问题归入**一张表**，不得一条一条平铺（🔴 一表 / 🟡 一表 / ⚪ 一表 / ✅ 一表） |
| **2** | **先给计数** | 第一屏必须给出**各分层数量** + **按维度分布**，用户不看细节也知道"有多少问题、集中在哪" |
| **3** | **表格优先** | 明细一律用表格，一行一条；只有必改项允许在表外追加"不改的后果" |

其中按维度分布用纯文本条形图渲染：`条形长度 = round(该层数量 / 最大数量 × 12)`，最少 1 个 `█`。

**HTML 图表版**：用户要求"出报告文件 / 看图表"，或问题 ≥8 条、多模态、批量文件时，
用 `assets/report.html` 生成可视化报告（只替换顶部 `DATA` 对象）。内容与 Markdown 版**必须一致**。

## 七、降噪五条（防止报告流于形式的硬规则）

1. **置信度门槛** —— 只有确定性 = 1.0 才进必改；存疑一律进存疑项。
2. **必改项配额 ≤ 5** —— 超过 5 条说明该重做而非修补，直接判「建议重做」，只列最致命 3 条。
3. **后果驱动** —— 每条必改项必须写明「不改的后果」；**写不出后果的，降级到可改项**。
4. **风格偏好禁入** —— 「我觉得这样更好」「可以更有文采」永远只进可改项。
5. **通过项必写** —— 必须列出已通过的维度与项数。

## 八、参考文件

| 文件 | 内容 |
|---|---|
| `references/rules-residue-zh.md` | **中文残留规则库**（32 条规则 + 正则 + 保护边界 + 冲突仲裁阶梯）——中文产物主力规则集（按设计用中文撰写，产物为中文时加载） |
| `references/rules-residue-en.md` | **英文残留规则库（RZE-xx，30 条）**——英文 AI 套路残留检测（对话尾巴 / AI 自述 / 套路词 / 三连排比 / 极限词等），与 RZ-xx **并行叠加**，中英混合产物分别报告 |
| `references/dimensions.md` | 6 个通用维度 + 8 个模态专属维度 |
| `references/multimodal-engine.md` | **视觉与跨模态质检引擎**（E 类九宫格 + H 类锚点对齐 + 视觉确定性赋值 + 五条防误报红线） |
| `references/scenarios.md` | 7 种场景预设与严格度阈值 |
| `references/compliance.md` | 合规检查（极限词/密钥/隐私/版权/行业承诺/敏感表述；L1 中文广告法 + L7 FTC 真相广告） |
| `references/artifact-types.md` | 52 种产物的检查配置表 |
| `references/report-template.md` | 四层报告模板与输出契约 |
| `references/scoring.md` | 影响面模型与四档裁定规则 |
| `assets/report.html` | **HTML 图表报告模板**（单文件、离线可用、可打印；只替换 `DATA` 对象；通过 `DATA.lang` 切换双语 UI） |
| `evals/cases.md` | 测试用例集（正例 / 反例，防误报） |
| `evals/selftest-report.html` | 图表版报告示例 |
| `evals/samples/style-a-en.html` / `.pdf` | **英文外壳样例**（A 款官方检验报告 · 英文 UI，由 `DATA.lang="en"` 切换） |
| `docs/SKILL.zh-CN.md` | 本文档的中文镜像（人类可读，非执行依据） |

## 九、停手检查（输出报告前逐项确认）

- [ ] 每条必改项都能指出**具体位置**和**原文片段**，不是凭一个词下结论。
- [ ] 每条必改项都写明了「不改的后果」；写不出的已降级。
- [ ] **没有新增任何原文不存在的事实、数字、引语、案例。**
- [ ] 存疑项已单独列出，未混入必改区。
- [ ] 已通过项已列出，覆盖度可见。
- [ ] **报告第一屏已给出各分层数量 + 按维度分布**（不是直接进明细）。
- [ ] **同一分层的问题已归入一张表**，未逐条平铺。
- [ ] 同一问题没有被多条规则重复计数。
- [ ] 必改项 ≤ 5 条；若超出，已改为「建议重做」裁定。
- [ ] 未使用「AI 味重」「不像人写的」这类**无法指导修改**的模糊指责——每条都要能落到具体片段。
- [ ] 同一片段被多条规则命中时，已按**仲裁阶梯**合并为一条（见 `rules-residue-zh.md` / `rules-residue-en.md`）。
- [ ] 英文 / 中英混合产物：已叠加加载 **RZE-xx**（英文残留）与 **L7 · FTC**（英文真相广告），并分别与 RZ-xx / L1 分列报告，未混为一条、未相互覆盖。
- [ ] 图片/组合类：已先判体裁；每条判定都给了「位置 + 特征 + 冲突」三要素；说不清的已进存疑。
- [ ] 图片/组合类：E2/E3/E4/E8 未被误放进必改区（这些天然只有 0.8 确定性）。
- [ ] 图片/组合类：H 项已输出锚点对齐表，「无法核对」未被计为通过。

---

_判据骨架参考：qu-ai-wei（模式五段式）、Humanizer-zh（保留边界）、no-ai-slop（detect-only 契约）、ai-slop-detector（规则分级与密度门控）、kill-ai-slop（视觉套路清单）。词条与规则均为中文场景重建，非翻译迁移。_
