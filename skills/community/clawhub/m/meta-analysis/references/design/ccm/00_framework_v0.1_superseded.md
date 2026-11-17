# meta-analysis · 对话上下文菜单（CCM）设计框架 v0.1

> 状态：**待确认（未动代码）** ｜ 提出日期 2026-09-10 ｜ 目标技能：`meta-analysis` v2.9.19
> 关联资产：`adapters/fullflow.py`（状态机）、`adapters/workbench/form_schema.py`（渲染契约）、
> `references/systematic_review_fullflow.md`（全流程剧本）、`ct-base/references/{interaction_frameworks,compute_menu,workbench_ui}.md`

---

## 0. 结论前置

| # | 结论 |
|---|---|
| 1 | **一句话架构**：一份 schema（`form_schema`）、一条状态机（`fullflow_session_ff-*.json`）、**两个渲染端**（工作台 HTML / 对话 CCM）。对话侧不再自造一套流程定义。 |
| 2 | **定位**：CCM 是 meta-analysis 的**第三条菜单通道**，只管**全流程轨道**；计算轨道的能力路由菜单、选题门控**原样冻结，互不越界**。 |
| 3 | **形态**：三层文本菜单（导航条 / 节点菜单 / 字段菜单）+ 一组全局指令（`/flow` `/rewind` `/workbench` …），**零依赖、不需要浏览器和端口**。 |
| 4 | **状态**：直接复用工作台同一份 session JSON → 对话与工作台**可中途无缝互切**（这是最大增量价值，不是"终端版工作台"）。 |
| 5 | **新增代码只有两块**：`scripts/flow_menu.py`（确定性渲染/状态 CLI）+ `references/conversation_flow_menu.md`（规范）；`form_schema.py` 增加 `menu_for()` 投影。 |
| 6 | **红线不降级**：🔴 闸位在对话侧同样无 `skipped` 选项（对齐 `fullflow._validate_decision`），且闸位渲染由代码产出、LLM 只转述。 |

---

## 1. 现状与缺口

### 1.1 工作台已经有什么（对话侧缺什么）

| 能力 | 工作台（已有） | 对话侧（现状） | 缺口 |
|---|---|---|---|
| 阶段地图 | 左栏 12 节点时间轴，进度由 `blocks[].envelope.stages` 重建 | Stage 0 口头列一次 5 段 | **每轮无位置感**，"我现在在哪"要问 |
| 节点面板 | `form_schema.schema_for()` 逐节点渲染（`object`/`dicttable`/`rowlist`/`textarea`/`bool`/`json`/`a4documents`） | 无 | **该展示什么、怎么展示全靠 LLM 即兴**，同一节点两次呈现不一致 |
| 闸位选项 | 按钮：批准 / 修订 / 打回 /（软停才）跳过 | 无 | 红线"不可跳过"、交接闸"只收 approved/rejected"等硬约束**会漂** |
| 回退 | `/api/rewind` 时间轴点选，回退重算下游 | 无 | 想改上游只能重开流程 |
| 状态 | session JSON + `cursor.{block,stage_id,await_kind}` | 线程内自然语言 | 长流程（5 阶段 12 节点）**必然丢状态** |
| 审计 | 右栏日志（`human_decisions`） | 无 | 无法回答"我批准过什么" |

### 1.2 根因

全流程有两套资产：**HTML 表单**（结构化、状态驱动）和 **NL 指南**（`systematic_review_fullflow.md`，散文剧本）。
只有前者是"结构化的"。对话侧缺的不是"说明文档"，而是**一份结构化的菜单契约**——所以 agent 每个闸位都要重新发明一次"问什么、给什么选项"。

---

## 2. 设计目标 / 非目标

**目标**

- G1 状态可见：任一轮次一眼看到 12 节点位置与下一步。
- G2 闸位可操作：每个闸位给出**该节点专属**的选项集（而非通用"继续吗？"）。
- G3 可回退：`/rewind <节点>` 触发块的清空与下游重算。
- G4 零漂移：菜单文案与选项**同源于 `form_schema`**，不出现"文档一套、代码一套"。
- G5 零额外成本：不需要浏览器、端口、`node`；纯文本即可驱动。

**非目标（明确不做）**

- N1 不做"把工作台搬进终端"：A3 逐条裁决 50 行、A4 逐篇 PDF 核验等**重度交互仍以工作台为主**，对话侧只做 Top-N + 文件交接。
- N2 不改计算轨道（Type-Compute）：纯算数请求继续"描述即执行"，不弹任何流程菜单。
- N3 不改变 `form_schema` 的既有语义（工作台面板结构不动，只**增加一层投影**）。

