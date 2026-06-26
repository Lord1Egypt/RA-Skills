## Description: <br>
Gws Skill helps authorized Google Workspace administrators and investigators query tenant-wide email, Vault, Directory, Reports, Drive, Calendar, Sheets, Docs, and People data through a service account with domain-wide delegation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmac122](https://clawhub.ai/user/jmac122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace administrators, security teams, and legal investigators use this skill to run read-only tenant investigations, including email searches, user and group lookups, audit log review, and file, calendar, spreadsheet, document, and directory reads across a Google Workspace domain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain-wide delegation can allow tenant-wide reads of sensitive email, files, calendars, documents, directory records, and audit logs. <br>
Mitigation: Install only in a tightly controlled Workspace admin or legal-investigation environment, restrict who can run the scripts, and require approval before impersonating users. <br>
Risk: The service account JSON key is a high-value credential. <br>
Mitigation: Use a dedicated service account, store the key outside repositories with restrictive filesystem permissions, protect and rotate the key, and narrow delegated scopes where possible. <br>
Risk: Vault exports and full Gmail reads may expose highly sensitive user content. <br>
Mitigation: Require ticketed approval for Vault exports or full-content reads and keep separate audit logs for each sensitive lookup or export. <br>


## Reference(s): <br>
- [Setup Checklist](references/setup-checklist.md) <br>
- [Project Homepage](https://github.com/jmac122/gws-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/jmac122/gws-dwd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command outputs from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Google Workspace API results may include sensitive tenant data, including email metadata or body text, audit logs, user records, contacts, files, calendar events, spreadsheet ranges, and document text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
