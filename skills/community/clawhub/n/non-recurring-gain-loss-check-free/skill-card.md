## Description:

Checks Chinese non-recurring gain and loss table text for row-level arithmetic, total tie-outs, duplicate rows, blank fields, and category conflicts, with each finding tied to source text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, securities affairs, audit, and sponsor teams at listed or pre-IPO companies use this skill before annual or interim disclosure to check exported non-recurring gain and loss table text for arithmetic tie-outs, duplicate rows, blank fields, and category inconsistencies. It supports review preparation but does not replace accounting, tax, legal, or audit judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat deterministic consistency checks as audit, legal, tax, or accounting judgment.

Mitigation: Use the output as review support only; route accounting classification, tax treatment, disclosure, and assurance conclusions through qualified reviewers.

Risk: Users may provide more financial data than the checker needs.

Mitigation: Provide only the specific non-recurring gain and loss table text needed for the check.

Risk: The free edition omits documented checks that may matter for a complete review.

Mitigation: Review the listed checks-not-run before relying on the result and perform any omitted checks separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/non-recurring-gain-loss-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable console text or structured JSON findings from a local Node.js runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on provided table text; findings include severity, category, message, and source evidence when checks execute.]

## Skill Version(s):

1.0.17 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
