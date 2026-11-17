> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

> 📚 **填写说明/口径/教训**：见仓库维护资料 （R-51）；本文件只保留填写骨架与机械校验锚点。

# 项目状态机 — run/<项目名>/status.md

> ⚠️ **本文件含运行期遥测，按敏感文件处理**：仅留本文件，不得转录进交付物；项目归档默认排除 `status.md`，确需留档时只保留脱敏副本 `status.redacted.md`；分享前余额/可用性只留档位符号（✅/⚠️/❌），`sessionKey`/`session id` 不记录。历史标识兜底截断仅用前 8 字符 + `…` 或哈希前 12 位。

> 真源 = [`../_shared/真源/关键协议.md`](../_shared/真源/关键协议.md) §遥测收容。

> **运行期呈现留痕（四节点每次都填；仅记录主控动作，不冒充主人已阅读）**：
> `checkpoint_id=<唯一值>` / `checkpoint_presented=true|false` / `checkpoint_presented_at=<时间>` / `checkpoint_materials=<路径列表>` / `checkpoint_status=<awaiting_owner|reminded|pending_owner|decided|preauthorized>`（preauthorized 仅 run_mode=生产·全自动 合法） / `reminder_sent=<true|false>` / `pending_owner_at=<时间|n/a>` / `owner_response_received=<true|false>` / `owner_response_at=<时间|n/a>` / `owner_decision_normalized=<合法枚举值|n/a>`

> **留痕纪律**：进入节点先写 `checkpoint_presented=true`；发送轻提醒后才写 `reminder_sent=true`；超时只写 `checkpoint_status=pending_owner`，不得写 accepted。主人回复后核对同一 `checkpoint_id` 和材料版本，再写 `owner_response_received=true` 与规范化决策。**生产·全自动短路（v2.18.0）**：进入节点先验预授权记录——有效 ⇒ 不呈现卡，直接写 `checkpoint_status=preauthorized` + decision 落值 + basis，对话流留一行备案通知；缺失/含糊 ⇒ 按人在四环走（fail-closed）。

> **🔒 v2.12.54 R-2 节点 id 合法性**：§二 / §四 出现的节点 id 必须取自 `_shared/真源/phase-order.yaml`；**禁止自创**节点 id。
> **🔒 v2.12.54 R-3 Done 记账一致性**：`Done` 必须对应磁盘上存在且非空的产物；`Not Triggered` / `opt_out` / `pending_owner` / 产物缺失一律**不得计 Done**。

> **读取指引**：主控/子代理运行期**只读「一~四」节（~3K）** 维护状态；「方法论足迹」「执行韧化记录」「维护说明」「重写说明」是扩展段（~7K），按需查阅——无需要时不必全量读。
>
> **重写**：原 markdown 表格 7 列 + 主控 edit 频繁失败（空格漂移 / old_string 不匹配 / 重复行 bug）。**改为「4 段结构化纯文本」+ key:value 字段**，主控用 `**当前**: X` → `**当前**: Y` 替换策略，零空格漂移、零编辑摩擦。
>
> 失败必须留原因；任一行停留超阈值无进展 → 主控介入（按 `_shared/真源/主动介入机制.md` 硬卡阈值表，角色分级：T1-T3 10 / T4 12 / T5 15 / T6 15 / T7 12 / T9 10 / G14 8 分钟）。
> **T3 案例检索**：Phase 0 确认需要案例时即 spawn（cases=0 走空卡协议）；T3 worker 不可用 ⇒ 主控接管该节点并记录；T2 不再兼带案例，状态独立行。

## 一、项目元数据（key:value 替换，主控用 `**当前**: X` 策略）

> **🔒 2026-10-08 审计 R-2（C1）本节为派生视图，不是第二真相**：
> 本节字段值**必须**与 §二「角色状态」末个 ✅ 节点、§三「闸门清单」、§「人在环决策记录」、§4.9 `status_json` **一致**；
> 不一致时以**详情段**为准，并按 §六 对账第 3 项处理。**主控不得独立编辑本节去「追平」详情段** —— 两处各改一次即双份真相漂移。
> 治本理由（2026-10-06 实跑）：同一 `status.md` 头部写「已通过 Phase 5 验收」，而 §二 记 `Phase 3.5 = 未决策`、
> `T7.5 = ⬜ Inbox`、§4.9 `status_json.updated_at` 停在项目早期 —— 无对账门时全程无人报红。
> **写入顺序**：先改详情段 → 再同步本节派生字段 → 最后跑 §六 对账（判据真源 = `可发表性判定表.md` §六）。

