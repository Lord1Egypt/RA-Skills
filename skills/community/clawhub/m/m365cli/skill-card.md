## Description: <br>
Manage Microsoft 365 work or school account services, including Exchange, OneDrive for Business, SharePoint, calendar, and organizational user search through the m365-cli command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrhah](https://clawhub.ai/user/mrhah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and AI agents use this skill to operate Microsoft 365 work or school accounts from a CLI workflow. It supports mail, calendar, OneDrive, SharePoint, and user-directory tasks while excluding personal Outlook.com accounts and tenant-administration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize broad Microsoft 365 work-account access. <br>
Mitigation: Install only after reviewing requested scopes, prefer narrow scopes where possible, and require explicit confirmation before sending, deleting, uploading, or sharing content. <br>
Risk: Anonymous sharing links can expose files publicly. <br>
Mitigation: Warn users before anonymous sharing and use organization or user-specific sharing unless public access is intentional. <br>
Risk: Local credential files may contain OAuth tokens. <br>
Mitigation: Do not read, print, log, or expose the local m365-cli credential file. <br>


## Reference(s): <br>
- [m365-cli Complete Command Reference](references/commands.md) <br>
- [m365-cli npm package](https://www.npmjs.com/package/m365-cli) <br>
- [ClawHub skill page](https://clawhub.ai/mrhah/m365cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers --json output for structured agent consumption; sensitive operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
