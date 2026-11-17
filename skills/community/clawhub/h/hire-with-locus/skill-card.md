## Description:

Enables AI agents to send USDC payments and order freelance services through an escrow-backed marketplace on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjorgensen](https://clawhub.ai/user/wjorgensen)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to fund wallets, send USDC, order freelance services through Locus escrow, and monitor order status until completion or cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend USDC or place paid freelance orders when configured with a valid API key.

Mitigation: Set strict allowance, maximum transaction size, and approval-threshold limits before use, and require human approval for larger payments.

Risk: A leaked Locus API key can allow another party to spend from the configured wallet.

Mitigation: Store the API key with restrictive permissions or a secret manager and send it only to api.paywithlocus.com.

Risk: The heartbeat recommends periodically fetching remote instructions, which can change outside the reviewed release.

Mitigation: Do not enable remote self-updating heartbeat behavior unless the user accepts that future instructions may change outside the reviewed package.

Risk: Freelance order requests may include confidential details or public asset links.

Mitigation: Avoid sharing confidential order details, private links, or sensitive source material in order requests.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/wjorgensen/skills/hire-with-locus)
- [Publisher Profile](https://clawhub.ai/user/wjorgensen)
- [Locus Homepage](https://paywithlocus.com)
- [Locus API Base](https://api.paywithlocus.com/api)
- [Skill Instructions](https://paywithlocus.com/skill.md)
- [Onboarding Guide](https://paywithlocus.com/onboarding.md)
- [Freelance Ordering Guide](https://paywithlocus.com/fiverr.md)
- [Heartbeat Routine](https://paywithlocus.com/heartbeat.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON, markdown]

**Output Format:** [Markdown guidance with curl commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate payment, escrow, order-placement, and order-polling workflows when used with a valid Locus API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
