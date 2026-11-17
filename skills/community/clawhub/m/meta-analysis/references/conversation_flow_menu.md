# meta-analysis · CCM 对话上下文菜单（Converse Context Menu）· 规范 v1.0

> ⛔ **[已停用 2026-09-27，用户裁定]** CCM 不再作为聊天侧呈现方式。技能的执行面收敛为两种：
> ① 网页应用（https://meta.app.workbuddy.host/，菜单式引导）② 上下文对话（agent 以自然语言
> 叙述当前阶段并向用户开放提问，批准/修订/回退由用户口头表达）。`flow_menu.py` /
> `flow_menu_widget.py` 降级为开发者 CLI 工具，状态机本身不变。**本文仅作设计归档保留**，
> 供日后重新启用时参考——不得在当前聊天行为中执行。见 SKILL.md §2.4 CCM DISABLED 横幅。
>
> **状态（历史）：已实现（2026-09-10）。** 设计与决策过程归档在 `references/design/ccm/`
> （`10_A_stage_menu_spec_v1.0.md` 是设计稿；**本文是落地后的规范版**，二者冲突以本文为准）。
> **代码**：`scripts/flow_menu.py` · **回归**：`tests/test_flow_menu.py`（175 PASS / 0 FAIL）。
> **范围**：全流程轨道的 `A1 → A2〔文献集：检索+初筛〕 → A4 →[交接]→ B1`，以及 11 节点导航条；
> B/C 节点走同一套投影（`nodes` 子命令），逐节点的对话菜单细节后续按需补。
>
> **2026-09-10 变更（A2/A3 合并）**：原独立节点 `A3.screening` 已并入 `A2.literature_search`
> （对话侧标题「文献集 · 检索 + 初筛（一张表）」）。A 阶段停靠点由 4 个收敛为 3 个：
> `A1 → A2(合并) → A4`。节点数（导航条）与 B/C 无关，仍为 11。
>
> **权威菜单逻辑参考**：各停靠点菜单的完整结构、摘要行、action 派生口径与已知缺口，见 `references/menu_logic_reference.md`（本文仅描述规范与决策）。

---

## 0. 它解决什么问题

工作台（`adapters/workbench/`）已有完整的 11 节点渲染契约（`form_schema.py`）与 HITL 状态机
（`fullflow.py`），但**对话侧没有菜单**：每轮展示什么、闸位有哪些选项，全靠 LLM 即兴，
同一节点两次渲染可能不一致。

CCM 给**同一套 schema 加一层「对话投影」**，不新建第二套流程定义。
产物是 `scripts/flow_menu.py`：**菜单由代码产出、LLM 只转述**。

触发时机：全流程轨道内的**每一次停靠**（软停 / 红线闸 / 块间交接）。

---

## 1. 六条硬约束（违反即视为实现缺陷）

| # | 约束 | 落地位置 |
|---|---|---|
| **R1** | 状态真源只有一个：复用 `fullflow_session_ff-*.json`；渲染**只读**（除 `decide` / `rewind`） | 回归 [8] 字节级只读断言 |
| **R2** | 菜单由代码产出、LLM 只转述——同输入同输出 | 回归 [9] 两次渲染字节一致 |
| **R3** | 🔴 选项由 `cc._REDLINE_GATES` 派生过滤，**不硬编码第二份清单** | `machine_options()`；回归 [1][2] |
| **R4** | 可编辑键由 `fullflow.EDITABLE_KEYS` 派生，**不自行声明**；未收录的修订项显式标注为不可用（不静默丢弃） | `_filter_options()`；回归 [4] |
| **R5** | 当前节点由 cursor / 信封派生，**不重写 `workbench.html` 的 JS 逻辑**；回退候选集从信封 stage 序列派生 | `_stage_entries()` / `rewind_candidates()`；回归 [11] |
| **R6** | **纯算数请求不出现 CCM**（「合并这 5 项 OR」/ NMA / 敏感性分析等），保住「描述即执行」卖点 | 不调用即满足；见 §7 |

