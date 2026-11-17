# 架构终态迁移规格（v0.1.0 · 设计期草稿）

> 版本：`v0.1.0` ｜ 阶段：**设计期草稿（开发期冻结，不发布、不部署）** ｜ 日期：2026-09-01
> 上游契约：`contracts/pipeline_stage/v1.0.0/SPEC.md`（per-stage 信封）、`contracts/fullflow/v0.1.0/SPEC.md`（HITL 编排）
> 决策来源：**架构终态原则（用户 2026-09-01 明确）** —— 有价值的分析/计算代码一律上 coze（保护代码 + 付费化），A/B/C 全上云，本地只留「编排 + 收发」。

---

## 0. 目标 / 非目标

### 目标
1. **coze = 唯一计算真相源**。A/B/C 三块的所有有价值的分析/计算（选题、筛选、抽取、pairwise/NMA、GRADE、过度声明、质量门、起草、AI 审、参考文献核验、证据 QA）全部在 coze 工作流内产出。
2. **本地只保留编排与收发**：`fullflow.py`（HITL 三档停靠）、`coze_client.py`（`run_stage`/`run_pipeline` 收发 + 红线闸）、`rendering.py`（展示层）、`contracts/`（信封规范）。
3. **发布即薄客户端**：计算代码永不随 GitHub/ClawHub/SkillHub 包分发（`adapters/coze/` 早已 gitignore/clawhubignore 排除）；coze 鉴权限流天然实现「付费才能用」。

### 非目标（本 spec 不做）
- ❌ 不修改发布冻结状态（DEV_POLICY.json）。所有 coze 节点部署、git push、三平台发布**等用户宣布「开发期结束」**才执行。
- ❌ 不改 coze R 引擎算法本身（已在 coze 侧，本 spec 只迁移「大脑」节点、不重造 R 计算）。
- ❌ 不引入本地离线计算兜底（已与用户确认：无 coze 授权即无法计算，是付费化预期代价）。

---

## 1. 现状盘点（2026-09-01，B 阶段已完成）

### 1.1 已在 coze（无需迁移）
| 能力 | 位置 | 说明 |
|---|---|---|
| R 引擎（meta/metafor/netmeta + dispatcher） | `adapters/coze/src/r_engine/` | 已 gitignore，计算真相源 |
| B1 pairwise（R meta） | coze `meta_analysis` 节点 | `run_analysis`/`run_block_b` 已走 `run_stage` |
| S3 外置 / 飞书归因 / 鉴权限流 | coze 工作流 | 付费化基础 |

### 1.2 B 阶段已落地（2026-09-01）
- `block_b.b1_meta_analysis` 默认 `engine="coze"`，B1 经 `run_stage` 发 ct-meta2；coze `stats` 经 `_coze_stats_to_pairwise` 映射为本地 `pairwise` 形状（**对数尺度同构**，B2/B3/B4 零行为变更）。
- `b1_pairwise_python` 降级为 **仅回归/调试 oracle**（`engine="local"`），非运行路径。
- **已删除** `adapters/_dev/local_engine.py`（本地 R 引擎残留）。
- `test_block_b.py` 用 `run_stage` 桩离线验证翻译层（20 测试绿）。

### 1.3 仍赖在本地、待迁移（本 spec 主体）
| 模块 | 函数 | 性质 | 备注 |
|---|---|---|---|
| `block_a.py` | `a1_topic_selection` | 选题启发式 | AI 大脑，应迁 coze |
| `block_a.py` | `a1_registry_check` | 注册库查重探针 | 可保留本地 I/O（ct-registry 调用），大脑逻辑迁 coze |
| `block_a.py` | `a2_build_tool_card` / `a2_literature_search` | 检索委派 | I/O 编排可留本地；结果解析可留本地 |
| `block_a.py` | `a3_screening` | 筛选启发式 | AI 大脑，应迁 coze |
| `block_a.py` | `a4_data_extraction` | 数据抽取 | AI 抽取 + A4 红线闸，应迁 coze |
| `block_b.py` | `b1_nma_r` | 本地 R netmeta | 待迁 coze NMA 节点（移除本地 R 依赖） |
| `block_b.py` | `b2_grade` | GRADE 启发式 | 计算大脑，应迁 coze |
| `block_b.py` | `detect_overclaims` / `b3` | 过度声明检测 | 计算大脑，应迁 coze |
| `block_b.py` | `b4_quality_gate` | 质量门 | 计算 + 红线闸，应迁 coze |
| `block_c.py` | `c1_draft` | 起草 | AI 大脑，应迁 coze |
| `block_c.py` | `c2_ai_review` | AI 评审 | AI 大脑，应迁 coze |
| `block_c.py` | `c3_reference_verify` | 参考文献核验 | 应迁 coze（对接 C3 红线闸） |
| `block_c.py` | `c4_evidence_qa` | 证据 QA | 应迁 coze |
| 分诊/路由 | `classify`（fullflow 入口分流） | 轻量路由 | 若含非平凡逻辑也上云，纯路由可留本地 |

