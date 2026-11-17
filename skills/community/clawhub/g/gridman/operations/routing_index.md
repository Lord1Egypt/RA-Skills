<!-- operations/routing_index.md —— 知识路由索引 -->

# 知识路由索引

> 本文件只维护领域入口、跨域硬闸和少量高价值强锚；执行程序见 `operations/routing_flow.md`。
>
> 默认机制是：**领域级宽路由 → 领域子树内实时发现 → 文件内精确定位 → 真实误路由后渐进补锚**。
>
> 新增或调整单个 knowledge / Workflow 通常无需登记。只有新增领域入口、跨域硬闸，或 `gridman-mind/05_learning/route_failures.md` 证实的高频强锚，才维护本索引。

## 路由总览

```text
用户问题
  → 轻量场景：走 SKILL.md 自我介绍
  → 记忆场景：按 operations/private_resources_rules.md 定位 Mind
  → 专业问题：先过 L-1，再以 L0/L1 定位领域
  → 在命中领域子树内实时发现 knowledge / Workflow
  → 需要外部操作：进入 operations/routing_flow.md 的能力发现、授权、执行与复核
```

## 知识路由（knowledge + 可选 workflows）

### L-1 前置硬闸（最高优先级）

| 触发场景 | 动作 |
|---|---|
| “查最新”“最新规定”“最近政策”“有没有更新” | 读 `operations/source_directory.md`，从官方源 fetch 核实 |
| 明确要求确认文号、效力状态 | 读 `operations/source_directory.md`，从官方源核实 |
| 涉及税率、优惠截止日期、具体文号 | 读 `operations/source_directory.md`，从官方源核实 |
| **答案正确性依赖现行政策**（税收优惠、加计扣除比例、征收率、起征点/免征额、预缴口径、适用条件、过渡期安排等），即使用户未说“最新” | 主动触发：先读 `operations/source_directory.md`，按「交叉验证方法」核实现行有效版本，再作答；不得仅凭内置记忆给出可能过期的数字或结论 |

L-1 只处理时效与权威来源，不替代专业领域路由。

> **主动核实原则**：优惠比例、税率、门槛、期限、文号这类“会随政策变动、答错会误导”的要素，古立特默认视为时效敏感，主动核实而非被动等用户追问“是不是最新”。确实无法联网核实时，明确加时效标签（“以最新官方为准”）并提示用户自行确认，绝不把内置记忆当作现行事实。

> **不触发（避免过度搜索）**：以下情形默认**不联网**，直接用内置知识作答，只在结论涉及具体数字/文号时附一句“如需引用请以最新官方为准”即可，不必每次都去搜：
> - 纯原理、纯方法论、准则/税种的机制与逻辑（如“递延所得税怎么理解”“增值税链条原理”）；
> - 举例说明、教学演示、口算示范中使用的假设数字（已声明为示例）；
> - 历史政策梳理、已明确时间点的追溯问题；
> - 用户已给定政策/数字、只要求据此计算或判断；
> - 概念定义、流程步骤、模板结构这类不随政策数字变动的内容。
>
> 判定口径：**只有当“答错会因政策已变而误导用户”时才主动核实**；能靠原理和用户给定条件答对的，不触发搜索。一次问答内已核实过的要素，同一会话不重复联网。

### L0 强锚快速通道

L0 只保留跨域歧义大、入口稳定或高频且能显著减少误路由的锚。命中后仍须在目标子树内实时发现，不把锚永久绑定到某个文件。

| 强锚/场景 | 领域入口与附加要求 |
|---|---|
| 审计底稿、整套底稿、审计项目 | `references/knowledge/audit/` + `references/workflows/audit/`；优先发现总控 Workflow，再由其调度专项流程 |
| 会计分录测试、JET、序时账、异常凭证、对方科目、多借多贷 | `references/knowledge/audit/` + `references/workflows/audit/`；优先匹配分录分析与测试内容 |
| 税费审计、应交税费勾稽、税会差异复核（审计视角） | 同时进入 `references/knowledge/audit/`、`references/knowledge/tax/`，Workflow 在 `references/workflows/audit/` 内发现 |
| CAS、IFRS、会计准则及准则应用 | `references/knowledge/accounting/`；涉及现行条文时同时触发 L-1 |
| 审计、税务、法律或监管问题中的“最新/有效/截止/文号” | 先过 L-1，再进入对应专业领域 |
| PDF/扫描件/OCR/Word/PPT/Excel/网页解析 | 进入执行流程，发现 `document.extract`；专业判断仍回到对应 knowledge 领域 |
| 工商信息、股价、行情等外部数据 | 进入执行流程获取数据，再按问题语义进入专业领域 |

单次长尾命中不进入 L0；其余专业表达统一交给 L1 和目录级发现。

### L1 领域级宽路由

