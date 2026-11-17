## Description:

Lista Lending assistant for position reports, market overviews, vault yield scans, liquidation risk checks, daily digests, and loop strategy analysis on BSC and Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawson-ccy](https://clawhub.ai/user/lawson-ccy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Lista to generate read-only Lista Lending analytics reports for wallet positions, market rates, vault yields, liquidation risk, daily summaries, and loop strategies. The skill is intended for report-style analysis, not lending execution, wallet signing, or transaction flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist wallet addresses and preferences locally under ~/.lista.

Mitigation: Review and clear local preference files when needed, and avoid using shared environments for wallet-linked reports.

Risk: Unsafe shell-write instructions could execute untrusted wallet or custom language text.

Mitigation: Validate wallet addresses and language values before use, and change file writes to avoid shell interpolation for user-provided text.

Risk: Reports depend on live Lista MCP or API data, so rates, APY, and liquidation metrics can become stale quickly.

Mitigation: Refresh data before acting on a report and treat output as analytics rather than execution advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lawson-ccy/skills/lista)
- [Lista MCP endpoint](https://mcp.lista.org/mcp)
- [Lista API base](https://api.lista.org)
- [Shared domain logic](artifact/references/domain.md)
- [Position report reference](artifact/references/position.md)
- [Market lending rates reference](artifact/references/market.md)
- [Vault yield reference](artifact/references/yield.md)
- [Risk check reference](artifact/references/risk.md)
- [Daily digest reference](artifact/references/digest.md)
- [Loop strategy reference](artifact/references/loop.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text reports with fixed templates; helper commands return JSON for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report values are rounded to two decimals; the skill can persist local language, wallet, and threshold preferences under ~/.lista.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
