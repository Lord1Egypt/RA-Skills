# Fullflow HITL 编排器设计规格（v0.1.0 · 设计期草稿）

> 版本：`v0.1.0` ｜ 阶段：**设计期草稿（开发期冻结，不发布）** ｜ 日期：2026-08-31
> 上游契约：`contracts/pipeline_stage/v1.0.0/SPEC.md`（per-stage 信封）
> 设计原则（用户 2026-08-31 定）：**人-AI 协作，非全自动**——低准确度环节随时可打断、改人工介入。

> ⚠️ **2026-09-10 事后变更（D21，A2/A3 合并）**：Block A 的阶段序列已由
> `A1→A2→A3→A4` 改为 **`A1→A2(文献集)→A4`**——原独立 A3 初筛并入 A2（同节点内去重 +
> 规则初筛，单节点单表）。本文中所有出现 `A3.screening` / 四阶段序列的示例均为**2026-08-31
> 当时的冻结稿，保留作历史记录**；当前实现以 `adapters/block_a.py`（`BLOCK_A_SEQUENCE`）、
> `adapters/fullflow.py`（`DEFAULT_PAUSE_AT` / `EDITABLE_KEYS`）与
> `references/conversation_flow_menu.md` 为准。

---

## 0. 目标 / 非目标

### 目标
1. 把 Block A（方向/文献/数据准备）→ Block B（分析）→ Block C（撰稿）串成一条**可交互流水线**，数据自动传递。
2. 每个低准确度环节提供**人工闸**：暂停 → 展示 AI 草稿 → 人工「确认 / 修改 / 跳过」→ 把人工结果**回写信封**后续跑。
3. 支持**中断后恢复**：会话状态落盘 JSON，任意时刻可从上次闸位续跑。
4. 复用既有原语（信封结构、`_REDLINE_GATES`、`_decision_approves`、`extraction_guard`），**不重造闸逻辑**。

### 非目标（本版不做）
- ❌ 不做全自动（控制器**绝不**伪造人工决策；🔴 闸只能由人放行）。
- ❌ 不部署 coze 端 A/C 图（A1/A3/A4/C3 的 AI 大脑接管属后续 Phase）。
- ❌ 不验证 ct-literature tool_card 真实接线（G5，后续单独做）。
- ❌ 不改三平台发布状态（DEV_POLICY.json 冻结中）。

---

## 1. 架构位置

```
agent / CLI
    │  调 run_fullflow / resume_fullflow
    ▼
adapters/fullflow.py   ← 新增：薄交互控制器（本 spec 主体）
    │  复用 ↓（不修改其闸语义）
    ├── adapters/block_a.py   run_block_a(...)   A1→A2→A3→A4
    ├── adapters/block_b.py   run_block_b(...)   B1→B2→B3→B4
    ├── adapters/block_c.py   run_block_c(...)   C1→C2→C3→C4
    └── adapters/coze_client.py  _REDLINE_GATES / 信封常量
```

控制器是**薄层**：只做「暂停调度 + 人工决策簿记 + 数据接缝传递 + 会话持久化」，阶段逻辑全部留在三块内。

---

## 2. 既有原语（已核实，直接复用）

| 原语 | 位置 | 语义 |
|---|---|---|
| 信封 | 三块返回值 | `{pipeline_id, pipeline, stages[], attachments[], tool_card_outputs[], done, await_human, gate, final, human_decisions[]}` |
| 阶段记录 | `_mk_stage` | `{mode:"stage", stage:{id,index,total,status,prev_stage_id}, stage_result, next_human_action, tool_cards[], _gate_blocked}` |
| 人工动作提示 | `next_human_action` | `{type:"approve", prompt, required:bool, gate:str}` |
| 红线闸集合 | `coze_client._REDLINE_GATES` | `{extraction_review(A4), final_inclusion(B4), reference_verification(C3), manuscript_approval(C4)}` |
| 放行凭据 | `human_decision` | `{"stage_id": <sid>, "action": "approved"}`，`_decision_approves()` 判定 |
| 提取守卫 | `scripts/extraction_guard.py` | 未 `stamp --confirm` 的 CSV → `META_STATUS=unverified_extraction` |

**关键既有行为**：三块当前**一次性跑完本块全部阶段**，仅在 🔴 红线闸处提前返回（`done=False, await_human=True`）。软停（A1/A3 的 `status="await_human"`）**不会**中断本块执行。

---

## 3. 停靠点（Pause Points）——「随时打断」的三档粒度

| 档位 | 触发点 | 实现方式 |
|---|---|---|
| P1 块间停靠 | A 完成 → 进 B 前；B 完成 → 进 C 前 | 控制器默认行为，**无需改块** |
| P2 红线闸 | A4/B4/C3/C4（`_gate_blocked=True`） | 三块已有，控制器转发给人工 |
| P3 任意阶段停靠 | 用户指定的 `pause_at={"A1","A3",...}` | **三块新增 `pause_at` 参数**（向后兼容，默认 `None`=现状） |

