## Description:

MintYourAgent is a pure Python CLI skill for Solana agents to launch pump.fun tokens, play poker with SOL stakes, link agent identity, and manage a local wallet in ~/.mintyouragent/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[operatingdev](https://clawhub.ai/user/operatingdev)

### License/Terms of Use:

MIT

## Use Case:

External developers and AI agents use this skill to manage a dedicated Solana wallet, launch tokens, inspect balances and limits, play wallet-authenticated poker, and link an agent profile to MintYourAgent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle real-money Solana transactions for token launches, poker deposits, transfers, and initial buys.

Mitigation: Use a dedicated low-balance wallet, test on devnet or with dry-run flows first, and avoid value-bearing actions until the human confirms the amount, network, and destination.

Risk: Local wallet and recovery files grant wallet control if exposed.

Mitigation: Treat wallet.json, RECOVERY_KEY.txt, backups, and console or JSON key output as full wallet-control secrets, and keep them outside logs, prompts, shared workspaces, and source control.

Risk: Skipping confirmations, running headless or AI-controlled actions, using custom endpoints, or disabling SSL verification can increase transaction and data-exposure risk.

Mitigation: Do not use --yes, headless mode, AI buy decisions, custom API/RPC endpoints, or SSL-disable settings for value-bearing actions unless the user has explicitly reviewed the risk.

Risk: Linking soul or profile data can associate an agent identity summary with the wallet and MintYourAgent service.

Mitigation: Link profile data only when the user is comfortable with that association and has reviewed the extracted identity information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/operatingdev/skills/mintyouragent)
- [MintYourAgent documentation](https://www.mintyouragent.com/for-agents)
- [MintYourAgent website](https://www.mintyouragent.com)
- [Project repository](https://github.com/operatingdev/mintyouragent-skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, terminal output, and optional JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local wallet, configuration, recovery, audit, history, and backup files under ~/.mintyouragent/ when commands are executed.]

## Skill Version(s):

3.6.3 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
