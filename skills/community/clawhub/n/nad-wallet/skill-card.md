## Description:

Nad Wallet helps agents create Monad wallets, sign SIWE messages, check MON balances, and register with Nad ecosystem services such as NadMail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to create and operate Monad wallet identities, inspect MON balances, and complete NadMail SIWE registration for automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys and mnemonics may be exposed in terminal output, JSON output, local files, shell startup files, shared logs, or managed wallet storage.

Mitigation: Use only isolated environments and wallets with no meaningful funds, prefer short-lived environment variables, avoid managed storage and shell startup persistence, and keep generated secrets out of shared terminals and logs.

Risk: NadMail registration signs a server-provided authentication message without enough local SIWE validation.

Mitigation: Treat registration as signing a third-party controlled authentication message and use throwaway wallets until SIWE validation is fixed and reviewed.

Risk: Wallet-name path handling requires review before trusting managed wallet files.

Mitigation: Use simple expected wallet names, keep wallet directories isolated, and review local paths before creating or loading managed wallets.

## Reference(s):

- [Nad Wallet ClawHub Release](https://clawhub.ai/daaab/skills/nad-wallet)
- [Monad RPC Endpoint](https://rpc.monad.xyz)
- [Monad Explorer](https://explorer.monad.xyz)
- [NadMail](https://nadmail.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JavaScript and bash commands; bundled scripts can emit shell exports, JSON wallet data, and balance or registration status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include wallet addresses, private-key export commands, mnemonic backup text, local wallet files, NadMail token files, and audit log entries depending on the selected mode.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
