## Description:

Guides agents through building a signal verification network where providers prove trading signals were issued before price moves using Ed25519 signatures, timestamp proofs, Merkle claim chains, performance metrics, escrow-linked subscriptions, rolling accuracy windows, and dispute workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this guide to design cryptographically verifiable trading-signal workflows with commit-reveal publication, independent verification, performance scoring, escrow-linked subscriptions, rolling monitoring, and dispute evidence packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-framed escrow release, dispute, webhook, and scheduled monitor examples could affect funds or user outcomes if copied directly into a live workflow.

Mitigation: Add human approval gates, server-side verification of immutable records, and tests for failed verification cases before using these patterns with real funds.

Risk: The guide references AGENT_SIGNING_KEY for Ed25519 request signing, creating key-management exposure if handled casually.

Mitigation: Store signing keys in a managed secret system, limit access, rotate keys when needed, and avoid logging or embedding private key material.

Risk: The examples depend on external APIs and dependencies but do not provide production hardening by themselves.

Mitigation: Pin dependencies, verify API endpoints and responses server-side, and add failure-mode coverage before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mirni/skills/greenhelix-signal-verification-network)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples reference AGENT_SIGNING_KEY and GreenHelix sandbox/API endpoints.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
