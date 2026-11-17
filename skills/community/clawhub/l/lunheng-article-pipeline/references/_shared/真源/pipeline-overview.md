> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 流水线全景与修订回环仲裁（**唯一派生视图**）

> **v2.14.0**：新增 Phase 4.5 后置压力测试轮；全景节点数由 24 调整为 25。
> **2026-10-08 审计 R-1（B1）**：Phase 1.5 拆为**两个求值点** —— 简报标记窗口（见下表 **seq 4**）+ T2.5 后置红数据窗口（见下表 **seq 6**）。原单节点排在完整性门之前，红数据触发项在首次到达时**恒为假**且被 `on_not_triggered` 静默吞掉（与「闸门真没跑」不可分）。全景节点数由 26 调整为 27。
> **v2.15.7**：新增 Phase 1 后置派发硬验证闸门（ECS 反馈：防 spawn 静默失败；节点 id 见下表 seq 3）；全景节点数由 25 调整为 26。

> 🔴 **本文件是全仓唯一承载「流水线全景」的派生视图**（v2.12.54 R-1 收敛）。SKILL.md、README、QUICKSTART、pipeline-readme、设计文档、checkpoint-card、glossary 等文档**已删除全景段，只留指向本文件的指针**——重列即构建期校验不通过（维护者机制；登记真源 = `phase-order.yaml` `panorama_sources`）。
>
> **流程顺序与阻断关系的唯一真源是 [`phase-order/`](phase-order/) 目录**；[`phase-order.yaml`](phase-order.yaml) 是装配视图（生成物，禁手改）。本文件是派生视图，与真源冲突时以真源为准。
> **真源与读法（v2.13.5 R-21 增量 2：真源已倒置）**：流程真源 = **`phase-order/` 目录**——[`index.yaml`](phase-order/index.yaml)（跨阶段共用契约 + 别名映射 + **节点路由/顺序**）与 `phase-order/<node-id>.yaml`（27 个节点切片，含 `kind` / `condition` / `next` / `after_each` / `output_chars_max` / `independence_rules` 等全部字段）**共同构成唯一真源**；[`phase-order.yaml`](phase-order.yaml) 是它们的**装配视图（生成物，禁手改）**，保留原路径供维护者校验 / 门 S / 既有引用读取。
> **主控读法**：每进入一个节点前读 **①[索引](phase-order/index.yaml)** + **②该节点切片**，**不必读装配视图全文**（单次运行读取量约 −95%）。装配视图被手改、或改了真源未重生成，均由门 AA（维护者侧生成器 --check）当场判红；**不凭本段文字记忆推进**。
>
> 📎 **与 [`pipeline-readme.md`](../../pipeline-readme.md) 的分工**（v2.12.40 起显式声明）：本文件 = **派生速查视图**（全景 + 修订回环仲裁）；`pipeline-readme.md` = **完整运行手册**（触发词 / 适用边界 / 模型配置 / 派发话术索引 / 模板加载策略等百科内容）。**两者不可互替、不可精简为对方。**

## 流水线全景（Phase 0-5，真源共 27 节点）

> ⚠️ **节点 id 是主控呈现进度的唯一合法取值**（v2.12.27）：主控**不得自创**节点名或 Phase 标签。历史实况：无编号节点曾被误标为「Phase 4.2」，导致整段跳过 T7 审计。

