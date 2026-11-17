# meta-analysis · CCM A 阶段上下文菜单规格 v1.0

> 定位：**汇总并取代** v0.1–v0.4 中关于 A 阶段的散落描述。
> 命名：CCM = Conversation Context Menu。
> 范围：仅全流程轨道的 `A1 → A2 → A3 → A4 →[交接]→ B1`，覆盖计算轨道的菜单不在此文档。
> 状态：A1–A4 菜单细节**已按已定决策落定**（D9 / D12 / D13 / D15 / D17 已实施），D10 / D11 / D14 / D16 待你拍。
> 日期：2026-09-10

> ⚠️ **本文是设计稿（archive），非落地规范。** 落地后的规范以
> `references/conversation_flow_menu.md` 为准，二者冲突以后者为准。
> **2026-09-10 事后变更（D21）**：原独立节点 `A3.screening` 已并入 `A2.literature_search`
> （「文献集」），A 阶段停靠点 `A1 → A2 → A4`（3 个）。本文中所有「③ A3 初筛」独立节点的
> 段落均视为**已被合并吸收**；节点表、选项、验收项以规范版为准。

---

## 0. 已定决策对 A 阶段的净影响（变更摘要）

| 决策 | 结论 | 对 A 阶段的影响 |
|---|---|---|
| **D9** | A3 **不逐条裁决**，= 导出裁决表 → 改 → 传回 → 直接接 A4 | A3 菜单塌成 5 项，**对话内零逐条编辑入口** |
| **D12** | A3 采信 ct-literature 的 `prisma` 规则初筛，且**必需** | 导出表必须预填 `rule_decision`；A3 面板显示"漏斗"而非"42 条待裁" |
| **D13** | A2/A1 的解释器路径 bug | **已修**（`resolve_python_exe()` + `{python}` 占位符），A2 端到端已回 20 篇 |
| **A4 直下** | 100% 按 A3 清单下载，**不做下载前类型甄别** | `_skip_page_screen` 成死代码已删；A4 菜单无"类型复核"项 |
| **D15**（升级为规则）| **人工确认类型后，全链路一律不再判类型**；改类型须人工确认/发起 | 抽取层规律 R1 短路返回已删；类型降为 `doc_type` / `type_notice` 标注；`excluded` 恒 False |
| **D17**（本轮实施·方案 A）| 「人工确认类型」落在 **A3 裁决表的「文献类型确认」列**：规则预填 → 人工确认/改判 → 权威值 | 类型成为**一等可审计字段**；A4 只读，抽取层探测降为"提示词"（不一致才提示）；规则预填复用 ct-literature `classify_record`（单一真源）|
| **R 路径** | 跳过不管，记为已知接受项 | `test_a4_b1_handoff.py` 的 [2][4] FAIL 是既有环境问题，**不是回归** |

---

## 1. 通用渲染框架

### 1.1 三层菜单

| 层 | 名称 | 内容 | 出现时机 |
|---|---|---|---|
| **L0** | 上下文导航条 | 12 节点压一行，标出 ✓ 已完成 / ▶ 当前 / ○ 未达 | **每轮必贴**（全流程轨道内） |
| **L1** | 节点菜单 | 节点头（编号 · 名称 · 闸类）+ 数据摘要 + 专属选项 | 闸位节点自动贴；非闸位仅在你问 `/node` 时贴 |
| **L2** | 字段菜单 | 仅列该节点 `EDITABLE_KEYS` / schema 声明可编辑的键 | 你选"改 X"后展开 |

**L0 样例**（停在 A3）：

```
📍 全流程  │  A: ①选题 ✓  ②检索 ✓  ③初筛 ▶  ④提取 ○  │  B: ⑤合并 ○ ⑥GRADE ○ ⑦过度声明 ○ ⑧质量门 ○  │  C: ⑨初稿 ○ ⑩评审 ○ ⑪参考核验 ○ ⑫QA ○
```

### 1.2 硬性渲染规则（防漂移）

1. **选项必须穷举编号**——禁止"你要继续吗？"这类开放问法。用户看不到 GUI 上"有哪些按钮"，所以选项由我方枚举。
2. **选项集由代码派生，不由 LLM 即兴**：
   - 🔴 节点的"跳过"项由 `cc._REDLINE_GATES`（`coze_client.py:923`）过滤 —— **不硬编码第二份清单**
   - 当前节点由 `fullflow_session_ff-*.json` 的 `cursor` 决定
3. **≤3 选项** → 可用 `AskUserQuestion` 卡片；**≥4 选项** → 编号文本菜单。
   （沿用既有先例：`references/topic-selection.md` / `upstream_orchestration.md` 的 2 选项路由）
4. **菜单由脚本产出、LLM 只转述**。新增 `scripts/flow_menu.py` 负责确定性 render/status/decide。
5. **回显块**固定前缀 `## 当前流程设定 / Current pipeline settings:`，与计算轨道的 `## 当前分析设定:` **分开、互不覆盖**。

### 1.3 动作矩阵（严格对齐 `_validate_decision`，`fullflow.py:541`）

| 动作 | 含义 | 允许节点 |
|---|---|---|
| `approved` | 放行 | 全部 |
| `revised` | 带 `revision` dict 修订 | 需 schema 声明可编辑键 |
| `skipped` | 本会话不再停靠，按默认放行 | **仅软停**（A1/A2/A3）|
| `rejected` | 打回 | 非 `handoff_confirm` 时可用 |

