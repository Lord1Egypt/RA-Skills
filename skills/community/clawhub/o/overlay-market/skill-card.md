## Description: <br>
Trade leveraged perpetual futures on Overlay Protocol (BSC), scan markets, analyze prices with technical indicators, check wallet balance, encode build and unwind transactions, and monitor positions with PnL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthurka-o](https://clawhub.ai/user/arthurka-o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Overlay Protocol markets on BSC, prepare leveraged perpetual futures transactions, review wallet and position state, and optionally sign and broadcast approved transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast real BSC transactions when configured with a private key. <br>
Mitigation: Prefer an external signer, smart-contract account, or dedicated low-value wallet, and review every generated transaction before broadcasting. <br>
Risk: The approval script can create unlimited USDT approvals by default. <br>
Mitigation: Pass a specific approval amount and confirm the spender and amount before signing. <br>
Risk: Trading commands can open or close leveraged positions with real funds. <br>
Mitigation: Confirm the destination, market, position ID, direction, leverage, collateral, and slippage before executing or piping output to send.js. <br>


## Reference(s): <br>
- [Overlay app](https://app.overlay.market) <br>
- [Overlay documentation](https://docs.overlay.market) <br>
- [ClawHub skill page](https://clawhub.ai/arthurka-o/overlay-market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON transaction objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Build and unwind scripts write unsigned transaction JSON to stdout and human-readable review details to stderr; send.js returns transaction status JSON after broadcasting.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
