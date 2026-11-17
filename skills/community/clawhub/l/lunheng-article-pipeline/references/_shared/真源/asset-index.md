> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 资产与文档索引（角色卡 / 模板 / 项目目录 / 核心文档）

> **本文件是 SKILL.md「项目目录结构 + 角色卡与模板」「核心文档索引」两段的外移正文**（按需加载：主控需要定位资产或查「某文档在哪个时机读」时才读）。

## 项目目录结构 + 角色卡与模板

**项目目录**（`run/<项目名>/`）：

```
├── 01-任务简报.md       # Phase 0
├── status.md            # 状态机（Inbox→Assigned→In Progress→Review→Done|Failed）
├── literature/文献卡.md # T1: [L01]...
├── data/数据卡.md       # T2: [D01]... 含来源机构+年份+URL+时效🟢🟡🔴
├── cases/案例卡.md      # T3: [C01]... 多方说法+≥2 来源
├── analysis/分析大纲.md # T4: 论点-论据映射 + 反方规划
├── analysis/批判报告-vN.md # T6: C1-C7 七维批判
├── drafts/初稿-vN.md + 修订说明-vN.md # T5 + 修订稿
├── audits/审计报告-vN.md# T7: P0/P1/P2
├── final/定稿.md + final/图件/ + final/证据包/ + final/交付说明.md # Phase 5
├── viz/index.html       # 运行期可视化快照（v2.17.1；遥测视图，**非交付物**，不进 final/）
```

**角色卡**（11 概念角色 / 12 物理卡文件，计数真源 = counts.yaml）：`references/agents/`（T8 终检有独立角色卡 `08-终检-final-inspector.md`，由主控亲完成不 spawn；T9b 默认不跑，见 phase-order）
**角色速查**（11 张角色卡，`references/agents/`；T8 由主控亲完成不 spawn）：

| 角色 | 职责 | 产出 |
|---|---|---|
| **T1** 文献检索 | 并行检索已发布文献 | `literature/文献卡.md` |
| **T2** 数据检索 | 并行检索数据（含时效 🟢🟡🔴） | `data/数据卡.md` |
| **T3** 案例检索 | 多 Agent + Phase 0 确认案例需求时并行检索；0 条出空卡 | `cases/案例卡.md` |
| **T4** 分析 | 论点-论据映射 + 反方规划 + 三角验证 | `analysis/分析大纲.md` |
| **T5** 写作 | 初稿 + 修订（引用标 [Lxx]、数字标 [Dxx]、案例标 [Cxx]） | `drafts/初稿-vN.md` |
| **T6** 批判 | C1-C7 七维批判（攻击 v2 不是 v1） | `analysis/批判报告-vN.md` |
| **T7** 审计 | G0-G18 独立审计（只审不改） | `audits/审计报告-vN.md` |
| **T8** 终检 | 可发表性 48 项终检（主控亲完成，不 spawn） | `final/定稿.md` + 交付说明 |
| **T9** 同行评审 | 6 维度评分（默认触发；主人显式 opt-out 才关闭） | `audits/审稿报告-vN.md` |

**流水线运行手册**（派发话术索引 + 模型配置 / 模板加载策略等百科内容；派发话术正文见 `references/dispatch/`，T8 不 spawn）：`references/pipeline-readme.md`

**模板**（类数以实际枚举为准，含 lite + full）：`references/templates/`（任务简报 / status状态机 / 交接报告 / 文献卡 / 数据卡 / 案例卡 / 先行者清单 / **证据登记表 / 主张—证据映射** / **检索覆盖矩阵（v2.17.0 新增，Phase 0 建表 + Phase 1 对账）** + 审稿报告 / 修订说明 / 投稿就绪检查表 / checkpoint-card）

**素材与论据检索（v2.17.0 升级面）**：工具清单与档位真源 = SKILL.md frontmatter `metadata.tools.academic_extra`（学术检索与元数据层，opt-in，23 项）；**用法 / 梯队 / 同意门 / 去重规则唯一真源** = [`中文数据源集成.md`](中文数据源集成.md)；三员决策树唯一真源 = 各角色卡（`01-文献检索` / `02-数据检索` / `03-案例检索` 的 §工具选用决策树），派发话术只留纪律不复制树；Phase 1 覆盖对账 + 冲突仲裁 = [`phase-1-details.md`](phase-1-details.md) §Phase 1 覆盖对账；T1b 机械核验路径 = [`../dispatch/T1b-定向回查.md`](../../dispatch/T1b-定向回查.md)。

**E1 证据对象基础层（第一阶段）**：对象、字段、枚举和边界唯一真源 = [`evidence-object-model.md`](evidence-object-model.md)；运行期登记模板 = [`evidence-register-template.md`](../../templates/evidence-register-template.md)；T4 初始映射模板 = [`claim-evidence-map-template.md`](../../templates/claim-evidence-map-template.md)。E1-0 仅落基础资产，尚未接入角色、闸门或外部全文服务。

**关键参考**：

