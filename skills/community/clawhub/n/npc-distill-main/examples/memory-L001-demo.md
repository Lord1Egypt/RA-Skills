---
npc_id: L001
relation: direct_superior
created: '2025-09-12'
updated: '2026-05-20'
evidence_count: 32
confidence: high
decision_axes:
  data_vs_intuition: 0.72
  short_vs_long_term: 0.40
  risk_appetite: 0.30
  innovation_vs_execution: 0.65
  top_down_vs_bottom_up: null
communication_style:
  prefers_bluf: true
  ideal_doc_length: one-pager
  tolerates_uncertainty: false
  interrupt_frequency: high
  feedback_style: direct
frequent_challenges:
- theme: ROI测算依据
  weight: 0.85
  evidence:
  - C-20250312-001
  - C-20250418-003
  - C-20260201-007
- theme: 竞品对标
  weight: 0.72
  evidence:
  - C-20250205-007
  - C-20250622-002
- theme: 执行人是谁
  weight: 0.68
  evidence:
  - C-20251015-004
- theme: 风险预案
  weight: 0.51
  evidence:
  - C-20251128-002
redlines:
- 避免"大概""可能"等模糊词,要给区间或置信度
- 汇报不超过3页,超过会被打断
- 不接受口头承诺,要书面跟进
- 不提"我以为""我感觉"开头的判断
- 数据必须有时间戳和样本量
preferred_patterns:
- 数字 + 同比 + 建议三段式
- 结论第一句先抛出,后面再展开
- 给2-3个选项让他选,而不是单方案
- 提风险时同时给缓解措施
evidence_by_axis:
  data_vs_intuition: 18
  short_vs_long_term: 8
  risk_appetite: 12
  innovation_vs_execution: 6
  top_down_vs_bottom_up: 2
---

# L001 画像综述

> ⚠️ 这是一个**虚构示例画像**,用于演示 Skill 功能。
> 真实使用时,请创建你自己的 memory-{npc_id}.md,从零构建。

## 决策风格综述

L001 是偏数据驱动型决策者,质疑数据来源与样本量是其高频反应模式。
对短期可量化结果敏感,长期愿景类汇报必须配阶段性里程碑才能通过。
风险偏好偏保守,但对成熟领域的创新有一定接纳度——拒绝是"在没验证的领域冒险"。

## 高频反应模式

- 听到"差不多/应该/可能" → 几乎必定追问具体数字与置信区间
- 听到新方案 → 先问"竞品有没有做过、做得怎样"
- 听到团队进度 → 追问"谁是责任人,什么时候节点"
- 听到风险 → 追问"如果发生了,Plan B 是什么"

## 沟通偏好

- BLUF 结构:第一句必须给结论,没耐心等铺垫
- 一页纸文档:超过 3 页会让人压缩重发
- 不接受不确定:回答"我不知道"比"我估计..."更安全
- 高频打断:平均每 2-3 分钟会插话,要随时停下来回应

## 雷区清单

参见 frontmatter 的 `redlines` 字段。

---

# 语料库

## C-20260201-007 · Q4复盘会上的方案讨论

- date: 2026-02-01
- scene: Q4复盘会
- channel: 会议
- attribution: direct
- weight: 1.0
- tags: [质询-ROI, 风格-直接]

**场景背景**: 增长团队汇报Q4 GMV超额完成,提出加大投放预算

**内容**:

> "GMV 涨了 30%,但 ROI 测算用的是哪个口径?
>  如果剔除节假日效应和现金券补贴,实际增长是多少?
>  下次汇报先把这个底层数据讲清楚。"

**抽取信号**:

- challenges_raised: ROI测算依据 (intensity: high)
- challenges_raised: 数据样本量 (intensity: high)
- style: prefers_bluf=true
- style: feedback_style=direct

**我的判断**: 他不接受表面数据,要看剥离干扰因素后的真实增长。
下次汇报必须主动说明"剔除 XX 后净增长 YY%"。

---

## C-20251128-002 · 战略会风险讨论