---

## 3. 三层菜单结构

### L0 · 上下文导航条（Context Bar）— 每轮一行

```
流程 [✔]①选题 [✔]②检索 [▶]③初筛 [ ]④提取 │ [ ]⑤合并 [ ]⑥GRADE [ ]⑦声明 [ ]⑧质量门 │ [ ]⑨初稿 [ ]⑩评审 [ ]⑪参考 [ ]⑫QA
```
- 12 节点压缩为一行，`✔` 已过闸 / `▶` 当前停靠 / `[🔴]` 红线未过 / `[ ]` 未达。
- 作用 = 工作台左栏时间轴的对话等价物；**每轮必贴**，成本一行。

### L1 · 节点菜单（Node Menu）— 停在闸位时

内容三件套：**节点头（闸类）+ 数据摘要（Chat 投影）+ 选项菜单**。实例（A3 初筛）：

```
③ 初筛 · 逐条裁决            〔软停 · 需你拍板〕
   去重 42 → 纳入 12 / 剔除 28 / 低置信 2 ｜ 疑似综述默认剔除 3
   ── 逐条（Top 5 / 共 42；完整 42 条用文件交接）
   1. Zhang 2023 · J Clin Oncol · RCT        [纳入]
   2. Lee 2021  · BMJ          · 综述·疑似   [剔除]
   …
   ── 你的选择
   [1] 批准放行 → 进 ④ 数据提取（🔴 红线，不可跳过）
   [2] 修订（⬇ 导出裁决表 → 改完 ⬆ 传回）
   [3] 跳过本阶段（软停专属）
   [4] 打回 / 回退到更早阶段
   [5] 解释本节点在做什么
   [6] 看原始数据（只读 JSON）
```

### L2 · 字段菜单（Field Menu）— 选"修订"后

只列该节点的 `EDITABLE_KEYS`，逐字段给"怎么改"的写法：

| 节点 | 可编辑字段 | 对话侧改法 |
|---|---|---|
| A1 | `report` / `include_reviews` | 回复 `改 include_reviews=是` 或粘贴新报告全文 |
| A2 | `query` | 回复 `改检索式：<新布尔式>` |
| A3 | `screened` | **文件交接**：⬇ 导出 → 改"裁决/理由"两列 → ⬆ 传回 |
| A4 | `extracted_rows` | 逐行 `修 S3 事件数=12` / 剔除整篇 / 补传 PDF |
| B4 | `report` | 粘贴修订后的质量报告 |
| C1 | `manuscript` / `sections` | 按章节 `修 讨论 <新正文>` |

### 全局指令（任意轮次可用）

| 指令 | 作用 |
|---|---|
| `/flow` | 打印 L0 + 当前 L1（等同于"重画菜单"） |
| `/node <id>` | 回看某节点结果（只读） |
| `/rewind <id>` | 回退到该节点所属块，清空下游并重算（对应 `rewind_fullflow`） |
| `/explain <id>` | 讲清该节点在流程里干什么、为什么需要人拍板 |
| `/raw` | 当前节点原始 JSON（对应工作台 `json` 面板） |
| `/workbench` | 用**同一 session** 启动 HTML 工作台继续（重度操作用） |
| `/export` | 导出审计（`human_decisions` → md） |

---

## 4. 渲染映射（工作台 kind → 对话形态）

| `form_schema` kind | 工作台渲染 | 对话 CCM 渲染 |
|---|---|---|
| `object` | 键值区 | Markdown 两列表（键/值） |
| `dicttable` | 表格 | Markdown 表格（列数 ≤6，超出转文件） |
| `rowlist` | 可编辑表 + 三态筛选 + ⬇⬆ | **Top-N 表格 + "还有 N 条" + 文件交接**（N≈5~10） |
| `textarea` | 大文本框 | 引用块 + "回复 `改 <字段> <新内容>`" |
| `bool` | 勾选框 | 选项式 `是 / 否` |
| `json` | 只读 `<pre>` | 折叠入口 `[6] 看原始数据` |
| `a4documents` | 逐篇卡片（含剔除/恢复/补传） | 逐篇一行（状态 · 来源 · 动作），补传走 `/upload` 或工作台 |
| `auto` 节点 | 无需操作、点击看结果 | 单行 `✅ 已完成` + 关键数字；不占菜单位 |

**新建节点**：`handoff_confirm`（A→B、B→C 交接闸）→ 显示 `n_studies` + 字段清单，选项只有 `批准 / 打回`。

---

## 5. 闸位与动作矩阵（与 `_validate_decision` 一一对齐）

