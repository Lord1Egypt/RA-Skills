## Description:

A local password manager skill for storing, searching, updating, deleting, importing, and exporting account credentials in a local vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyieleven11](https://clawhub.ai/user/wangyieleven11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to manage local account credentials through an agent-accessible command-line password manager. It supports adding, querying, searching, updating, deleting, tagging, importing, and exporting password records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and retrieves real local credentials and the authoritative security verdict is suspicious.

Mitigation: Install only after accepting local credential storage limitations, and review the vault, key, and export file handling before using real secrets.

Risk: Passwords may be exposed through command-line arguments, terminal output, shell history, or CSV export files.

Mitigation: Avoid entering real passwords as command-line arguments where history may persist, limit display/export operations, and protect and delete CSV exports securely.

Risk: If the cryptography dependency is unavailable, the artifact behavior falls back to plaintext password storage.

Mitigation: Verify cryptography is installed before adding secrets and test the workflow with non-sensitive data first.

Risk: The encryption key and password vault are both stored locally under the same workspace directory.

Mitigation: Restrict local file permissions for the vault and key, and avoid syncing or sharing the workspace directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyieleven11/skills/local-passwords-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Plain text CLI output, local JSON vault data, and CSV import/export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local password data to ~/.openclaw/workspace/passwords.json and uses ~/.openclaw/workspace/.password_key when encryption is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
