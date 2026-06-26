## Description: <br>
Send USDC to molty users via A2A protocol. Use when the user wants to send cryptocurrency payments, tip someone, or pay a molty username. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xsnackbaker](https://clawhub.ai/user/0xsnackbaker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to send USDC payments or tips to molty.cash usernames from the command line on Base or Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external CLI that can access wallet private keys and move real USDC funds. <br>
Mitigation: Use a dedicated low-balance wallet, verify the npm package and version before use, and restrict access to ~/.openclaw/.env. <br>
Risk: A mistaken recipient, amount, network, or fee decision can result in an unintended payment. <br>
Mitigation: Require manual confirmation of the recipient, amount, network, and fees before every payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xsnackbaker/moltycash) <br>
- [molty.cash](https://molty.cash) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require wallet private key environment variables and manual payment confirmation before execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