---

## 2. 三层菜单

| 层 | 名称 | 内容 | 出现时机 |
|---|---|---|---|
| **L0** | 上下文导航条 | 11 节点压一行，`✓` 已完成 / `▶` 当前 / `○` 未达 | **每轮必贴**（全流程轨道内） |
| **L1** | 节点菜单 | 节点头（标题 · 闸类）+ 摘要行 + ⚠️ 预警 + **穷举编号选项** | 停靠节点自动贴；非停靠节点用 `nodes` 查询 |
| **L2** | 字段菜单 | 该节点 `EDITABLE_KEYS` 的键 + 全局指令 | 用户选「改 X」后展开 |

**L0 样例**（停在 A2「文献集」）：

```
## 当前流程设定 / Current pipeline settings:
📍 全流程  │  A: ①选题 ✓  ②文献集 ▶  ③数据提取 ○  │  B: ④合并计算 ○  ⑤GRADE ○  ⑥过度声明 ○  ⑦质量门 ○  │  C: ⑧初稿 ○  ⑨AI 评审 ○  ⑩参考核验 ○  ⑪投稿前 QA ○
```

**回显块前缀固定 `## 当前流程设定 / Current pipeline settings:`**，与计算轨道的
`## 当前分析设定:` 分开、互不覆盖。

### 2.1 渲染规则

1. **选项必须穷举编号**——禁止"你要继续吗？"这类开放问法；用户看不到 GUI 上"有哪些按钮"。
2. **选项集由代码派生**，不由 LLM 即兴：decision 选项 ⊆ `machine_options()`，编号从 1 连续。
3. **≤3 选项** 可用 `AskUserQuestion` 卡片；**≥4 选项** 用编号文本菜单（合并后 A 阶段：A1/A2 各 4 项、A4 5 项）。
4. `--json` 输出为纯数据（供程序消费）；文本输出可直接贴给用户。

---

## 3. 状态真源映射（对话侧只读，不另起一份）

| 菜单要显示的东西 | 真源 |
|---|---|
| 当前节点 / 闸类 | `last_view.fullflow.await.kind` / `.stage_id`；缺失时从信封 `status=="await_human"` 兜底 |
| 是否红线 | `fullflow.STAGE_TO_GATE[sid] ∈ cc._REDLINE_GATES` —— **不看 `await.gate`**（`run_fastpath` 会把它写成 `True`，不可靠） |
| 合法 action 集 | `machine_options()`：红线 → `approved/revised/rejected`；软停 → `+skipped`；交接 → `approved/rejected` |
| 可编辑键 | `fullflow.EDITABLE_KEYS[sid]` |
| 节点标题 | zh = `form_schema.SCHEMA[sid].title`；en = `form_schema.title_for(sid,"en")`（新增 `TITLE_EN`，纯增量） |
| 各节点摘要 | `信封 stages[i].stage_result` + `next_human_action` |
| 11 节点进度 | 信封 stage 序列（与 `workbench/server.build_state` 的 `progress` 同源同轴） |
| 文献类型（权威值） | `nha.summary.doc_type_dist`（A2 文献集，原 A3）/ `per_doc[i].doc_type`（A4，只读）|

---

## 4. A 阶段逐节点菜单

```
① 选题确认 ──② 文献集（检索·覆盖确认 + 初筛·合并表）──③ 数据提取核验══►[块间交接]══► B1
   soft                    soft                          🔴 redline        approved/rejected
  gate=none               gate=none                      gate=extraction_review   （仅二选）
```

> **2026-09-10 合并**：原 `② 检索·覆盖确认` 与 `③ 初筛·导出裁决表` 两个软停节点合并为单节点
> `② 文献集`——一次软停内完成「检索覆盖确认 + 去重/规则初筛」，只产出一张合并表。A 阶段
> 停靠点由 4 → 3。旧会话的独立 `A3.screening` 阶段仍可被读回（兼容），但不再新发。

