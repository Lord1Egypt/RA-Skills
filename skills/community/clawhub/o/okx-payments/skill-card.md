## Description:

Okx Payments guides agents through buyer or seller setup for x402 payment-gated APIs, including OnchainOS installation, language-specific seller references, and OKX payment constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate x402 payment-gated APIs as buyers or add OKX x402 payments to their own APIs as sellers. It guides role selection, installation, reference retrieval, credential handling, and implementation constraints for TypeScript, Go, or Rust.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run mutable remote installer scripts or install unpinned agent skills.

Mitigation: Review the remote installer scripts and resolved source before installation; prefer pinned releases or commit hashes with checksum or signature verification.

Risk: Seller setup involves OKX API credentials, wallet addresses, and generated payment code.

Mitigation: Do not provide credentials or wallet-related values until the generated code, dependencies, and payment configuration have been reviewed.

## Reference(s):

- [OKX Web3 Homepage](https://web3.okx.com)
- [OKX x402 Docs](https://web3.okx.com/onchainos/dev-docs/payments/overview)
- [OKX Payments SDK](https://github.com/okx/payments)
- [OnchainOS Skills](https://github.com/okx/onchainos-skills)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/skills/okx-payments)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and generated implementation code when seller references are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch language-specific seller reference files before generating code; should stop rather than write seller code from memory if reference retrieval fails.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