**项目名**: <项目名>
**模式**: 学术论文 / 商业评论 / 行业分析 / 公众号深度长文
**当前阶段**（枚举由 `phase-order.yaml` 的 `phase_order` 生成，禁止手工维护）：`<当前 phase 值>`
**当前活动**: <一句话描述>
**最后更新**: YYYY-MM-DD HH:MM
**架构**: 多 Agent 九角色流水线（固定，不设总开关）。**worker 接管记录**（每节点失败时填一行；无失败留空）：<角色 / 原因 timeout|failed|no_artifact / 接管者=主控 / L1 影响>。**不记录宿主配置明细、不记 deny 原文**——论衡不读取宿主配置，OpenClaw 平台负责多 Agent 运行与工具策略。
**接管 L1 披露**: <无 worker 接管时填 `n/a`；有接管时必填：接管角色 / 原因 / 判定者=主控（L1）/ 交付说明须披露无法独立复核的残留风险>
**worker 终态**: <worker_not_started|worker_running|worker_failed|worker_empty_output|worker_timeout|main_controller_takeover|owner_decision_required|not_executed> / 原计划执行者=<角色> / 实际执行者=<角色|n/a> / 产物状态=<present|missing|empty|unverified>
> **终态纪律（B1-M1）**：`worker_empty_output` 不得记为成功；主控接管不得把原角色记为 `Done`；T9 只能 `retry_spawn_only`，耗尽后记 `missing_blind_review`，不得主控代笔。
**运行性质**: 生产·人在四环 / **生产·全自动** / **测试模式**（三值枚举，Phase 0「运行模式」拍板；真源 = [`运行模式对照表.md`](../_shared/真源/运行模式对照表.md)）
  - 生产·全自动 = Phase 0 一次性预授权（2.5 → approved+采用T4建议 / 3.5 → no_insight / 5 → accepted+对账照跑+delivery_readiness 机械判定；**预授权 ≠ 自动继续**，各节点仍写合法枚举值 + basis）
  - 测试模式 = 3 个节点自动通过，不具备交付效力（v2.12.38 语义不变）
  - **生产·全自动与测试模式均必须在此 + 任务简报 + 交付说明三处同步披露**；**T8 终检机械核对三处一致，缺任一 = P1 并重跑终检**（v2.12.43 纪律对全自动同样适用，v2.18.0 扩展）
**运行模式预授权**: run_mode=<生产·人在四环|生产·全自动|测试模式> / preauthorized_at=<Phase 0 时间|n/a> / preauthorization_basis=01-任务简报.md「运行模式」 / nodes_preauthorized=<phase2_5_outline, phase3_5_insight, phase5_acceptance|n/a>（仅生产·全自动填后两项）
**活体冒烟**: smoke_level=<n/a|L1|L2> / smoke_run_id=<n/a|唯一值> / smoke_started_at=<时间|n/a> / smoke_finished_at=<时间|n/a> / smoke_verdict=<pending|pass|fail>（L2 不得自动通过 owner_checkpoint）
**M 门**: v2.2.12 / v2.5.x
**数据信任档**: 全外发 / 混合 / 全人工（Phase 0 拍板）
  - 全外发：默认 web_search + tavily_search 检索，主人不投喂一手数据
  - 混合：部分一手（主人投喂 / 限定检索） + 部分 LLM 检索
  - 全人工：所有数据均为主人一手，LLM 不检索
**G14 状态**: enabled（目标语言含中文，必跑）/ selfcheck（轻量档内置自检）/ exempted_by_owner（主人显式豁免，已披露）/ n/a（纯外语，客观不适用）（按 Phase 0「目标语言」客观判定，全项目不变；位置 = Phase 4.4 前置，定稿前唯一一次）
**当前稿件**: draft_id=<唯一标识> / draft_version=v1 / 来源=T5
**draft_ref（B3）**: path=drafts/current_draft.md / sha256=<verified|unavailable> / section_manifest=<path|n/a> / changed_sections=<列表|n/a> / hash_status=<match|mismatch|unavailable> / resync=<not_needed|requested|completed>
**上下文指标（B3）**: raw_input_bytes=<数值|unavailable> / structured_output_bytes=<数值|unavailable> / context_reduction_ratio=<数值|unavailable> / critical_evidence_preserved=<true|false|unavailable> / locator_preserved=<true|false|unavailable> / false_negative_count=<数值|unavailable>
**审计修订轮**: 0 / 上限=2
**节点重入**: node_reentry=<reused|executed|forced> / reentry_probe_at=<时间|n/a> / reentry_evidence=<产物路径:字节|pending_owner_verification>
**T8 技术终检**: ⬜ 未完成 / ✅ 完成
**Phase 5 主人验收**: ⬜ 未决策 / ✅ accepted / 🔁 revision_requested / ↩ restart_phase / ⏸ deferred
**验收前置对账（R-2）**: reconciliation=<未跑|pass|fail|path_or_param_error> / 四项=<决策齐?报告齐?状态自洽?产物在盘?> / checked_at=<时间>
**交付就绪（R-3）**: delivery_readiness=<submission_ready|accepted_with_open_items>（**必填，禁留空**）/ 未闭合项=<路径或 n/a>
> **R-3 纪律**：`accepted` **不等于** `submission_ready`。本字段只在 §六 四项对账全过后才可填；取 `accepted_with_open_items` 时 `final/交付说明.md`「已知局限」段必须逐条列出未闭合项。判据真源 = `可发表性判定表.md` §六。

## ▲ 重要写入验证记录（B1-M2）

> 高风险文件写入后必须 read-back；未验证不得推进节点。`append:true` 不作为通用工具语义。完整字段见 [`关键协议.md`](../_shared/真源/关键协议.md)「重要写入完整性」。

- `target=<路径>` / `operation=<replace|append_fragment|edit_section>` / `before_bytes=<数值|unavailable>` / `after_bytes=<数值|unavailable>` / `readback=<verified|failed|unavailable>` / `anchor_preserved=<true|false|unavailable>` / `unrelated_sections_preserved=<true|false|unavailable>` / `verified_by=<主控|n/a>`

## ▲ 降级运行记录（fallback 每次一行，主人扫一眼可见）

