## Description: <br>
Google Workspace Alert Center: Manage Workspace security alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Google Workspace administrators and automation agents use this skill to inspect Alert Center resources, list or retrieve security alerts, update Alert Center settings, and perform delete or undelete workflows through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Admin-level Alert Center commands can delete alerts, undelete alerts, or update customer-level settings when directed. <br>
Mitigation: Use least-privileged Google Workspace credentials where possible, and confirm alert IDs, customer context, and intended changes before running delete, batch delete, undelete, or update settings commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/gws-alertcenter) <br>
- [Publisher Profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace credentials; commands that delete, undelete, or update settings should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
