## Description: <br>
Provides GMGN market-data workflows for token price charts, trending rankings, launchpad token discovery, and real-time token signals across Solana, BSC, Base, and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmgnai](https://clawhub.ai/user/gmgnai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market researchers use this skill to query GMGN market data through gmgn-cli for token charts, trending tokens, launchpad activity, and real-time token signals. Outputs should support research and discovery workflows, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or rely on the external gmgn-cli package. <br>
Mitigation: Install it only in environments where use of the GMGN CLI is approved. <br>
Risk: The skill configures and stores a GMGN API key locally. <br>
Mitigation: Confirm before saving credentials, use gmgn-cli config set-key, and protect the resulting local credential file. <br>
Risk: First-time setup may generate a temporary private key at /tmp/gmgn_private.pem. <br>
Mitigation: Remove /tmp/gmgn_private.pem after setup if it is no longer needed. <br>
Risk: Troubleshooting may inspect IPv6 interface data and contact an IP-check service. <br>
Mitigation: Run troubleshooting only when network inspection and an external IP check are acceptable. <br>
Risk: Token signals and market rankings can be mistaken for investment advice. <br>
Mitigation: Present outputs as research signals and avoid treating them as financial advice. <br>


## Reference(s): <br>
- [ClawHub GMGN Skill Market](https://clawhub.ai/gmgnai/gmgn-market) <br>
- [GMGN API Key Setup](https://gmgn.ai/ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, tables, and summarized market-data results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include gmgn-cli commands, API key setup guidance, rate-limit retry timing, parsed JSON summaries, and risk notes for token signals.] <br>

## Skill Version(s): <br>
1.4.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