**红线约束（代码层，非提示词层）**：
- `STAGE_TO_GATE[A4.data_extraction] = "extraction_review"` ∈ `_REDLINE_GATES` → **A4 菜单不得出现"跳过"**，且 `action=skipped` 会被 `_validate_decision` 直接拒绝（`fullflow.py:567-570`）。
- **块间交接闸**（A4 → B1）只收 `approved` / `rejected`（`fullflow.py:551-553`）。

### 1.4 状态真源映射（对话侧只读，不另起一份）

| 菜单要显示的东西 | 真源 |
|---|---|
| 当前节点 / 闸类 | `cursor.stage_id` / `cursor.await_kind` |
| `await.gate` | A4 = `extraction_review`；A1/A2/A3 = `none`（软停） |
| 各节点摘要字段 | `stage_result.*` + `next_human_action.*`（见 §3 逐节点表） |
| 可编辑键 | `EDITABLE_KEYS[sid]` ∩ `stage_result`（`fullflow.py:332`） |
| 文献类型（权威值）| `screened[i].doc_type` + `doc_type_source`（`human` / `rule`）+ `nha.summary.doc_type_dist`；A4 侧只读、经 `block_a._read_doc_type()` 取值（D17-A）|
| 回退候选集 | **必须从 `/api/session` 的 `progress` / `next_human_action` 服务端派生**，不得在 `flow_menu.py` 重写工作台那段"块序 + 块内次序 + `curIdx=-1`"JS 逻辑 |

---

## 2. A 阶段总览（4 节点 + 1 出口闸）

```
① 选题确认 ──② 检索·覆盖确认──③ 初筛·导出裁决表──④ 数据提取核验══►[块间交接]══► B1
   soft          soft              soft                🔴 redline        approved/rejected
  gate=none     gate=none        gate=none        gate=extraction_review   （仅二选）
```

| # | stage_id | 标题 | 闸 | `gate` 值 | 可编辑键 |
|---|---|---|---|---|---|
| ① | `A1.topic_selection` | 选题确认（PICOS） | 软停 | `none` | `report` · `include_reviews` |
| ② | `A2.literature_search` | 检索策略与覆盖确认 | 软停 | `none` | `query`（**见 D16**）|
| ③ | `A3.screening` | 初筛 · 导出裁决表 | 软停 | `none` | `screened` |
| ④ | `A4.data_extraction` | 数据提取核验 | **🔴 红线** | `extraction_review` | `extracted_rows` |
| ⤍ | `handoff_confirm` | A→B 块间交接 | 交接闸 | `—` | 无（仅批准/打回）|

---

## 3. 逐节点菜单细节

### ① A1 · 选题确认（PICOS）

**状态真源**：`stage_result`（`block_a.a1_topic_selection`，`:112`）+ `nha.gate="none"`

**菜单**

```
① 选题确认（PICOS）                          〔软停 · 需你拍板〕
   选题：奥希替尼 vs 化疗 一线 NSCLC
   P 非小细胞肺癌 ｜ I 奥希替尼 ｜ C 化疗 ｜ O （待填） ｜ S （待填）
   缺失维度：O · S
   注册库探针：CT.gov 相关试验 137 项 → 拥挤度 moderate
   检索范围：仅原始研究（= 源头排除综述）
   [1] 批准  [2] 改 PICOS 报告  [3] 改检索范围（纳入综述类）
```

> **A1 选项收敛（v1.1 裁定）**：不提供 `展开明细` / `跳过` / `打回`。A1 是"选题对不对 + 检索范围"的单点确认，其余入口属噪声。菜单窄化不影响状态机：`machine_options` 仍按软停语义派生（含 `skipped`）。

**面板 → 菜单映射**

| 工作台 panel | kind | 对话侧处置 |
|---|---|---|
| PICOS 推断（P/I/C/O/S） | `object` 只读 | **降级为 5 列一行**文本 |
| 缺失维度 | `json` | 行内拼接；空则省略该行 |
| 注册库探针 | `json` | **降级为"条数 + 拥挤度 + 风险提示"一行**（`report.feasibility`）|
| 是否纳入综述类文献 | `bool` | **保留为选项 [3]**（这是 A1 唯一真正需要拍的开关）|
| PICOS 报告 | `textarea` | **不内联展示**；`[2]` 触发 L2 → 回显全文供改 |

**注意**：`feasibility.risk_alert` 非空时（如"注册库仅 3 项，meta 效能可能不足"）必须在菜单上方以 `⚠️` 行置顶——这是选题阶段唯一的高价值预警。

---

### ② A2 · 检索策略与覆盖确认

**状态真源**：`nha.coverage`（`block_a._a2_coverage_nha`，`:2044`）

**菜单**

```
② 检索 · 覆盖确认                             〔软停 · 需你拍板〕
   合并 20 篇 ｜ 状态 ok ｜ OpenAlex 12 · EuropePMC 8 ｜ 撤稿 1 ｜ 沉默漏检：无
   检索上限：5/源（合并上限 = 源数 × 上限，本次 4 源 → 20）
   原始主题：奥希替尼 vs 化疗 NSCLC
   优化检索式：("osimertinib") AND ("NSCLC" OR "non-small cell lung cancer") AND (…)
   未翻译残留：无
   [1] 批准  [2] 改检索式  [3] 看各库明细
```

