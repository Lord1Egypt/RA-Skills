## Description:

Build agent credential wallets with Verifiable Intent, SD-JWT delegation chains, cross-protocol presentation for AP2, UCP, ACP, and x402, eIDAS 2.0 EUDI compliance, and reputation-bound credentials using detailed Python examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to design agent credential wallets for delegated authorization, selective disclosure credentials, cross-protocol presentation, EUDI-related flows, reputation binding, and revocation patterns. The examples are production-framed but should be treated as conceptual until replaced with audited identity, payment, compliance, and approval controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-framed financial credential examples contain serious security and safety gaps if copied directly into commerce, identity, payment, or compliance workflows.

Mitigation: Treat the skill as a conceptual guide and replace credential handling, verification, endpoint, budget, EUDI, and SCA logic with audited standards-compliant implementations before production use.

Risk: The referenced GREENHELIX_API_KEY can provide read/write access to purchased API tools.

Mitigation: Scope, rotate, and protect the API key, use sandbox credentials where possible, and require explicit human approval before any real transaction or delegated spend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-credential-wallets)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [Agent delegation credential schema](https://greenhelix.net/credentials/agent-delegation/v1)
- [Verifiable intent credential schema](https://greenhelix.net/credentials/verifiable-intent/v1)
- [EUDI delegation credential schema](https://greenhelix.net/credentials/eudi-delegation/v1)
- [Reputation-bound delegation credential schema](https://greenhelix.net/credentials/reputation-bound-delegation/v1)
- [Dispute evidence credential schema](https://greenhelix.net/credentials/dispute-evidence/v1)
- [GreenHelix agent production hardening skill](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guide with Python examples, inline shell commands, API request patterns, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; references GREENHELIX_API_KEY for GreenHelix gateway access.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
