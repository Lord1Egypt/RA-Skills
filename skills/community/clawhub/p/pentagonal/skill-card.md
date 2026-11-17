## Description:

Use when the user asks to create, generate, build, audit, fix, compile, or look up smart contracts and tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achilles1089](https://clawhub.ai/user/achilles1089)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to research existing tokens, generate and audit smart contracts, fix reported vulnerabilities, compile contract outputs, and prepare deployment commands across EVM chains and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment examples can affect funded wallets or mainnet contracts if executed without review.

Mitigation: Use testnets or devnets first, review generated contracts and deployment commands, and prefer safer signer workflows before any mainnet deployment or token minting.

Risk: Pentagonal MCP/API lookups can send token identifiers, contract prompts, or code to Pentagonal.

Mitigation: Review what will be sent before calling external tools or APIs, and avoid sharing sensitive contract logic or private material unless that disclosure is intended.

Risk: Deployment commands may involve private-key based tooling.

Mitigation: Do not paste private keys into prompts or commands, avoid command-line private keys for funded wallets, and use wallet or hardware-backed signing where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/achilles1089/skills/pentagonal)
- [Deployment Guide](references/deployment.md)
- [Example Conversation Flows](references/examples.md)
- [Pentagonal Security Knowledge Base](references/security-rules.md)
- [Pentagonal token lookup API](https://www.pentagonal.ai/api/fetch-contract)
- [Remix IDE](https://remix.ethereum.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, JSON API responses, contract source snippets, ABI/bytecode summaries, and deployment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external Pentagonal MCP/API results, chain-specific deployment guidance, and security findings grouped by severity.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
