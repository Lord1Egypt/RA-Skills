## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasminehuang98613](https://clawhub.ai/user/jasminehuang98613) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent propose gog CLI setup and commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gog CLI can access Google Workspace data through OAuth-enabled services. <br>
Mitigation: Install and authenticate only when that access is intended, and enable only the narrowest Google services required for the task. <br>
Risk: Commands can send email, create calendar events, or change spreadsheet and document data. <br>
Mitigation: Require explicit user confirmation before executing write actions, especially mail sends, event creation, and Sheets or Docs updates. <br>
Risk: The install path depends on an external Homebrew package. <br>
Mitigation: Review the Homebrew package source and installed binary before using it with sensitive Google Workspace accounts. <br>


## Reference(s): <br>
- [gog homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/jasminehuang98613/gog-jasmine) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command examples for scripting with gog.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