- （无降级时保持此空行；有降级必须写：`▲ DEGRADED RUN：<角色> 由主控顶替（<原因：401/超时/配额>）HH:MM → 产物头部已标注`）

## 人在环决策记录（四节点，缺一不可）

- **Phase 0 定题**: decision=<approved|revision_requested> / owner_confirmed_at=<时间> / evidence=01-任务简报.md / **未启动时**：decision=n/a + `pre_pipeline_exit=<pause|reject>`（v2.12.61：「是否启动」是流水线**外**前置门，其字面值**不进** `decision`；真源 = `phase-order.yaml` `phase0_definition.decisions`）
- **Phase 2.5 大纲**: decision=<approved|revision_requested|restart_phase> / owner_confirmed_at=<时间> / evidence=analysis/分析大纲.md / **v2.12.49 M-11**：figures=<N> / figure_decision=<采用 T4 建议|调整图位数|取消图表> —— **任一字段缺失 = 不合格**（t7_5_integrity / T8 机械门均报）/ **生产·全自动**：owner_confirmed_at=<Phase 0 预授权时间> + preauthorization_basis=任务简报「运行模式」
- **Phase 3.5 洞察**: decision=<insight|direction_correction|no_insight> / owner_confirmed_at=<时间> / evidence=drafts/初稿-v1.md / correction_scope=<方向纠偏时必填> / **生产·全自动**：owner_confirmed_at=<Phase 0 预授权时间> + preauthorization_basis=任务简报「运行模式」
- **Phase 5 验收**: decision=<accepted|revision_requested|restart_phase|deferred> / owner_confirmed_at=<时间> / evidence=final/定稿.md / **生产·全自动**：owner_confirmed_at=<Phase 0 预授权时间> + preauthorization_basis=任务简报「运行模式」+ delivery_readiness=机械判定二态

> 仅有材料、主控代判、子代理声称已确认，均不构成决策；`no_insight` 是明确决策，不是跳过。

## 能力自检（Phase 0 首次 spawn 前填；越权回报即时追加）

**主控工具面**: 与 documented 集一致 ⬜ / 超限 ⬜：可见计数 ___ / 差值计数 ___ / 高危类别具名：___（执行类 / 外发类 / 写入类 / 会话类；其余超限计入差值计数、不逐条枚举，v2.12.74；超限即向主人披露）

| 档位 | 角色 | 自检结果 | 工具面超限（警告级：记录+继续） | 越权调用（阻断级：停止+回报） |
|---|---|---|---|---|
| allow_research | T1/T2/T3 | ⬜ 未报 / ✅ 通过 / ⚠️ 面超限·继续 / ⛔ 调用越权·阻断 | — | — |
| allow_analysis | T4 | ⬜ | — | — |
| allow_writing | T5 | ⬜ | — | — |
| allow_audit | T6/T7 | ⬜ | — | — |
| allow_review | T9/G14 | ⬜ | — | — |

> 自检口径见 [`permissions.md`](../permissions.md)「能力自检」与 [`dispatch-header.md`](../_shared/真源/dispatch-header.md)「启动自检」：只核对本角色声明与当前会话工具面；实际调用未声明工具才阻断。**本表不记录宿主配置明细。**

## 二、角色状态（key:value 替换，每角色一行）

> **维护规则**：主控用 `**T<n> 角色**: ⬜ Inbox` → `**T<n> 角色**: ✅ Done (时间)` 替换。**禁止** 用表格行替换，零空格漂移风险。

- **T1 文献检索**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, N 文献卡）
- **T2 数据检索**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, N 数据卡 + M 缺口）
- **Phase 1 后置 派发硬验证**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, post_phase1_dispatch_verify, 3 行派发记录核验 passed|path_error|conflict）
- **T2.5 完整性门**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, 主控 checkpoint）
- **T3 案例检索**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, result=required|empty_card|waived, N 案例卡）
- **T4 分析**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, analysis/分析大纲.md）
- **Phase 2.5 大纲确认**: ⬜ Inbox → 🔄 In Progress → ✅ Done（主人确认日期, 拍板图位 N）
- **T5 写作**: ⬜ Inbox → 🔄 In Progress → ✅ Done v1/v2/v3（YYYY-MM-DD HH:MM, 初稿-v3.md, M 字数）
- **Phase 3.5 洞察补充**: ⬜ Inbox → 🔄 In Progress → ✅ Done（主人确认日期, 洞察内容或「无补充」决策）
- **T6 批判伙伴**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, C1-C7 报告）
- **Phase 1.5 定向回查**: ⬜ not_triggered（必须写未触发依据）→ 🔄 triggered → ✅ Done（YYYY-MM-DD HH:MM, T1b 回查报告 + T2.5 重跑）
- **G14 中文 AI 痕迹闸**（Phase 4.4 前置，定稿前唯一一次）: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, 9 类检测, Pass/Warning/Fail；纯外语 → n/a） <!-- G14 九类判定真源 = gates/14-中文AI痕迹-gate.md §二 + checkers/中文AI痕迹-checker.md（本节不重列九类） -->
- **T7 审计**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, 审计报告-vN.md + 反哺报告-vN.md）
- **修订回环**（≤2 轮）: ⬜ Inbox → 🔄 第 1 轮 → ✅ Done / 🔄 第 2 轮 → ✅ Done / 🔒 Acknowledged Limitations 模式 <!-- 本行仅为 status 状态取值；轮次映射与各通道判定的真源 = _shared/真源/pipeline-overview.md『修订回环仲裁规则』（本行不复述轮次定义） -->
- **T7.5 完整性门**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, 主控 checkpoint）
- **T8 技术终检**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, final/定稿.md 技术检查）
- **Phase 5 主人验收**: ⬜ 未决策 → 🔄 In Progress → ✅ accepted / 🔁 revision_requested / ↩ restart_phase / ⏸ deferred
- **T9 同行评审**: ⬜ Inbox → 🔄 In Progress → ✅ Done（YYYY-MM-DD HH:MM, 6 维度评分 XX/30 + Top 3 期刊）

