## Description: <br>
Delivers user notifications with optimized channel, timing, formatting, batching, and escalation to prevent spam and ensure clarity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to decide when, where, and how to send user notifications, including channel selection, quiet hours, batching, escalation, and message formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The live API example can send recipient and message data to a third-party notification service. <br>
Mitigation: Review the provider's data-handling terms before production use and avoid putting secrets or regulated personal data in notification bodies. <br>
Risk: The skill can require sensitive credentials such as SKILLBOSS_API_KEY. <br>
Mitigation: Store credentials in a secret manager or protected environment variable and configure recipient channels explicitly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-notify) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with notification examples and optional API code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference user notification preferences, recipient channels, quiet hours, and sensitive API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