| `await_kind` | 出现节点 | 可选动作 | 对话侧硬约束 |
|---|---|---|---|
| `pause`（软停） | A1 A2 A3 C1 | 批准 / 修订 / **跳过** / 打回 | 跳过 = 本会话不再停靠该节点（`effective_pause_at` 语义，须说明） |
| `gate`（🔴 红线） | A4 B4 C3 C4 | 批准 / 修订 / 打回 | **不得出现"跳过"**；渲染由代码产出，LLM 不得自行增删选项 |
| `handoff_confirm` | A→B、B→C | 批准 / 打回 | 仅两选项 |
| `guard_blocked` | B 块入口 | 批准（放行凭据） | 触发条件：抽取 CSV 未 `stamp --confirm`；给"怎么解锁"指引 |
| `done` / `error` | 终态 | — | `error` 给"看错误 / 重试 / 导出诊断"三选项，**不自动重试** |

---

## 6. 状态与跨轮连续性

### 6.1 回显块（新增前缀，与计算轨道区分）

```
## 当前流程设定 / Current pipeline settings: session=<session JSON 路径> | block=A | node=A3.screening | await=pause | gate=— | schema=v0.1 | next=A4.data_extraction
```

- 与计算轨道的 `## 当前分析设定 / Current analysis settings:` **前缀不同、互不覆盖**；同轮同现时，分析块在后（更近）。
- `session` 是**指针**（路径字符串），不搬数据本体——与 `continuity.md` §6.3 数据集指针继承同理。
- 节点专属计数（如 `k=42 | in=12 | ex=28`）追加在块尾，供下一轮免重读。

### 6.2 追问规则（继承 compute_menu §6.1 三条）

1. 每次渲染后回显该块；
2. 追问时先读**最近一个流程块**，只覆盖变化字段（如 `node←A4.data_extraction`、`await←gate`）；
3. 拿不准时用 `scripts/flow_menu.py --session <path> --status` 兜底——**状态真源在文件，不在 LLM 记忆**。

> 关键差异：计算轨道的 config 只在**线程内**（易漂），流程轨道有**落盘 session**（不漂）。CCM 的连续性风险低于计算轨道，这是它更好做的地方。

---

## 7. 触发与「不干扰」策略

| 场景 | CCM 行为 |
|---|---|
| 全流程触发（`系统综述全流程` / `从检索到meta分析` …） | **开启**：Stage 0 贴 L0 全图；此后每轮贴 L0，闸位自动贴 L1 |
| 计算轨道（"合并这 5 项研究的 OR"、NMA、敏感性…） | **完全不开**（保持"描述即执行"）；仅 Complex 选型时保留既有能力路由菜单 |
| 选题轨道（`选题评估` / 可行性） | **不开 L1**；选题报告末尾给一个入口 `[进入全流程？]` |
| 用户显式输入 `/flow`、`菜单`、`流程菜单` | 强制打印 L0 + 当前 L1 |
| 非闸位轮次（如闸后自由提问） | 只贴 L0 一行，不贴 L1（避免刷屏） |

**调用预算**（需回写 `references/speed-discipline.md`）：闸位菜单渲染 = 1 次 `flow_menu.py` 调用；**不计入计算轨道"开火前 ≤1 调用"红线**（不同轨道，不同预算）。禁止在同一闸位重复渲染。

---

## 8. 降级矩阵

| 失效场景 | CCM 降级表现 |
|---|---|
| ct-literature 未安装 | ② 节点行标注"委托降级为 ct-search 远端 / Europe PMC 探针"；覆盖表缺列显式标注"可能沉默漏检"，不假装满覆盖 |
| coze 不可达 | ⑤~⑧ 节点转 `error` 菜单（看错误 / 重试 / 导出诊断），**不本地兜底**（对齐 §0 铁律 4） |
| 付费墙 PDF | ④ 节点显示"待补传清单 + 篇数"，给上传引导；不阻塞其余篇目 |
| A3 列表 k>30 | L1 只出 Top-N + 强制文件交接（对话不做全量逐条） |
| 无浏览器 / 端口被占 | CCM 独立可用（这正是它的核心场景）；反向提示 `/workbench` 当前不可用 |
| session 文件缺失/损坏 | 明确报错 + 给"从哪个阶段重建"选项；**不静默新建**（避免伪造历史） |

---

## 9. 落地清单

