## Description:

Crypto-native Web3 news and flash intelligence from MarsBit through hosted MCP for L1/L2 ecosystems, DeFi/CeFi, regulation, exchange flows, and market-moving events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domilin](https://clawhub.ai/user/domilin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve MarsBit crypto and Web3 news, flash updates, topic searches, article details, and related coverage through a hosted MCP endpoint. It supports market-moving headline review, narrative tracking, and event or risk monitoring across chains, protocols, exchanges, ETFs, and regulators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broader local tool authority than its public news lookup purpose requires.

Mitigation: Review before installing, prefer the ClawHub release, and narrow permissions by removing unused read access and replacing broad exec authority with a scoped HTTP or MCP mechanism where supported.

Risk: Prompts or requests may be sent to the MarsBit hosted MCP endpoint.

Mitigation: Use the skill only for public crypto news lookups and avoid sharing portfolio details, private trading plans, secrets, wallet data, or personal information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/domilin/skills/marsbit-crypto-flashskill)
- [MarsBit Hosted MCP Endpoint](https://www.marsbit.co/api/mcp)
- [Publisher Profile](https://clawhub.ai/user/domilin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and structured guidance, with curl commands for MCP calls when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include TL;DR summaries, market-impact labels, key entities, sources, publication times, and surfaced MCP errors.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact package.json reports 0.3.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
