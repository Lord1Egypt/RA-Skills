## Description:

Provides AI-native payment tools for creating payment requests, checking payment status, and initiating refunds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neversatrabbit](https://clawhub.ai/user/neversatrabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce teams can use this skill to let an agent create payment requests, query transaction status, and initiate refunds through a configured payment API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle payment API keys and signing secrets.

Mitigation: Install only for trusted publishers, provide secrets through controlled environment variables, avoid running setup with real payment credentials loaded, and rotate any credentials whose fragments may have appeared in logs.

Risk: The refund tool can initiate monetary actions without strong built-in safeguards.

Mitigation: Require an explicit approval workflow for refunds before allowing production use.

Risk: Payment traffic and dependencies require operational hardening before production use.

Mitigation: Require HTTPS-only API endpoints and update vulnerable dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neversatrabbit/skills/payment-skill)
- [Publisher Profile](https://clawhub.ai/user/neversatrabbit)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON objects emitted by CLI tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires payment API credentials in environment variables; refund operations should be gated by external approval controls.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