### 派发清单（00-主控-扩展职责.md §十六点五硬验证输入；每次 spawn 一行，v2.15.7 新增）

- **<node_id>** @ <ISO 8601 时间> | runId=<runId> | sessionKey=<childSessionKey> | model=<resolvedModel>
- 派发失败也必须留痕：`派发失败 = <node_id> @ <时间>（原因：<摘要>）`
- 任一字段为空 ⇒ `incomplete_dispatch`；三条 runId 重复 ⇒ 冲突（post_phase1_dispatch_verify 拦截）

## 三、闸门清单（checklist）

- [] **M-Integrity-1**（T2.5 数据完整性，T2 → T4 间触发）
- [] **M-Integrity-2**（T7.5 审计完整性，T7 → T8 间触发）
- [] **M-Form-6**（数据卡信任级别完整性）
- [] **M-Form-7**（交付边界纯净，T8 终检必跑）
- [] **M-Form-8**（三角验证覆盖率）
- [] **M-Exist-1**（数据 URL 真实存在）
- [] **M-Exist-2**（证据包完整性校验）
- [] **M-Exist-3**（数据信任级别一致性）
- [] **G14 中文 AI 痕迹闸**（Phase 4.4 前置触发，定稿前唯一一次；纯外语 → n/a）
- [] **T2.5 数据完整性门**
- [] **T7.5 审计完整性门**

## 三.五、M 门执行记录（主控每 phase 跑完登记）

> **用途**：M 门从「T8 终检一次性跑」升级为「每 phase 强制跑 + 记录」。主控每跑一道 M 门，在此登记结果（时间 + 结论 + 通过/失败）。

| Phase | M 门 | 执行时间 | 结论 | 状态 |
|-------|------|---------|------|------|
| T2.5 完整性门 | M-Integrity-1 + M-Form-6 + M-Exist-3 | YYYY-MM-DD HH:MM | 通过/失败 + 一句话 | ✅/❌ |
| T7.5 完整性门 | M-Integrity-2 + M-Form-8 + M-Exist-2 | YYYY-MM-DD HH:MM | 通过/失败 + 一句话 | ✅/❌ |
| v1→v2 修订后 | 章节级 M 门| YYYY-MM-DD HH:MM | 变更点 N 处 | ✅/❌ |
| T8 终检 | M-Form 8 + M-Exist 3 = 11 项 | YYYY-MM-DD HH:MM | exit 0 / exit 1 | ✅/❌ |

## 三.六、B7 质量与人机交互摘要

```yaml
b7_quality_hmi:
  run_mode: 生产·人在四环 | 生产·全自动 | 测试模式
  g14_caption_recheck: pass | warning | fail | n/a | unavailable
  caption_scope: <组装新增或变形范围|n/a>
  caption_checked_at: <时间|n/a>
  block_t9: true | false | unavailable
  direction_decision: insight | direction_correction | no_insight | n/a
  correction_scope: <摘要|n/a>
  phase_summary: {recorded_in_status: true|false, owner_notified: true|false, owner_acknowledged: true|false}
```

> `recorded_in_status=true` 不等于主人已收到或确认；缺少渠道确认不得写 `owner_acknowledged=true`。

## 三.六、pipeline-doctor 诊断快照（B6）

> 这是结构化诊断，不是自动执行器、自动继续或 gate 替代。三态必须有证据；`blocked` 必须列阻断原因，`proceed_with_limits` 必须列限制与下一步。

```yaml
doctor:
  verdict: blocked | proceed_with_limits | proceed
  blocking_findings: []
  warnings: []
  evidence: []
  required_action: []
```

## 三.六、事件、路由与 gate telemetry（B5）

> 运行期只记录事实，不自动继续、不替代主人决策。事件账本建议写入项目内 `control/events/`，每个事件独立文件；此处保留当前运行摘要。

```yaml
runtime_observability:
  event_log: {path: control/events/, last_event_id: <id|n/a>, last_event_type: <type|n/a>}
  routing: {requested: [], actually_used: [], unavailable: [], fallback_chain: [], degradation_level: none | L1 | L2 | owner_halt, reason: []}
  gate_telemetry:
    <gate_id>:
      triggered: 0
      blocked: 0
      current_run: 0
      cumulative: 0
      pass: 0
      warning: 0
      fail: 0
      not_applicable: 0
      unavailable: 0
      last_result: pass | warning | fail | not_applicable | unavailable
      # 仅计真实运行期判定；反向注入、构建测试、文档演练不计入。零触发必须显式写 0。
```

> `requested` 不等于 `actually_used`；反向注入、构建测试和文档演练不计 gate telemetry；零触发必须显式写 `0`。

