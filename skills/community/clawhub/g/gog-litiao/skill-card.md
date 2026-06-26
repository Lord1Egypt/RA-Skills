## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to run Google Workspace tasks through the gog CLI, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gog CLI can access or change sensitive Google Workspace data when OAuth permissions are granted. <br>
Mitigation: Install only if you trust the gog CLI, use the narrowest OAuth service set possible, and review where credentials are stored. <br>
Risk: Commands can send email, create calendar events, or modify and clear Sheets data. <br>
Mitigation: Confirm user-directed commands before running them, especially write operations and scripts using --no-input. <br>


## Reference(s): <br>
- [Gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/gog-litiao) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include gog commands that use JSON flags for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
