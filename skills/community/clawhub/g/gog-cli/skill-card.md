## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saisake](https://clawhub.ai/user/saisake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Gmail, Calendar, Drive, Contacts, Sheets, and Docs from an agent-guided command-line workflow after configuring Google OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on live Google Workspace data, including email, calendar, spreadsheet, and document content. <br>
Mitigation: Use the narrowest Google OAuth services possible and test on non-critical data before broad use. <br>
Risk: Send, create, update, append, delete, or clear operations can modify external accounts or user data. <br>
Mitigation: Require explicit confirmation before any write operation. <br>


## Reference(s): <br>
- [Gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill release](https://clawhub.ai/saisake/gog-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command suggestions when scripting with gog.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
