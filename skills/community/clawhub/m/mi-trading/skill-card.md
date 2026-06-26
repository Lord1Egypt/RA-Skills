## Description: <br>
Trade tokens on Solana using the ClawDex CLI when the user asks to swap tokens, check balances, get quotes, or manage a Solana trading wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidpolotm](https://clawhub.ai/user/davidpolotm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate a Solana trading wallet through ClawDex, including balance checks, quotes, simulations, safety-guarded swaps, and post-trade verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to install a remote CLI and execute real wallet trades that may move or lose funds. <br>
Mitigation: Use a dedicated wallet with small funds, pin and verify the ClawDex CLI package instead of relying on @latest, and require the agent to show the quote and simulation result before explicit approval of each real swap. <br>
Risk: Swap execution can be affected by slippage, price impact, safety violations, failed simulations, or delayed RPC balance reads. <br>
Mitigation: Set strict ClawDex safety limits, simulate before execution, abort on non-zero exit codes or JSON violations, and verify balances after allowing for RPC lag. <br>


## Reference(s): <br>
- [Mi Trading on ClawHub](https://clawhub.ai/davidpolotm/mi-trading) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented command output requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawDex commands to use --json; real swaps require explicit execution commands and can move wallet funds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
