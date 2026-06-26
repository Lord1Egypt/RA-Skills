## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to operate Google Workspace resources through the gog CLI, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows. It is useful for scripted account setup, search, export, and data update tasks after OAuth configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth setup can grant access to sensitive Google Workspace data. <br>
Mitigation: Grant only the Google services needed for the task and review the account configuration before use. <br>
Risk: Commands can send email, create calendar events, or change and clear spreadsheet data. <br>
Mitigation: Require confirmation before running write-capable commands and prefer --json plus --no-input for scripted read workflows. <br>
Risk: The skill depends on the external gog CLI and its Homebrew source. <br>
Mitigation: Install only from a trusted gog CLI distribution and verify the Homebrew tap before deployment. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/xiaomaju-888/gog-xiaoshu) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON output modes when the gog CLI supports --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