| seq | 节点 id | Phase 标签 | 执行者 | 产物 / 出口 |
|---|---|---|---|---|
| 0 | `phase0_definition` | Phase 0 | 主人 × 主控 | `01-任务简报.md` + `status.md`（含外发同意记录 / 目标语言 / 项目名） |
| 1 | `pre_spawn_enforcement` | Phase 0 后置（spawn 前核验） | 主控 | `status.md`（同意记录 + 标准架构声明 + **顶配档探活门**） |
| 2 | `retrieval` | Phase 1 | T1 ∥ T2 ∥ T3（真并行） | `literature/文献卡.md` + `data/数据卡.md` + `cases/案例卡.md`（T3 含 0 条空卡协议） |
| 3 | `post_phase1_dispatch_verify` | Phase 1 后置（派发硬验证闸门） | 主控（亲为） | `status.md`（T1/T2/T3 三行派发记录 runId/sessionKey/model 齐全且唯一；v2.15.7） |
| 4 | `phase1_5_targeted_review` | Phase 1.5 | 主控 spawn T1b（条件触发，**只认简报 [Dxx]/[Lxx] 待复核标记**） | `literature/回查报告-vN.md`；未触发记 `not_triggered` |
| 5 | `t2_5_integrity` | T2.5 完整性门 | 主控 checkpoint | 数据卡条数 ≥ 需求数 + 信任级别完整 → 通过才派 T4 |
| 6 | `phase1_5b_post_t2_5_review` | Phase 1.5 后置（T2.5 红数据窗口） | 主控 spawn T1b（条件触发，**排在完整性门之后**） | `literature/回查报告-vN.md`；未触发记 `not_triggered` |
| 7 | `t4_analysis` | Phase 2 | T4 | `analysis/分析大纲.md` + `analysis/T5-写作上下文.md` |
| 8 | `phase2_5_outline` | Phase 2.5 | 主人 × 主控（**人在环**） | 大纲确认 + **图位拍板**（含 `figure_decision`） |
| 9 | `t5_draft_v1` | Phase 3 | T5 | `drafts/初稿-v1.md`（铁律：`[Lxx]`/`[Dxx]`/`[Cxx]` + AI 去味 10 项） |
| 10 | `phase3_5_insight` | Phase 3.5 | 主人 × 主控（**人在环**） | `insight` / `direction_correction` / `no_insight`（无补充也须留痕；方向纠偏不得降格为普通补充） |
| 11 | `current_draft_sync` | Phase 3.6 前置 | 主控（亲为） | `drafts/current_draft.md`（权威稿指针） |
| 12 | `t6_critique` | Phase 3.6 | T6（轻量档必跳） | `analysis/批判报告-vN.md`（攻击**含主人洞察的 v2**） |
| 13 | `t5_feedback_revision` | Phase 3.7 | T5（条件触发） | `drafts/初稿-v{N+1}.md` + `drafts/修订说明-v{N+1}.md` |
| 14 | `t7_audit` | Phase 4 | T7 | `audits/审计报告-vN.md`（G0-G18；G14 为独立风格闸，G18 方法论审计按真源执行） |
| 15 | `audit_revision` | Phase 4.2 | T5（有界回环） | 修订稿 + 修订说明；`max_rounds: 2`，耗尽走三选一 |
| 16 | `t1b_targeted_review` | Phase 4.3 定向回查（T1b） | T1b（条件触发，复用 T1） | `literature/回查报告-vN.md`（「待人工核验」引用定向回查；≤2 轮，未触发记 `not_triggered`） |
| 17 | `t7_5_integrity` | T7.5 完整性门 | 主控 checkpoint | `final/M-Gate-Report-*.json`（**审完才放行 T9/T8**） |
| 18 | `g14_style_gate` | Phase 4.4 前置（G14 风格闸） | G14（含中文必跑） | `audits/G14-检测报告-vN.md`（**首审只审一次**；如触发风格修订，按闸门 §四全文复检 ≤2 轮） |
| 19 | `t5_style_revision` | Phase 4.4 前置·风格修订 | T5（G14 Fail 唯一出口） | 仅风格层修订稿（**不得动论证/数据/引用/结论**） |
| 20 | `phase4_4_figures` | Phase 4.4 | 主控（亲为） | `final/图件/*.svg`（零外发、零 exec；有图位才触发） |
| 21 | `final_assembly` | Phase 4.4 后置（定稿组装） | 主控（亲为） | `final/定稿.md`（**只产投稿版**，禁入工程元数据段；组装后必须完成 `g14_caption_recheck`） |
| 22 | `t9_review` | Phase 4.5 | T9（盲审独立子代理） | `audits/审稿报告-vN.md`（6 维度 + D1/D2 → accept/minor/major/reject） |
| 23 | `t9b_stress_test` | Phase 4.5 后置（压力测试轮） | 主控（亲为） | `audits/压力测试报告-vN.md`（三剧本、建议性；**默认不跑**，冲刺投稿时 Phase 0 勾选 `owner_stress_test_opt_in`） |
| 24 | `t8_technical_final` | Phase 5 终检 | 主控（T8 亲为） | `final/交付说明.md`（Acknowledged Limitations 时 `final/局限性.md`） |
| 25 | `methodology_snapshot` | Phase 5 终检后置（方法论留档） | 主控（亲为） | `audits/methodology-footprint-*.md`（**默认触发**，主人可 opt-out） |
| 26 | `phase5_acceptance` | Phase 5 验收 | 主人 × 主控（**人在环**） | `accepted` / `revision_requested` / `restart_phase` / `deferred`（四个 owner_checkpoint 一律 fail-closed） |

