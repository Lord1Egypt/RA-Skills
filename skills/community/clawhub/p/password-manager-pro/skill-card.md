## Description: <br>
Local password-management skill for adding, editing, deleting, searching, categorizing, backing up, importing, exporting, and generating passwords, with local data storage and password-strength guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liningg](https://clawhub.ai/user/liningg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage personal or work account credentials locally, including search, categorization, password generation, import/export, backup, and password safety checks. It is not appropriate for enterprise team password sharing or regulated secret management without stronger access controls and encryption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passwords, backups, and exports may be stored in plaintext local files. <br>
Mitigation: Use a vetted encrypted password manager for real credentials, or require encryption at rest and restrictive file permissions before storing sensitive secrets. <br>
Risk: Viewing, exporting, importing, deleting, or backing up credentials can expose or irreversibly change sensitive data. <br>
Mitigation: Require explicit user confirmation for those actions and keep exported or backup files in protected locations. <br>
Risk: Automatically created backups can multiply copies of plaintext secrets. <br>
Mitigation: Limit backup locations, retention, and access permissions, and delete unneeded backups securely. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liningg/password-manager-pro) <br>
- [README](README.md) <br>
- [Password Security Guide](references/password_security_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local Python code and JSON/CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local password, backup, import, and export files under user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
