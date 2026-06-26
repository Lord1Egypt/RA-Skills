## Description: <br>
Lista Lending assistant — position report, market overview, yield scan, liquidation risk check, daily digest, and loop strategy on BSC and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lawson-ccy](https://clawhub.ai/user/lawson-ccy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and DeFi analysts use this skill to generate read-only Lista Lending reports for positions, market rates, vault yield, liquidation risk, daily status, and loop strategies on BSC and Ethereum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save wallet addresses and preferences under ~/.lista and send wallet/report queries to Lista MCP or API services. <br>
Mitigation: Use only public wallet addresses, do not provide private keys or signing credentials, and review or clear saved ~/.lista files when local persistence is not desired. <br>
Risk: Telegram, Discord, alert, and digest subscription flows are under-specified in the security evidence. <br>
Mitigation: Treat subscription confirmations as unverified unless a separate notification system is configured and tested; do not rely on this skill alone for liquidation monitoring. <br>
Risk: Generated lending and loop reports may be incomplete, stale, or affected by unavailable data sources. <br>
Mitigation: Use the reports as read-only analysis, verify important figures against Lista or chain data, and do not use the skill for deposit, withdrawal, borrow, repay, signing, or other execution flows. <br>


## Reference(s): <br>
- [Lista Skill Definition](artifact/SKILL.md) <br>
- [Shared Domain Logic](artifact/references/domain.md) <br>
- [Position Report](artifact/references/position.md) <br>
- [Market Lending Rates](artifact/references/market.md) <br>
- [Vault Yield](artifact/references/yield.md) <br>
- [Risk Check](artifact/references/risk.md) <br>
- [Daily Digest](artifact/references/digest.md) <br>
- [Loop Strategy](artifact/references/loop.md) <br>
- [Lista MCP Endpoint](https://mcp.lista.org/mcp) <br>
- [Lista API](https://api.lista.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text reports with optional shell commands and JSON data retrieval] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English, Simplified Chinese, Traditional Chinese, or a custom language; report data may come from Lista MCP tools, moolah.js, or Lista REST APIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
