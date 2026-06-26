## Description: <br>
Launch, buy, and sell tokens on BitAgent bonding curves via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parasyte-x](https://clawhub.ai/user/parasyte-x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to launch BitAgent agent tokens and execute buy or sell trades on BitAgent bonding curves across BSC Mainnet or Testnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a wallet private key to launch tokens and execute irreversible BSC trades. <br>
Mitigation: Use a dedicated low-balance wallet, keep PRIVATE_KEY out of logs and shared configs, and require explicit user approval before every mainnet launch, buy, or sell. <br>
Risk: Transactions depend on BitAgent APIs, npm dependencies, and chain state at execution time. <br>
Mitigation: Verify the source and installed dependencies, prefer testnet first, and review command parameters before running the CLI. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/parasyte-x/openclaw-bitagent) <br>
- [BitAgent app](https://app.bitagent.io) <br>
- [BitAgent testnet app](https://testnet.app.bitagent.io) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with CLI commands and command stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRIVATE_KEY configuration and explicit network, token, and amount inputs for trading commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
