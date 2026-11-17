## Description:

进度款申请与产值确认表逐项核对（申请/确认产值比对、确认产值×支付比例复算、累计确认产值滚动、本期实付勾稽、合计逐列复核、重复与空缺检测），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Construction and engineering finance teams use this skill to check progress payment applications and output-value confirmation tables before payment review. It verifies table arithmetic and reports line-cited discrepancies or missing required columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks table arithmetic but does not validate construction completion, approvals, contract legality, or other business and legal facts.

Mitigation: Treat findings as calculation support and have qualified reviewers verify the underlying project records, approvals, and contract terms before payment decisions.

Risk: Missing headers or incomplete table data can prevent reliable conclusions.

Mitigation: Provide the full table including headers and review any insufficient-input response before rerunning the check.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/progress-output-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable text or JSON results with line-cited findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports insufficient input instead of making unsupported conclusions.]

## Skill Version(s):

1.0.8 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
