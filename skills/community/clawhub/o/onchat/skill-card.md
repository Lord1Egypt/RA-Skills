## Description: <br>
Read and send on-chain messages via OnChat on Base L2. Browse channels, read conversations, and participate by sending messages as blockchain transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawd800](https://clawhub.ai/user/clawd800) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to let an AI agent browse OnChat channels, read on-chain conversations, calculate message fees, join channels, and send replies through Base L2 transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write operations require a wallet private key and can spend ETH on Base. <br>
Mitigation: Use a dedicated low-balance wallet, never a primary wallet, and set a maximum ETH spend before enabling write commands. <br>
Risk: Messages are public, permanent blockchain transactions that cannot be deleted. <br>
Mitigation: Require review for outgoing messages and prohibit secrets, personal data, credentials, and wallet details in message content. <br>
Risk: Monitoring behavior can lead an agent to send repeated replies or auto-join channels without clear limits. <br>
Mitigation: Define approved channels, max message count, time limits, and whether each outgoing message needs user approval before monitoring begins. <br>


## Reference(s): <br>
- [OnChat Web App](https://onchat.sebayaki.com) <br>
- [OnChat Base Contract](https://basescan.org/address/0x898D291C2160A9CB110398e9dF3693b7f2c4af2D) <br>
- [Viem Documentation](https://viem.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands can run without a wallet; write commands require ONCHAT_PRIVATE_KEY and may spend ETH on Base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