| # | stage_id | 闸 | `gate` | 可编辑键 | 跳过后 |
|---|---|---|---|---|---|
| ① | `A1.topic_selection` | 软停 | `none` | `report` · `include_reviews` · `sources` | 菜单无 skip（机器可） |
| ② | `A2.literature_search` | 软停 | `none` | `query` · `screened`（**对话内无逐条入口**）| 菜单无 skip（机器可） |
| ③ | `A4.data_extraction` | **🔴 红线** | `extraction_review` | `extracted_rows` | **无 skip** |
| ⤍ | `handoff_confirm` | 交接闸 | — | 无 | 仅批准/打回 |

### ① A1 · 选题确认（PICOS）

```
选题确认（PICOS）                             〔软停 · 需你拍板〕
   ⚠️ 方向空白，可能原始研究极少，预期可纳入研究数量不足（meta 至少 k≥2）。
   奥希替尼 vs 化疗 一线 NSCLC
   P 非小细胞肺癌 ｜ I 奥希替尼 ｜ C 化疗 ｜ O - ｜ S -
   缺失维度：O · S
   注册库探针：ok → 相关试验 137 项 → 拥挤度 moderate
   检索范围：仅原始研究（= 源头排除综述） ｜ 数据源：OpenAlex、EuropePMC
   [1] 批准  [2] 改 PICOS 报告  [3] 改检索范围（综述 + 数据源）  [4] 帮助选题（可行性速览）
```

- `feasibility.risk_alert` 非空时**置顶**为 ⚠️ 行——这是选题阶段唯一的高价值预警。
- 注册库探针**降级为一行**（条数 + 拥挤度 + 状态）；PICOS 报告**不内联**，`[2]` 才展开。
- **A1 收敛为「批准 / 修订 / 可行性速览」三态**：不提供 `展开明细` / `跳过` / `打回` / `上传`（历史 [4][5][6] 已删；「上传裁决表」入口于 2026-09-11 用户裁定**移出 A1**、仅保留在 A2 合并节点）。理由：A1 唯一真正要拍的是"选题对不对 + 检索范围"，其余入口在对话里只增加噪声。状态机侧的 `machine_options` 仍按软停语义派生（含 `skipped`），菜单只是窄化展示，契约未变。
- **选题菜单先出现、尚无有效选题时（2026-09-11 逻辑修正）**：菜单**只渲染提示行（hint）**——「请先输入选题（含 PICOS 更佳），直接发主题文字即可；选题确认后菜单才会给出批准 / 改 PICOS / 改检索范围 / 可行性速览」，并附空 PICOS 模板；**不渲染任何可操作选项**（批准 / 修订 / 可行性速览在选题缺失时均无意义）。判定靠 `_a1_topic_missing`（空或占位符「（新课题 — 在 A1 设定主题）」即视为缺失）。用户发来主题文字、选题确认后，菜单才重新给出 `[1][2][3][4]`。这样就避免了"还没选题就出现批准选项"的怪异状态。
- **`[4] 帮助选题（可行性速览）`（2026-09-11 新增，辅助动作）**：选题阶段即可**按需触发一次注册库探针**，不跑整条检索管线，先看拥挤度 / 证据量 / 风险预警，再决定是否放行 ②。语义：agent 调 `python flow_menu.py probe --apply` → `a1_feasibility_probe` 跑 `block_a.a1_registry_check` 并把 `registry_probe` / `feasibility` 写回 A1 的 `stage_result`，菜单摘要随即多出「注册库探针」行（条数 + 拥挤度 + 风险预警）。`[4]` **非状态机决策项**（不推进流程、不进 `human_decisions`）；选题缺失时菜单自动隐藏（与 hint 同语义：先输入选题）。探针异常（`ct-registry` 缺失 / 网络失败）优雅降级为 `status=error`，由 `feasibility.risk_alert` / `_a1_warnings` 暴露，不阻断 A1。
- **`[3] 改检索范围（综述 + 数据源）`（2026-09-11 扩展，原仅控综述）**：选题阶段可同时改两件事——① 综述纳入开关 `include_reviews`（原始研究-only ↔ 含综述类，伞评/范围综述场景用）；② **检索数据源增减** `sources`（从可选池 `block_a.AVAILABLE_SOURCES` = OpenAlex / EuropePMC / bioRxiv / medRxiv / SemanticScholar / arXiv 中选子集，与 ct-literature `_SOURCE_DISPLAY` 单一真源一致）。**链路已实测打通**（2026-09-11）：A1 批准提交 → `fullflow._run_block` 读 `latest_revision("A1.topic_selection")` 注入 `run_block_a(sources=…)` → `a2_literature_search` → `a2_build_tool_card`（列表归一为**逗号串**写入 `params.sources`，因 `execute_tool_cards` 对 arg_map 值做 `str(val)`）→ `tool_mapping_meta.json` 的 `arg_map("sources"→"--sources")` → **ct-literature 新增的 `--sources` 参数**（逗号子集，覆盖各 `--with-*`/`--cochrane` 默认；未知源名报错退出）。⚠️ 非独立源（早先清单有误，已更正）：`PubMed` 并入 EuropePMC、`Cochrane` 是 EuropePMC 的 journal-filter 子模式、`WebOfScience`/`Scopus` 无授权 API；OpenAlex 为管线基座不可关闭。A1 摘要「检索范围」行同步列出当前数据源（`数据源：OpenAlex、EuropePMC…`），无选题时该选项随菜单整体隐藏。
- **`[3] 改检索范围` 之后回到 A1 等待批准（2026-09-11 行为修正）**：A1 修订属「检索前最后可改点」，`resume_fullflow` 对 `stage_id=A1.topic_selection` 的 `revised` 决策**只回写信封（把 `include_reviews` / `sources` 补丁进 A1 的 `stage_result`）并停回 A1**，绝不重跑整块检索、也不越过 A1 批准闸跳到 A2。菜单随即反映新检索范围（摘要「检索范围」行更新），用户复核后再于 A1 批准，此时才按新范围触发真正的检索。`[2] 改 PICOS 报告` 同理停回 A1（同属选题阶段预检索修订）。

