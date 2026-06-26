## Description: <br>
AI agent toolkit for Solana - launch tokens, play poker, link your agent identity to mintyouragent.com, read agent personality files for profile linking, and manage a local wallet through a pure Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[operatingdev](https://clawhub.ai/user/operatingdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI-agent operators use this skill to create and manage a Solana wallet, launch pump.fun tokens, play agent poker with SOL stakes, link agent identity, and automate wallet-oriented CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and stores a Solana wallet under ~/.mintyouragent/ and can expose signing keys through setup or export output. <br>
Mitigation: Use a dedicated low-balance wallet, protect ~/.mintyouragent/ and RECOVERY_KEY.txt, and avoid logging JSON setup or export output. <br>
Risk: Launch, poker, transfer, and signing commands can spend funds or authorize wallet activity. <br>
Mitigation: Prefer devnet and --dry-run during evaluation, keep mainnet balances minimal, and avoid unattended --yes or --skip-balance-check use. <br>
Risk: API, RPC, and SSL environment variables can redirect traffic or weaken transport checks. <br>
Mitigation: Review SOUL_API_URL, SOUL_SSL_VERIFY, HELIUS_RPC, and SOLANA_RPC_URL before funding a wallet or running mainnet commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/operatingdev/mintyouragent) <br>
- [MintYourAgent agent documentation](https://www.mintyouragent.com/for-agents) <br>
- [MintYourAgent website](https://www.mintyouragent.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can write command results to files and supports text, JSON, CSV, and table-style output modes.] <br>

## Skill Version(s): <br>
3.6.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
