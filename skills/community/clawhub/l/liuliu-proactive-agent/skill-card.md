## Description: <br>
Helps an AI agent act more proactively by anticipating user needs, surfacing issues early, and reporting progress without waiting for repeated prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanish-wu](https://clawhub.ai/user/vanish-wu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent toward proactive assistance, including progress updates, early warnings, reminders, and suggested next steps. It is best suited for agents whose operators want more initiative while retaining clear limits on sensitive monitoring and file-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages monitoring calendar, email, market, weather, and other potentially sensitive information. <br>
Mitigation: Require explicit approval before enabling monitoring, and restrict it to named accounts, data sources, paths, and time windows. <br>
Risk: The skill suggests file cleanup, documentation updates, memory edits, and code commits without asking the user first. <br>
Mitigation: Require user confirmation before memory edits, file cleanup, document changes, code commits, or other persistent workspace changes. <br>
Risk: More autonomous behavior can become intrusive or interrupt users at inappropriate times. <br>
Mitigation: Define quiet hours, notification frequency limits, and escalation criteria before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vanish-wu/liuliu-proactive-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown prose and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Behavioral guidance for agent responses, progress updates, reminders, and proactive checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