> **A2 选项收敛（v1.1 裁定）**：不提供 `跳过` / `打回`。**批准即直接产出检索结果 `xlsx`**
> （`A2_检索结果_<pid>.xlsx`，复用 ct-literature `export_xlsx` 模板、无裁决列）供人工审阅，
> 不必等到 A3 导出裁决表。告警口径同时收敛为**只看核心二源** OpenAlex + EuropePMC。

**字段映射**

| 菜单行 | 来源字段 | 变化处理 |
|---|---|---|
| 合并 N 篇 | `coverage.total` | — |
| 状态 | `coverage.search_status` | 由**核心二源**派生（`block_a.CORE_SOURCES`）；核心源齐 → `ok`。`≠ok` → 加 `⚠️` 行 |
| 各库条数 | `coverage.by_source`（dict） | 压成 `k=v · k=v` 一行；**核心源缺位 = 沉默漏检信号**（非核心源缺失不告警） |
| 撤稿 | `coverage.retracted` | 0 则省略 |
| 检索上限 | `coverage.max_results` | **必须标 "/源"**（见 §5 陷阱 A）|
| 原始主题 | `coverage.raw_topic` | — |
| 优化检索式 | `coverage.translated_query` | `[2]` 展开 L2 可改 |
| 未翻译残留 | `coverage.untranslated` | 非空 → `⚠️` 行"建议补全或换英文主题" |

**`[3] 看各库明细`** → 展开 `by_source` 完整 dicttable（对应用户 v0.2 里"选项必须穷举"原则）。

**沉默漏检是本节点唯一的存在理由**：核心二源（OpenAlex / EuropePMC）`search_status≠ok` 或 `by_source` 缺位 = 无 token 静默跳库 / skill 缺失。菜单必须把这两项**放在最显眼处**，不能折叠。

**告警收敛（v1.1 裁定）**：只有核心二源的缺位算异常。bioRxiv / arXiv / Semantic Scholar（无 key 时跳过）缺失属**已知常态**，不降级 `search_status`、不触发告警；原始 CLI 返回码另存 `coverage.cli_status` 供审计。

---

### ③ A3 · 初筛 · 导出裁决表（纯文件交接）

**状态真源**：`nha.summary` + `nha.decisions`（`block_a._a3_nha_from_screened`，`:587`）；规则裁决来自 ct-literature 的 `prisma_included` / `prisma_reason`

**菜单（对话内零逐条编辑入口）**

```
③ 初筛 · 导出裁决表                            〔软停 · 需你拍板〕
   去重 42 ｜ 规则纳入 14 ｜ 规则剔除 28（非原创类型 3 · 主题无关 25）
   类型（规则预填）：原创 36 · 综述/Meta 3 · 指南共识 2 · 研究方案 1 · 不确定 0
   规则来源：ct-literature PRISMA 确定性初筛 + classify_record（均已预填进导出表）
   ⬇ 导出 screening_v3.xlsx → 改「裁决」「理由」「文献类型确认」三列 → ⬆ 传回，即接 ④
   [1] 导出裁决表  [2] 传回裁决表  [3] 看统计  [4] 打回规则 → 回退 ②  [5] 跳过  [6] 打回
```

> 回传后回显带类型确认计数：
> `已应用 42 条（纳入 14 · 剔除 28 · 低置信 0）｜类型确认 39 篇（改判 2 / 未填 3）→ ④ 数据提取（🔴 红线）`

**关键设计点**

1. **导出表必须预填 `rule_decision`**（来自 `prisma_included`）。
   不预填 = 用户面对 42 行空白表 = 规则白跑。**这是 D12 从"可选"升为"必需"的原因。**
   现成接口：`block_a.export_screening_xlsx(session_path, out_path, lang)`（`:690`）
2. **回传校验失败一律不前进**：
   - 列完整（含「裁决」「理由」）
   - 行可对齐（DOI 优先，缺则归一化标题；`_match_keys` 多键任一命中）
   - `decision` ∈ {include, exclude, uncertain}
   - `exclude` 必填 `reason`
   - **不允许新增行**（防偷偷扩样）
   现成接口：`block_a.parse_screening_xlsx(xlsx_path, current_decisions)`（`:750`）→ 返回 `stats{matched, updated, unmatched, total}`
3. **汇总回显后直接进 A4**：
   `已应用 42 条（纳入 14 · 剔除 28 · 低置信 0）→ ④ 数据提取（🔴 红线）`
4. **不写** `pending_actions`（文件已回传，待办即清）。
5. **D8 仍需落地，但不再服务 A3**——只剩 A4 非 OA 补传一处，落地面变小。
6. **「文献类型确认」列（D17-A，已实施）**——导出表末尾追加一列，**规则预填**为显示标签
   （原创研究 / 综述·Meta / 指南·共识 / 研究方案 / 不确定），下拉可选，回传后成为**权威类型值**：

   | 回传情形 | 结果 |
   |---|---|
   | 单元格非空 | `doc_type` = 该值，`doc_type_source="human"`，`doc_type_confirmed=True` |
   | 与规则预填不同 | 记 `doc_type_changed=True`（可审计"改判几篇"），并留 `doc_type_rule` 对照 |
   | 留空 | 视为未确认 → 沿用规则预填，`doc_type_source="rule"`（不拦流程，但计数可见）|
   | 取值非法 | **报错不前进**（与裁决列同口径），并指出具体行 |

   规则预填是**单一真源复用**：直接调 ct-literature `doc_type_filter.classify_record`
   （pubType 元数据 + 声明短语 + head 词典三通道打分），不是 meta 里再写一套判定；
   该模块不可用时回退本技能既有的 `is_likely_review()`，语义同族。