---

## 2. 目标架构

```
agent / CLI
   │  run_fullflow / resume_fullflow
   ▼
adapters/fullflow.py          ← 薄编排：三档停靠 + 人工决策簿记 + 会话持久化
   │  per-stage 信封
   ▼
adapters/coze_client.py       ← 唯一收发：run_stage / run_pipeline + 红线闸
   │  HTTPS → ct-meta2 /run
   ▼
coze 工作流（图引擎）
   ├── A 节点：a1 选题 / a3 筛选 / a4 抽取 (+ A4 extraction_review 红线)
   ├── B 节点：B1 pairwise(R) + NMA / B2 GRADE / B3 过度声明 / B4 质量门 (+ B4 final_inclusion 红线)
   ├── C 节点：c1 起草 / c2 AI审 / c3 参考文献核验 (+ C3 reference_verification 红线) / c4 证据QA
   ├── R 引擎（meta/metafor/netmeta）
   └── 飞书归因 / S3 外置 / 鉴权限流
   ▲
   │  stage_result（stats / figures / notes）
adapters/rendering.py         ← 仅展示层：HTML 报告 / SVG→PNG
```

**本地不得保留任何独立计算引擎**：所有数值结论均由 coze 产出，本地仅解析结构、呈现、编排。

---

## 3. 迁移清单（可执行 checklist）

状态：⬜ TODO  ⬜ DOING  ✅ DONE（每项含「现状 → 目标 → 改动 → 验证闸门」）

### M1 — coze A 节点部署（a1 / a3 / a4）
- **现状**：`block_a.py` 的 `a1_topic_selection` / `a3_screening` / `a4_data_extraction` 为本地启发式；A4 `extraction_review` 红线闸本地强执。
- **目标**：coze 图新增 A 节点，产出同构信封（`next_human_action` / `stages[]`），A4 闸在 coze 侧（或保留本地闸但数据由 coze 抽）。
- **改动**：`coze/src/graphs/graph.py` 扩 A 节点；`block_a.run_block_a` 改调 `run_stage`（仿 `b1_meta_analysis` coze 路径）。
- **验证闸门**：① coze 契约测试（envelope roundtrip）；② 用本地 `a1/a3/a4` 启发式作**回归基线**对比 coze 输出（人工抽审）；③ 绿后删本地 `a1/a3/a4` 计算体，保留信封构造。
- **状态**：⬜ TODO（部署类，等开发期结束）

### M2 — coze C 节点部署（c1 / c2 / c3 / c4）
- **现状**：`block_c.py` 的 `c1_draft` / `c2_ai_review` / `c3_reference_verify` / `c4_evidence_qa` 为本地 LLM/启发式。
- **目标**：coze 图新增 C 节点；C3 `reference_verification` 红线闸对接 coze。
- **改动**：`coze/src/graphs/graph.py` 扩 C 节点；`block_c.run_block_c` 改调 `run_stage`。
- **验证闸门**：① 契约测试；② 本地 `c1-c4` 作回归基线；③ 绿后删本地计算体。
- **状态**：⬜ TODO

### M3 — B2/B3/B4 上云（GRADE / 过度声明 / 质量门）
- **现状**：`b2_grade` / `detect_overclaims` / `b4_quality_gate` 本地启发式（`run_block_b` 已 coze-only 取 B1，但 B2-B4 仍本地）。
- **目标**：coze 图 B 节点内计算 GRADE/过度声明/质量门，B4 `final_inclusion` 红线在 coze 侧。
- **改动**：`coze` 扩 B 节点；`run_block_b` 的 B2-B4 改调 `run_stage`（保留 `_soft_stop`/`_REDLINE_GATES` 接线）。
- **验证闸门**：① 契约测试；② 本地 `b2/b3/b4` 作回归基线（尤其 GRADE 降级矩阵、OC1-OC12 命中、B4 闸阻断/放行）；③ 绿后删本地计算体。
- **状态**：⬜ TODO

### M4 — NMA 上云（移除本地 R 依赖）
- **现状**：`b1_nma_r` 调本机 `C:/Tools/R-4.6.1/bin/Rscript.exe`（本地 R 引擎）。
- **目标**：NMA 走 coze NMA 节点（netmeta），删除 `b1_nma_r` 与本地 R 调用。
- **改动**：`coze` 扩 NMA 节点；`b1_meta_analysis` 的 NMA 分支改调 `run_stage`；删除 `R_BIN` 相关 subprocess 调用。
- **验证闸门**：① coze NMA 契约测试（用 `TestB1NMAReal` 样本比对）；② 绿后删 `b1_nma_r` + `_NMA_R_SCRIPT`。
- **状态**：⬜ TODO

