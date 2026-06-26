## Description: <br>
The Pocket Alert skill enables OpenClaw agents and workflows to send push notifications to iOS and Android devices through the PocketAlert service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Akellacom](https://clawhub.ai/user/Akellacom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to help agents send mobile push notifications for automated tasks, CI/CD events, monitoring checks, workflow updates, and background process alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notifications may include sensitive operational details or secrets if an agent is allowed to send arbitrary message content. <br>
Mitigation: Avoid sending secrets or sensitive operational data in notification titles or messages, and review notification content before use in production workflows. <br>
Risk: The skill covers account-management and configuration commands, including delete operations, API key configuration, and custom base URL configuration. <br>
Mitigation: Use a least-privilege API key where possible, verify the CLI download source, and require explicit approval before delete, API-key, or base-url configuration commands are run. <br>


## Reference(s): <br>
- [PocketAlert](https://pocketalert.app) <br>
- [PocketAlert CLI](https://info.pocketalert.app/cli.html) <br>
- [ClawHub skill page](https://clawhub.ai/Akellacom/pocketalert) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated pocketalert CLI; generated commands may send notifications or manage PocketAlert resources.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