### ② A2 · 文献集（检索 + 初筛 · 合并节点）

> **2026-09-10 用户裁定**：原 `② 检索·覆盖确认` 与 `③ 初筛·导出裁决表` 合并为**单节点单表**。
> 检索完在同一节点内立刻去重 + 规则初筛，只软停一次，只产出一张合并表。

```
文献集 · 检索 + 初筛（一张表）                 〔软停 · 需你拍板〕
   合并 20 ｜ 状态 ok ｜ OpenAlex 12 · EuropePMC 8
   检索上限：5/源（合并上限 = 源数 × 上限）
   原始主题：奥希替尼 vs 化疗 NSCLC
   优化检索式：("osimertinib") AND ("NSCLC" OR "non-small cell lung cancer")
   未翻译残留：（无）
   去重 20 ｜ 规则纳入 6 ｜ 规则剔除 14 ｜ 低置信 0
   类型（规则预填）：原创研究 15 · 综述/Meta 3 · 指南/共识 1 · 研究方案 1
   改「裁决」「理由」「文献类型确认」三列 → [4] 传回，即接 ③
   [1] 批准并下载 PDF  [2] 改检索式  [3] 导出检查（不改变状态）  [4] 传回修改后的合并表
```

- **陷阱 A**：`--max` 是**每源**上限，不是合并上限 → 菜单必须标 `/源`。
- **A2 选项收敛（合并后，2026-09-11 二次裁定恢复 4 项）**：不提供 `跳过` / `打回`。
  四项 = **批准并下载 PDF**（批准触发 A4 自动落盘：OA 下载 + 本地 `pdf_dir` 优先抽取）/
  改检索式 / 导出检查（不改变状态）/ **[4] 传回修改后的合并表 = revise/screened**
  （离线改三列后回传，`apply_screening_upload` 解析 → 标准 decide 通路落
  `screened` 修订 → 重跑下游）。
  **批准即自动落盘合并表 `A2_文献集_<pid>.xlsx`**（含裁决 / 理由 / 文献类型确认列，复用
  ct-literature `export_xlsx` 模板）供人工审阅。