7. **为何列名不叫「类型」**：Works 表已有一列「类型」（`col.type`，ct-literature 的元数据原始
   类型，只读）。确认值必须与之**分列**，否则"库方标注"与"人工确认"会混为一谈、无法审计。

**副作用（正面的）**：A3 本来就是工作台侧 ⬇⬆ 通道，对话侧走同一套 `export_/parse_screening_xlsx` → **双端行为完全一致，漂移风险归零**。所以 A3 是四个节点里实现成本最低的一个——**不用新写逻辑，只需接线**。

---

### ④ A4 · 数据提取核验（🔴 红线）

**状态真源**：`stage.n_screened / n_downloaded / n_extracted` + `a4documents` 面板 + `nha.gate="extraction_review"`（`block_a.py:1896`）

**菜单**

```
④ 数据提取核验                                 〔🔴 红线 · 必须你放行〕
   初筛通过 14 ｜ 已下载全文 11 ｜ 已抽取 9（含 2×2 表 9）
   待补传 PDF：3 篇（非 OA / 付费墙）→ 影响纳入量，请处置
   类型（只读 A3 确认值）：综述/Meta 1 篇 → 抽取 0 行属正常（review_note）
   [1] 批准（放行 → Block B）  [2] 上传补 PDF  [3] 修订 2×2 表  [4] 回退 ③  [5] 打回
   ⚠️ 本节点无「跳过」——红线闸不接受 skipped
```

**四条硬约束**

1. **无"跳过"项**。选项集由 `_REDLINE_GATES` 派生过滤（`fullflow.py:567`）；即使 LLM 误造"跳过"，`_validate_decision` 也会拒。**双保险，不靠提示词**。
1b. **类型一律只读 A3 确认值**（D17-A，已实施）。`a4_stream` 经唯一入口
   `block_a._read_doc_type(sc, study)` 取值：`doc_type` = A3 裁决表确认值（人工优先）；
   抽取层自己探测到的类型记为 `doc_type_detected`，**只在与确认值不一致时给 `doc_type_notice`**
   （"以 A3 确认为准，如需改判请回到 ③ 初筛"）。`review_note` 也由确认值驱动。
   per_doc 的 `skip / needs_upload / deferred` 占位分支同样带该字段——三处读到同一值，不再出现"有的行有类型、有的没有"。
   **要改类型只能回 ③ 改裁决表**，A4 无改判入口。
2. **不做下载前类型甄别**（2026-09-10 起）。
   `_a4_fetch_one`（`block_a.py:1200`）已删类型门；`_skip_page_screen` 已从代码路径归零。行为变化：
   - 人工纳入的综述**会进抽取**（多为 0 行），带 `review_note` 软提示
   - 概览的 `excluded_review` 计数**归零**
   - **红利**：原"回传必须置 `_skip_page_screen`"那条硬约束**从根上消失**——门没了，豁免补丁就是死代码。
3. **`[2] 上传补 PDF` 允许且在对话内收文件/路径**（= D10 建议"允许"）。
   - 理由：这是 A4 **最高频的阻塞点**（非 OA / 反爬 / 付费墙 → `needs_upload`）
   - 简化口径：只收文件/路径 → 按 DOI/标题**自动匹配到具体篇目** → **只问未匹配项**
   - 抽取与核验仍由脚本 + 人工完成，红线不松
   - 待办承载：非 OA 未补传时写 `pending_actions`，**闸位保持，`approve` 被拒**（D8）

**A4 → B1 交接闸**：`[1] 批准` 后进入 `handoff_confirm`，**只收 approved / rejected**，菜单为 2 项（可用 `AskUserQuestion` 卡片）。

---

## 4. 与工作台的差异处置（你上一轮提的点，落到 A 阶段）

| 工作台操作 | 对话侧 | 依据 |
|---|---|---|
| A3 逐条裁决（`rowlist`，42 行） | **整节点跳过·转出** → 文件交接 | 四问判定 Q2（>10 条逐条编辑）|
| A3 点行展开详情（18 个字段） | 不提供；`[3] 看统计` 只给汇总 | Q1（需视觉/空间）|
| A2 各库 dicttable | 压一行；`[3]` 可展开 | ② 降级简化 |
| A1 PICOS 只读面板 | 5 列一行 | ② 降级简化 |
| A4 逐篇「提取 ↔ 原文页对应」 | **不迁移**；重度核验留 `/workbench` 逃生门 | Q1 |
| A4 上传 PDF | **迁移**（收文件/路径 + 自动匹配） | ① 原生迁移 |
| 选单确认（按钮） | **选项穷举编号**；🔴 节点选项由代码过滤 | §1.2 规则 2 |

**`defer` ≠ `skip`**（沿用 v0.2 定义，A 阶段只有 A4 用得上）：

| | `skip` | `defer` |
|---|---|---|
| 含义 | 本会话不再停靠，按默认放行 | 人工动作**未完成**，流程**不得前进** |
| 适用 | 仅软停（A1/A2/A3） | 任意节点，尤其 🔴（A4 补传） |
| 审计 | 写 `human_decisions` | **不写**，改写 `pending_actions` |
| 效果 | 下游继续跑 | 闸位保持，`approve` 被拒 |

---

