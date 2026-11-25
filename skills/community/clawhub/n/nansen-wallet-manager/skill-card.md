## Description:

Wallet management — create (local or Privy server-side), list, show, export, send, delete. Use when creating wallets, checking balances, or sending tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and Nansen CLI users use this skill to create and manage local or Privy wallets, inspect wallet information, export local keys, and send tokens. It provides command guidance for wallet operations on supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account or credential checks and saved-password removal may be outside what a user expects from wallet-management guidance.

Mitigation: Review these behaviors against your needs before installing, as advised by the security guidance.

Risk: Exporting private keys with --reveal can expose them in terminal scrollback, shell logs, or agent transcripts.

Mitigation: Prefer --file, which creates a file readable only by its owner and refuses to overwrite an existing file.

## Reference(s):

- [Nansen CLI browser-login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen Wallet Manager on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-wallet-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Wallet operation guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers operations that can create or delete wallets, export private keys, and send tokens.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
