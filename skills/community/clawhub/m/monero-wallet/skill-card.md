## Description: <br>
Official KYC-rip Monero Agent Skill. Manage XMR wallets on Mainnet/Stagenet via Ripley Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbtoshi](https://clawhub.ai/user/xbtoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent check Monero wallet status, generate subaddresses, and initiate XMR transfers or XMR402 payments through a local Ripley Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent spend real cryptocurrency through the configured Monero wallet gateway. <br>
Mitigation: Require manual approval for every transfer and XMR402 payment, verify the recipient, amount, and site, and keep gateway spending limits low. <br>
Risk: The gateway API key authorizes wallet actions if exposed to an untrusted endpoint or operator. <br>
Mitigation: Protect AGENT_API_KEY, use the local gateway binding, and run the Docker gateway only from a trusted source. <br>
Risk: Duplicate XMR402 payment attempts can spend funds more than once for the same challenge. <br>
Mitigation: Check the transaction log for an existing matching nonce and recover proof from the prior transaction instead of paying again. <br>


## Reference(s): <br>
- [ClawHub Monero Wallet Skill](https://clawhub.ai/xbtoshi/monero-wallet) <br>
- [Ripley XMR Gateway](https://github.com/KYC-rip/ripley-xmr-gateway) <br>
- [Ripley Gateway Setup](https://kyc.rip/ripley) <br>
- [XMR402 Protocol](https://xmr402.org) <br>
- [KYC-rip Swap](https://kyc.rip/swap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AGENT_API_KEY and a local Ripley Gateway at 127.0.0.1:38084.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