## 三.六、审计门触发计数（R-52）

## 三.六、机械对账快照（B4）

> 先机械提取集合、计数和差异，再由 T7/T8 做语义审查；此快照不替代理论、证据充分性、反方质量或作者声音判断。零异常也必须保留 ``，未知写 `unavailable`，不得猜测。

```yaml
mechanical_reconciliation:
  citation_reconciliation: {body_refs: 0, registered_cards: 0, matched: 0, body_without_card: [], card_without_body: [], duplicate_identifiers: [], semantic_review_required: []}
  data_reconciliation: {body_data_refs: 0, registered_data_cards: 0, verified: 0, unresolved: [], missing_fields: []}
  gate_coverage: {declared: 0, executed: 0, skipped: [], missing_reason: [], false_green_risk: []}
  version_reconciliation: {expected: "", matched: [], mismatched: [], generated_views_stale: []}
  verdict: pass | fail | path_or_param_error | not_enabled
```

## 三.七、审计门触发计数（R-52）

> **运行期真实判定计数**：T7/T8 在实际审计中逐门回填；只统计本轮真实产物被判为「不通过」并因此打回/阻断的次数，**不计反向注入测试、构建期测试或文档演练**。未触发的门必须明确记 `0`，不得省略或用「已审计」代替。
>
> **口径真源**：门号与门项集合取 [`audit-checklist-quickref.md`](../_shared/真源/audit-checklist-quickref.md)、[`M-Gate-核心.md`](../_shared/真源/M-Gate-核心.md) 与 `counts.yaml`；本表只留运行期观测，不改变任何门的判据。

| 门号/项目 | 本轮触发次数 | 累计触发次数 | 判定版本/报告 | 备注 |
|---|---:|---:|---|---|
| G0-G18（逐门展开） | 0 | 0 | <T7/T8 报告版本> | 未触发项也必须填 0 |
| M-Form-1～8（逐项展开） | 0 | 0 | <M-Gate 报告版本> | 只计真实运行判定 |
| M-Exist-1～3（逐项展开） | 0 | 0 | <M-Gate 报告版本> | 只计真实运行判定 |
| M-Integrity-1～2（逐项展开） | 0 | 0 | <M-Gate 报告版本> | 阶段门阻断也须记账 |

**本轮死门观察**：连续 ≥3 次真实运行零触发的门：`<门号 / n/a>`；是否进入裁撤审查：`<yes|no|n/a>`；依据报告：`<路径 / n/a>`。

## 四、产物路径（key:value 替换）

> **v2.12.49 M-7 状态对账机械真源**：本节每条产物路径**必含节点 id**（主控 spawn 后同步），与 §二 角色状态行**双向机械断言**由 T8 终检执行：
> - **磁盘产物在 → 对应节点不得为 `Inbox`**（产物不存在时为 `Inbox`/In Progress 合法；产物存在时必须 Review/Done）
> - **节点 `Done` → 对应产物必须存在**（含 `Done (时间)` 字段）
> - **同一节点 / 角色只允许出现一次**（重跑加 `v(N+1)` 版本号）
>
> **异常注入示例**（反向用例，防漏检）：
> - 磁盘 `final/定稿.md` 存在 但 `T8 技术终检: ⬜ Inbox` ⇒ T8 必须报「状态漂移」
> - `T7 审计: ✅ Done` 但 `audits/审计报告-vN.md` 不存在 ⇒ T8 必须报「产物缺失」
>
>

- **drafts/初稿** [节点: T5]: drafts/初稿-v{N}.md
- **analysis/分析大纲** [节点: T4]: analysis/分析大纲.md
- **analysis/批判报告** [节点: T6]: analysis/批判报告-v{N}.md
- **audits/审计报告** [节点: T7]: audits/审计报告-v{N}.md
- **audits/反哺报告** [节点: T7]: audits/反哺报告-v{N}.md
- **audits/审稿报告** [节点: T9]: audits/审稿报告-v{N}.md
- **audits/G14 检测报告** [节点: G14]: audits/G14-检测报告-v{N}.md
- **literature/回查报告** [节点: T1b]: literature/回查报告-v{N}.md
- **final/定稿** [节点: final_assembly + t8_technical_final]: final/定稿.md
- **组装后 G14 轻量复检** [节点: final_assembly]: `g14_caption_recheck=<pass|warning|fail|n/a>` / `scope=<组装新增或变形的图注/可见文本范围>` / `checked_at=<时间>` / `阻断进入 t9_review=<yes|no>`（未完成或无法判定不得进入 T9）
- **final/交付说明** [节点: t8_technical_final]: final/交付说明.md
- **final/M-Gate 报告** [节点: t7_5_integrity]: final/M-Gate-Report-v2.2.12.json
- **final/定稿指纹** [节点: t8_technical_final]: final/定稿.sha256
  - sha256: unavailable # v2.12.64：**主人侧量值**，host shell 补算后回填；未回填保持 unavailable，判定档 = pending_owner_verification（**禁止判通过**）
  - bytes: unavailable # 同上（`wc -c` 可得；零 exec 下 agent 不可得）
  - 文本度量: <行数 / 字符数 / 首末行摘要> # agent 侧可确知，`read` 后填

### 4.8 主控上下文预算与余量检测

