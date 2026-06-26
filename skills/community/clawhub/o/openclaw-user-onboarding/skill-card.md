## Description: <br>
Bootstraps new OpenClaw users with guided setup and configurable feature introductions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dukesky](https://clawhub.ai/user/dukesky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to complete first-run setup, create starter workspace files, and receive scheduled introductions to core OpenClaw capabilities at a chosen pace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is always loaded and can change persistent workspace files during onboarding. <br>
Mitigation: Review the files it plans to create or update before first use, especially USER.md, SOUL.md, HEARTBEAT.md, and ONBOARDING_PROGRESS.md. <br>
Risk: The skill schedules recurring feature-introduction messages using stored channel details. <br>
Mitigation: Use a verified delivery channel, confirm the schedule and timezone, and keep pause or removal instructions available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dukesky/openclaw-user-onboarding) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates onboarding state, user profile, persona, heartbeat, and scheduled feature-introduction configuration when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
