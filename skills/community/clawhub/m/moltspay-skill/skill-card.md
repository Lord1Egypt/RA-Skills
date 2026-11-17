## Description:

MoltsPay Skill helps an agent discover paid AI services and pay for them through MoltsPay using supported crypto chains or Alipay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqing2023](https://clawhub.ai/user/yaqing2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent find paid AI services, check wallet status, configure spending limits, and initiate payments for services such as video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer broad service-generation requests into real-money payment flows.

Mitigation: Require manual confirmation before every payment and keep low balances or use testnet funding where possible.

Risk: Setup paths can install and initialize unpinned wallet/payment tooling.

Mitigation: Review and pin the MoltsPay CLI version and provenance before running the global install or postinstall setup path.

Risk: Wallet creation and payment activity may expose funds if run in a normal user environment.

Mitigation: Use an isolated environment and enforce spending limits before funding any wallet.

## Reference(s):

- [MoltsPay Docs](https://moltspay.com/docs)
- [MoltsPay Services](https://moltspay.com/services)
- [ClawHub Skill Page](https://clawhub.ai/yaqing2023/skills/moltspay-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate wallet setup, service discovery, balance checks, spending-limit configuration, and payment commands through the MoltsPay CLI.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
