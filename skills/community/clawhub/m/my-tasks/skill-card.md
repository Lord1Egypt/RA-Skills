## Description: <br>
View your personal task history and status on OpenAnt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenAnt users use this skill to inspect their own task history, active work, created tasks, submitted work, and completed tasks through authenticated read-only CLI queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated task queries may expose private OpenAnt work history, submissions, rewards, and deadlines to the active agent session. <br>
Mitigation: Use the skill only in trusted sessions and review outputs before sharing or storing them outside OpenAnt. <br>
Risk: Commands fail or return no personal task data when the OpenAnt session is missing or expired. <br>
Mitigation: Run `openant status --json` first and authenticate before using `--mine` task queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/my-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with read-only OpenAnt CLI commands that request JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated OpenAnt session; commands query the user's own task data and are read-only.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
