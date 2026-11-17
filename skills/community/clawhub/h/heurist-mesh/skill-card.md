## Description:

Real-time crypto token data, DeFi analytics, blockchain data, Twitter/X social intelligence, enhanced web search, and crypto project search in one skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjw12](https://clawhub.ai/user/wjw12)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external agent users use this skill to query Heurist Mesh agents for cryptocurrency market data, DeFi metrics, wallet intelligence, project research, Twitter/X signals, and summarized web research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require agents to handle payment private keys and create on-chain payment signatures.

Mitigation: Prefer the API-key payment path; if x402 is used, require explicit user approval of recipient, amount, network, and endpoint before signing.

Risk: Production private keys stored in project .env files could be exposed to local tooling, logs, or repository mistakes.

Mitigation: Use a dedicated low-balance wallet for x402 and avoid storing production private keys in project .env files.

Risk: The artifact documents a curl-to-bash Foundry installer command.

Mitigation: Do not run remote installer commands without independent verification and local review.

## Reference(s):

- [Heurist Mesh](https://mesh.heurist.ai)
- [Heurist API Documentation](https://docs.heurist.ai)
- [Heurist API Key Reference](references/heurist-api-key.md)
- [x402 Payment Reference](references/x402-payment.md)
- [Inflow Payment Reference](references/inflow-payment.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external API responses from Heurist Mesh when credentials and payment setup are configured.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
