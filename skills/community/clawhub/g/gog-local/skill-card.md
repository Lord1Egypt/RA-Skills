## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[czm448](https://clawhub.ai/user/czm448) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run the gog command-line tool for common Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external Homebrew-installed gog package and Google Workspace OAuth access. <br>
Mitigation: Install only if you trust the gog package source, grant the minimum Google services needed, and review OAuth consent before use. <br>
Risk: Generated commands can send email, create calendar events, or modify and clear Google Workspace data. <br>
Mitigation: Review commands before execution, start with read-only operations where possible, and limit targets such as accounts, ranges, and service scopes. <br>


## Reference(s): <br>
- [Gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub release page](https://clawhub.ai/czm448/gog-local) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Operational guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may use JSON output for scripting when gog is run with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
