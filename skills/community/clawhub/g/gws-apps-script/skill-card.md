## Description: <br>
Google Apps Script: Manage and execute Apps Script projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace administrators use this skill to inspect Google Apps Script API commands and guide an agent through Apps Script project, process, deployment, version, and script execution workflows with the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated gws operations can change, deploy, version, or execute remote Google Apps Script projects. <br>
Mitigation: Confirm the active Google account before use and require explicit user approval before updateContent, script run, deployment, or version operations. <br>
Risk: The skill depends on related shared/helper gws skill files for authentication, global flags, and helper behavior. <br>
Mitigation: Review the referenced shared and helper gws skill files before relying on this skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-apps-script) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of gws apps-script commands and gws schema inspection; does not produce standalone files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
