## Description: <br>
Learn me: Lets OpenClaw proactively learn more about you through natural conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YevhenDiachenko0](https://clawhub.ai/user/YevhenDiachenko0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to let their agent ask occasional, consent-based personal follow-up questions and remember safe future question directions. It supports manual use and optional scheduled prompts that can be rescheduled or disabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is privacy-sensitive because it asks optional personal follow-up questions and keeps local notes about future question directions. <br>
Mitigation: Only use it when the user wants this behavior, avoid storing secrets or private information, and review or delete memory/next-questions.md as needed. <br>
Risk: Scheduled prompts can feel intrusive if timing or topic selection is wrong. <br>
Mitigation: Confirm any schedule before enabling it, skip during focused or stressful work, and let the user reschedule or disable prompts. <br>
Risk: Repeated or unwanted personal questions can create discomfort. <br>
Mitigation: Respect deflection, record sensitive topics with cooldowns or permanent avoidance, and ask at most one natural question per interaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YevhenDiachenko0/learn-me) <br>
- [Publisher profile](https://clawhub.ai/user/YevhenDiachenko0) <br>
- [Project homepage](https://github.com/YevhenDiachenko0/openclaw-learn-me-skill) <br>
- [Example questions](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory/next-questions.md and propose OpenClaw cron entries after user confirmation.] <br>

## Skill Version(s): <br>
0.5.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
