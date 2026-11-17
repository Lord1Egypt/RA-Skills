## Description:

Nex Vault is a local contract and document vault for tracking business agreements, extracting key dates and clauses, monitoring costs, and alerting users about expirations, renewals, and termination notice deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, SME owners, directors, and managers use this skill to manage local contract and document records, track expiration and renewal obligations, search clauses, and export vault data for compliance or budgeting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review marks the release suspicious because Telegram setup can execute shell input and modifies shell startup files.

Mitigation: Review setup commands before installation, avoid using Telegram configuration commands as written unless fixed, and store credentials in a restricted configuration file or keyring.

Risk: Telegram alerts may disclose document metadata to a third-party messaging service.

Mitigation: Enable Telegram only for metadata that is appropriate to send outside the local vault, and document this data-sharing behavior for users.

Risk: Untrusted export filenames may overwrite files outside the vault export folder.

Mitigation: Use trusted export paths and constrain export destinations to the vault export directory before running exports.

## Reference(s):

- [Nex Vault on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-vault)
- [Nex AI](https://nex-ai.be)
- [Publisher profile](https://clawhub.ai/user/nexaiguy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI outputs use structured plain text with ISO-8601 dates, document statuses, and monetary values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
