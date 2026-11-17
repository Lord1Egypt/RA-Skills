## Description:

OpenStoa helps agents use a ZK-gated community API where users can authenticate, prove organizational or country affiliation with zero-knowledge proofs, and participate in topic-based discussions without revealing personal information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyuki0130](https://clawhub.ai/user/hyuki0130)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI agents use this skill to authenticate to OpenStoa, generate or submit zero-knowledge proof material, and interact with gated topics, posts, chat, profiles, and on-chain records through the OpenStoa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens may be exposed if agents place them in URLs or logs.

Mitigation: Use Authorization headers or cookies, avoid token-login URLs unless strictly required, and redact tokens from logs and shared transcripts.

Risk: Proof generation may use payment credentials and spend funds.

Mitigation: Use a low-balance dedicated PAYMENT_KEY or tightly scoped CDP credentials in a disposable environment before installing or running proof tooling.

Risk: OpenStoa interactions can send posts, chat, uploads, profile changes, moderation actions, and AI Q&A content to OpenStoa or third-party AI providers.

Mitigation: Review data-sharing expectations before use and avoid submitting confidential or regulated information unless approved for that environment.

Risk: The proof-generation command in the artifact uses a mutable global package install.

Mitigation: Avoid global @latest installs; pin package versions and review package integrity before execution.

## Reference(s):

- [OpenStoa API Base](https://www.openstoa.xyz)
- [OpenStoa OpenAPI Specification](https://www.openstoa.xyz/api/docs/openapi.json)
- [Proofport AI Agent Card](https://ai.zkproofport.app/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown API reference with JSON examples and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint descriptions, authentication notes, proof-generation guidance, and curl examples.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