**P3 的块内改动（最小侵入）**：`run_block_*` 每算完一个阶段，若 `stage.id ∈ pause_at` 且本调用未带对应人工决策 → 立即返回 `{done:False, await_human:True, gate:<软闸名>, final:<该阶段>, ...}`。默认 `pause_at=None` 时行为与现状逐字节一致（回归由现有测试保证）。

### 默认停靠点配置
```python
DEFAULT_PAUSE_AT = {
    "A1.topic_selection",    # 选题（低准确度：本地启发式 PICOS 须人工确认）
    "A3.screening",          # 筛选（易带偏）
    "A4.data_extraction",    # 🔴 红线
    "B4.quality_gate",       # 🔴 红线（final_inclusion）
    "C1.draft",              # 初稿人工改
    "C3.ref_verify",         # 🔴 红线
    "C4.evidence_qa",        # 🔴 红线终闸
}
```
（B1–B3 计算由 AI 高准确完成，默认不停靠；用户可用 `pause_at` 自行加停。）

---

## 4. 控制器接口

新增模块 `adapters/fullflow.py`，两个入口 + 一个会话类：

```python
def run_fullflow(topic: str, *,
                 max_results: int = 50, year_from: int | None = None,
                 effect_measure: str = "OR", nma: bool = False,
                 pause_at: set[str] | None = DEFAULT_PAUSE_AT,
                 extraction_table: str | None = None,   # 人工已备好的提取 CSV（可选）
                 session_dir: str = ".",                # 会话 JSON 落盘目录
                 debug: bool = False) -> dict:
    """启动 fullflow：跑 Block A，遇停靠点即停。
    返回 = 当前块信封 + 控制器层字段（见 §5 FullflowView）。"""

def resume_fullflow(session_path: str, decision: dict, *,
                    debug: bool = False) -> dict:
    """带人工决策续跑。decision 见 §6。自动判断该进下一阶段/下一块/结束。
    返回同 run_fullflow。"""

class FullflowSession:
    """会话状态（§7 schema）的加载/保存/游标推进。路径 <session_dir>/fullflow_session_<pipeline_id>.json"""
```

**agent-mediated 为主交互模式**（CLI 交互循环不做进 v0.1：agent 收到 `await_human` 信封 → 渲染给用户 → 收集答复 → 调 `resume_fullflow`。`pause_at=None` + 无人值守时等价于现状的一次性跑块）。

---

## 5. 控制器返回视图（FullflowView）

在块信封之上追加控制器层字段（不动块信封原字段）：

```jsonc
{
  // ...原块信封字段...
  "fullflow": {
    "session_path": ".../fullflow_session_ff_xxx.json",
    "cursor": { "block": "A", "stage_id": "A4.data_extraction" },
    "await": {
      "kind": "gate" | "pause" | "handoff_confirm" | "done",
      "gate": "extraction_review",          // kind=gate 时
      "stage_id": "A4.data_extraction",
      "prompt": "请人工核验提取数据…",        // 透传 nha.prompt
      "options": ["approve", "revise", "reject"],
      "editable_payload": { ... }            // 可被 revise 替换的 stage_result 键
    },
    "handoff_preview": {                     // kind=handoff_confirm 时（进 B 前）
      "next": "Block B", "n_studies": 12, "fields": ["study","te","sete",...]
    }
  }
}
```

---

## 6. 人工决策（HumanDecision）——统一 schema 与回写

### 6.1 决策 schema（控制器层，比块层凭据 richer）

```jsonc
{
  "decision_id": "d-<uuid>",
  "stage_id": "A4.data_extraction",
  "gate": "extraction_review",            // 软停时为 null
  "action": "approved" | "revised" | "skipped" | "rejected",
  "revision": null | { ... },             // action=revised 时：替换后的 stage_result 载荷
  "note": "人工备注（可选）",
  "decided_by": "user",
  "decided_at": "2026-08-31T15:40:00+08:00"
}
```

### 6.2 动作语义

| action | 语义 | 红线闸可用 | 软停可用 | 回写行为 |
|---|---|---|---|---|
| `approved` | 认可 AI 草稿，放行 | ✅ | ✅ | 决策追加进 `envelope.human_decisions[]` |
| `revised` | 人工改了数据/文本，以 revision 替换后放行 | ✅ | ✅ | revision **覆盖**对应 `stage_result`（键见 editable_payload），再追加决策 |
| `skipped` | 跳过该停靠（仅软停） | ❌ 拒绝 | ✅ | 决策追加，继续跑 |
| `rejected` | 打回重做（终止本块，等新输入） | ✅ | ✅ | 会话停在原地，`await.kind="gate"` 重新出 |

### 6.3 与块层凭据的降级映射（关键兼容点）

