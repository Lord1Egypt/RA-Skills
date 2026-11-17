# 用户交互菜单逻辑 · 权威参考（Menu Logic Reference）

> 本文件是 meta-analysis 技能「对话侧菜单」的**唯一权威依据**。
> 排查菜单行为时，以此为准；代码仅是实现。改菜单前先读本节，改完同步 §8 列出的所有落点。
>
> 适用范围：HITL orchestrator 在 `adapters/fullflow.py` 状态机驱动下，由
> `scripts/flow_menu.py` 渲染的**对话侧决策菜单**（L0 导航条 + L1 决策菜单）。
> 工作台（adapters/workbench/）侧渲染契约见 `form_schema.py`，二者节点一一对应，
> 但对话侧可窄化展示（见 §6）。

---

## 1. 总架构（三层）

| 层 | 作用 | 每轮必出 |
|---|---|---|
| **L0 导航条** | 11 节点进度（done / current / pending 线性轴） | 是 |
| **L1 决策菜单** | 当前停靠点：标题 + 摘要行 + 告警 + 编号选项 | 仅停靠点 |
| **消费方式** | LLM 转述 `render_menu_text`；用户发编号/关键词 → 对应 `action` → `fullflow._validate_decision` 校验（红线拒 `skipped`） | — |

代码落点：`build_menu()` `flow_menu.py:823`；导航条 `render_nav()`；文本渲染 `render_menu_text()` `flow_menu.py:926`。

---

## 2. 11 节点全景

节点真源：`form_schema.STAGE_ORDER`（`form_schema.py:21-34`）。
停靠点真源：`fullflow.DEFAULT_PAUSE_AT`（`fullflow.py:43-52`）。

| # | 节点 | 名称 | 闸类 | 有菜单 | 菜单来源 |
|---|---|---|---|---|---|
| 1 | A1.topic_selection | 选题 | 🟡软停 | ✅ | A1 专属 builder |
| 2 | A2.literature_search | 文献集（A2+A3 合并） | 🟡软停 | ✅ | A2 专属 builder |
| 3 | A4.data_extraction | 数据提取 | 🔴红线 | ✅ | A4 专属 builder |
| 4 | B1.meta | 合并计算 | ⚙️auto | ❌ | 自动跑过 |
| 5 | B2.grade | GRADE | ⚙️auto | ❌ | 自动跑过 |
| 6 | B3.overclaim | 过度声明 | ⚙️auto | ❌ | 自动跑过 |
| 7 | B4.quality_gate | 质量门 | 🔴红线 | ✅ | **fallback 通用** |
| 8 | C1.draft | 初稿 | 🟡软停 | ✅ | **fallback 通用** |
| 9 | C2.ai_review | AI 评审 | ⚙️auto | ❌ | 自动跑过 |
| 10 | C3.ref_verify | 参考核验 | 🔴红线 | ✅ | **fallback 通用** |
| 11 | C4.evidence_qa | 投稿前 QA | 🔴红线 | ✅ | **fallback 通用** |
| — | handoff_confirm | 块间交接（非节点） | 交接闸 | ✅ | handoff builder |
| — | done | 终态 | — | ❌ | 仅 ✅ |

> 节点数 = **11**（A2 检索与 A3 初筛已于 2026-09-10 合并为单节点「文献集」）。
> 任何文档/注释里出现「12 节点」均为合并前化石，以本文件 11 为准。

---

## 3. 各停靠点菜单详情（中文展示；`lang="en"` 时仅文案切换，结构/动作不变）

### A1 选题（软停）
- **标题**：选题（无对话侧 override）
- **摘要行**（`_a1_summary` `flow_menu.py:347`）：
  需输入提示 / 选题 / PICOS(P I C O S) / 缺失维 / 注册库探针(相关试验N·拥挤度) / 检索范围(模式+数据源)
- **告警**：无专属 warning builder
- **菜单**（`_a1_options` `flow_menu.py:580`）：
  1. 批准（decision·approved）
  2. 改 PICOS 报告（revise·report）
  3. 改检索范围 综述+数据源（revise·include_reviews+sources，toggle）
  4. 可行性速览（probe，非决策项，agent 调 `flow_menu.py probe --apply` 落地）
- **选题缺失**（占位符/空）→ 菜单全空，只显示"请先输入选题" hint（`_a1_topic_missing` `flow_menu.py:339`）
- **修订键** `EDITABLE_KEYS["A1.topic_selection"]` = `report, include_reviews, sources`

### A2 文献集（软停，原 A2+A3 合并）
- **标题 override**：文献集 · 检索 + 初筛（一张表）（`_CCM_TITLE_OVERRIDE` `flow_menu.py:704`）
- **摘要行**（`_a2_summary` `flow_menu.py:379`）：合并N+各源计数 / 每源上限 / 原始主题 / 检索式 / 撤稿 / 未译 / 漏斗(去重·纳入·排除·不确定) / 类型分布 / 文件交接提示
- **告警**（`_a2_discrepancy` `flow_menu.py:421`，挂 `_WARN_BUILDERS`）：仅核心二源（OpenAlex+EuropePMC）缺位/空/状态非 ok 才报
- **菜单**（`_a2_options` `flow_menu.py:608`）：
  1. 批准并下载 PDF（decision·approved → 触发 A4 自动落盘，本地 pdf_dir 优先）
  2. 改检索式（revise·query）
  3. 导出检查（file，非决策项，agent 侧动作）
  4. 传回修改后的合并表（revise·screened，Excel/CSV 逐条裁决解析）
