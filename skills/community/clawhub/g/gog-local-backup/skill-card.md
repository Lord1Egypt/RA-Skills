## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[12357851](https://clawhub.ai/user/12357851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to install and run the gog CLI for Google Workspace tasks such as Gmail search, calendar lookup, Drive search, Sheets operations, and Docs export after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can access selected Google Workspace services through OAuth tokens. <br>
Mitigation: Authorize only the services needed for the task, and keep OAuth client JSON files and cached tokens private. <br>
Risk: Some commands can send email or modify Google data. <br>
Mitigation: Require explicit confirmation before sending email, creating events, or updating or clearing Sheets data. <br>
Risk: Installation depends on a local gog binary from a Homebrew formula. <br>
Mitigation: Verify the Homebrew package source and installed binary before granting account access. <br>


## Reference(s): <br>
- [gog homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/12357851/gog-local-backup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OAuth setup guidance and command examples, including JSON-oriented flags for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
