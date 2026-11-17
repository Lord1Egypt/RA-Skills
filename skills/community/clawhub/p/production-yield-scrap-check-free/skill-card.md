## Description:

生产投入产出与报废表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, and operations staff use this skill during monthly close, reconciliation, or inventory checks to verify production input, output, scrap, WIP, yield, duplicate rows, blanks, and negative quantities from a Chinese-language production yield and scrap table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version omits several production-control checks, including inter-process quantity matching.

Mitigation: Review the checks_not_run list and validate omitted controls outside the skill before relying on results.

Risk: The interface and findings are Chinese-language oriented.

Mitigation: Use it with Chinese-language source tables or route outputs to a reviewer who can read the source material and findings.

Risk: One inconsistent disclaimer line may confuse the exact scope of the checker.

Mitigation: Treat the release security guidance and the runtime checks_not_run output as the governing scope for what was and was not checked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/production-yield-scrap-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON produced by local Node.js commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows and list checks not run when the free version omits checks.]

## Skill Version(s):

1.0.57 (source: evidence.json release and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