- **修订键** `EDITABLE_KEYS["A2.literature_search"]` = `query, screened`

### A4 数据提取（红线）
- **标题**：数据提取（无 override）
- **摘要行**（`_a4_summary` `flow_menu.py:461`）：漏斗(已筛/已下/已抽 2×2 M) / 待补PDF N / 类型分布 / 抓取 gate 分布(暴露沉默漏检) / pdf_dir 提示
- **告警**：无专属（gate_dist 已在摘要暴露）
- **菜单**（`_a4_options` `flow_menu.py:633`）：
  1. 批准（放行 → Block B）
  2. 上传补 PDF（upload，非决策项）
  3. 修订 2×2 表（revise·extracted_rows）
  4. 回退 ② 文献集（rewind→A2.literature_search）
  5. 打回（rejected）
- ▶ 红线：`machine_options` 拒 `skipped`，故无"跳过"
- **修订键** `EDITABLE_KEYS["A4.data_extraction"]` = `extracted_rows, pdf_dir`

### B4 质量门（红线）— fallback 通用
- **标题**：质量门（默认 `_ccm_title`）
- **摘要/告警**：无专属 builder → 不渲染摘要行、无告警
- **菜单**（`_fallback_options` `flow_menu.py:673`）：
  1. 批准（approved）　2. 打回（rejected）
- ▶ 不含"修订"：`EDITABLE_KEYS["B4.quality_gate"]` 含 `report`，但 fallback 故意不生成 revised 项（B/C 未实现字段级修订 UI，避免选了无字段可改）

### C1 初稿（软停）— fallback 通用
- **标题**：初稿
- **菜单**（fallback）：
  1. 批准（approved）　2. 跳过（skipped）　3. 打回（rejected）
- ▶ 不含"修订 manuscript/sections"（`EDITABLE_KEYS["C1.draft"]` = `manuscript, sections`，但 fallback 未暴露）

### C3 参考核验 / C4 投稿前 QA（均红线）— fallback 通用
- 同 B4：`[1]` 批准　`[2]` 打回

### handoff_confirm（块间交接闸，非节点）
- **菜单**（`_handoff_options` `flow_menu.py:648`）：
  1. 批准进入下一块（approved）　2. 打回（rejected）

### done（终态）
- 无菜单，仅显示 ✅

---

## 4. 防漂移过滤（`_filter_options` `flow_menu.py:904`）

每个 decision 选项都会过此关：
- **decision 项**：`action` 必须 ∈ `machine_options(sess,aw)`（红线自动挡掉 skip）
- **revise 项**：`key` 必须 ∈ `EDITABLE_KEYS[sid]`，否则标 `blocked`（不静默丢）
- 过滤后**重新连续编号**

---

## 5. 红线 / 软停 / 交接 的 action 派生（`machine_options` `flow_menu.py:277`）

| 闸类 | 节点 | 状态机允许集 |
|---|---|---|
| 红线 | A4 / B4 / C3 / C4 | `approved, revised, rejected`（无 skipped） |
| 软停 | A1 / A2 / C1 | `approved, revised, skipped, rejected` |
| 交接 | handoff_confirm | `approved, rejected` |

⚠️ **状态机允许集 ≠ 菜单展示集**：菜单由 builder/fallback 决定，可**窄于**允许集（如 A1 不展示 skip、B4 不展示 revised）。这是**有意收窄**，不是 bug。收窄的 menu 项由 builder 主动不生成，而非被 `_filter_options` 判掉。

---

## 6. 已知有意缺口（维护者须知，非缺陷）

1. **B/C 节点（B4/C1/C3/C4）用 fallback 通用菜单，仅 `[批准/打回]`（C1 含跳过），无字段级"修订"入口。**
   `EDITABLE_KEYS` 已为 B4=`report`、C1=`manuscript,sections` 预留，但 fallback 未生成 revised 项。
   补节点专属细化菜单时，在 `_OPTION_BUILDERS` / `_SUMMARY_BUILDERS` 注册对应 builder 即可（见 §8）。
2. **A1/A2 软停节点在菜单中隐藏 skip**（仅状态机语义保留、菜单不展示）。
   这是 2026-09-10/11 用户裁定，与旧设计稿（软停显式带[跳过]）相反，维持现状。

---

## 7. 旧会话兼容

合并前会话停在 `A3.screening` → 渲染**投影**到 A2（摘要/选项/标题全用 A2），顶部加黄字
"本会话创建于 A2/A3 合并之前…"，但**决策仍走真实 sid**（`_LEGACY_SID_ALIAS` `flow_menu.py:714`）。

