## Description: <br>
Manage Google Apps Script projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and run gws script commands for managing Google Apps Script projects, including project metadata, content, metrics, deployments, versions, and process listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running gws commands through this skill can overwrite Google Apps Script project contents. <br>
Mitigation: Confirm the target script ID, source directory, and backup or recovery path before executing update or push commands. <br>
Risk: Using the wrong Google or gws account can apply changes to an unintended Apps Script project. <br>
Mitigation: Check the active Google/GWS account and intended project before running commands that modify project content. <br>


## Reference(s): <br>
- [Gws Script ClawHub release](https://clawhub.ai/googleworkspace-bot/gws-script) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and an authenticated Google Workspace context.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
