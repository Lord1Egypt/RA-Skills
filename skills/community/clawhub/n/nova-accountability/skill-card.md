## Description: <br>
Manage accountability items on a Monday.com board for creating new items, checking existing ones, running work sessions, and responding to scheduled accountability events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novalystrix](https://clawhub.ai/user/novalystrix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to let an agent track Monday.com accountability items, run scheduled work sessions, create sub-items, update statuses, and write progress updates. It is intended for configured Monday.com boards where the user wants recurring agent follow-through rather than status-only reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled work sessions can change Monday.com data, delegate work, alter systems, and message people. <br>
Mitigation: Use a dedicated least-privilege Monday.com token, restrict the board and recipients, and keep the hourly cron disabled or tightly controlled until approvals are in place. <br>
Risk: The skill can move accountability items through statuses, including Done for agent-assigned work. <br>
Mitigation: Require review before status changes to Done and enforce the documented rule that owner-assigned tasks can only be marked Done by the owner. <br>
Risk: Delegated code or configuration work may proceed without enough project context. <br>
Mitigation: Require approval before code or configuration changes and include the full Details or Doc column text whenever delegating work to a sub-agent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/novalystrix/nova-accountability) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Monday.com API v2 endpoint](https://api.monday.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, GraphQL snippets, and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Monday.com board ID and a Monday.com API token environment variable.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