> 真源 = `phase-order.yaml` `pre_spawn_enforcement.context_budget_gate`；预算模型 = [`performance-benchmarks.md`](../_shared/真源/performance-benchmarks.md) §五。
> **机械兜底边界**：窗口余量是运行期自观测，构建期无法机械校验；本段是纪律层 + 可追溯留痕，不宣称能机械拦截窗口压爆。

**预算估算（Phase 0 后置）**: tier=<轻量|中段|重量> / 主控预算≈<N tokens> / 来源=performance-benchmarks.md §五 / 估算日期=<时间>
**当前预算状态**: 已消耗≈<N tokens> / 余量=<百分比|unavailable> / 判定=<充足|偏低|危险|无法判定> / 超支=<否|overspend_alert>
**阶段边界复核**（每个阶段追加一行，不覆盖历史）：
- `<Phase/node>` | consumed≈<N> | margin=<百分比|unavailable> | verdict=<充足|偏低|危险|无法判定> | offload=<无|已指针化/局部读/停止非必要全文> | HH:MM

### 4.9 status_json 机器可解析快照

> **用途**：把本文件的人读留痕投影为可脚本化监控的 JSON 快照，供主人/维护者聚合性能指标并反哺 [`performance-benchmarks.md`](../_shared/真源/performance-benchmarks.md)。由主控在阶段边界整体重写；它是派生快照，不取代上方人读字段。
> **诚实边界**：JSON 在运行期由主控写入，构建期只校验结构锚点；缺失值必须写 `null` / `unavailable`，禁止把未知伪装成 0 或通过。

```json
status_json: {
  "project": "<项目名>",
  "phase": "<phase-order.yaml node id>",
  "run_mode": "生产·人在四环|生产·全自动|测试模式",
  "updated_at": "YYYY-MM-DD HH:MM",
  "spawn_landing": [{"node": "<id>", "role": "T1", "result": "ok|missing|retry:<N>"}],
  "display_cap_truncated": [],
  "g14": {"verdict": "pass|warning|fail|n/a|unavailable"},
  "m_gate": [{"gate": "M-Integrity-1", "verdict": "pass|fail|undecidable|path_or_param_error"}],
  "tokens": {"orchestrator_in": null, "orchestrator_out": null, "roles": []},
  "revision_rounds": 0,
  "smoke": {"level": "n/a|L1|L2", "run_id": "n/a", "verdict": "pending|pass|fail"}
}
```

---

## 📊 方法论足迹

> **借鉴 deep-research-pro 的方法论透明**（论衡化，非竞品简单复制）
> **作用**：让主人/读者实时看到「**为什么是这个进度、证据强度是多少、下一步预测什么**」
> **维护方**：主控自动更新（每个 Phase / 闸门 / 子代理完成时刷新）
> **镜像工件（v2.17.1）**：本段 + §三 闸门清单 + T9 评分 + 修订轮次 + 降级记录，同步写入 `viz/index.html`（自包含单文件：零外链 / 零 exec / 零外发；纯 `write` 产物）。**面板渲染是宿主侧职责** —— 论衡不声明也不调用 `show_widget` / `dashboard` / `portal` / `canvas`。该文件不进 `final/`，按本文件同档管理。

### 4.1 当前阶段（实时）

| 字段 | 当前值 | 更新时机 |
|------|--------|---------|
| **Phase** | Phase X.X（阶段名）| T0 启动阶段时 |
| **核心活动** | 当前在做 XX | 子代理 ACK 时 |
| **已进入时间** | N 分钟 | 阶段启动时 |
| **预计剩余** | N-N 分钟 | 子代理 ACK 时 |

### 4.2 证据强度（实时，三角验证可视化）

| 维度 | 当前 | 目标 | 状态 | 备注 |
|------|------|------|------|------|
| **文献覆盖** | N 篇（核心 X / 次要 Y） | ≥X 篇核心 | ✅/⚠️/❌ | T1 完成后刷新 |
| **数据来源** | N 个（来源 1 + 来源 2 + ...）| ≥X 个独立 | ✅/⚠️/❌ | T2 完成后刷新 |
| **案例支撑** | N 个（事件/主体 X） | ≥X 个 | ✅/⚠️/❌ | T3 完成后刷新 |
| **三角验证** | N 论点 X 三档齐 | ≥X% 三档齐 | ✅/⚠️/❌ | T4 完成后刷新 |
| **基线编号**| N 条 [D-基-xx-xx] | ≥X 条 | ✅/⚠️/❌ | T2 完成后刷新 |
| **G14 AI 痕迹**| Pass / Warning / Fail | Pass | ✅/⚠️/❌ | G14 闸门后刷新 |

### 4.3 已触发闸门（实时清单）

参见顶部「## 三、闸门清单」checklist。

### 4.4 下一步预测（实时，LLM 推理预测）

```
当前阶段完成后，下一阶段预计：
- 触发 T6 批判伙伴（预计 5 分钟内）
- T5 进入 Phase 3 写作（预计 40 分钟内进入 Phase 4.5）
- G14 闸门（Phase 4.4 前置）在「已可定稿」后触发，全流程仅一次

▲ 预测仅供主人参考，不作为承诺
```

### 4.5 不确定性（实时，主人看到的所有风险点）