| 意图大类 | knowledge 子树 | 可选 Workflow 子树 |
|---|---|---|
| 会计处理、准则、分录、行业核算 | `references/knowledge/accounting/` | 按任务语义在 `references/workflows/` 的对应职业子树发现 |
| 审计、内控、底稿、抽样、科目测试、舞弊风险 | `references/knowledge/audit/` | `references/workflows/audit/` |
| 财务分析、管理会计、经营分析、舞弊识别 | `references/knowledge/analysis/` | 在 `references/workflows/` 内按职业领域受限发现 |
| 税法、申报、纳税调整、税务风险 | `references/knowledge/tax/` | 在 `references/workflows/tax/` 等实际存在的相关子树发现 |
| 投行、估值、尽调、公司金融、财报研究 | `references/knowledge/investment/` | 在 `references/workflows/investment/` 等实际存在的相关子树发现 |
| 合规、ESG、经济法、监管处罚 | `references/knowledge/compliance/` | 在 `references/workflows/compliance/` 等实际存在的相关子树发现 |
| 政府/非营利会计、财务数字化、共享服务/RPA | `references/knowledge/specialized/` | 在 `references/workflows/specialized/` 等实际存在的相关子树发现 |
| 学术研究、实证方法、教学案例 | `references/knowledge/academic/` | 在 `references/workflows/academic/` 等实际存在的相关子树发现 |

目标 Workflow 子树不存在时不报错：使用命中的 knowledge + `operations/routing_flow.md` 通用流程，并明确未加载专用 Workflow。

### L2 领域子树内实时发现

L0/L1 选定领域后，只在已命中的 knowledge 子树及任务需要的 Workflow 子树内进行受限发现：

1. 列出该子树当前实际存在的文件；不得先扫描整个 `references/`。
2. 按以下信号综合排序候选：
   - 文件名与用户原话、任务对象、交付物的语义相关度；
   - 文件头/frontmatter 中的领域、职责、适用场景、触发条件、排除条件；
   - 首个标题和前置说明；
   - 与已命中候选的显式关联。
3. 优先读取最相关的少量候选；信息不足时再渐进扩大到同一子树内的次优候选。
4. knowledge 与 Workflow 分开判断：knowledge 提供专业依据；Workflow 只有与任务和输入条件匹配时才加载。
5. 没有统一元数据时，以“文件名 + 首个标题 + 前置说明”兜底，不要求为发现能力维护集中式逐文件清单。
6. 候选仍不明确时，向用户澄清关键歧义，或诚实使用通用流程降级。

这是受限目录发现，不是整库扫描。跨领域问题按 L4 分别进入各自子树。

### L3 文件内精确定位（grep-first）

命中具体文件后：

1. 小文件可按需全文读取。
2. 大文件先运行 `grep "^## "` 或宿主等价标题扫描，实时取得章节图。
3. 只读取相关章节的行区间；不足时再扩展相邻章节。
4. 章节图实时生成，不在文件内或别处预存章节目录，避免正文变化后漂移。

### L4 跨领域动态组合

跨领域问题拆成子问题，分别执行“领域宽路由 → 子树发现 → 文件内定位”，再统一口径：

| 组合场景 | 路由方式 |
|---|---|
| 审计 + 税务 | 分别进入 `references/knowledge/audit/` 与 `references/knowledge/tax/`；审计执行 Workflow 在审计子树发现 |
| 投行 + 财务分析/会计 | 分别进入 `references/knowledge/investment/` 与对应 analysis/accounting 子树 |
| 准则 + 实务执行 | 先取得 accounting 专业依据，再由匹配 Workflow 或通用流程执行 |
| 外部数据 + 财税处理 | 先通过执行流程获取并验证数据，再进入专业知识路由 |

不得因跨领域而扫描所有领域。

### L5 反馈与渐进补锚

`route_failures.md` 只记录**真实、可复用、值得跨会话留存**的误路由或未发现事件。记录位置和写入前提由 `operations/private_resources_rules.md` 管理；本节唯一负责晋升规则。

1. 先区分路由失败与知识缺失、工具报错、用户输入不足；后三者不得伪装成路由失败。
2. 记录建议包含：日期、用户原话、实际进入领域/文件、正确目标、失败原因、建议修正。
3. 定期聚类复核，不在失败发生当场机械修改 L0。
4. 仅当同类表达重复出现，或存在高确定性、高影响且可稳定判定的模式时，才晋升为 L0 强锚或调整 L1 领域入口。
5. 单次、低频、歧义大或仅靠个案上下文成立的长尾失败，不补专用锚；优先改善文件名、文件头或领域内发现信号。
6. 晋升后用原失败案例和相邻反例回归验证，避免新锚截获其他领域。

目标不是让 L0 覆盖所有文件，而是让真实使用逐步提高命中率。