### M5 — 传输层统一（本地仅信封 + 收发）
- **目标**：`block_a/block_b/block_c` 三个驱动器收敛为「构造信封 → `run_stage` → 解析返回 → 驱动 HITL 闸」的薄封装；删除所有 `numpy`/`R` 直接计算。
- **改动**：抽公共 `_call_coze_stage(block, stage_id, payload)` 助手（已在 `b1_meta_analysis` 验证模式），三块复用。
- **状态**：⬜ TODO（依赖 M1-M4 节点就位）

### M6 — 删除本地回归 oracle（收尾）
- **现状**：`b1_pairwise_python` 作为 `engine="local"` 回归 oracle 残留。
- **目标**：M1-M4 全部绿后，把 oracle 逻辑**移入 `tests/`**（作为 coze 输出的回归对照），从 `adapters/` 运行时移除。
- **验证闸门**：oracle 仍在 `tests/` 中用于 coze vs 本地一致性比对；确认无运行时 import。
- **状态**：⬜ TODO（最末一步）

### M7 — SKILL.md 铁律更新
- **现状（2026-09-01 修订）**：SKILL.md §0 铁律 4 已改为「**Coze is the sole source of truth for computation**：所有数值计算在 coze R 引擎完成，本地仅编排+收发、无计算引擎；coze 不可达/未授权即抛结构化错误、绝不回退本地；无授权即无法计算（付费化预期代价）」。§3 执行模型段同步加粗「coze = sole computation source of truth；本地不保留计算引擎；无授权即无法计算」；§6 失败兜底段澄清「declined → 仅文本说明未使用云端分析，绝非本地计算替代」。
- **目标**：改为「**coze 为唯一计算真相源；本地不保留计算引擎；无授权即无法计算（付费化）**」——**已完成**。
- **改动**：SKILL.md（§0 铁律 4 / §3 执行模型 / §6 失败兜底）；README_zh-CN 经核查无「本地计算兜底」矛盾表述（仅「绝不传输」属数据出境同意、非计算），无需改。
- **状态**：✅ DONE

### M8 — 文档清扫
- **目标**：`adapters/README.md` / `AGENTS.md` / `requirements.txt` / `coze_client.py` 注释中移除「本地引擎 / 本地 numpy 兜底 / local_engine」等过期引用。
- **完成**（2026-09-01）：`run_analysis.py`/`coze_client.py` 头部（B 阶段）+ `README.md`/`AGENTS.md`/`requirements.txt`（M8）已全部清除对 `local_engine.py` 的「保留 / 仅参考」描述；该文件已于 2026-09-01 删除，无本地回退。
- **状态**：✅ DONE

### M9 — ct-literature tool_card 真实接线验证（G5）
- **现状**：`a2_literature_search` 委派 `ct-literature` 的接线未端到端验证。
- **目标**：开发期结束后用真实 `ct-literature` 技能做 A2 端到端验证。
- **状态**：⬜ TODO

### M10 — 发布（等开发期结束，统一三平台）
- **顺序**：GitHub → SkillHub → ClawHub（ClawHub 不传 `--version`）。
- **前置**：M1-M9 全绿 + `deploy_retest` G1-G9（G9 发布闸为冻结期预期 NO-GO，结束后再跑）。
- **状态**：⬜ TODO（发布类，红线管控）

---

## 4. 顺序与护栏

1. **M1-M4 为 coze 部署类**：必须等用户宣布「开发期结束」后，在 coze 侧新增 A/B/C/NMA 节点并部署，再回本地改 `run_block_*`。
2. **每步先「契约测试 + 本地 oracle 回归」后删本地**：删除本地计算体前，必须用现有本地启发式/`b1_pairwise_python` 作为**回归基线**对比 coze 输出，避免数值漂移。
3. **HITL 闸语义不变**：`_REDLINE_GATES`（A4/C3/B4）、`_decision_approves`、`_soft_stop`、信封结构在迁移中保持向后兼容（参考 `contracts/pipeline_stage/v1.0.0/BACKWARD_COMPAT.md`）。
4. **零离线计算**：迁移完成后，本地 `import numpy` 仅允许出现在 `tests/`（oracle），运行时模块不得再做数值计算。

---

## 5. 付费化与访问控制

- coze 工作流的**鉴权 + 限流**即付费闸门：未授权请求在 `coze_client` 侧抛 `AuthRequiredError`，结构化返回 `_auth_required=True`，绝不回退本地。
- 计算代码（R 引擎 + A/C 大脑）**恒不在发布包内**（`adapters/coze/` 已排除），外部无法获得源码 —— 满足「保护代码」诉求。
- 开源发布的技能包 = 编排 + 收发 + 展示 + 契约，对未授权用户是「能编排、不能算」的壳，符合付费化定位。

---

## 6. 回滚策略

- 单节点迁移失败 → 该块回退到「本地启发式 + coze_ready=False」占位（M1-M4 完成前本就是此态），不影响整体管线。
- coze 集群异常 → `run_stage` 返回 `coze_error`，`b1_meta_analysis` 已结构化返回错误（不崩、不谎报），由上层提示用户重试/授权。
- 全量迁移后无本地回退（设计使然，已与用户确认）。
