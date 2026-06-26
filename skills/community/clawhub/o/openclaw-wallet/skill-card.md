## Description: <br>
Openclaw Wallet gives AI agents multi-chain wallet, trading, bridging, token research, token launch, and fee-management guidance for Solana and EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loomlay](https://clawhub.ai/user/loomlay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent operators use this skill to connect agents to the OpenClaw wallet plugin for wallet setup, balance checks, swaps, transfers, bridges, market research, token launches, fee claims, and raw RPC calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority over a crypto wallet, including transfers, swaps, bridges, fee claims, token launches, and raw RPC calls. <br>
Mitigation: Require explicit user approval before installation, API registration, wallet creation, key export, transfers, swaps, bridges, fee claims, token launches, and raw RPC calls. <br>
Risk: Wallet credentials, seed material, and private keys may be exposed or persisted if handled carelessly. <br>
Mitigation: Do not log seed phrases or private keys; instruct users to store seed phrases offline, review where credentials are stored, and avoid funding the wallet until storage and custody are understood. <br>
Risk: Market data, token identifiers, routes, or trade quotes may be incorrect or stale and could lead to unintended financial actions. <br>
Mitigation: Quote before execution, verify token addresses with token search instead of guessing, show expected transaction details to the user, and verify balances and transaction results afterward. <br>
Risk: The npm package and automatic setup path introduce supply-chain and account-registration risk. <br>
Mitigation: Review the npm package, pin a trusted version before use, and require approval before automatic registration or setup. <br>


## Reference(s): <br>
- [Openclaw Wallet ClawHub listing](https://clawhub.ai/loomlay/openclaw-wallet) <br>
- [OpenClaw Wallet GitHub repository](https://github.com/loomlay/openclaw-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOOMLAY_API_KEY; LOOMLAY_BASE_URL is optional.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