- **沉默漏检**（本节点的存在理由）：判据收敛为**只看核心二源** OpenAlex + EuropePMC：
  - 核心源（OpenAlex/EuropePMC）缺位 → 报
  - `by_source` 为空 / `total == 0` → 报
  - `search_status ≠ ok` → 报（该字段本就由核心源派生）
  - 调用方显式给 `--expected-sources a,b` → 差集比对，**仅核心源生效**
  - **非核心源**（bioRxiv / arXiv / 无 key 的 Semantic Scholar）缺失 = 已知常态 → **不报**
  - 原始 CLI 返回码保留在 `coverage.cli_status`，供审计而不参与告警
  - ⚠️ **`source` 大小写**：`by_source` 的键是 ct-literature 原样输出（生产为 `OpenAlex`/`EuropePMC`，TitleCase）；`CORE_SOURCES` 与之同形。用小写喂数会让核心源判定漏配、`search_status` 误降级。
- `[2] 改检索式`：`EDITABLE_KEYS["A2.literature_search"]` 收录 `query`，revise 经 `override_query` 真正传播到重跑（D16 已落地）。同节点 `screened` 亦在 `EDITABLE_KEYS`，但**对话侧不给逐条编辑入口**。
- **对话内零逐条编辑入口**（D9）。`[3]/[4]` 走 `block_a.export_screening_xlsx()` / `parse_screening_xlsx()`——与工作台**同一套函数**，双端行为一致、漂移风险归零。工作台保留 rowlist 逐条裁决（GUI 合适），对话侧不成立。
- 回传校验失败一律不前进（列完整 / 行可对齐 / decision 合法 / exclude 必填理由 / 不新增行）。
- **批准后不再重跑检索**（2026-09-10 修复）：合并节点批准 → 续跑复用 A2 缓存信封，只跑 A4，**保住人工在 Excel 上做的复核**。此前只在旧 A3 已批准时才复用，导致批准 A2 会整块重算、检索漂移、复核作废。

### ③ A4 · 数据提取核验（🔴 红线）

```
数据提取核验（🔴 红线）                       〔🔴 红线 · 必须你放行〕
   初筛通过 103 ｜ 已下载全文 11 ｜ 已抽取 9（2×2 9）
   待补传 PDF：3 篇（非 OA / 付费墙）→ 影响纳入量，请处置
   类型（只读 A2 确认值）：原创研究 8 · 综述/Meta 1
   ▸ 首次进入：若手头已有部分文献的 PDF，请直接发送其所在文件夹（或文件）路径——
     将优先用本地 PDF 抽取，减少付费墙漏检；没有可回「跳过本提示」。
   [1] 批准（放行 → Block B）  [2] 上传补 PDF  [3] 修订 2×2 表  [4] 回退 ② 文献集  [5] 打回
   ⚠️ 本节点无「跳过」——红线闸不接受 skipped
```

- **首次出现提示（2026-09-11）**：A4 菜单首次出现即要求用户提供本地 PDF 所在路径。
  路径作为 A4 修订键 `pdf_dir` 登记（EDITABLE_KEYS），`_run_block` 注入
  `run_block_a(pdf_dir=…)` → 覆盖 A4 PDF 缓存目录，本地已有 PDF 优先被抽取；
  已登记后提示行改为展示路径值。启动配置亦可预置 `cfg.pdf_dir` 跳过提示。

**四条硬约束**
1. **无「跳过」**：选项集由 `_REDLINE_GATES` 派生过滤；即使 LLM 误造，`_validate_decision`
   也会拒。**双保险，不靠提示词**。
