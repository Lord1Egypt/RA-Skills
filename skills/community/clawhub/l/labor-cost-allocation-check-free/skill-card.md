## Description:

工时与人工成本分摊表逐项核对，覆盖逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, bookkeeping, and operations staff use this skill during monthly close, reconciliation, or inventory review to check labor-hour and labor-cost allocation tables. It recalculates included arithmetic checks, flags duplicate or blank rows, and cites source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release omits listed checks, so users may miss issues outside the included free checks.

Mitigation: Use the skill only for the included checks and apply manual review or a fuller tool for omitted and out-of-scope checks.

Risk: Results depend on complete, correctly formatted user-provided tables.

Mitigation: Provide tables with headers and source rows; treat insufficient-input responses as no conclusion.

Risk: Chinese-language prompts and output may not fit every review workflow.

Mitigation: Install only where Chinese-language input and output are acceptable for the intended users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/labor-cost-allocation-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing check results, missing-input guidance, included checks, and omitted free-edition checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided labor cost allocation tables; the free edition reports omitted checks and returns insufficient-input status rather than a conclusion when required material is missing.]

## Skill Version(s):

1.0.53 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
