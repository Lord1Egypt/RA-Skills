## Description:

Provides an OWASP-aligned security hardening guide for autonomous AI commerce agents on GreenHelix, covering identity, credentials, payments, prompt injection defenses, financial guardrails, monitoring, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this guide to harden autonomous commerce agents that interact with GreenHelix payments, escrow, identity, trust, and monitoring workflows. It provides threat modeling guidance, defensive code examples, configuration patterns, and deployment checklists for agents that may handle credentials or funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste examples can touch live financial APIs or real credentials.

Mitigation: Use sandbox credentials first and review every example before connecting it to real funds.

Risk: The security evidence flags unsafe fail-open examples and active permission probing.

Mitigation: Replace probing with read-only capability introspection and fail closed for payment, escrow, and credential paths.

Risk: Private keys and payment credentials may be exposed if copied into a normal runtime environment.

Mitigation: Keep keys in a signer, KMS, or secret manager and scope GreenHelix and Stripe credentials to the minimum required actions.

Risk: Autonomous payment, escrow, or key revocation actions can have high-value impact.

Mitigation: Require explicit human approval for key revocation, escrow release, and other high-value payment actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-commerce-security)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix developer documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python, YAML, and shell-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples require review before use with real credentials or funds.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
