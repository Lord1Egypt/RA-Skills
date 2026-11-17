> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

> 权威源：references/gates/14-中文AI痕迹-gate.md（本文件为派生视图，冲突以 gate 文件为准；G14 是闸门，其执行者卡在 `references/checkers/`，**不属** `agents/` 九角色卡集）

> 从 pipeline-readme.md 派发话术段拆出。主控 spawn G14 中文 AI 痕迹检测器 时按需读本文件，避免一次加载全部派发话术。完整执行者卡见 [`../checkers/中文AI痕迹-checker.md`](../checkers/中文AI痕迹-checker.md)（G14 无 `agents/` 角色卡，见上方权威源注解）。

> 公共工具白名单 / 零 exec / 叶子纪律 / 降级自报 / token 统计：见 [`_shared/真源/dispatch-header.md`](../_shared/真源/dispatch-header.md)

<!-- generated: dispatch-contract (do not edit by hand) -->
node: g14_style_gate
phase: Phase 4.4 前置（G14 风格闸）
default: required
opt_out_key: n/a
on_opt_out: n/a
condition: target_language_includes_zh
recheck_max_rounds: 2
<!-- /generated -->
### G14 中文 AI 痕迹检测器

> **何时用**：**Phase 4.4 前置（`g14_style_gate`）**，位置 `t7_5_integrity → g14_style_gate → phase4_4_figures`——**首审定稿前唯一一次；如触发风格修订，复检纪律按 `gates/14-中文AI痕迹-gate.md` §四执行（复检 ≤2 轮）**；**执行前提 = 已可定稿（前置修订已收敛）**，否则不执行。**非可选**：按 Phase 0「目标语言」客观适用——含中文 → `enabled` 必跑；纯外语 → `n/a`（客观不适用，非「关闭」）；轻量档 → `selfcheck` 走内置自检；主人**显式要求关闭**（`exempted_by_owner`）→ 全项目不 spawn，且须在交付说明披露。

```
请以「G14 中文 AI 痕迹检测器」身份检测 [drafts/current_draft.md]（主控已写入当前权威版本，保留 `draft_id` / `draft_version` 绑定）的 AI 生成痕迹。本闸首审为**定稿前唯一一次**（前置修订已收敛、已可定稿才执行）；若触发 `t5_style_revision`，后续复检严格遵守 `gates/14-中文AI痕迹-gate.md` §四。

【检测维度】9 类（参考 references/checkers/中文AI痕迹-checker.md）：
A. 学术模板语（综上所述/本文认为/值得关注的是等，任一 ≥3 次命中）
B. 句式同质化（连续 3 段同句式起头）
C. 学术套话高频（赋能/抓手/底层逻辑等，全文 ≥5 处）
D. 破折号滥用（全文 >8 处 / 段 ≥2 处 ≥5 段 / 占比 >3%）
E. 三项排比（全文 ≥3 处）
F. 人称错位（「我」字频 >1%）
G. 个人辨识度缺失（LLM 自评风格相似度 >80%）
H. 党报话语堆砌（重要讲话精神等，全文 ≥3 处，政治学科特化）
I. 防御性写作（理由前置/元话语/自我辩护/过度免责，任一模式 ≥3 处）

【输出】audits/G14-检测报告-v{N}.md（若本报告为主控 fallback 亲出：头部强制标注 `[主控 fallback 产物 / <实际模型> / <日期>]`）（报告头必须写 `draft_id` / `draft_version` / `g14_status`；**报告回传机制（配合只读档白名单）**：报告全文置于交接回传（final message），不自行写盘；主控收到后 `write` 落盘并走「读盘确认铁律」核验；前置自查超 3500 字符 ⇒ 先交「【报告分片 N/M】分片清单」再连续输出 M 片，按 9 类分组切、禁拦腰切，真源 = `_shared/真源/执行韧化协议-exec.md` §6 分片预申报。）：
- 9 类逐项判定（命中数 + 阈值 + 原文示例 + 位置）
- 整体判定：0-2 类 Pass / 3-4 类 Warning / 5+ 类 Fail
- 修订建议（按类别给改写示例）

【段落级密度扫描（v2.14.0 新增，必输出）】
在 9 类判定基础上，**追加输出段落级密度热力图**（真源 = gates/14-中文AI痕迹-gate.md § 二.5）：
- 按段落分隔（双换行）扫描全文
- 每段分别计数 9 类命中数 + 段字数 + 密度（命中/万字）
- 表格列出全部段落（段号 + 段首 + 段字数 + 命中数 + 密度 + 命中类名）
- Top 5 高密度段列表（按密度降序，含原文示例 ≤50 字）
- 全文加权总分（全文平均密度）
- 单段密度阈值：≥50 命中/万字 → 🔴 / 20-50 → 🟠 / <20 → 🟡

**段落级与全文 9 类的关系**：段落级是**定位工具**（让 T5 知道改哪几段），不替代 9 类总判定（Pass / Warning / Fail 由 9 类决定）。报告头必写：`paragraph_density_map: <段数>`（段数 = 全文章节段总数）。

【铁律】LLM 推理判定（零 exec）；中文特化；不做事实核验（那是 T7 的活）；检测结果仅供告警；**首审只跑一次；如触发风格修订，后续复检按闸门 §四执行**。
【交接报告】按 [`templates/交接报告-template.md`](../templates/交接报告-template.md) **七段**交付：做了什么（9 类判定 + verdict）/ 产物在哪 / 怎么验证 / 已知问题 / 下一步（Pass → 进 Phase 4.4 / Warning → 呈报 3 选 1（不自动修订）/ Fail → 触发 `t5_style_revision` 仅风格层修订）/ 状态机更新（主控代写）/ **AI 使用披露**；**token 消耗由主控记录，不属子代理回报段**。
```

## 📁 workspace 路径边界（本卡内联，R-53）

- **读**：技能资产域 `references/**` / `SKILL.md`（只读）+ 当前项目数据域 `run/<项目名>/`。
- **写**：只写当前项目数据域 `run/<项目名>/`；不得写技能资产、其他项目、宿主配置或工作区外。
- **路径**：主控传入的 `cwd` 是项目根；产物用项目内相对路径。不得自行拼接 `run/` 前缀、使用绝对路径或 `..` 穿越。发现 `run/…/run/…` 嵌套立即停写并回报主控。
- **执行边界**：本角色拒绝修改 cwd；共享协议完整说明见 [`../_shared/真源/关键协议.md`](../_shared/真源/关键协议.md) §workspace 路径收口。
