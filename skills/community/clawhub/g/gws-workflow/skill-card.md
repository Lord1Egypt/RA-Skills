## Description: <br>
Google Workflow: Cross-service productivity workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace automation users use this skill to discover and run Google Workspace workflow commands for cross-service flows across meetings, email, tasks, Drive, and Chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates workflow actions to the local gws CLI and authenticated Google Workspace account, so commands can post messages, create tasks, share files, send email, or otherwise change workspace data. <br>
Mitigation: Install gws from a trusted source, review shared authentication rules, inspect command schemas before use, and confirm data-changing workflows before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>
- [Standup report helper](../gws-workflow-standup-report/SKILL.md) <br>
- [Meeting prep helper](../gws-workflow-meeting-prep/SKILL.md) <br>
- [Email to task helper](../gws-workflow-email-to-task/SKILL.md) <br>
- [Weekly digest helper](../gws-workflow-weekly-digest/SKILL.md) <br>
- [File announce helper](../gws-workflow-file-announce/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gws CLI and shared authentication rules.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
