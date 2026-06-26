## Description: <br>
Microsoft Ops Gadget is a CLI for Microsoft 365 covering Mail, Calendar, Drive, Contacts, Tasks, Word, PowerPoint, Excel, and OneNote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visionik](https://clawhub.ai/user/visionik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to guide agents in installing, configuring, and running mog commands for Microsoft 365 workflows. It supports account operations across mail, calendar, OneDrive, contacts, tasks, Office documents, spreadsheets, and OneNote. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can change or delete live Microsoft 365 account data. <br>
Mitigation: Use human review for destructive commands, especially delete and clear operations, and avoid running them through unattended automation. <br>
Risk: The CLI requests broad delegated Microsoft 365 permissions. <br>
Mitigation: Use an isolated or least-privileged Azure app registration and grant only the permissions required for the intended workflows. <br>
Risk: OAuth tokens may be stored in ~/.config/mog/tokens.json when file storage is used. <br>
Mitigation: Prefer keychain storage where possible and treat the token file as sensitive secret material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/visionik/mogcli) <br>
- [Go Reference](https://pkg.go.dev/github.com/visionik/mogcli) <br>
- [dashdash Specification](https://github.com/visionik/dashdash) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read, create, update, send, clear, or delete Microsoft 365 account data.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata and CHANGELOG, released 2026-01-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
