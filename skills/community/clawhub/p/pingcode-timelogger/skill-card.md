## Description: <br>
Automates PingCode timesheet workflows by creating sub-tasks, setting work item properties, logging work hours, and optionally deriving entries from Git commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers who track work in PingCode use this skill to prepare timesheet entries, create task structures under existing work items, and register hours after reviewing a proposed plan. It also supports generating candidate time entries from configured GitHub or GitLab commit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a PingCode session cookie and can optionally read Git commit history through a token. <br>
Mitigation: Store cookie and token files with restrictive permissions, never commit or share them, and use the narrowest Git token scopes available. <br>
Risk: Approved runs can create PingCode tasks, update work item properties, and register work hours. <br>
Mitigation: Review the full task plan and target work item details before approval, and use the first-time setup test call to validate configuration before real changes. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Configuration Template](references/config-template.yaml) <br>
- [PingCode Work Category IDs](references/category-ids.md) <br>
- [Git Integration](references/git-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with YAML and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated PingCode API calls or browser actions after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