- ▲ **T1 覆盖**：某主题文献可能偏窄（仅 X 篇核心），下一步计划补检
- ▲ **T2 数据**：「某数据」最新数据待 G11 时效校验
- ▲ **T3 案例**：某事件案例可能涉及未公开信息，需谨慎引用
- ▲ **G14 痕迹**：9 类检测维度若有命中，按闸门规则触发修订
- ▲ **依赖外部**：论衡核心是 LLM 推理 + 文件读写 + Web 检索，若工具不可用自动降级

### 4.6 本轮模型分配（Phase 0 静态映射）

>
> 🔒 **遥测分级 + 收容仍适用**：本表只记「能力档 → 模型名」；**不记可用性探测结果、不记宿主余额**（v2.12.42 起不采集）；`session id` / `sessionKey` 见 §4.7（不记录）。

| 能力档 | 角色 | 候选池（描述性，见模型候选池.md） | **本轮实际（静态映射）** |
|--------|------|-------------------------------|--------------------------|
| 检索 | T1 / T2 / T3 | 小参数模型 + 高 token/秒 | `<映射结果>` |
| 分析写作 | T4 / T5 | 中大参数推理模型 | `<映射结果>` |
| 批判审计 | T6 / T7 / G14 | 顶级推理模型 | `<映射结果>` |
| 主控 | T0 | 中参数稳定模型 | `<映射结果>` |
| 终检 | T8 | 主控亲完成（不 spawn 子代理）| 主控亲完成 |

**运行时降级**：「配置存在 ≠ 可用」的残余风险改由**运行时首败降级**承担：首次实际调用失败（401/403/429/配额）→ 子代理 `degraded` 自报 → 按候选池 §三 降级规则重派（**优先换 provider 族**；零产物决策树：同档 ≤2 次 → 降档）→ **配额耗尽类暂停等主人拍板**（行为预授权，fail-closed）→ **顶配档连续 2 次失败 ⇒ 断路器暂停呈报主人三选一**。撞墙成本从「Phase 0 多次探测 spawn」降为「一次失败调用 + 自动降档」。（**顶配档可用性只在 Phase 0 后置探活一次** = §二·补；不引入 per-dispatch 探测。）

**降级提示**：当前会话未提供**顶配档（批判审计）模型** → 主控**必须显式告知主人**「当前会话无顶配审计模型，审计/批判深度将降级，是否继续」——禁止静默降级。

**spawn 落地验证留痕**：每次 `sessions_spawn` 后，主控按 [`_shared/真源/执行韧化协议-exec.md`](../_shared/真源/执行韧化协议-exec.md)「编排循环三防」做**落地验证**（`subagents(action=list)` 确认 runId 在 active runs；不在 = 重试 ≤2 次），并逐节点记账：

```
| 节点 | 角色 | spawn_landing | 备注 |
|---|---|---|---|
| <节点 id> | T1 | ok / missing / retry:<N> | <重试原因 / 未落地处置> |
```

### 4.7 token 消耗记录（精确机制）

> **用途**：T8 终检时汇总「token 总成本」呈现给主人（deliverables.md 成本指标字段的落地）。
>
> **精确机制**（取代三级降级）：
> - **`sessionKey` / `sessionId` 不记录**：Stats line 虽含会话标识，主控只提取 Token usage / Runtime / Estimated cost 三类字段；会话关联用**角色名**即可（聚合成本报告不需要会话标识——回应外部扫描）。
> - **子代理**：主控 `sessions_yield` 收到每个子代理 completion event 时，从末尾 Stats line 提取 `Token usage` 的 input/output/total 记入下表——**主控独占记录**，子代理无法也无需回传自己的 token
> - **主控自身**：T8 终检前用 `session_status({sessionKey: "current"})` 拿主会话精确值（含 cost）
> - **Stats line 缺失 = 平台异常**：该角色格标「Stats line 缺失」并在对话/告警告知主人，**禁止估算、禁止静默跳过**——不是填「未配置」或「N/A」

**主控收到每个子代理 completion 时填**（数据源 = completion event Stats 行）。⚠️ 本节属「Operational Telemetry」manifest 段，**默认不收集**——主人 Phase 0 显式勾选「token 成本 / 统计」才启用本表全量字段；未勾选时，主控仅在交付说明中写「token 总计 ≈ Σ（精度 0）」，不展示 in/out 分项也不持久化任何 stats。

| 角色 | token 消耗（in / out） | 模型 | 记录人 |
|------|------------------------|------|--------|
| T1 文献 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T2 数据 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T3 案例 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T4 分析 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T5 写手 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T6 批判 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T7 审计 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| T9 评审 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| G14 检测 | `<tokens.in> / <tokens.out>` | `<model>` | 主控（completion Stats line） |
| **主控自身** | `<session_status 查 main>` | `<model>` | T8 汇总 |
| **总计** | `<Σ>` | — | T8 汇总 |

**T8 终检汇总规则**：Phase 5 终检时主控把上表 Σ + session_status 主会话值 Σ 填入 `final/交付说明.md`「成本指标」字段，并在对话中向主人呈现：
```
## 本轮 token 成本（精确）
- 总计：<Σ> tokens（in <N> / out <M>）
- 子代理 Σ：<Σ_sub> tokens（各子代理完成事件 Stats line 的 Token usage 汇总）
- 主控自身：<session_status 主会话值> tokens + $<cost> cost
- 主要消耗：T5 写手 <N> / T7 审计 <N> / T9 评审 <N>
- 数据源：子代理完成事件末尾 Stats line（Token usage input/output/total）+ session_status 工具（OpenClaw 9.1+）
```

