## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JX-76](https://clawhub.ai/user/JX-76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and run gog commands for Gmail, Calendar, Drive, Contacts, Sheets, Docs, and related Google Workspace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad Google Workspace account access through gog and OAuth. <br>
Mitigation: Review requested OAuth scopes during setup and install the external gog CLI only from a trusted source. <br>
Risk: Credentials, client secrets, or OAuth tokens could be exposed in chats, logs, or repositories. <br>
Mitigation: Keep client secrets and tokens out of prompts, transcripts, command output, and source control. <br>
Risk: Commands can send email, create calendar events, or change and clear Workspace data. <br>
Mitigation: Require explicit user confirmation before running visible or destructive actions. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/JX-76/jx76-gog) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command options such as --json and --no-input for scripting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