- 字数判定表（T7+T8 共用单一真源）：[`字数判定表.md`](字数判定表.md)
- 状态归约契约（字段级写入权 + 归约器；全产物族并发写唯一真源）：[`状态归约契约.md`](状态归约契约.md)
- 退化场景规范（跳过 Phase 3.5）：[`degraded-scenarios.md`](degraded-scenarios.md)
- 期刊数据库 + 匹配算法：[`期刊数据库.md`](期刊数据库.md) + [`期刊匹配算法.md`](期刊匹配算法.md)
- 中文数据源集成（OpenAlex/Crossref 默认关闭、Phase 0 勾选，无需 Key）：[`中文数据源集成.md`](中文数据源集成.md)
- 多格式导出（可选 `--format md/latex/docx/pdf`）：[`format-export.md`](format-export.md)
- 性能基准（四维实测登记）：[`performance-benchmarks.md`](performance-benchmarks.md)
- 实战案例库：[`references/case-studies.md`](../../case-studies.md)（设计文档已收敛为纯索引页，不入本表）
- 方法论实时可见面板（6 字段：当前阶段/证据强度/已触发闸门/下一步预测/不确定性/本轮模型分配）：[`status-template.md`](../../templates/status-template.md)「方法论足迹」段；**镜像工件 = `viz/index.html`**（v2.17.1，自包含单文件；规格 = [`图表-SVG-template.md`](../../templates/图表-SVG-template.md) §七；渲染面板属宿主侧职责）

**T9 同行评审**（默认触发；主人显式 opt-out 才关闭）：6 维度 1-5 分（原创性 / 方法论 / 证据强度 / 论证结构 / 写作质量 / 引文规范），26-30 accept / 21-25 minor / 16-20 major / <16 reject。详见 [`references/agents/09-审稿-peer-reviewer.md`](../../agents/09-审稿-peer-reviewer.md) + [`references/templates/审稿报告-template.md`](../../templates/审稿报告-template.md)。

**G14 中文 AI 痕迹深度检测闸**：9 类检测维度（学术模板语 / 句式同质化 / 学术套话高频 / 破折号滥用 / 三项排比 / 人称错位 / 个人辨识度缺失 / 党报话语堆砌 / 防御性写作），**LLM 推理判定**（零 exec 依赖）。0-2 类 Pass / 3-4 类 Warning（主控呈报 3 选 1，不自动修订）/ 5+ 类 Fail → `t5_style_revision`（仅风格层修订 + 复检 ≤2 轮；不重跑全流程其余节点）。详见 [`references/gates/14-中文AI痕迹-gate.md`](../../gates/14-中文AI痕迹-gate.md)。**目标语言含中文即必跑（非可选）；位置 = Phase 4.4 前置（`g14_style_gate`），首审只一次；如触发风格修订，按闸门 §四全文复检 ≤2 轮（v2.13.0 P0-2）**。 <!-- G14 九类判定真源 = gates/14-中文AI痕迹-gate.md §二 + checkers/中文AI痕迹-checker.md（本节不重列九类） -->

## 核心文档索引（按需加载）

主控按需加载时查此表，不凭记忆找文件：

| 用途 | 文档 | 加载时机 |
|------|------|---------|
| 核心概念单一真源（11 概念角色 + 三层防御 + 数据信任 3 档 + 工具边界）| [`glossary-full.md`](glossary-full.md)；子代理必读精简版 [`glossary-core.md`](glossary-core.md) | 🟡 按需 |
| 运行模式判据单源（全自动语义 / 27 节点行为矩阵 / 永不自动停点 / 模式切换）| [`运行模式对照表.md`](运行模式对照表.md)（真源） | Phase 0 定运行模式时（🔴 必读） |
| 快速开始（5 分钟上手）| [`QUICKSTART.md`](../../../QUICKSTART.md) | 新用户首读 |
| 模型 5 档候选池 + 映射规则 | [`模型候选池.md`](模型候选池.md)（唯一真源；[`model-assignment.md`](../../model-assignment.md) 已降级为指针页） | Phase 0 静态映射 |
| 交付边界 + F1-F9 失败模式 + M 门 + 阶段闸门 | [`deliverables.md`](../../deliverables.md) | Phase 0 读 / Phase 4-5 复核 |
| F 体系详解 | [`failure-modes.md`](failure-modes.md) | Phase 0 / 4 |
| 错误友好化（13 类常见错误）| [`errors.md`](../../errors.md) | 出错时查 |
| 配图 + 写手禁做 + 成本模型 | [`operations.md`](../../operations.md) | Phase 4.4 |
| 证据检索边界（能/不能主动采集，判断口诀「这是已发布证据吗」）| [`phase-1-details.md`](phase-1-details.md)「检索边界」| Phase 1 |
| G0-G18 审计详解 | [`audit-checklist-quickref.md`](audit-checklist-quickref.md) | Phase 4 |
| M 门算法完整规约 | [`M-Gate-核心.md`](M-Gate-核心.md)（🟠 分片必读：伪代码段必读 / 附录按需 → [`M-Gate-Algorithm-appendix.md`](M-Gate-Algorithm-appendix.md)）| 跑 M 门前 + T8 终检前 |
| 实战案例库（商业热点 / 品牌一致性 / 原创性悖论）| [`case-studies.md`](../../case-studies.md) | 参考 |

---
