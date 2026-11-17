## Description:

Wallet management — create (local or Privy server-side), list, show, export, send, delete. Use when creating wallets, checking balances, or sending tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use the Nansen CLI to create and manage local or Privy-backed wallets, inspect wallet details and balances, export local keys when needed, and send supported tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet passwords may be stored in a keychain or, when unavailable, an insecure fallback credentials file.

Mitigation: Prefer OS keychain storage where available, keep passwords out of files, logs, and conversation history, and follow the CLI warning if secure storage is unavailable.

Risk: Sending tokens or exporting private keys can expose assets or credentials if the details or output destination are wrong.

Mitigation: Check the recipient, chain, token, and amount; use --dry-run to preview transfers; prefer a protected --file export over --reveal to stdout.

## Reference(s):

- [Nansen Wallet Manager on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-wallet-manager)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can create, inspect, export, send, and delete wallets; some operations depend on provider credentials and user confirmation.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