## 5. 实现时会踩的坑（实测得到，非推断）

**陷阱 A · `--max` 是每源上限，不是合并上限**
`--max 5` × 4 源 = 20 篇。工作台 A2 面板现标"检索上限 5"是**误导**；CCM 菜单必须写 "5/源（合并上限 = 源数 × 上限）"。

**陷阱 B · `_read_literature_dir` 是主路径，不是兜底**
stdout 只吐 NDJSON 日志，数据全在 `.merged.json`，所以 `_extract_studies` **恒为 0**。源码注释里"回退读取"的措辞是维护陷阱——后人照着删掉这分支，A2 就真废了。**建议改注释/命名**（已列入 v0.4 修订清单）。

**陷阱 C · `arg_map` 布尔格式化只认 include/exclude 命名**
`--original-only` 是 `store_true`，naive 传参会生成 `--original-only True` 让 argparse 报错。需给 `arg_map` 加 `bool_true` 语义。

**陷阱 D · A2 timeout 写死 120s**
A2 若要前置下载（`--download-pdf`，= D11），必然超时。须放宽 + 走 `--progress` 流式（`on_line` 路径已有）。

**陷阱 E · `_a4_extract_pdf` 元数不对称 —— 下载路径静默失败（2026-09-10 已修）**

`_a4_extract_pdf` 自 v0.3 起返回 **6 元组**（末位新增 `doc_info`），三个调用点里**只有下载路径没跟着改**：

| 调用点 | 位置 | 修复前 |
|---|---|---|
| 上传快速通道（人工传 PDF） | `block_a.py:1013` | 6 元组 ✅ |
| **下载路径（`_a4_fetch_one`）** | `block_a.py:1248` | **5 元组 ❌** |
| 缓存分支（`a4_stream`） | `block_a.py:1420` | 6 元组 ✅ |

**后果**：每次「下载成功 → 抽取」都抛 `ValueError: too many values to unpack (expected 5, got 6)`，
被 `a4_stream` 的 `except Exception`（`:1443`）兜成 `gate=worker_error` / `status=needs_upload`。
**症状极具迷惑性**：首轮下载全篇显示"待补传 PDF"，**重跑却正常**（因为 PDF 已落盘 → 走缓存分支，那条是 6 元组）。
用户会以为是 OA 覆盖问题，实际是解包元数不对称。

**本机为活跃 bug**：`pdfplumber` 存在 → `pdf_extractor` 可导入（`a4_stream:1331`）→ 不走 `is None` 早返回 → 必然命中。
（注：我此前验证「类型门已摘」时传的是 `pdf_extractor=None`，在 `:1244` 早返回，**恰好绕过了这个 bug**——所以那次验证没能发现它。）

**修法**：`:1252` 补齐 `doc_info` 并透出 `doc_type` 作标注（不作门），与另外两个调用点对齐。
**实测**：修复后 `event=extracted / status=extracted / gate=pass_downloaded / n_rows=1 / n_tworows=1`。
既有测试 `tests/test_a4_b1_handoff.py` 除 R 相关项外逐条一致，**无回归**。

**陷阱 F · 本机缺 PyMuPDF（`fitz` / `pymupdf` 均无）—— A4 抽取链路的环境前提**

| 依赖 | 本机状态 | 影响 |
|---|---|---|
| `pdfplumber` | ✅ 在 | T1 有框表通道可用 |
| `fitz`（PyMuPDF）| ❌ **缺失**（`pymupdf` 亦无）| `classify_pdf()` 与 `parse_pdf()` 都依赖它 |

`classify_pdf` 的 `import fitz` 在 `try` **之外**，此前会直接抛出并被 `_a4_extract_pdf` 的
`except` 兜成 `gate=extract_fail` → 表现为"每篇都抽取失败"。本轮改动已把 `classify_pdf`
的调用包进 `try/except` 降级为 `unknown`，**但 `parse_pdf` 仍硬依赖 fitz** —— 所以
**在本机 A4 仍无法真正抽取**，需补装 PyMuPDF 才能端到端跑通（`pip install pymupdf`）。

按 SOUL 的 Python 三级策略，这属于「Anaconda base 缺包 → 直接装进 base」一档，
**建议补装，但未动手**（不在本轮"类型判断"的改动范围内）。

**陷阱 G · 裁决表的 Works 表没有 DOI 列 —— 回传实际按「标题」匹配（2026-09-10 已修）**

**原状**：`_WORKS_COLS`（ct-literature `export_xlsx.py`）是
`类型 / 研究类型 / 年份 / 期刊 / 作者 / 标题 / 摘要 / 被引 / 安全性 / OA链接 / PDF 本地路径`——**无 DOI 列**。

| 端 | 建键方式 | 实际键 |
|---|---|---|
| 导出（写值） | `_norm_doi(w["doi"])` | **DOI** |
| 回传（读值） | 表内无 DOI 列 → 只剩 `_norm_title(标题)` | **标题** |

能工作是因为 `_match_keys(doi, title)` 生成**多键**、回传侧同时产出标题键，而匹配发生在
**基线 decisions**（有 DOI 也有标题）上——**这是巧合的容错，不是设计**：一旦两端标题
归一化口径分叉，匹配会静默降为 0 且不报错。

**修法（两步，均已实施）**

