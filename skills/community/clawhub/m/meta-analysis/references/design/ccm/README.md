# CCM — Conversation Context Menu / 对话上下文菜单（设计归档）

> **状态：设计完成 · 已实现（2026-09-10）。** 本目录只放设计文档；
> **可运行代码在 `scripts/flow_menu.py`，规范版在 `references/conversation_flow_menu.md`，
> 回归在 `tests/test_flow_menu.py`（153 PASS / 0 FAIL）。** 以规范版为准，本目录仅存设计过程。
> **背景：** 工作台（`adapters/workbench/`）已有完整的 12 节点渲染契约（`form_schema.py`）与 HITL 状态机（`adapters/fullflow.py`），但**对话侧没有菜单**——每轮展示什么、闸位有哪些选项，全靠 LLM 即兴，同一节点两次渲染可能不一致。
> CCM 的目标是给同一套 schema 加一层「对话投影」，**不新建第二套流程定义**。

---

## 归档清单

| 文件 | 状态 | 内容 |
|---|---|---|
| **`10_A_stage_menu_spec_v1.0.md`** | 🗄 已被收编 | A 阶段四节点菜单规格 —— **内容已收编进规范版 `references/conversation_flow_menu.md`，以那份为准**；此处仅存设计过程 |
| `03_v0.4_A2fix_A3_contract.md` | ✅ 已实施 | A2 解释器路径修复记录（含端到端回归证据）+ A3 纯文件交接契约 + A4 按清单直下 |
| `02_v0.3_A2A3_handoff.md` | ✅ 已实施 | A2/A3 向 ct-literature 移交的可行性评估、简化后菜单、风险 |
| `01_framework_v0.2_draft.md` | 📐 框架草案 | 三层菜单（L0 导航条 / L1 节点菜单 / L2 字段菜单）+ **操作四策略分流**（原生迁移 · 降级简化 · 文件交接 · **跳过转出**）+ 四问判定 + `defer` 语义 |
| `00_framework_v0.1_superseded.md` | 🗄 存档 | 最初框架，已被 v0.2 取代（保留备查） |

> ⚠️ 阅读顺序：先 `01`（拿框架与分流规则），再 **`references/conversation_flow_menu.md`**（拿现行规范与落地细节）。`02`/`03` 是已实施的改动记录，`00`/`10` 可跳过。
>
> **实测遗留（2026-09-10）**：规范版 **§7.1 会话版本漂移** + **§8 的 D18 / D19**
> （A4 下载配额与菜单未暴露 `fetch_log`）来自真实会话验收，**尚未修复**，交接前先读那两节。

---

## 框架要点（来自 `01`，尚未实现）

**三层菜单**
- **L0 上下文导航条** —— 12 节点压一行，每轮必贴（解决「每轮无位置感」）
- **L1 节点菜单** —— 节点头 + 数据摘要 + 该节点专属选项
- **L2 字段菜单** —— 只列该节点 `EDITABLE_KEYS`；全局指令 `/flow` `/node` `/rewind` `/explain` `/raw` `/workbench` `/export`

**操作四策略**（对话侧不是工作台的能力等价物）

| 策略 | 判据 | 例 |
|---|---|---|
| 原生迁移 | 读 + 单决策 | 9 个节点的主体面板 |
| 降级简化 | 可自动化掉人工步骤 | 上传按 DOI/标题自动匹配，只问未匹配项 |
| 文件交接 | >10 条逐条编辑，表格更合适 | A3 裁决表（⬇ 导出 / ⬆ 传回） |
| **跳过转出** | 需视觉/空间信息、多选拖拽指派 | PDF 页码预览、文件↔条目映射 |

**四问判定**（命中任一即转出，不进对话）
1. 需要视觉/空间信息（PDF 页面、图片、并排）？
2. 涉及 >10 条记录逐条编辑？
3. 需要多选/拖拽/指派（文件↔条目映射）？
4. 只是读 + 单决策？→ 优先进

**`defer` ≠ `skip`（关键概念）**

