## Description: <br>
MooTeam (moo.team) API v1 integration for projects, teams, tasks, drafts, comments, workflows, statuses, labels, timers, time logs, and activity logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antokhin-digital](https://clawhub.ai/user/antokhin-digital) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a MooTeam workspace from OpenClaw, including project, task, comment, workflow, label, timer, time log, and activity-log workflows. It requires a MooTeam API token and company alias. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete live MooTeam projects, tasks, comments, workflows, statuses, labels, team mappings, timers, and time logs. <br>
Mitigation: Use least-privileged credentials, verify target IDs before mutating commands, and supervise destructive or state-changing actions. <br>
Risk: MooTeam credentials grant account access when exposed to the agent runtime. <br>
Mitigation: Provide MOOTEAM_API_TOKEN and MOOTEAM_COMPANY_ALIAS through environment configuration, keep tokens out of chat and logs, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [MooTeam API Usage Guide](references/api_docs.md) <br>
- [MooTeam API endpoint](https://api.moo.team/api) <br>
- [ClawHub listing](https://clawhub.ai/antokhin-digital/mooteam) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-line JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOOTEAM_API_TOKEN and MOOTEAM_COMPANY_ALIAS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