2. **不做下载前类型甄别**（2026-09-10 起）：100% 按 A2 文献集清单下载。
3. **类型只读 A2 确认值**：抽取层探测降为 `doc_type_notice` 提示词，`review_note` 由确认值驱动。
4. `[2] 上传补 PDF` 允许（D10 建议「允许」）；非 OA 未补传时写 `pending_actions`，
   **闸位保持，`approve` 被拒**（D8）。

### ⤍ A4 → B1 块间交接

```
块间交接确认                                  〔交接闸 · 仅批准/打回〕
   块 A 完成，即将进入 Block B。请确认交接数据。
   待交接研究 9
   [1] 批准进入下一块  [2] 打回
```

`defer ≠ skip`：

| | `skip` | `defer` |
|---|---|---|
| 含义 | 本会话不再停靠，按默认放行 | 人工动作**未完成**，流程**不得前进** |
| 适用 | 仅软停（A1/A2，A3 已并入 A2） | 任意节点，尤其 🔴（A4 补传） |
| 审计 | 写 `human_decisions` | **不写**，改写 `pending_actions` |
| 效果 | 下游继续跑 | 闸位保持，`approve` 被拒 |

> **混淆这两者 = 让红线的人工复核被静默绕过。**

---

## 5. 命令行

```bash
PY=C:/Tools/Anaconda3/python.exe   # 绝对路径；不要依赖 PATH 里的 python

# L0 导航条（+ 机器可读状态）
$PY scripts/flow_menu.py status [--session P] [--lang zh|en] [--json]

# L0 + L1 节点菜单（可直接贴给用户）
$PY scripts/flow_menu.py menu   [--session P] [--lang zh|en] [--json]

# 11 节点总表（闸类 / 是否停靠）
$PY scripts/flow_menu.py nodes  [--lang zh|en]

# 决策：默认只校验不落盘；--apply 才真正推进状态机
$PY scripts/flow_menu.py decide [--session P] --option 1 [--set k=v ... | --revision '<json>'] [--note S] [--apply]

# 回退（候选集从信封派生，非法目标直接拒）
$PY scripts/flow_menu.py rewind [--session P] --target A2.literature_search [--apply]
```

- `--session` 省略时取 `adapters/workbench/runs/` 下 `updated_at` 最新的会话。
- 退出码：`0` 成功 / `2` 用法或校验错误 / `3` 会话缺失或不可读。
- `decide` / `rewind` 的校验**一律走 `fullflow._validate_decision`**，本层不复述规则。

### 5.1 全局指令（L2 层）

| 指令 | 行为 |
|---|---|
| `/flow` | 重贴 L0 导航条（等价 `status`） |
| `/node <编号或 stage_id>` | 贴非停靠节点的只读详情 |
| `/rewind <stage_id>` | 回退到上游人工节点并重算下游 |
| `/explain` | 解释当前节点的判据与字段来源 |
| `/raw` | 输出 `--json` 原始模型 |
| `/workbench` | 逃生门：需要视觉/空间信息的操作（PDF 页面对照、逐条表格编辑）转到工作台 |
| `/export` | 导出当前节点数据（A2 = 合并表） |

---

## 6. 验收标准与证据

`tests/test_flow_menu.py` —— **175 PASS / 0 FAIL**（`python tests/test_flow_menu.py`）