| | `skip` | `defer` |
|---|---|---|
| 含义 | 本会话不再停靠该节点，按默认值放行 | 人工动作**未完成**，流程**不得前进** |
| 适用 | 仅软停 | 任意节点，尤其 🔴 |
| 审计 | 写 `human_decisions` | **不写**，改写 `pending_actions`（双端共享待办） |
| 效果 | 下游继续跑 | 闸位保持，`approve` 被拒 |

> **混淆这两者 = 让红线的人工核验被静默绕过。** 因此 `pending_actions` 非空时须在**脚本层**直接拒绝放行，不靠提示词约束。

**选项穷举原则** —— GUI 的选项是「可见的」，对话里用户不知道有哪些选项，所以**选项必须由我方穷举编号**（禁止「你要继续吗？」这类开放式问法）；≤3 个用卡片，≥4 用编号文本菜单；🔴 节点选项集中**禁止出现「跳过」**（由 `_REDLINE_GATES` 派生过滤）。

---

## 实现时的硬约束

1. **状态真源只有一个**：复用工作台 `fullflow_session_ff-*.json`，CCM 不另起一套。收益是**对话 ↔ 工作台可中途无缝互切**。
2. **菜单由代码产出、LLM 只转述** —— 避免同节点两次渲染不一致。
3. **`/rewind` 候选集须服务端派生** —— `workbench.html:737` 的候选枚举是纯 JS（块序 + 块内次序 + `curIdx=-1`），对话侧**不可重写这套逻辑**（第二份真源必然漂移），应从 `/api/session` 的 `progress`/`next_human_action` 派生。
4. **🔴 选项由 `cc._REDLINE_GATES` 派生** —— 不硬编码第二份清单。
5. **不干扰纯算数请求** —— 「合并这 5 项 OR」/ NMA / 敏感性分析等**完全不出现 CCM**，保住「描述即执行」卖点。
6. **回显块前缀分离** —— CCM 用 `## 当前流程设定 / Current pipeline settings:`，与计算轨道的 `## 当前分析设定:` 互不覆盖。

---

## 待落地清单

> ⚠️ **以下清单已于 2026-09-10 落地**（`scripts/flow_menu.py` + `tests/test_flow_menu.py`）。
> 保留原文仅作设计意图对照；实现细节与偏差以 `references/conversation_flow_menu.md` 为准。

| 项 | 说明 |
|---|---|
| `scripts/flow_menu.py` | 确定性 render / status / decide / rewind |
| `form_schema.py` `menu_for()` | 12 节点 → 对话投影 |
| `references/conversation_flow_menu.md` | 规范（当前内容即本目录 `10_A_stage_menu_spec_v1.0.md`） |
| `adapters/fullflow.py` | 加 `pending_actions` + `pending` 闸态（**核心状态机改动，须同步 `contracts/fullflow/v0.1.0/SPEC.md`**） |
| `tests/` | 冒烟：12 节点 × zh/en 无缺键；🔴 节点菜单不含 skip；软停节点含 skip |
| `references/interactive_menu.md` / `references/speed-discipline.md` / `SKILL.md` | 小改 |

**实现时的实际偏差（3 处，均已在规范版记录）**
1. 未新增 `form_schema.menu_for()`——投影实现在 `flow_menu.py` 内（避免 form_schema 反向依赖 fullflow）；
   仅向 form_schema **增量**加了 `TITLE_EN` + `title_for()` 以支持 en 标题。
2. `pending_actions` 闸态**仍未加**（D8）——A4 非 OA 未补传的拦截暂未闭合，属未决项。
3. `A1/A2/A3` 的 `by_source 缺库` 判据改为**保守版**：不拿「可调度源全集」当期望（必然误报），
   改为 `status≠ok` / 空结果 / 仅 1 库 硬判 + `--expected-sources` 显式比对。

**归属**：先在 meta 内验证，稳定后可回写 ct-base 作第三原型 Type-Flow（D6，二期）。