---

## 八、模型接管声明（fallback 协议落地段；v2.15.7 新增）

> **真源**：字段定义见 [`../_shared/真源/model_fallback_takeover_protocol.md`](../_shared/真源/model_fallback_takeover_protocol.md) §三；本段仅提供 status.md 落盘模板。
> **触发时机**：仅在主控进程失联 + fallback 模型接管时填写；常规项目**整段留空**。
> **字段任一为空 ⇒ 记 `takeover_incomplete`**（下游 T8 终检按 M-Exist 判「路径或参数错误」档）。

**接管触发时间**（ISO 8601，精确到秒）：<YYYY-MM-DDTHH:MM:SS+08:00>
**原主控 session_key**：<原 sessions_history 可见到的 key；若已不可见记 `unknown`>
**fallback 模型**（provider/model）：<如 kkaiapi/gpt-5.6-terra>
**接管时 seq 序号**：<数字>
**接管时 node_id**：<如 t4_analysis>
**正在运行的 worker 数**：<数字>
**takeover-log 路径**：<相对路径，如 audits/takeover-log-v1.md>
**原主控恢复状态**：<recovered | not_recovered | unknown>
**主人是否已告知**：<yes | no | pending>
**接管清单一览**（每个正在运行的 worker 一行）：

    - <node_id> | last_heartbeat=<ISO 8601> | final_state=<worker_running|worker_failed|worker_timeout> | takeover_action=<continued|reset_by_fallback>

**接管动作执行记录**（按 model_fallback_takeover_protocol.md §二 6 步顺序）：

    - [step 1] 读 status.md 快照：<完成时间> | sha=<前 12 位>
    - [step 2] 写 §八 段：<完成时间>
    - [step 3] 列接管清单：N 个 worker
    - [step 4] 写 takeover-log：<路径>
    - [step 5] 重读 phase-order.yaml：从 seq=N 继续
    - [step 6] status.md 头部 banner 已加：<完成时间>

**后续状态记录**：

    - 原主控恢复时间（若 recovered）：<ISO 8601>
    - fallback 模型继续推进的 node 数：<N>
    - 是否触发主人三选（换 provider / 换档 / 接受同源）：<yes | no>

---

## 五、执行韧化记录（主控/角色更新）

### 5.1 心跳记录

- 每个角色启动 30 秒内 + 每 5 分钟一次追加：`[心跳 HH:MM] role=<角色> model=<model-id>`
- **启动宽限期 = 2 分钟**：spawn 后 2 分钟内主控复验第 4 件不期望心跳；2 分钟后再检。不足宽限的「心跳缺失」= 误报，不作复验失分。

### 5.2 分阶段 ack（5-15 分钟任务必走 5 段）

- `[ack 0% HH:MM] <一句话进度>`
- `[ack 25% HH:MM] <进度>`
- `[ack 50% HH:MM] <进度>`
- `[ack 75% HH:MM] <进度>`
- `[ack 100% HH:MM] 完成`

### 5.3 模型降级记录

- `[降级 HH:MM] primary→fallback<N>, 原因=<ping超时/超时/其他>`

### 5.4 主控介入记录（如有）

- `[介入 HH:MM] session-kill/换模型/接受 partial, 说明=`

### 5.5 硬卡超时记录

- `[硬卡 HH:MM:SS] 超 <角色> 阈值 Xmin, kill + 接受 partial`（主控不允许「再等一下」）

### 5.6 失败记录（如有）

- `[失败 HH:MM] 角色=<角色>, 原因=<超时/上下文爆/其他>, 重派=N次`

### 5.7 修订回环记录

- 第 1 轮：P0 x / P1 x → 写手修订 → 审计复核：通过/未通过
- 第 2 轮：P0 x / P1 x → 写手修订 → 审计复核：通过/未通过（仍不过 → 升级主控）
- **G14 触发记录**（Phase 4.4 前置，**首审仅 1 次；风格修订后全文复检 ≤2 轮**）：
  - 判定 = Pass（0-2 类）→ 进 Phase 4.4
  - 判定 = Warning（3-4 类）→ 主控呈报 3 选 1（默认暂停；选 B 则 `t5_style_revision` 风格修订 1 次）
  - 判定 = Fail（5+ 类）→ `t5_style_revision`（仅风格层）→ 按全文复检严格度 ≤2 轮复检后进 Phase 4.4

### 5.8 项目历史记录归档

> **安全边界**：本节为"过期项目整理"的过程记录，**不涉及文件删除**。论衡工作流本身不执行任何 cleanup；本节的"结题归档/标记"动作由主人**在论衡工作流外手动完成**，本节仅记录"哪些项目已结题、已结题项目的素材是否被未来项目引用"。
>
> **术语消歧**：与 §方法论足迹的**留档副本**区分——留档副本是工作流内**新增**一个快照文件（`methodology-footprint-*.md`），既不移动也不删除；结题归档是工作流外的项目整理动作。两者不混称同一个"归档"。

- `[archive HH:MM] 项目 <名> 标记结题，结题产物路径 = <路径>，后续复用需主人在新项目任务简报中显式指定`
- `[reuse HH:MM] 项目 <新名> 引用 <旧名> 的 <素材类型>（已由主人在任务简报勾选授权）`

---

> 📚 维护说明与重写背景已下沉至仓库维护资料 ；运行期只填写本文件字段。
