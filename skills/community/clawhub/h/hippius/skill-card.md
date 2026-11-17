## Description:

Hippius decentralized storage on Bittensor Subnet 75 helps agents upload files, query storage, manage buckets, and guide users through S3-compatible storage workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxquick](https://clawhub.ai/user/maxquick)

### License/Terms of Use:


## Use Case:

Developers, operators, and external users use this skill to configure Hippius S3 credentials, run storage commands, inspect buckets and objects, and understand when to use S3 instead of the deprecated public IPFS endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storage and delete commands can move or remove user data if bucket names, object keys, or local paths are wrong.

Mitigation: Review every generated command, verify bucket and path values, and manually confirm destructive actions before execution.

Risk: Hippius credentials and wallet seed phrases may grant access to storage or blockchain accounts if exposed.

Mitigation: Use least-privilege credentials, keep secrets out of chat and shell history, and avoid storing seed phrases in plaintext configuration.

Risk: Private files may be uploaded without appropriate encryption or to an unintended destination.

Mitigation: Confirm encryption expectations and destination before upload, and do not use --no-encrypt for private data.

Risk: Unpinned package installs and the script's plaintext default RPC endpoint can increase supply-chain or transport risk.

Mitigation: Install pinned dependencies in an isolated environment and prefer secure endpoints when querying RPC data.

## Reference(s):

- [Hippius Storage Guide](references/storage_guide.md)
- [Hippius CLI Commands Reference](references/cli_commands.md)
- [Hippius Docs](https://docs.hippius.com)
- [Hippius Console](https://console.hippius.com)
- [Hippius Stats](https://hipstats.com)
- [Hippius CLI GitHub](https://github.com/thenervelab/hippius-cli)
- [ClawHub Skill Page](https://clawhub.ai/maxquick/skills/hippius)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local helper script commands and Hippius S3 or RPC endpoints; users should review commands before execution.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, released 2026-02-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
