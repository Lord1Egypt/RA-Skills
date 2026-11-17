## Description:

Create and manage self-rewarding meme coins on Solana via the OP0 Altar protocol, including pump.fun token deployment and automatic holder rewards across 129 payout token options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[op0prot](https://clawhub.ai/user/op0prot)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create OP0 Altar tokens, check deployment status, list and inspect altars, and view available reward token options through the OP0 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through high-impact crypto token deployment and funding actions.

Mitigation: Require explicit user confirmation for token name, ticker, marketing wallet, payout token, SOL amount, and funding address before sending any API request or funds.

Risk: The OP0 API key authorizes access to the deployment API and may be exposed in shell history, config files, or logs.

Mitigation: Store OP0_API_KEY as a secret, avoid sharing private keys or seed phrases, and rotate the API key if exposure is suspected.

Risk: The optional MCP setup uses an unpinned npx package, which can change behavior across installs.

Mitigation: Prefer the documented curl flow or use a pinned, reviewed MCP server package version before enabling agent access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/op0prot/skills/op0-altar)
- [OP0 Altar public API endpoint](https://api.op0.live/functions/v1/altar-api-public)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OP0 API request payloads, status summaries, funding instructions, and OpenClaw MCP configuration commands.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
