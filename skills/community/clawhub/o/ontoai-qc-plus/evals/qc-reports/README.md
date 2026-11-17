# Self-QC Reports / 自我质检报告

**English**: These are the real QC reports produced by ontoAI Quality Inspector inspecting **itself**, each run in an independent session (the inspector never reads its own development context — see the "independence rule" in `SKILL.md`). Two full inspection rounds were run; every Must-Fix finding was repaired in the following release.

**中文**：以下是 ontoAI 质检官**质检它自己**的真实报告，每轮均在独立会话中执行（质检官不读自己的开发过程——见 `SKILL.md` 的"独立调用三约束"）。共两轮全量质检，所有必改项已在后续版本中修复。

## Round 1 → inspected v1.4.1 / 第一轮 → 受检版本 v1.4.1

- **File**: `qc-report-round1-v1.4.1.html` (Style C · Modern Charts, Chinese chrome)
- **Findings**: 5 Must Fix / 6 Should Fix / 3 Unverified → all repaired in **v1.4.2** (MIT LICENSE, `PROTECT()` field protection, L1–L7 alignment, delivery contract, …)

## Round 2 → inspected v1.4.2 / 第二轮 → 受检版本 v1.4.2

- **Files**: `qc-report-round2-v1.4.2.html` + `qc-report-round2-v1.4.2.pdf` (Style A · Official Inspection Report, delivered as both HTML and PDF per the delivery contract)
- **Findings**: 4 Must Fix / 4 Should Fix / 2 Unverified → all repaired in **v1.4.3** (RL1–RL4 rule-level renaming, scoring precedence rule, counting self-consistency, upstream links, …)

> **Note / 说明**: The findings listed inside each report describe the *old* version under inspection and are kept verbatim for authenticity — check the corresponding release notes in [`CHANGELOG.md`](../../CHANGELOG.md) to see how each was fixed.
>
> 报告内的"必改/可改"描述的是**受检当时**的旧版本，为保持真实性原文未作改动；每条如何修复见 [`CHANGELOG.md`](../../CHANGELOG.md) 对应版本条目。
