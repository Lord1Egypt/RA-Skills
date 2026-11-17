## Description:

政府补助与递延收益核对表逐项核对，执行免费版的逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill during monthly close, reconciliation, or inventory-style review to check government subsidy and deferred income schedules for arithmetic, roll-forward consistency, totals, duplicate rows, blanks, placeholders, and negative amounts. It does not make accounting judgments about subsidy classification or recognition timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version intentionally omits several checks, so a clean result is limited to the included checks.

Mitigation: Treat results as a scoped table-reconciliation aid and separately review omitted checks or use a complete review workflow when those risks matter.

Risk: The skill processes government subsidy and deferred income table data through a local Node script.

Mitigation: Run it only in a trusted local environment and review outputs against source records before using them in financial reporting.

Risk: The skill does not judge subsidy classification, recognition timing, tax treatment, or document-term compliance.

Mitigation: Have qualified finance or accounting personnel make those judgments outside the tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/gov-subsidy-deferred-income-check-free)
- [Skill instructions](artifact/SKILL.md)
- [Execution wrapper](artifact/scripts/run.mjs)
- [Checking engine](artifact/scripts/engine/gov-subsidy-deferred-income-check.js)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text]

**Output Format:** [Human-readable text or JSON report with cited findings, executed-check scope, omitted checks, and insufficient-input messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally according to artifact behavior and server security evidence; no network use was reported.]

## Skill Version(s):

1.0.42 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
