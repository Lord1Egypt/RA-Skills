## Description:

Lightweight Wallet Signer CLI for generating wallets, deriving addresses, and signing messages across EVM, Solana, Bitcoin, Cosmos, and Tron chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[njdawn](https://clawhub.ai/user/njdawn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and run a local wallet signing CLI for test or self-managed wallet workflows across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path depends on an upstream repository and may build changing source code.

Mitigation: Install only from trusted, reviewed, and pinned source; prefer a versioned release or audited commit with checksum or signature verification.

Risk: Mnemonic phrases can be exposed through command-line arguments, shell history, logs, or shared terminals.

Mitigation: Avoid using real seed phrases in command lines or shared terminals; use test wallets until the install and secret-handling path is independently verified.

Risk: Wallet descriptors are stored locally under the LWS data directory.

Mitigation: Review local storage behavior and secure or remove wallet data when uninstalling, especially before using the purge option.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/njdawn/skills/lws)
- [LWS GitHub Repository](https://github.com/dawnlabsai/lws)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet CLI commands that handle sensitive mnemonic phrases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