| 编号 | 验收项 | 回归段 |
|---|---|---|
| AC-A1 | 停在 A4 菜单**不出现**「跳过」，`action=skipped` 被 `_validate_decision` 拒 | [1] |
| AC-A2 | 停在 A1/A2 菜单**不出现**「跳过」（菜单窄化；机器可） | [2] |
| AC-A2b | A2「文献集」合并菜单**无任何逐条编辑入口**（无 revise / 无 rowlist），2026-09-11 二次裁定恢复 4 项：`[1]批准并下载 PDF / [2]改检索式 / [3]导出检查 / [4]传回修改后的合并表` | [3] |
| AC-A4 | revise 选项 ⊆ `EDITABLE_KEYS`；A2 `query` 未收录 → 显式标注 blocked（D16） | [4] |
| AC-A6 | A2 检索上限标注 `/源` | [5] |
| AC-A7 | A2 空结果 / 仅 1 库 / 显式期望缺库 → 出现 ⚠️ 沉默漏检（且**不误报**） | [5] |
| AC-A9 | 11 节点 × zh/en 渲染无缺键、无 `None`、无裸 i18n key | [7] |
| R1 | 渲染只读：会话文件字节不变 | [8] |
| R2 | 渲染确定性：两次输出字节一致 | [9] |
| R3 | 选项编号从 1 连续，decision ⊆ `machine_options` | [10] |
| R5 | 回退候选集从信封派生：不含自身、不含下游、不含 auto 节点 | [11] |
| — | `expected_sources` 与 ct-literature `_SOURCE_DISPLAY` 同步 | [12] |
| — | CLI dry-run 端到端（非法选项 / 非法回退目标被拒，且不落盘） | [13] |

**未破坏既有回归**：`tests/test_a3_doc_type_confirm.py` **28 PASS / 0 FAIL**；
`adapters/workbench/form_schema.py` 自检通过（新增 `TITLE_EN` / `title_for` 为纯增量）。

---

## 7. 边界：什么时候**不**出现 CCM

- **纯算数请求**（合并效应量 / NMA / 敏感性分析 / 亚组 / 森林图 …）→ 走计算轨道，**零 CCM**。
- 单次文件转换、格式转换、图表渲染 → 不触发。
- 只有**全流程轨道**（系统综述全流程 / 工作台会话续跑）才贴菜单。
- 需要视觉/空间信息的操作（PDF 页面对照、>10 行表格逐条编辑、文件↔条目拖拽指派）
  **不迁移**到对话侧，保留 `/workbench` 逃生门。

### 7.1 会话版本漂移（实测踩坑，2026-09-10）

CCM **只做投影**，同一节点渲染是否可信取决于会话数据是不是当前契约写的。
`runs/` 里存量会话可能早于当天的契约变更，此时菜单会**照实渲染出旧语义**，
看起来正常、实则误导。实测两例：

| 会话 | `updated_at` | 症状 |
|---|---|---|
| `ff-9fc5c5469a4d` | 2026-09-10 08:06（D17 **之前**） | `per_doc` 有 **16 条 `status="excluded_review"`**（该机制已从代码移除，全仓只剩 `block_a.py:1398/1738` 两处注释）；`await.gate` 是布尔 `true`（新格式为闸名）；`cursor.block='B'` 却指向 A 块 |
| `ff-65e2e0076337` | 2026-09-09 20:51（D17 **之前**；A3 合并**之前**） | 独立 A3 节点的 103 行**无 `doc_type` / `doc_type_source` / `decision`**，只有 `include`(T29/F74) + `is_review` + `review_reason`；`human_decisions` 里 A3 是**整批 `approved`**（`decided_by: workbench`），不是逐条类型确认 |

**判断动作**：贴菜单前先验四个字段——`await.gate` 是否为**闸名字符串**、
`per_doc[*]` 是否含 `doc_type_confirmed`、A2 行是否有 `doc_type_source`（合并前会话则是 A3 行）、
`cursor.block` 与 `stage_id` 是否同块。任一条不满足 = 旧数据，**菜单仍会渲染，但不得据此放行**。

**更稳的替代**：多数场景直接用**当前代码重跑该阶段**，而不是复用旧会话结论。

---

## 8. 待你拍板（未决项，菜单已按建议实现但语义未闭合）

