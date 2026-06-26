## Description: <br>
Multi-chain security API designed exclusively for autonomous AI agents, with prompt injection detection, token scam scanning, transaction simulation, MEV detection, policy checks, cross-agent threat sharing, and wallet monitoring for Solana and Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cazaboock9](https://clawhub.ai/user/cazaboock9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and autonomous agent operators use this skill to scan external inputs, token metadata, transactions, NFTs, wallets, and OpenClaw skills with NeoGriffin's Solana/Base security API before acting on-chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected agent and web3 data to an external security service. <br>
Mitigation: Set clear rules for what may be sent and redact secrets or confidential context before scanning. <br>
Risk: Paid calls, wallet monitoring registration, and public threat reports may have financial or operational impact. <br>
Mitigation: Require approval before paid API calls, wallet monitoring registration, or public threat reports. <br>
Risk: Sensitive signing material or credentials could be exposed if submitted to the service. <br>
Mitigation: Never submit private keys, seed phrases, credentials, or raw signing material. <br>


## Reference(s): <br>
- [NeoGriffin API homepage](https://api.neogriffin.dev) <br>
- [ClawHub skill page](https://clawhub.ai/cazaboock9/neogriffin-security) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with HTTP request examples and JSON response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require NEOGRIFFIN_PAYMENT_WALLET and payment transaction signatures for paid API endpoints.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
