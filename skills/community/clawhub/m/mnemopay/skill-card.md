## Description:

MnemoPay is a Trust OS for AI agents that handle money or consequential actions, adding governed memory, payments, reputation, identity, approvals, audit evidence, and durable browser, code, and computer jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t49qnsx7qt-kpanks](https://clawhub.ai/user/t49qnsx7qt-kpanks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use MnemoPay to give agents governed memory, payment, identity, approval, audit, and durable job capabilities while controlling high-impact or monetary actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run a money and identity MCP service from unpinned packages.

Mitigation: Review before installing and prefer a pinned, reviewed SDK version or a fixed local executable instead of unattended npx package resolution.

Risk: Payment and other high-impact actions could execute without sufficient user intent if exposed too broadly.

Mitigation: Require explicit approval and a clear amount, currency, recipient, and reason before payment actions or other consequential operations.

Risk: Admin, operator, or broad tool groups could give ordinary agents excessive authority.

Mitigation: Use only the minimum needed tool group and keep organization_admin, operator, and all outside ordinary or untrusted agent configurations.

## Reference(s):

- [MnemoPay website](https://mnemopay.com)
- [MnemoPay SDK on npm](https://www.npmjs.com/package/@mnemopay/sdk)
- [MnemoPay Python package](https://pypi.org/project/mnemopay/)
- [MnemoPay SDK repository](https://github.com/mnemopay/mnemopay-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
