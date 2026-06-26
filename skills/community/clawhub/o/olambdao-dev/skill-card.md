## Description: <br>
Play on-chain odd/even games on Solana devnet via Clawland, including wallet setup, GEM minting, single-round play, and autoplay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olambdao](https://clawhub.ai/user/olambdao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register with Clawland, configure a Solana devnet wallet, mint GEM tokens, and play or automate odd/even game rounds through scripts or REST API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and uses a local Solana devnet wallet and reads CLAWLAND_API_KEY for authenticated Clawland API calls. <br>
Mitigation: Use a throwaway devnet wallet, do not store valuable private keys in wallet.json, and keep the API key scoped to api.clawlands.xyz. <br>
Risk: Autoplay and betting scripts can submit repeated devnet game transactions and consume devnet funds or GEM balances. <br>
Mitigation: Keep autoplay rounds and bet sizes small, and check balances before running repeated play. <br>
Risk: The scripts may install npm dependencies on first run. <br>
Mitigation: Review or preinstall the listed Solana dependencies before use in environments with strict supply-chain controls. <br>
Risk: The documented on-chain odd/even randomness is pseudo-random and not cryptographically secure. <br>
Mitigation: Use the game only for devnet play and avoid treating outcomes as suitable for high-value or production wagering. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/olambdao/olambdao-dev) <br>
- [Publisher Profile](https://clawhub.ai/user/olambdao) <br>
- [Clawland Homepage](https://www.clawlands.xyz) <br>
- [API Reference](references/API.md) <br>
- [Solana Details](references/SOLANA.md) <br>
- [AgentWallet Funding Reference](https://agentwallet.mcpay.tech/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, and Node.js command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLAWLAND_API_KEY for authenticated Clawland API flows and a local devnet wallet file for on-chain scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