---

## 9. 独立启动架构（A / B / C 三阶段各自可独立入口）

**目标**：ABC 三阶段都应能从对应阶段作为入口独立启动，而非只能从 A1 一条线走到底。

### 9.1 当前能力（2026-09-15 实现并验证）

| 入口 | 函数 / 接口 | 机制 | 状态 |
|---|---|---|---|
| **A**（全流水线）| `run_fullflow(topic)` / `POST /api/start` | 跑 Block A，遇闸即停 | ✅ |
| **A4**（自备 PDF）| `run_fastpath(topic,"pdf",a4_result=)` / `POST /api/start_data?data_mode=pdf` | 跳过 A1/A2，停在 A4 红线 | ✅ |
| **B**（自备抽取数据）| `run_fastpath(topic,"raw_csv",rows=)` / `POST /api/start_data?data_mode=raw_csv` | 跳过整块 A，注入 rows→B1，跑到 B4 红线 | ✅ |
| **C**（自备 B 信封）| `run_fastpath(topic,"draft",b_env=)` / `POST /api/start_data?data_mode=draft` | 跳过 A+B，注入 b_env，停在 C1 软停 | ✅ |

### 9.2 实现形态

**沿用 `run_fastpath` 魔法 `data_mode` 模式**（而非原设想的统一 `run_fullflow(..., start_stage=...)`）：

- 三入口统一由 `run_fastpath(topic, data_mode, ...)` 承载：
  - `raw_csv` → 跳过 Block A，注入 extracted_rows，跑 B1-B4 停在 B4 红线
  - `pdf` → 跳过 A1/A2，停在 A4 红线
  - `draft` → 跳过 A+B（A/B 块均标 done），注入用户 B 信封（`b_env`），再 `_advance` 跑 Block C
- `b_env` **必填**（用户 2026-09-15 裁定）：C2/C3/C4 需要 Block B 上下文才能跑，从 C 起必须携带 Block B 信封。
- C1 软停后走标准续跑链路：`resume_fullflow(decision={"action":"approved","stage_id":"C1.draft"})`
  → `_advance` → `run_block_c` 中 `_soft_stop` 因持有 C1 approved 凭据放行 → C2(auto) → C3(红线) → C4(红线) 终闸。

**菜单层零改动**：flow_menu 对任意暂停节点渲染菜单，与入口无关（§1/§2）。C1 软停在 `_fallback_options` 兜底下产出 `[批准/跳过/打回]`，与 A1/A2 软停行为同源。

### 9.3 验证结果（2026-09-15 实跑）

| 入口 | 实测 cursor | 菜单 | 验证文件 |
|---|---|---|---|
| `draft` | `{'block':'C','stage_id':'C1.draft','await_kind':'pause'}` | `[批准,跳过,打回]` | `_verify_draft_entry.py`（已跑，PASSED） |

### 9.4 同步落点（实现时一并改）

- `adapters/fullflow.py`：`run_fastpath` 新增 `data_mode="draft"` 分支（含 `b_env` 必填校验）+ docstring。
- `adapters/workbench/server.py`：`/api/start_data` 新增 `b_env_text` Form 参数 + `data_mode="draft"` 分支（两种录入：粘贴 JSON / 上传 `.json` 文件）。
- `scripts/flow_menu.py`：无需改（菜单层已 stage-agnostic）。
- 回归：`tests/test_flow_menu.py` 189 PASS / 0 FAIL。

### 9.5 已知缺口

- 用户自备 B 信封需满足 `_extract_b_summary` 格式（至少含 `pairwise/grade/nma/overclaims/critical`）；不满足时 `c1_draft` 会用空值填充初稿。前端应明确提示用户上传 `blocks.B.envelope` JSON。
- `run_fastpath("draft")` 不生成 Excel 交付物（`AUTO_EXPORT_ON_APPROVE` 仅含 A2）；C1 软停后如需"导出改稿"，后续按需补。

---

## 10. 改菜单时的同步落点（防再次"靠 code 反推"）

改动任一停靠点菜单，必须同步以下位置，并跑 `tests/test_flow_menu.py`：
- `scripts/flow_menu.py`：`_OPTION_BUILDERS` / `_SUMMARY_BUILDERS` / `_WARN_BUILDERS`（注册）
- `scripts/flow_menu.py`：对应 `_aN_options` / `_aN_summary` 函数体，及 `_fallback_options`（兜底）
- `adapters/fullflow.py`：`EDITABLE_KEYS`（revise 项键）、`DEFAULT_PAUSE_AT`（停靠点增删）、`GATE_TO_STAGE`/`STAGE_TO_GATE`（红线增删）
- `adapters/workbench/form_schema.py`：`STAGE_ORDER`（节点数/顺序）、`SCHEMA` 各节点 `gate_type`
- 节点数若变，同步本文件 §2 表与所有"11 节点"表述

---

_最后更新：2026-09-15（v0.2：§9 C 入口已落地并验证）_
