## Description: <br>
Google Workspace Events: Renew/reactivate Workspace Events subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Google Workspace administrators use this skill to renew or reactivate Workspace Events subscriptions, either for a specific subscription or for subscriptions nearing expiration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Renewing all subscriptions automatically can keep Workspace Events subscriptions active beyond the operator's intended scope. <br>
Mitigation: Prefer targeted --name renewals when possible, and use --all or scheduled renewal only when automatic renewal is intentional. <br>
Risk: The skill depends on Google Workspace credentials and shared authentication setup outside this artifact. <br>
Mitigation: Review the shared authentication instructions before use and apply least-privilege Google Workspace credentials. <br>


## Reference(s): <br>
- [Gws Events Renew on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-events-renew) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and CLI flag tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and shared Google Workspace authentication guidance.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence); artifact metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
