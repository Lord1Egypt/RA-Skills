## Description: <br>
Execute token swaps and manage on-chain transactions, including supported-chain and token lookup, swap quotes, signable transaction construction, gas or fee estimation, and signed transaction broadcast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide wallet-authenticated crypto swap workflows through the LiberFi CLI, including quote review, transaction preparation, fee estimation, and broadcast. It is intended for careful, confirmation-gated operation because swaps and broadcasts can move funds irreversibly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet-authenticated swaps or transaction broadcasts that may move funds irreversibly. <br>
Mitigation: Require explicit user confirmation after presenting token addresses, chain, smallest-unit amount, slippage, estimated fees, and expected transaction outcome before any execute or send command. <br>
Risk: The artifact instructs agents to silently install a global LiberFi CLI if the command is missing. <br>
Mitigation: Do not allow silent installation; have the user install or approve the CLI, prefer a pinned package version, and verify the installed binary before use. <br>
Risk: Using the wrong wallet, token address, chain, amount unit, or slippage setting can cause loss of funds. <br>
Mitigation: Verify the active wallet with whoami and confirm exact token addresses, chain family, chain ID, smallest-unit amount conversion, slippage, fees, and transaction hash with the user. <br>


## Reference(s): <br>
- [LiberFi homepage](https://liberfi.io) <br>
- [Liberfi Swap on ClawHub](https://clawhub.ai/bombmod/liberfi-swap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline CLI commands and JSON-oriented command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured CLI output via --json and requires explicit user confirmation before transaction execution or broadcast.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