- date: 2025-11-28
- scene: 战略会
- channel: 会议
- attribution: direct
- weight: 0.95
- tags: [质询-风险, 风格-追问]

**内容**:

> "你说这个方案落地不会有大问题,但'不会'是什么概率?
>  万一出问题,我们的兜底方案在哪?谁负责?
>  没有兜底方案的方案,我不批。"

**抽取信号**:

- challenges_raised: 风险预案 (intensity: high)
- redline_signals: 没有 Plan B 的方案不批
- preferences: risk_appetite direction=0 strength=0.7

---

## C-20251015-004 · 邮件回复 - 项目进度

- date: 2025-10-15
- scene: 项目周报回复
- channel: 邮件
- attribution: direct
- weight: 1.0
- tags: [质询-执行人]

**内容**:

> "看了你发的周报。\"团队会跟进\" - 团队是谁?
>  我需要看到具体的责任人姓名和承诺日期。
>  请重新发一版,把这个补齐。"

**抽取信号**:

- challenges_raised: 执行人是谁 (intensity: high)
- redline_signals: 不接受"团队会跟进"这种模糊主语
- style: feedback_style=direct

---

## C-20250622-002 · 周会方案评审

- date: 2025-06-22
- scene: 周会
- channel: 会议
- attribution: direct
- weight: 0.9
- tags: [质询-竞品]

**内容**:

> "在做之前,先看看竞品已经做到什么程度。
>  如果他们做过且失败了,我们要想清楚为什么我们能成功;
>  如果他们没做,要想为什么他们没做。"

**抽取信号**:

- challenges_raised: 竞品对标 (intensity: high)
- preferences: innovation_vs_execution direction=0.5 strength=0.5
- preferences: risk_appetite direction=0 strength=0.6

---

## C-20250418-003 · 邮件 - 预算讨论

- date: 2025-04-18
- scene: 预算回复
- channel: 邮件
- attribution: direct
- weight: 0.95
- tags: [质询-ROI]

**内容**:

> "申请的预算我看了,你说'预计带来 200 万收入'。
>  这 200 万的口径是 GMV 还是净收入?投入产出比是多少?
>  按现有数据,我能算出来这个 ROI 不及格。
>  你重新算一遍,带个 Excel 给我。"

**抽取信号**:

- challenges_raised: ROI测算依据 (intensity: high)
- style: prefers_bluf=true
- preferences: data_vs_intuition direction=1 strength=0.9

---

## C-20250312-001 · Q1业务复盘会

- date: 2025-03-12
- scene: Q1业务复盘会
- channel: 会议
- attribution: direct
- weight: 0.85
- tags: [质询-ROI, 风格-直接]

**场景背景**: 产品团队汇报Q1新功能上线效果,展示了DAU增长曲线

**内容**:

> "DAU 这个数字我看了,但用户使用时长有没有同步提升?
>  如果时长没涨,可能只是把存量用户挪进来了。
>  你拿过去 6 周的时长数据和留存数据再算一遍,下周二之前给我。"

**抽取信号**:

- challenges_raised: ROI测算依据 (intensity: high)
- challenges_raised: 数据样本量 (intensity: medium)
- style: prefers_bluf=true
- style: interrupt_frequency=high
- preferences: data_vs_intuition direction=1 strength=0.8

**我的判断**: 他不是反对 DAU 这个指标,而是怀疑指标的代表性。
下次汇报功能效果,必须**同时给 DAU、时长、留存**的组合指标,
而且要说清楚样本时间窗口。

---

## C-20250205-007 · 战略讨论会

- date: 2025-02-05
- scene: 战略讨论会
- channel: 会议
- attribution: direct
- weight: 0.85
- tags: [质询-竞品]

**内容**:

> "在评估这个机会前,先把竞品矩阵列出来:
>  谁在做、做到什么阶段、用户反馈如何、商业模式跑通了没。
>  没有这个矩阵,我们的方案就是闭门造车。"

**抽取信号**:

- challenges_raised: 竞品对标 (intensity: high)
- preferences: data_vs_intuition direction=1 strength=0.7
