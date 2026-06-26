## Description: <br>
Guides OpenClaw agents to bind reliable user-visible delivery paths for reminders, scheduled checks, background task completion updates, and recurring monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonicrang](https://clawhub.ai/user/sonicrang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose reliable delivery paths for reminders, scheduled checks, background task completion reports, and other user-visible follow-up messages in OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect or modify local OpenClaw cron configuration and send test notifications. <br>
Mitigation: Review the generated cron job, verify the stored schedule and delivery fields, and manually trigger a test only for the intended chat or notification target. <br>
Risk: Automation that uses authenticated local tools can affect the wrong account or workspace if credentials are broader than intended. <br>
Mitigation: Use credentials limited to the intended account and review OpenClaw cron commands before allowing them to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sonicrang/openclaw-msg-delivery-guide) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local OpenClaw cron configuration and notification targets when validating delivery behavior.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
