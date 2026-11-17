## Description:

Migrate an existing nansen-cli wallet from insecure password storage (env files, .credentials) to the new secure keychain-backed flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using nansen-cli can use this skill to identify where an existing wallet password is stored and follow the documented paths for moving it to an OS keychain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration steps may not reliably complete the stated keychain migration or verify that the saved password can decrypt the wallet.

Mitigation: Clarify the steps against current nansen-cli behavior and verify migration success before treating the wallet as migrated.

Risk: Wallet passwords or private keys could be exposed through chat, shell execution, files, logs, or command output.

Mitigation: Do not share passwords in chat or source credential files as shell code; keep secrets out of files and logs, and discard decrypting command output as the skill directs.

Risk: Removing an old credential file before a successful migration could leave the wallet inaccessible.

Mitigation: Perform cleanup only after the migration succeeds and its verification passes.

Risk: The security assessment is incomplete because two local references were unresolved.

Mitigation: Review the unresolved references before relying on the migration guidance.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-wallet-keychain-migration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
