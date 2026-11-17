## Description:

Calculates China court litigation fees, case acceptance fees, and application fees under the Measures for Payment of Litigation Fees using user-provided case facts and the skill's local fee-rule references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

External users, legal practitioners, and developers use this skill to organize China court fee facts, call the available deli-cli calculation flow, and produce a fee calculation summary with applicable segments, caps, and rule references.

### Deployment Geography for Use:

Global, for China court fee calculations

## Known Risks and Mitigations:

Risk: The skill asks agents to run a mutable third-party CLI package.

Mitigation: Review the package before use and prefer a pinned CLI version for routine workflows.

Risk: Fee-calculation facts may be sent to an external calculation service.

Mitigation: Avoid entering names, identity numbers, case numbers, addresses, or unrelated confidential details.

Risk: API-key setup and storage may affect credential handling.

Mitigation: Use safer API-key entry and storage practices and limit access to the configured CLI environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/coolalam/skills/litigation-fee-calculator)
- [deli-cli 通用前置](references/cli-common.md)
- [诉讼费用 CLI 场景指南](references/cli-litigation-fee-guide.md)
- [诉讼费用交纳办法费用规则](references/litigation-fee-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with calculation breakdowns and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Amounts should preserve the user's stated amount basis, show segments or caps where relevant, and cite local rule articles or CLI-returned basis fields.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata shows 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
