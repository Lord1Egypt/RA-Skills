## Description: <br>
Google Workflow: Today's meetings + open tasks as a standup summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace operators use this skill to generate a read-only standup summary from today's meetings and open tasks in Google Workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report can expose private calendar and task details in local output. <br>
Mitigation: Run it only against the intended Google account, review the generated report before sharing it, and avoid storing outputs in public locations. <br>
Risk: The skill depends on the local gws CLI and its Google Workspace authentication state. <br>
Mitigation: Install gws from a trusted source, confirm it is authenticated to the intended account, and follow the available shared gws security guidance before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-workflow-standup-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with gws CLI commands; the underlying command can emit JSON, table, YAML, or CSV output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted, authenticated gws CLI and reads calendar and task data without modifying it.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
