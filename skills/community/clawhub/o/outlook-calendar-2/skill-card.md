## Description: <br>
Outlook Calendar helps agents manage Microsoft Outlook calendars and events through MorphixAI-mediated access to Microsoft Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users use this skill to inspect calendars, list and retrieve events, create meetings, update event details, delete events, and review schedules across date ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Outlook Calendar data through a linked MorphixAI and Microsoft account. <br>
Mitigation: Install only when MorphixAI and the required OpenClaw MorphixAI plugin are trusted; confirm the linked account and review event details before approving create, update, or delete actions. <br>
Risk: The skill requires a MORPHIXAI_API_KEY credential. <br>
Mitigation: Store the key securely, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paul-leo/outlook-calendar-2) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with YAML-like tool-call examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked MorphixAI/Microsoft Outlook Calendar account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
