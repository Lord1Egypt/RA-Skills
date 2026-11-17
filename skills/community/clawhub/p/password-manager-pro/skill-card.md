## Description:

Password Manager helps an agent guide users through local password record management, including adding, editing, searching, categorizing, backing up, importing, exporting, and generating passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liningg](https://clawhub.ai/user/liningg)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage personal or work account records in local files, search and categorize saved entries, generate passwords, and produce basic password safety reports. It is not appropriate as a vault-grade password manager without additional protections for stored, backed-up, and exported credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, backups, and exports are stored as plaintext local files.

Mitigation: Use only on encrypted local storage, restrict file access, avoid syncing credential files to cloud services, and prefer an established encrypted password manager for real accounts.

Risk: CSV and JSON exports can expose secrets outside the local data file.

Mitigation: Export only when necessary, store exports in an encrypted location, and remove exported files after use.

Risk: Generated passwords rely on a weak random source.

Mitigation: Use a cryptographically secure generator or a trusted password manager for production credentials unless the generator is revised.

## Reference(s):

- [Password Security Guide](references/password_security_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional Python command examples and local JSON/CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, read, back up, import, or export local credential records when the bundled scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
