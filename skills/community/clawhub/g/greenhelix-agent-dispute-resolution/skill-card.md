## Description:

Agent Dispute Resolution & Chargeback Defense guides agents through automated dispute resolution pipelines, Verifiable Intent-compatible evidence chains, and chargeback defense for agent-to-agent transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-commerce operators use this guide to design dispute, escrow, SLA, Verifiable Intent evidence, and chargeback-defense workflows for autonomous agent transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may encourage credentialed production API use and consequential escrow or dispute automation.

Mitigation: Use sandbox-only or narrowly scoped credentials, and require human approval for escrow release, dispute concessions, refunds, and other financial or legal-state changes.

Risk: Evidence workflows may disclose more mandate detail than needed for a dispute.

Mitigation: Redact full mandates unless explicitly approved, and share the minimum evidence needed for the dispute or chargeback process.

Risk: Automated dispute and chargeback actions can affect funds or legal positions.

Mitigation: Treat examples as educational patterns, test in sandbox, and add policy checks, audit logging, and reviewer gates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-dispute-resolution)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python code examples and REST API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples reference GreenHelix sandbox and REST API flows.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
