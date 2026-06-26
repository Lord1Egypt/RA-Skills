## Description: <br>
Transfers native SOL on Solana to a recipient address using a funded signing key from environment configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xxbrain01](https://clawhub.ai/user/0xxbrain01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare and execute native SOL transfers on Solana devnet, mainnet-beta, or a custom RPC after validating the recipient, amount, network, and signing key configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send irreversible SOL transfers when provided a funded private key, especially on mainnet-beta. <br>
Mitigation: Use devnet first, verify recipient, amount, and network before confirmation, and require explicit user confirmation for mainnet transfers. <br>
Risk: The skill requires SOLANA_PRIVATE_KEY to sign transactions. <br>
Mitigation: Store the key only in environment variables or a secrets manager, never paste it into chat, and avoid logging or echoing the value. <br>
Risk: Incorrect RPC selection can execute against an unintended Solana network. <br>
Mitigation: Confirm the selected network and SOLANA_RPC_URL before execution; use a mainnet RPC URL only when the user intentionally chooses mainnet-beta. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/0xxbrain01/labor-solana-skill) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/creating-skills) <br>
- [Solscan transaction explorer](https://solscan.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports transaction signature, explorer URL, network, amount, sender, recipient, and transfer status when execution succeeds.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