| ID | 决策 | 现状 |
|---|---|---|
| **D16** | A2「改检索式」的语义：只写补丁（=假交互）/ revise+rewind 重跑 / 取消该选项 | ✅ **已落地**（2026-09-10）：`EDITABLE_KEYS` 补 `A2.literature_search=["query"]`，revise 经 `override_query` 真重跑 |
| **D10** | A4 是否允许对话内收文件/路径 | ⏳ 菜单已按「允许」实现（`[2] 上传补 PDF`） |
| **D11** | A2 是否前置下载（`--download-pdf`） | ⏳ 待定（须配 timeout 放宽 120s + 流式） |
| **D14** | A1 注册库探针是否展示 | ⏳ 菜单已按「展示」实现（一行条数 + 拥挤度） |
| **D18** | A4 下载配额 `max_attempts=12`（`block_a.py:1645` `quota_deferred`）：**与「100% 按列表下载」直接冲突** | ⏳ 实测 `ff-65e2e0076337`：59 篇过初筛门控（当时为独立 A3，现并入 A2），仅 12 篇发起下载，**45 篇被配额静默 defer**；且 A4 菜单**没有「继续下一批」入口** → 这 45 篇在对话侧不可达。配额值来自 `fullflow.py:232` `cfg.get("max_attempts", 12)`，菜单无法设置 |
| **D19** | A4 菜单未暴露 `fetch_log` 门控分布 | ✅ **已落地**（2026-09-10）：A4 摘要新增 `gate_dist` 行，摊开 blocker（`relevance_skip / quota_deferred / quad_deferred / no_candidate / extract_fail`），不再只报成功态；不含 `pass_*` |
| **D20** | A2 告警口径（2026-09-10 用户裁定） | ✅ 收敛为**只看核心二源** OpenAlex + EuropePMC；非核心源缺失不降级、不告警（原始码留 `coverage.cli_status`）。**批准即自动落盘 `A2_文献集_<pid>.xlsx`** |
| **D21** | **A2 检索 与 A3 初筛是否合并**（2026-09-10 用户裁定） | ✅ **已落地**：合并为单节点「文献集」（`A2.literature_search`），只软停一次、只产出一张合并表（含裁决/理由/文献类型确认列）。A 阶段停靠点 4→3。**两条入口**：① A1 批准后系统自动检索+初筛；② 用户上传 Excel（**仅 A2 合并节点内 `[4]传回修改后的合并表`**，2026-09-11 曾一度移除、同日二次裁定恢复），识别到「裁决」列即按裁决表解析。**顺带修复**「批准即重跑检索」：合并节点批准后复用缓存、只跑 A4，不再整块重算、不再作废 Excel 复核 |

**已知接受项**：R 路径硬编码 `C:/Tools/R-4.6.1`（`coze_client.py:1414`）→
`tests/test_a4_b1_handoff.py` 的 4 项 FAIL 属既有环境问题，不是本轮回归。

**已知 i18n 缺口（上游，非本模块）**：A1 的 `feasibility.risk_alert`、A2 的 `prompt` 等
文案由 `block_a.py` 生成，**只有中文**；`--lang en` 时菜单骨架/标签为英文，但这些**引用自
上游的正文**仍是中文。本模块不重写上游文案（避免出现第二份判定/建议文本）。
若需彻底双语，应在 `block_a` 侧加文案表，属独立改动。

---

## 9. 相关文档

| 文档 | 用途 |
|---|---|
| `references/design/ccm/README.md` | 设计归档索引（框架 v0.1–v0.4 + A 阶段设计稿） |
| `references/design/ccm/01_framework_v0.2_draft.md` | 三层菜单 + 操作四策略（原生迁移 / 降级简化 / 文件交接 / 跳过转出）+ 四问判定 |
| `references/HANDOFF_2026-09-10.md` | A 阶段契约、18 项改动、静默失败模式、陷阱 A–H |
| `references/systematic_review_fullflow.md` | 全流程轨道 playbook（Stage 3 文件交接 / Stage 4 按清单直下） |
| `adapters/workbench/` | 工作台（同一套 schema 的 GUI 投影 + `/workbench` 逃生门） |
