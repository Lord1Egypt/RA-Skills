## Description:

Guides buyers through verifying AI agent identity, auditing performance claims, and building trust scores with GreenHelix cryptographic reputation APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprises, and autonomous-agent operators use this guide to automate buyer-side due diligence before sharing data, delegating work, or committing funds to an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful GreenHelix credentials may be exposed to workflows derived from the guide.

Mitigation: Use least-privilege credentials, keep AGENT_SIGNING_KEY out of integrations unless explicitly reviewed, and separate sandbox from production secrets.

Risk: Escrow sample code could lock funds without sufficient safeguards.

Mitigation: Require explicit user confirmation, validate payee and amount, enforce spending limits and idempotency, and complete verification before escrow creation.

Risk: Documentation examples may be copied into production workflows without review.

Mitigation: Review and scan adapted code before deployment, especially code that signs requests, uses credentials, or moves funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-agent-trust-verification)
- [GreenHelix API Reference](https://api.greenhelix.net/docs)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GREENHELIX_API_KEY for authenticated examples and references AGENT_SIGNING_KEY for signing-key workflows.]

## Skill Version(s):

1.3.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