1. **补列**：`_WORKS_COLS` 在「期刊」之后插入 `("doi", "col.doi", 30)`（i18n 键 `col.doi`
   早已存在，中英均为「DOI」）。**纯文本写入**，不加超链接——① 便于人工复制核对；
   ② 回传端按文本读，不受超链接结构影响（标题单元格仍有 doi.org 超链可点）。
   列序插入位置安全：`parse_screening_xlsx` **按列名定位**（`_hdr_idx`），不按位置。
2. **兜底拦截**：`parse_screening_xlsx` 新增——`matched == 0 && 基线非空` → 抛
   `ValueError`，**不前进**。同时在 `stats` 增 `doi_column`，工作台日志显式打印
   「匹配键：DOI 列 有/无」——旧模板无此列时回退标题匹配，**可见**而非猜测。

**验证**（`tests/test_a3_doc_type_confirm.py`，28/28 PASS）

| 断言 | 结果 |
|---|---|
| 表头含 DOI 列、逐行值与 works 一致 | PASS（`['类型','研究类型','年份','期刊','DOI','作者']`）|
| **人工改动标题后仍 4/4 匹配**（DOI 键生效）| PASS |
| 标题改动行的裁决仍正确回写 | PASS |
| 上传他会话的表 → 零匹配**抛错拦截** | PASS |
| 不传 `decision_extra` 时导出器表头仍以「理由」结尾（向后兼容）| PASS |

**扩展位在 ct-literature 侧，通用且向后兼容（已实施）**

「文献类型确认」列不是 meta 硬编码进去的，而是给 ct-literature `export_xlsx` 加了通用能力：
`export_workbook(..., decision_extra=[{key,label,width,options,error_message}])` →
`build_works` → `_write_works_table` 追加列 + 下拉校验；`_build_decision_map(decisions, extra_keys)`
改为携带附加键。**不传 `decision_extra` 时行为与旧版逐字节一致**（已实测表头仍以「理由」结尾）。

---

## 6. A 阶段决策点现状

| ID | 决策 | 状态 |
|---|---|---|
| D9 | A3 对话内逐条裁决 | ✅ **已定**：不逐条，纯文件交接 |
| D12 | A3 采信 ct-literature `prisma` | ✅ **已定**：是，且必需（导出表须预填规则裁决）|
| D13 | A2/A1 解释器路径 bug | ✅ **已实施** + 端到端回归通过 |
| A4 直下 | 100% 按清单下载，不判断不改 | ✅ **已实施** + 编译/单测/人造综述验证通过 |
| **A4 元数 bug** | `_a4_extract_pdf` 下载路径 5 元组解包（见 §5 陷阱 E）| ✅ **本轮已修** + 实跑验证 `status=extracted` |
| **D15** | 抽取层类型门（`pdf_extractor` 规律 R1）| ✅ **已定并实施**：全链路不再判类型，`type_notice` 降为提示 |
| **D17** | 「人工确认类型」的落点 | ✅ **已定（方案 A）并实施**：A3 导出表增「文献类型确认」列，规则预填 → 人工确认 → A4 只读；回归 `tests/test_a3_doc_type_confirm.py` 22/22 |
| **D10** | A4 是否允许对话内收文件/路径 | ⏳ 建议**允许**（菜单已按"允许"写）|
| **D11** | A2 是否前置下载（`--download-pdf`） | ⏳ 待定（须配 timeout 放宽 + 流式）|
| **D14** | A1 注册库探针（`ct-registry`）是否在对话侧展示 | ⏳ 建议**展示**（一行条数 + 拥挤度；A1 唯一高价值预警）|
| **D16** | **A2「改检索式」的语义**（新发现，见下） | ⏳ 需你定 |

### D16 · A2 的 revision 是个悬空接缝（新发现）

`fullflow.py:17-19` 的模块注释写得很直白：

> *"revision 走输入参数的接缝**目前只有 A4**（`extracted_rows` → Block B studies）；其余阶段的 revision 为记录后的 `stage_result` 事后补丁（下游已按原值计算）"*

而 `EDITABLE_KEYS`（`:59`）里**根本没有 `A2.literature_search`**：

| stage_id | `EDITABLE_KEYS` 是否收录 |
|---|---|
| `A1.topic_selection` | ✅ `["report", "include_reviews"]` |
| **`A2.literature_search`** | ❌ **缺失** |
| `A3.screening` | ✅ `["screened"]` |
| `A4.data_extraction` | ✅ `["extracted_rows"]` |

**后果**：工作台 A2 面板声明了 `revision_key: "query"` 和可编辑 textarea，但 `fullflow.py:332` 用 `EDITABLE_KEYS.get(sid, [])` 组装 `editable_payload` → **A2 的 editable_payload 恒为空**。

**这不是 CCM 引入的，是既有接缝不闭合。** 但对 CCM 是**必须回答**的问题：A2 菜单上的 `[2] 改检索式` 点了之后，究竟：

- **(a)** 只写补丁、不重跑 → 改了等于白改（下游已按原式检索完），**菜单里就不该有这个选项**
- **(b)** 触发 **revise + rewind 重跑 A2** → 语义正确，但需要 `EDITABLE_KEYS["A2.literature_search"] = ["query"]` 并让 A2 支持重入
- **(c)** 对话侧不提供改检索式，改为 `[2] 打回并重述需求` → 由 agent 重新组检索式再跑

**我的建议：(b)**。改检索式是 A2 最自然的修订动作，做成 (a) 就是假的交互；(c) 则丢掉了"直接改布尔式"的能力。代价是 `EDITABLE_KEYS` 加一行 + A2 确认支持 rewind 重入——量不大，但**我先不动，等你定**。

