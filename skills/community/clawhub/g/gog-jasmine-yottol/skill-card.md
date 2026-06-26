## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yottol](https://clawhub.ai/user/yottol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and run the gog command-line tool for Google Workspace workflows across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. It supports interactive use and scripting with JSON output after Google OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad Google Workspace account authority through OAuth. <br>
Mitigation: Use a verified Google OAuth client, inspect the consent screen, and grant only the services needed for the workflow. <br>
Risk: Commands can send mail, create calendar events, or modify Sheets data. <br>
Mitigation: Require explicit approval before running commands that send messages, create events, update spreadsheets, append rows, or clear ranges. <br>
Risk: The release evidence notes under-disclosed OAuth and package provenance details. <br>
Mitigation: Install only if you trust the Homebrew formula and publisher, and review the package source before use. <br>


## Reference(s): <br>
- [gog homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yottol/gog-jasmine-yottol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and Google OAuth setup; examples include JSON output and no-input mode for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
