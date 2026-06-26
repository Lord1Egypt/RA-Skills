## Description: <br>
Daily learning habit builder with check-ins and smart reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daizongyu](https://clawhub.ai/user/daizongyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to record daily learning completion, view streak status, and optionally configure reminders around a local learning habit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores check-in history, reminder configuration, and reminder logs in a local data folder next to the skill. <br>
Mitigation: Tell users where the local data folder is before use and provide a clear path for reviewing, editing, or deleting that data. <br>
Risk: Ambiguous phrases such as generic completion statements may be interpreted as a learning check-in. <br>
Mitigation: Use explicit check-in language, such as "record today's learning check-in," when asking the agent to record progress. <br>
Risk: The setup-cron helper proposes scheduled check-in commands rather than reminder-message commands. <br>
Mitigation: Avoid using the setup-cron helper unless it is changed to send reminders; confirm the scheduler, reminder time, and disable path with the user before enabling reminders. <br>


## Reference(s): <br>
- [ClawHub listing: Learning Checkin](https://clawhub.ai/daizongyu/learning-checkin) <br>
- [Publisher profile: daizongyu](https://clawhub.ai/user/daizongyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores check-in history, reminder status, and reminder logs in a local data folder next to the skill.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