> **Phase 详细操作按需加载**：[`phase-1-details.md`](phase-1-details.md)（检索边界 / 强相关性 / 三角验证 / 数据信任 3 档）、[`phase-2-details.md`](phase-2-details.md)（退化场景）、[`phase-3-details.md`](phase-3-details.md)（写作铁律 10 项 + 洞察补充 + T6/G14 + 修订回环）。

---

## 修订回环仲裁规则

<!-- generated: rounds-contract (do not edit by hand) -->
audit_revision.max_rounds: 2
t1b_targeted_review.max_rounds: 2
g14_style_gate.recheck_max_rounds: 2
t5_style_revision.style_recheck_rounds_max: 2
t9_review.recheck_max_rounds: 0
<!-- /generated -->

> **✅ v2.12.54 主人裁定（2026-09-18 20:42）**：`≤2 轮` 覆盖 **{Phase 3.6/3.7 批判修订, Phase 4.2 审计修订}**；**Phase 3.5 主人洞察轮不计入**该预算。

| 轮次 | 内容 | 计数 |
|---|---|---|
| **0 轮** | T5 初稿 v1（Phase 3 `t5_draft_v1`） | — |
| 不计轮 | v1 → v2：**主人洞察修订**（Phase 3.5；主人选 `no_insight` 则**仍产 v2（实质 = v1，标注「主人未投喂洞察」）**） | ❌ 不计入 ≤2 轮 |
| **轮 1** | v2 → v3：**批判修订**（Phase 3.6 `t6_critique` 出报告 → Phase 3.7 `t5_feedback_revision`） | ✅ 计入 |
| **轮 2** | v3 → v4（→ v5）：**审计修订**（Phase 4.2 `audit_revision`，审计阶段内部 ≤2 轮；对外计 1 轮） | ✅ 计入 |
| minor | v 之后 minor cosmetic（≤5% 字 / 引用格式 / 拼写）→ T8 inline 亲修 | 独立登记（不计轮） |
| B 类扩写 | T9「扩写/改写清单」经主人选 B → spawn T5 v4（任务书附扩写清单 + 目标期刊要求；字数档位字段须主人拍板后才同步） | 独立登记（不计轮；决策协议真源 = `agents/09-审稿-peer-reviewer.md`「主控决策协议」） |
| 超限 | 耗尽 2 轮仍有 P0 / 结构性 P1 → **Acknowledged Limitations**（主人 20:42 裁定维持；须主人拍板） | 例外通道 |

> **对外承诺口径**：论衡对外承诺「**常规批判/审计修订 ≤2 轮**」；Phase 3.5 主人洞察轮、minor 修补通道（含「章节级 minor」）、超限例外通道均为**显式披露的独立计数**（在交付说明中登记，不混入 2 轮承诺）——不存在静默的无限修订。章节级 minor 的判据：仅改单章、不改整体结构、跨章引用/结论不变、该章字数波动 ≤5%；否则不得走 minor 通道。

> **批判项关闭核验（v2.12.70 收口，P2-1）**：T5 批判修订（Phase 3.7）后**不新增 T6 复检**；批判项「已关闭/未关闭」由 **T7 审计报告对照 T5 修订说明逐条核验**（T7 不查论证结构，仅核「逐条回应是否落实」）。确需论证结构复检时，主人可额外授权一轮 T6。

> **字数核验收口（修订回环收口，P0-4）**：论衡字数 = **单点权威核验**（T8 终检实测，或主人 host shell 跑 `匹配 '\p{Han}'` 回填 `body_char_count`），其余各阶段（T5 自报 / 修订净增）一律**估算 + 误差标注**，**主控不得每轮 read 全文数中文字符数**。修订净增用「估算 delta + 量级 sanity check」（差量级才回查），不用精确阈值。

T7 / T9 报告头部显式写 `修订回环 = N/2`（**G14 不计入修订回环 —— 首审只一次；风格修订后全文复检 ≤2 轮，v2.13.0 P0-2**）；T8 终检按此表仲裁。T9 minor 默认 T8 inline 处置；T9 major / 扩写建议 → 呈主人拍板是否启 v4。

---
