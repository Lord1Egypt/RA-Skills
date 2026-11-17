> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

> **核心精简版**（子代理必读，约 2.5K）。完整设计者文档见 [`glossary-full.md`](glossary-full.md)（含关键协议 / 工具边界 / 版本管理 / 引用形式 / 关键术语）。

## 核心角色（11 张卡，T8 终检主控亲完成不 spawn；含 T9b 压力测试卡）

| 编号 | 角色 | 关键职责 |
|---|---|---|
| T0 | 主控（Coordinator） | 任务拆解 / 派发 / 状态机 / T8 终检亲完成 |
| T1 | 文献侦查（Literature Scout） | web_search + tavily_search 检索中英文文献 + 先行者清单 |
| T2 | 数据检索（Data Scout） | 国家统计局 / 世行 / CEIC / 皮书 |
| T3 | 案例检索（Case Scout） | 企业行为 / 事件 / 司法案件 |
| T4 | 分析（Analyst） | 论点-论据映射 + 反方规划 + 三角验证 |
| T5 | 写手（Writer） | 严格按大纲 / 数据卡写，AI 去味 10 项 |
| T6 | 批判伙伴（Critical Companion） | C1-C7 七维反方对抗性复核（Phase 3.6 / `t6_critique`） |
| T7 | 审计（Auditor） | G0-G18（含 G0.5 / G2.5，共 21 项）形式核验 + 修订任务书（Phase 4） |
| T8 | 终检（Final Inspector） | 主控亲完成，不 spawn；48 必查项（可发表性判据，见 `可发表性判定表.md`）+ 小幅修补权限 |
| T9 | 同行评审（Peer Reviewer） | 6 维度评分 + 期刊匹配（Phase 4.5，默认触发；主人显式 opt-out 才关闭） |

## E1 证据对象基础层（可选能力）

启用 E1 时，使用 `PaperRecord`、`SnippetRecord` 与 `ClaimEvidenceLink` 建立主张—证据链；对象、字段、枚举和边界的唯一真源见 [`evidence-object-model.md`](evidence-object-model.md)。E1 不新增质量门、不替代 G15，也不改变旧项目兼容性；没有登记表的旧项目不得声称已完成 E1 覆盖。

## 数据信任级别 与 来源类型（两轴不混用；🟢🟡🔴 专用于时效评级）

- **信任级别（数据卡字段，M-Form-6 / M-Exist-3 校验）**：已发布（最高信任）/ 主人投喂（中）/ 二手转引（低，严格限制）—— 纯文字取值
- **来源类型（判定依据）**：一手来源（官方统计 / 同行评议 / 学术专著 / 官方一手发布，即使转载、链接指官方原文）· 二手来源（媒体转引 / 百科 / 行业报告 / 聚合平台汇编）· 单边证据（平台单方公告 / 自媒体 / 单一来源）

> **聚合类铁律**：头条聚合/数据聚合站 ≠ 一手——除非链接直接指向发布机构原文，否则一律按二手来源起步。

## 关键协议

完整 5 协议见 [`关键协议.md`](关键协议.md)。子代理执行时只需知道：

- **Phase 0 同意关卡**：外发数据必须先经主人拍板（4 选 1，全同意 / 脱敏 SVG+本地 / 部分 / 全部拒绝）
- **修订回环**：轮次计数与各通道判定 → 见 [`pipeline-overview.md`](pipeline-overview.md)「修订回环仲裁规则」（单一真源；本文件不复述轮次）
- **Phase 3.6（`t6_critique`）**：T6 从反方攻击 current_draft 出报告
- **Phase 4.4 前置（`g14_style_gate`）**：G14 定稿前最后一道闸，首审只一次（不再与 T6 同批）；风格修订后全文复检 ≤2 轮（v2.13.0 P0-2）；主人 Phase 5 签字是闭环终点
- **零 exec**：所有子代理不允许 `exec` / `process` / `browser` / `apply_patch` 等

## 工具边界（5 档子代理最小工具集声明）

| 档 | 角色 | 工具集（声明） |
|---|---|---|
| allow_research | T1/T2/T3 | read + write + edit + web_* + tavily_* |
| allow_analysis | T4 | read + write + edit |
| allow_writing | T5 | read + write + edit |
| allow_audit | T6/T7 | **read（只读）** |
| allow_review | T9/G14 | **read（只读）** |

> v2.7.12：以上为声明/部署建议，不是 spawn 传参——OpenClaw 2026.9.x 的 `sessions_spawn` 已无 toolsAllow 参数，子代理实际权限 = 平台硬性剥除（含 session_status，子代理不可持有）+ 主控策略快照 + 宿主 config `tools.subagents`（详见 SKILL.md「执行能力边界」）。
>
> **「只读」的准确定义**：指**工具面只读**（该档不得 write/edit、不得改产物），**不等于「不产出内容」**——T6/T7/T9 的报告正文一律**随交接报告回传**（final message），由**主控** `write` 落盘。故「审计员只读」与「审计报告落盘」不矛盾：写盘主体是主控，不是审计员。

> image_generate（opt-in 默认关闭）/ exec 等均在 denied 或非默认工具面；T8 由主控亲完成不 spawn。

## 编号体系

- **[Lx]** 文献 / **[Dx]** 数据 / **[Cx]** 案例——三角验证基础
- **E1 证据对象**（若项目启用）：PaperRecord / SnippetRecord / ClaimEvidenceLink 三类对象与枚举唯一真源 = [`evidence-object-model.md`](evidence-object-model.md)；`E-xxx` 证据片段 / `C-xxx` 正文主张编号均属项目内登记，不取代 [Lxx]/[Dxx]/[Cxx] 交付编号
- **D-基-xx-xx** 基线数据（资金 R / 阈值 T / 案例 C / 其他 E）必保留完整编号
