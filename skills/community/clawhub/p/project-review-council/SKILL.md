---
name: project-review-council
description: 世界级项目评审委员会。Use when 用户需要项目审计、项目评审、项目复盘、项目诊断、技术评审、投资评审、商业评估、项目风险分析、Red Team、项目 Go/No-Go 决策、上线前评审、季度复盘、项目体检、投后复盘、竞品对比评审。20 角色委员会从战略/技术/产品/安全/增长/财务/竞争等维度独立审计，交叉对抗验证后输出基于证据的可执行决议。触发词：项目审计、项目评审、评审委员会、项目复盘、项目诊断、技术评审、投资评审、项目体检、Go/NoGo、Red Team、项目会诊。
---

# 项目评审委员会

20 位独立评审角色，对任意项目做对抗式多维度审计，输出基于证据的 Go/No-Go 决议。
所有角色独立思考，允许相反观点，目标是发现真问题而非给建议。

## 何时触发

项目审计 / 评审 / 复盘 / 诊断 / Go-NoGo / 投资尽调 / 上线前体检 / 投后复盘 / 季度评审。

## 角色注册表

📍 按需加载：[config/roles.yaml](./config/roles.yaml)（启用角色 + 权重）。
默认 20 角色：CEO / VC / CTO / Chief Architect / Staff Engineer / Product / UX / Growth / Security / DevOps / QA / Data / Compliance / Marketing / Sales / Customer Success / Competitor / Devil's Advocate / Independent Auditor / Future Analyst。
每角色人格与关注点见 [roles/](./roles/)，输出 schema 统一引用 [templates/role-report.md](./templates/role-report.md)。

## 执行流程（Pipeline，强制顺序，不可跳阶段）

| 阶段 | 输入 | 输出 | 文档 | Exit Gate |
|------|------|------|------|-----------|
| P1 理解 | 项目材料 | 项目画像 9 要素 | 📍 [workflows/01-understand.md](./workflows/01-understand.md) | 9 要素齐全或未知项已列出 |
| P2 证据 | 画像 | 证据清单 | 📍 [workflows/02-evidence.md](./workflows/02-evidence.md) | 每结论标记 证据/推测/待验证 |
| P3 角色审计 | 证据 | N 份角色报告 | 📍 [workflows/03-role-audit.md](./workflows/03-role-audit.md) | 每角色 7 字段齐全 |
| P4 交叉审计 | 角色报告 | 反驳记录 | 📍 [workflows/04-cross-review.md](./workflows/04-cross-review.md) | ≥3 组交叉，无遗漏 |
| P5 风险排序 | 全部问题 | 风险分级表 | 📍 [workflows/05-risk-ranking.md](./workflows/05-risk-ranking.md) | 每项含影响/概率/成本/优先级 |
| P6 隐藏问题 | 上述 | 盲区清单 | 📍 [workflows/06-hidden-issues.md](./workflows/06-hidden-issues.md) | 过度/不足已标注 |
| P7 商业评估 | 全局 | 11 维评分 | 📍 [workflows/07-business-eval.md](./workflows/07-business-eval.md) | 每维 0~10 |
| P8 执行评估 | 风险 | Top10 行动项 | 📍 [workflows/08-execution-eval.md](./workflows/08-execution-eval.md) | 含 ROI/风险/工作量 |
| P9 决议 | 全部 | Executive Summary | 📍 [workflows/09-decision.md](./workflows/09-decision.md) | 含评级 + 路线图 + Go/No-Go |
| P10 红蓝对抗 | 决议 | Final Memo | 📍 [workflows/10-red-blue.md](./workflows/10-red-blue.md) | Auditor 裁决三方观点 |

**回退规则**：证据不足致 >30% 结论标【待验证】→ 回退 P2 补证据；架构性误解 → 回退 P1。

## 评分与决策

📍 [rubrics/scoring.md](./rubrics/scoring.md) | [rubrics/risk-level.md](./rubrics/risk-level.md) | [rubrics/decision-matrix.md](./rubrics/decision-matrix.md) | [rubrics/grade-scale.md](./rubrics/grade-scale.md)

## 关键约束

1. **独立思考** — 角色间不得迎合，必须允许相反结论
2. **证据优先** — 无证据结论必须标【推测】【假设】【需要验证】
3. **干验分离** — Independent Auditor 不参与审计，只验证他人产出
4. **不保守不降标** — 不为照顾项目而弱化结论

## 输出模板

📍 [templates/](./templates/)：executive-summary / decision-memo / risk-report / scorecard / role-report

## 配置

📍 [config/settings.yaml](./config/settings.yaml)：`depth`(quick/standard/deep) | `language` | `evidence_level` | `min_report_words` | `enable_phase_10`

## 用户检查点

- P1 后：确认项目画像无误再继续
- P3 后：确认角色集再进入交叉
- P9 后：确认决议再进入红蓝

## Gotchas（上线后填充）

- 待补充：常见误判模式（如角色评分趋同 = 独立性失效）
- 待补充：证据不足时的降级策略
- 待补充：小型项目过度审计的裁剪规则
