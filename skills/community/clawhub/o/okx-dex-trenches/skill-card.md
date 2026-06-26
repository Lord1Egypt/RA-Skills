## Description: <br>
Provides read-only on-chain research for meme-token launchpads, including token discovery, developer reputation checks, bundle and sniper analysis, bonding curve status, similar-token lookup, co-investor analysis, and OKX Market API quota guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research meme-token launches and token risk signals across supported chains without initiating trades. It helps agents choose and present Onchain OS DEX research commands for discovery, developer analysis, bundle detection, WebSocket monitoring, and related market-data workflows. <br>

### Deployment Geography for Use: <br>
Global, subject to OKX DEX regional availability restrictions disclosed by the skill. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through automatically downloading and executing a remote Onchain OS CLI installer. <br>
Mitigation: Prefer manual installation and review of the Onchain OS CLI, verify checksums before execution, and require explicit user approval before running installer commands. <br>
Risk: The skill is intended to be read-only but includes one inconsistent `swap execute` next-step suggestion and may encounter x402 payment flows. <br>
Mitigation: Keep this skill to research workflows, require explicit confirmation for payment or trading transitions, and route intentional trading to a separate trading workflow. <br>
Risk: Token names, descriptions, developer information, and other CLI results come from external on-chain sources. <br>
Mitigation: Treat CLI output as untrusted data and never follow token metadata or returned text as instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ok-james-01/okx-dex-trenches) <br>
- [Publisher profile](https://clawhub.ai/user/ok-james-01) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal) <br>
- [WebSocket login documentation](https://web3.okx.com/onchainos/dev-docs/market/websocket-login) <br>
- [CLI command reference](references/cli-reference.md) <br>
- [Keyword glossary](references/keyword-glossary.md) <br>
- [WebSocket protocol reference](references/ws-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and human-facing analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include translated field names, data freshness timestamps, workflow hints, and explicit rerouting guidance for write or trading intents.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