### D15 · 抽取层类型门 —— ✅ **已定并实施（2026-09-10）**

**用户裁定（规则化，非选项）**：
> 「人工确认文献类型后，一律不再做类型判断。如果需要修改类型，也是要人工给出确认或者发出提示词。」

即 **类型一经人工确认（A3 裁决表），从解析层到闸位层的任何一环都不得再依据类型做判断**；
类型只能作**标注/提示**。改类型的唯一合法路径 = 人工确认 / 人工发起。

**实施改动（5 处）**

| # | 位置 | 改动 |
|---|---|---|
| 1 | `pdf_extractor.extract()` | 删掉规律 R1 的**短路返回**。`classify_pdf` 保留但只作标注；探测本身加 `try/except` 降级（缺 PyMuPDF 也不再阻断抽取）|
| 2 | `pdf_extractor.extract()` 返回 | `review_summary` 增 `excluded: False`（恒）、`doc_type`、`signals`、**`type_notice`**（给闸位的人读提示）|
| 3 | `block_a._a4_extract_pdf` | `doc_info["excluded"]` 恒 False，新增 `type_notice` 透传 |
| 4 | `block_a` 上传快速通道 | 删掉 `if doc_info.get("excluded")` 分支 → 一律 `status="extracted"`；无错误时把 `type_notice` 放进 `reason` 作提示；`included` 恒 True |
| 5 | `block_a.a4_stream` | 删掉缓存分支的 `doc_info.excluded` 判断、删掉 `elif out["status"] == "excluded_review"` 死分支；`per_doc` 增 `doc_type`，`is_review` 改为纯标注，`included` 恒 True |

**验证（4 项实测）**

| 测试 | 结果 |
|---|---|
| 类型=review 时 `extract()` 是否仍走到 `parse_pdf`（哨兵法） | **通过** —— 不再短路 |
| `classify_pdf` 抛 `ModuleNotFoundError`（缺 fitz）是否阻断抽取 | **通过** —— 吞掉并降级为 unknown |
| `_a4_extract_pdf` 的 `doc_info.excluded` | **恒 False**，`type_notice` 正常透出 |
| 综述 PDF 走下载路径 | `event=extracted / status=extracted / gate=pass_downloaded / doc_type=review`，**未被排除** |
| `tests/test_a4_b1_handoff.py` | A4/A3 段全 PASS，与改动前逐条一致（FAIL 项仍为 R 缺失） |

**残留的类型判断（合规，不越界）**

| 位置 | 为何保留 |
|---|---|
| A3 的 `is_likely_review()` review-guard（预填 `rule_decision`）| 处于**人工确认之前**，是给裁决表的**预填建议**，人工可改 |
| `a4_stream` 的 `review_note` / `is_review`、工作台 `🔍 疑似综述` 徽标 | 纯**提示**（正是用户所说"发出提示词"），不做任何排除 |

---

#### 附：D15 裁定前的分析（保留备查）

**原矛盾**：首轮（下载路径）与重跑（缓存分支）对同一篇综述给出两种结论。

修掉陷阱 E 之后，A4 出现一条**同一篇 PDF 首轮与重跑结论不同**的路径：

| 路径 | 是否检查 `doc_info.excluded` | 综述/指南 PDF 的结局 |
|---|---|---|
| **下载路径**（`_a4_fetch_one`，首轮）| 否（本次已按你的决策摘除）| `extracted`，0 行，带 `doc_type` 标注 |
| **缓存分支**（`a4_stream:1428`，重跑）| **是** | `excluded_review`，`gate=type_screen` |

即：**同一篇人工纳入的综述，首轮"抽取成功 0 行"，重跑变"类型排除"**。这不是下载门（已摘），是 `pdf_extractor.extract()` 内部的规律 R1（`pdf_extractor.py:1200-1217`）经缓存分支二次表述。

三个选项：

| 选项 | 做法 | 代价 |
|---|---|---|
| **(a) 保持一致——两处都不判类型**（建议）| 删掉 `a4_stream:1428-1437` 的 `doc_info.excluded` 分支，类型统一降为 `doc_type` 标注 | 综述转述的二手数据理论上可能入池（但 0 行概率高 + `review_note` 提示 + 🔴 人工闸可见）|
| (b) 保持一致——两处都判 | 把下载路径也加回 excluded 分支 | **与你"A4 直下、不判断"的决策直接冲突**，且 `_skip_page_screen` 类豁免补丁会复活 |
| (c) 维持现状 | 首轮/重跑不一致 | 用户看到同一篇两种结论，无法解释 |

**(a) 与你的决策同向**：你说过"A4 的下载 100% 按照列表做"，那么"抽取层再判一次类型"就是同一类越权。且 🔴 闸位本身就要人看 `review_note`，不需要靠自动排除兜底。

→ **结论：用户裁定为 (a) 的加强版**——不止两处一致，而是**全链路一律不判**（见上）。

### D17 · 「人工确认类型」的落点 —— ✅ **用户选定方案 A，已实施**

| 方案 | 状态 |
|---|---|
| **(A) A3 导出表加「文献类型确认」列** | ✅ **选定并实施**（见 §3③ 第 6 条、§3④ 约束 1b、§5 陷阱 G）|
| (B) 维持现状（纳入/剔除即事实确认）| 未选：类型不是一等字段，改类型无落点、不可审计 |
| (C) A4 逐篇类型下拉 | 未选：与"确认在 A3"原则冲突，且在红线闸上扩编辑面 |

