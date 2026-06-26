## Description: <br>
Crypto trading: swap, perps, transfer, pay, deposit (credit card / crypto), withdraw, AI chat, market discovery, x402 payment, autopilot. Built-in wallet via Minara CLI. EVM + Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larisgtu](https://clawhub.ai/user/larisgtu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and crypto users use this skill to route agent requests into Minara CLI workflows for wallet management, swaps, transfers, deposits, perpetual futures, market discovery, AI analysis, and x402 payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact financial authority over a real crypto wallet or trading account. <br>
Mitigation: Install only if the user trusts Minara, use a low-balance wallet or narrowly scoped credentials where possible, and verify every recipient, token, chain, amount, and leverage setting before approval. <br>
Risk: Automated trading behavior such as autopilot can create financial exposure without continuous user review. <br>
Mitigation: Avoid autopilot unless explicit risk limits and a stop plan are in place, and keep manual transaction confirmation enabled. <br>
Risk: The installation metadata uses minara@latest, which can change over time. <br>
Mitigation: Consider pinning or verifying the Minara CLI package before installing or updating it. <br>


## Reference(s): <br>
- [Minara homepage](https://minara.ai) <br>
- [ClawHub skill page](https://clawhub.ai/larisgtu/minara-skill-v2) <br>
- [x402 quickstart for buyers](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fund-moving actions require explicit user confirmation; Minara chat commands may be long-running.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
