## Description: <br>
Pre-built HEARTBEAT.md templates for common agent tasks such as email checking, calendar monitoring, weather alerts, system health, and news digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add scheduled heartbeat checks by copying and customizing Markdown templates for email, calendar, weather, system health, news, social notifications, and project status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heartbeat templates may prompt periodic background checks against email, calendar, weather, repository, social, or news sources depending on what the user enables. <br>
Mitigation: Before enabling a template, review the HEARTBEAT.md content, set only the intended accounts and location, and confirm which connectors the agent can access. <br>
Risk: Recurring checks can keep running after they are no longer needed or after account access expectations change. <br>
Mitigation: Remove or disable the HEARTBEAT.md file when checks are no longer wanted, and revisit account permissions when changing templates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/heartbeat-kit) <br>
- [README.md](README.md) <br>
- [combined-lite.md template](templates/combined-lite.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with configuration comments and brief setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Templates are customized through variables such as email account, location, quiet hours, priority senders, urgency keywords, repositories, and topics.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
