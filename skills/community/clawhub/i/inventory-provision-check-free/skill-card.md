## Description:

存货跌价准备计提表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during month-end close, reconciliation, inventory counts, or impairment provision review to check inventory provision tables for arithmetic errors, roll-forward mismatches, duplicate rows, missing required fields, and negative amounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version intentionally does not run several accounting checks, so users may over-rely on a clean result.

Mitigation: Review the listed checks that are not run and use additional accounting review before relying on the result for close, audit, or tax work.

Risk: The checker relies on the table text supplied by the user and does not validate the business basis for net realizable value or tax treatment.

Mitigation: Confirm the source assumptions, supporting records, and accounting policy outside the tool before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/inventory-provision-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with local shell commands and text or JSON checker output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; JSON output is available with --json.]

## Skill Version(s):

1.0.60 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
