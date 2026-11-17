## Description:

租赁负债摊销表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly close, reconciliation, or inventory checks to review lease liability amortization tables. It checks local table arithmetic, totals, duplicate periods, blank placeholders, and negative amounts, and it reports findings with source line references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as professional accounting assurance or rely on it for checks it does not run.

Mitigation: Use the findings as local table checks only, and separately verify omitted areas such as discount-rate interest calculations, negative-liability conditions, accumulated depreciation limits, and lease term assumptions.

Risk: One disclaimer phrase overstates interest-rate checking that the free version omits.

Mitigation: Use the explicit free-version scope and checks_not_run output when deciding whether additional accounting review or a fuller tool is required.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/chenqg618/skills/lease-liability-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable console text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js, reads a supplied lease amortization table or the bundled sample, and reports insufficient input instead of making unsupported conclusions.]

## Skill Version(s):

1.0.39 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
