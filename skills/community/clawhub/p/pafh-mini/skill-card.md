## Description: <br>
PAHF-Memory is a continual personalization framework that guides agents to clarify user preferences, use local preference memory, and integrate user feedback over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welkeyever](https://clawhub.ai/user/welkeyever) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to add consent-aware personalization behavior to an agent, including preference clarification, preference-grounded action, and feedback-based memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains persistent local personalization memory and can record broad observations about user preferences. <br>
Mitigation: Install only when persistent personalization is desired, decide whether automatic daily observations are acceptable, and periodically review or delete the local memory files. <br>
Risk: Personal memory may include sensitive personal context if users or agents store it carelessly. <br>
Mitigation: Avoid storing addresses, contacts, schedules, credentials, financial data, health data, or other sensitive data. <br>


## Reference(s): <br>
- [Preference Memory Schema Definition](references/preference-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/welkeyever/pafh-mini) <br>
- [Learning Personalized Agents from Human Feedback](https://arxiv.org/abs/2602.16173) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown instructions and preference-memory entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local memory file reads and preference updates after consent according to the skill policy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