块层 `_decision_approves` 只认 `{"stage_id", "action": "approved"}`。控制器续跑时映射：
- `approved` → 原样传 `{"stage_id": ..., "action": "approved"}`；
- `revised` → **先**把 revision 写进本次调用的输入参数（A4→`extraction_table` 或块内替换、C1→draft 文本），**再**传 approved 凭据。即：**revision 永远走输入参数，不走块层凭据**——块层代码零改动即可消费人工修改。
- `rejected` / `skipped` → 不传凭据（块自然重新停回闸/继续）。

### 6.4 数据接缝（revision 落点）

| 接缝 | 上游产物 | 下游入参 | revise 落点 |
|---|---|---|---|
| A→B | A4 `extracted_rows` | `run_block_b(studies=...)` | revision 中的 rows 直接作为 studies 传入 |
| B→C | B 信封 | `run_block_c(b_env=...)`（已有 `_extract_b_summary`） | B4 revise → 更新 b_env 后再传 |
| A 内 | A2 `studies` → A3 → A4 | 块内已串 | A3 revise 的 screened 名单影响 A4 输入 |

---

## 7. 会话持久化（FullflowSession schema）

```jsonc
{
  "session_version": "0.1.0",
  "pipeline_id": "ff-<uuid>",
  "topic": "...",
  "created_at": "...", "updated_at": "...",
  "cfg": { "max_results": 50, "effect_measure": "OR", "nma": false, "pause_at": [...] },
  "cursor": { "block": "A" | "B" | "C" | "done", "stage_id": "...", "await_kind": "gate|pause|handoff_confirm|done" },
  "blocks": {
    "A": { "envelope": { ... }, "status": "await_human | done" },
    "B": { "envelope": { ... }, "status": "pending | ..." },
    "C": { "envelope": { ... }, "status": "pending | ..." }
  },
  "human_decisions": [ { ...§6.1... } ],
  "handoff": { "studies_for_b": [ ... A4 放行后的 rows ... ] }
}
```

- 每次停靠/续跑后原子落盘（临时文件 + rename）。
- `resume_fullflow` 读会话 → 据 cursor + decision 推进；会话文件即**审计日志**（全部人工决策留痕）。

---

## 8. 红线与边界

1. 🔴 **控制器绝不自动 approve**：`resume_fullflow` 收到空/缺 decision 时只回视图，不推进。
2. 🔴 required 闸（A4/B4/C3/C4）不接受 `skipped`；软停才可 skip。
3. 🔴 B 计算仍走 coze 唯一路径（`run_block_b` → `run_stage` → ct-meta2）；coze 失败返回结构化错误，不回退本地。
4. A4 若来自 `extract_assist.py` 的 CSV，仍受 `extraction_guard` 约束（未 `stamp --confirm` 拦截）——控制器在进 B 前再调一次守卫（双保险）。
5. 会话文件含研究数据，落用户工作区（`session_dir`），不进技能目录、不入发布包（发布排除清单已含 `tests/` 等，`fullflow_session_*.json` 由命名约定排除，见 §10）。

---

## 9. 测试计划（确定性、离线、不触 coze/网络）

`adapters/tests/test_fullflow.py`：
1. **向后兼容**：`pause_at=None` 时 `run_block_a/b/c` 输出与现状一致（golden 比对）。
2. **P3 停靠**：`pause_at={"A1"}` → A1 后返回 await_human；带 approved 续跑 → 到 A3 再停。
3. **红线闸**：A4 无决策停闸；`revised`（替换 extracted_rows）→ studies 正确传入 B。
4. **降级映射**：revised → 输入参数替换 + approved 凭据，块层无感知。
5. **会话**：落盘→重载→cursor 一致；rejected 后重停同闸。
6. **守卫双保险**：未核验 CSV 进 B 被拦（exit 3 语义）。
7. **skip 语义**：软停 skip 通过、红线闸 skip 被拒。

---

## 10. 发布排除（冻结期约定）

- `adapters/fullflow.py` 属运行时代码，随技能包发布（开发期结束后）。
- `fullflow_session_*.json` / `*_session_*.json` 不入发布包。
- 本 spec 在 `contracts/fullflow/v0.1.0/`，随包发布（同 pipeline_stage 契约先例）。

---

## 11. 实施清单（待批准后执行）

| # | 事项 | 改动面 |
|---|---|---|
| 1 | 三块新增 `pause_at` 参数（P3 停靠） | block_a/b/c.py 各 ~10 行 |
| 2 | `adapters/fullflow.py`：run_fullflow / resume_fullflow / FullflowSession | 新文件 |
| 3 | B 进前置守卫复检（extraction_guard 双保险） | fullflow.py 内 |
| 4 | `adapters/tests/test_fullflow.py`（§9 七项） | 新文件 |
| 5 | CHANGELOG 条目（开发期，不发版） | CHANGELOG.md |
| 6 | `deploy_retest` 回归（G1–G8 应保持全绿；G9 冻结预期 NO-GO） | 仅运行 |
