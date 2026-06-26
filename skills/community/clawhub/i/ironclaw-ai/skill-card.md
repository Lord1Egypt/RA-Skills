## Description: <br>
IronClaw AI is a military-style productivity OS that routes mission, habit, goal, tennis, sleep, discipline-score, briefing, and coaching requests in English or Indonesian to structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[susiloandreas](https://clawhub.ai/user/susiloandreas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused individuals use this skill to convert natural-language planning, tracking, sleep, tennis training, and coaching requests into IronClaw service commands and concise status responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send mission, habit, tennis, sleep, discipline-score, briefing, and coaching activity to an external IronClaw service. <br>
Mitigation: Install only when the configured IronClaw service is trusted and users are comfortable with that productivity and wellness data being stored there. <br>
Risk: Scheduled notification checks can create recurring background calls and prompts. <br>
Mitigation: Review the configured automations before use and disable any schedules that are not wanted. <br>


## Reference(s): <br>
- [IronClaw AI ClawHub release](https://clawhub.ai/susiloandreas/ironclaw-ai) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, text, guidance] <br>
**Output Format:** [Structured slash-command API requests with concise text or Markdown responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IRONCLAW_SERVICE_URL for command dispatch and may use scheduled notification checks when supported by the host environment.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
