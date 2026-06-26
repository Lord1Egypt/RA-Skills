# Market Research

## 1. Goal

Combine current market signals with the user’s recorded preferences to produce a clear topic decision and title decision.

This stage is the decision core of Discovery.

---

## 2. Required input

You must have:
- a hot-search / trend-scan artifact
- a user-preference artifact
- enough direction to compare candidate topics meaningfully

Recommended upstream artifacts:
- `00A_热点扫描.md`
- `00B_用户偏好.md`

---

## 3. Forbidden to start if

Do not start if:
- no scan artifact exists
- no preference artifact exists
- the project still lacks enough direction to compare real options

---

## 4. Required analysis dimensions

For each serious candidate direction, evaluate:
- current heat or commercial viability
- target reader fit
- hook clarity
- emotional value
- conflict engine
- sustainability for long serialization
- saturation risk
- differentiation angle
- adaptation potential if relevant

A candidate that cannot be compared across these dimensions is not a complete candidate.

---

## 5. Required output

This stage must produce a conclusion-oriented topic report written into:
- `00_选题报告.md`

The report must not be only a raw information dump.
It must include clear conclusions.

---

## 6. Mandatory report structure

Use `references/topic-report-template.md` as the default template for `00_选题报告.md`.
Do not invent a radically different report shape unless the user explicitly asks for it.

`00_选题报告.md` must include all of the following sections:

1. 用户偏好摘要
2. 热点扫描摘要
3. 候选题材对比（3-5个，除非用户明确要求更少）
4. 最终推荐题材
5. 推荐理由
6. 不选其他方向的原因
7. 标题候选
8. 最终标题 / working title
9. 一句话核心钩子
10. 项目方向结论
11. 风险提醒
12. 下一阶段建议

---

## 7. Discovery-stage artifact rule

Discovery stage should leave reusable artifacts behind.
At minimum, the following three records should exist by the end of Discovery:

- `00A_热点扫描.md`
- `00B_用户偏好.md`
- `00_选题报告.md`

Do not rely only on chat memory for these three layers.
They must be written to files so the project can resume after interruption.

Discovery also runs the Cliche Exhaustion Loop in `quick` mode:
- surface the intuitive cliché version for each serious candidate
- preserve only the novelty axes worth carrying forward into planning
- keep the branch-level anti-cliche scratch work under `staging/` unless a supervisor-approved branch conclusion authorizes backfill

---

## 8. Completion standard

This stage is complete only if:
- `00_选题报告.md` exists
- it contains explicit candidate comparison
- it contains one explicit top recommendation
- it contains title candidates
- it contains a final title or explicitly approved working title
- it contains a one-sentence core hook
- it contains project-direction guidance
- the user explicitly approves the discovery result and allows advancement

---

## 9. Do not advance if

Do not advance if:
- the report is only descriptive and not decision-oriented
- no top recommendation exists
- title status is unresolved
- the three discovery artifacts are incomplete
- the user still has unresolved objections
- explicit user approval to advance is missing

---

## 10. Rollback condition

Return to market research or earlier discovery work if:
- title selection reveals poor positioning
- the chosen topic proves structurally weak for planning
- the user changes audience, platform, or commercial goal in a way that invalidates the current recommendation
- the scan and preference artifacts are no longer aligned with the chosen recommendation

---

## 11. Quality bar

A valid market research result is:
- comparative
- decision-oriented
- audience-aware
- platform-aware
- explicit about risks
- written in reusable project artifacts

Invalid output includes:
- generic hype with no comparison
- no top choice
- no title candidates
- title candidates disconnected from topic logic
- no conclusion layer
- no persistent discovery artifacts