| 文件 | 动作 | 内容 | 量级 |
|---|---|---|---|
| `scripts/flow_menu.py` | **新增** | 子命令 `render / status / decide / rewind / explain`；读 session JSON + `form_schema`；输出双语 Markdown 菜单；`decide` 直接调 `fullflow.resume_fullflow` | M |
| `references/conversation_flow_menu.md` | **新增** | 规范正文：三层菜单 / 渲染映射 / 动作矩阵 / 回显块 / 降级 / 指令表 | M |
| `adapters/workbench/form_schema.py` | 扩展 | 新增 `menu_for(stage_id, lang)` 投影 + `MENU_SCHEMA` JSON 导出 + i18n key（照 ct-advisor `menu.json`/`menu.py` 模式，双端同源） | S |
| `references/interactive_menu.md` | 小改 | §0 加"双菜单通道"说明：计算轨道 vs 流程轨道，互不越界 | S |
| `references/speed-discipline.md` | 小改 | 菜单调用预算一行 | S |
| `SKILL.md` | 改 | 新增 §2.6 对话上下文菜单；`triggers` 加 `流程菜单` / `flow menu` / `/flow` | S |
| `tests/` | 新增 | 冒烟：12 节点 × 2 语言渲染无缺键；🔴 节点断言**不含**跳过选项；`decide` 红线拒绝 `skipped` | S |
| `ct-base/references/interaction_frameworks.md` | 可选 | 升为第三原型 **Type-Flow**（人工闸状态机），写进 §6 兼容性矩阵 | S |
| `CHANGELOG.md` | 改 | v2.10.0 条目 | S |

**验收标准（AC）**

1. 同一 session，从对话切工作台、再切回对话，`node` 与 `await_kind` 完全一致；
2. 12 个节点在 `zh/en` 下均能渲染，无缺键、无硬编码中文；
3. 🔴 节点（A4/B4/C3/C4）菜单**不含**"跳过"，且脚本层拒绝 `action=skipped`；
4. 纯计算请求（如"合并 OR"）**不出现任何 CCM 输出**；
5. `/rewind A3.screening` 能清空 A3 及下游并重算回原闸位。

---

## 10. 待确认决策点

| ID | 决策点 | 选项 | 建议 |
|---|---|---|---|
| **D1** | 触发形态 | (a) 闸位自动贴 L1 + 非闸位只贴 L0 ｜ (b) 全程按需（用户说"菜单"才出）｜ (c) 全自动每轮贴 L0+L1 | **(a)**；(c) 会刷屏，(b) 失去"状态可见"价值 |
| **D2** | 载体 | (a) 纯文本菜单 ｜ (b) `AskUserQuestion` 卡片（≤4 选项）｜ (c) 内联 widget | **(a) 为主，(b) 仅在选项 ≤3 的闸位补充**；(c) 与"HTML 报告唯一呈现面"冲突 |
| **D3** | 状态真源 | (a) 复用工作台同一 session JSON ｜ (b) 对话侧另建轻量状态文件 | **(a)**——无缝互切是最大卖点；代价是 CCM 依赖 `adapters/fullflow.py` |
| **D4** | 作用范围 | (a) 仅全流程轨道 ｜ (b) 也覆盖计算轨道 | **(a)**；(b) 会废掉"描述即执行"头号卖点（compute_menu §2 明令） |
| **D5** | A3/A4 重度交互 | (a) Top-N + 文件交接，重度回工作台 ｜ (b) 全量在对话内逐条 | **(a)**；(b) 在 k>30 时不可用 |
| **D6** | 家族层归属 | (a) 仅 meta-analysis 内部实现 ｜ (b) 同步升为 ct-base 第三原型 Type-Flow | **(b)**，但可分两步：先在 meta 内验证，稳定后回写 ct-base（ct-samplesize / ct-literature 工作台同构，可直接复用） |
| **D7** | schema 机器可读化 | (a) 直接在 `form_schema.py` 加 `menu_for()` ｜ (b) 另建 `menu.json` + i18n key（ct-advisor 模式） | **(b)** 更防漂移、双端同源，但多一份资产要维护 |

---

## 11. 主要风险

| 风险 | 说明 | 缓解 |
|---|---|---|
| 双端漂移 | 对话菜单与工作台面板说的不一样 | 单一 schema + 冒烟测试断言同源 |
| 与计算轨道混淆 | 用户以为"以后算数也要走菜单" | §7 触发策略 + `interactive_menu.md` §0 明文边界 |
| 对话刷屏 | 每轮 L0+L1 过长 | L0 压一行；非闸位不贴 L1 |
| 对话做重度编辑不可靠 | A3 42 条逐条在聊天里改易错 | D5 文件交接；`/workbench` 逃生门 |
| session 依赖 | CCM 依赖 `adapters/fullflow.py` 可用 | 与工作台同一依赖，非新增耦合 |

---

> 本文为**设计提案**，确认后按 §9 落地并按 §10 决策执行。
