## Description:

长期待摊费用摊销台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。触发词包括 长期待摊费用摊销核对、长期待摊费用摊销台账对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during month-end close, reconciliation, or inventory checks to recalculate a long-term prepaid expense amortization ledger and identify arithmetic, total-row, duplicate-entry, and missing-field issues. It is a local free-tier checker and does not judge capitalization policy or amortization-period reasonableness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free-tier checker as a complete accounting review.

Mitigation: Review the listed free-version limitations before relying on output for accounting decisions; the skill states which checks are not run.

Risk: Incomplete or malformed ledger input can lead to unsupported conclusions.

Mitigation: Provide the required amortization table fields; when input is insufficient, the skill reports missing fields and withholds conclusions.

Risk: The skill executes a local Node-based checker on user-provided accounting data.

Mitigation: Install and run it only if local Node execution is acceptable in the user's environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/long-term-amortization-check-free)

## Skill Output:

**Output Type(s):** [text, json, analysis, shell commands, guidance]

**Output Format:** [Plain text or JSON findings with cited source rows and local command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports executed checks, checks not run in the free tier, local execution status, missing-input guidance, and issue summaries.]

## Skill Version(s):

1.0.57 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