**实现落点（4 处，均已改）**

| 文件 | 改动 |
|---|---|
| `block_a.py` | 新增 `DOC_TYPE_*` 词表 + `_norm_doc_type()` + `rule_doc_type()`（单一真源复用 ct-literature `classify_record`）+ `_doc_type_cell_for_export()` + `_read_doc_type()`；`a3_screening` / `_a3_decision_row` / `_a3_nha_from_screened` 携带类型与分布；`export_screening_xlsx` 预填并传 `decision_extra`；`parse_screening_xlsx` 读取+校验+记 `doc_type_source`/`doc_type_rule`/`doc_type_changed`；`a4_stream` 全量改只读 |
| `ct-literature/scripts/export_xlsx.py` | 通用 `decision_extra` 附加列能力（`export_workbook` / `build_works` / `_write_works_table` / `_build_decision_map`）+ i18n key `col.doc_type_confirmed` |
| `workbench/form_schema.py` | A3 / A4 的 `intro` 写明"类型确认列 + A4 只读" |
| `workbench/workbench.html` | 导出/上传的日志补「文献类型确认」与"确认/改判/未填"计数 |

**回归证据**：`tests/test_a3_doc_type_confirm.py` **22/22 PASS**（规则预填 4 类 → 导出预填 → 人工改判/留空 → 非法值拦截 → A4 只读 + 不一致提示 → 导出器向后兼容）。

---

## 7. 落地清单（A 阶段部分）

| 新增/改动 | 内容 |
|---|---|
| **新增** `scripts/flow_menu.py` | 确定性 render / status / decide / rewind；A2 `gate=none` 与 A4 `extraction_review` 从 `fullflow_session` 读，选项集由 `_REDLINE_GATES` 过滤 |
| **新增** `references/conversation_flow_menu.md` | 本规格的规范版（含 i18n key）|
| **新增** 回显块 | `## 当前流程设定 / Current pipeline settings:` |
| **小改** `form_schema.py` | 加 `menu_for()` 投影 → 从同一 `SCHEMA` 派生对话侧菜单 |
| **小改** `interactive_menu.md` / `speed-discipline.md` / `SKILL.md` | 挂载 CCM，声明"纯算数请求不出 CCM" |
| **接线**（非新写）| `export_screening_xlsx` / `parse_screening_xlsx` 已在 `block_a` 就绪 |
| **已实施** 类型确认列 | `decision_extra` 扩展位 + 规则预填 + 回传校验 + A4 只读（见 §6 D17）|
| **待定** `fullflow.py` | `EDITABLE_KEYS` 是否补 `A2.literature_search`（= D16）|
| **待定** Works 表 DOI 列 | 回传目前靠标题键命中（§5 陷阱 G），是否补列需你定 |
| **测试** `tests/` | 4 节点 × 2 语言无缺键；A4 菜单**不含** skip；A1/A2/A3 菜单**含** skip；类型确认链（已有 `test_a3_doc_type_confirm.py`）|

---

## 8. 验收标准（A 阶段）

- **AC-A1** 停在 A4 时菜单**不出现**"跳过"，且 `action=skipped` 被 `_validate_decision` 拒
- **AC-A2** 停在 A1/A2/A3 时菜单**出现**"跳过"（软停语义）
- **AC-A3** A3 菜单**无任何逐条编辑入口**；导出/回传走 `export_/parse_screening_xlsx`
- **AC-A4** A3 导出表**预填** `rule_decision`（取自 `prisma_included`）
- **AC-A5** A3 回传校验失败（缺列 / 行不可对齐 / decision 非法 / exclude 缺 reason / 新增行）**不前进**
- **AC-A6** A2 菜单的检索上限**标注 "/源"**
- **AC-A7** 停在 A2 且 `search_status≠ok` 或 `by_source` 缺库时，菜单出现 `⚠️ 沉默漏检` 行
- **AC-A8** A4 非 OA 未补传时写 `pending_actions`，`approve` 被拒
- **AC-A9** 12 节点 × zh/en 菜单渲染无缺键
- **AC-A10** A4 对任意类型（综述/指南/协议）PDF 均返回 `extracted`（或明确的失败态），**不存在** `excluded_review` 状态
- **AC-A11**（D17-A）A3 导出表含「文献类型确认」列，且**每行均已按规则预填**（不为空）；下拉可选五值
- **AC-A12**（D17-A）回传后类型成为权威值：非空 → `doc_type_source="human"`；留空 → 沿用规则值并计 `type_blank`；取值非法 → **报错不前进**
- **AC-A13**（D17-A）A4 **全程不调用类型判定**：`per_doc.doc_type` 恒等于 A3 确认值；抽取层探测仅在 `doc_type_notice` 中提示，`review_note` 由确认值驱动；`skip/needs_upload/deferred` 占位行同样带类型
- **AC-A11** `pdf_extractor.extract()` 对 review/guideline/protocol **不短路**；`classify_pdf` 失败（如缺 PyMuPDF）**不阻断**抽取
- **AC-A12** 同一篇 PDF 首轮（下载路径）与重跑（缓存分支）结论**一致**（`doc_info.excluded` 恒 False）
- **AC-A13** 类型信息仅以 `doc_type` / `type_notice` / `review_note` 形式出现，**无任何分支据其改变状态或计数**
