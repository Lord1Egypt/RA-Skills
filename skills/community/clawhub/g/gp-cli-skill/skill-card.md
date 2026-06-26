## Description: <br>
Close empty Solana SPL token accounts and reclaim locked rent SOL, track Ghost Point earnings, claim SOUL tokens at weekly epoch close, manage encrypted wallets, and view stats from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[graveyardprotocol](https://clawhub.ai/user/graveyardprotocol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent run documented gp-cli commands for Solana rent reclamation, Ghost Point and SOUL reward tracking, wallet management, and JSON-based reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill allows agents to run wallet-affecting Solana commands, including wallet import, rent-reclaim transactions, SOUL claims, and unattended JSON-mode workflows. <br>
Mitigation: Install only when the publisher is trusted, use dry-run before transactions, avoid --all unless intentional, and require explicit approval before add-wallet, close-empty, claim-soul, --yes, or unattended JSON-mode workflows. <br>
Risk: Wallet material is stored locally by gp-cli, and misuse could expose or alter wallet configuration. <br>
Mitigation: Do not let agents search for key files or inspect gp-cli wallet storage directly; use only the documented gp commands for wallet operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/graveyardprotocol/gp-cli-skill) <br>
- [gp-cli source repository](https://github.com/graveyardprotocol/gp-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output can be human-readable or machine-readable JSON; close-empty with --all may emit newline-delimited JSON per wallet.] <br>

## Skill Version(s): <br>
1.2.2 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
