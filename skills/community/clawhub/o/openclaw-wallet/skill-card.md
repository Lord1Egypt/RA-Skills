## Description:

Openclaw Wallet provides multi-chain wallet management, trading, bridging, DEX market data, token launch, fee, and RPC tooling for AI agents across Solana and EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loomlay](https://clawhub.ai/user/loomlay)

### License/Terms of Use:


## Use Case:

Developers and external agent operators use this skill to connect agents to wallet setup, balance checks, token swaps, transfers, bridges, market research, token launches, fee claims, and chain RPC calls. It is intended for workflows where an agent needs to inspect or act on Solana and EVM wallet state with explicit review for funded actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create wallets, expose recovery material, export private keys, and move funds through swaps, transfers, bridges, fee claims, and token launches.

Mitigation: Require explicit user confirmation and independent transaction review before funded operations, and avoid passing seed phrases or private keys through chat.

Risk: The integration relies on an npm package installation for high-impact financial actions.

Mitigation: Pin and audit the npm package before use, and review automatic credential and wallet creation behavior before enabling the skill.

Risk: Automatic credential registration and local credential storage may create unintended API keys or wallet state.

Mitigation: Use a reviewed LOOMLAY_API_KEY where possible, protect local credential files, and disable or manually review automatic setup in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loomlay/skills/openclaw-wallet)
- [OpenClaw Wallet Homepage](https://github.com/loomlay/openclaw-wallet)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls return standardized success, data, and error objects; funded operations should be quoted, confirmed, executed, and verified.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
