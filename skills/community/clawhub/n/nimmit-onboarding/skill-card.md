## Description: <br>
Guides new Nimmit users through first-run Telegram chat onboarding for organization setup, industry, language, team size, priorities, and briefing setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rithythul](https://clawhub.ai/user/rithythul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Nimmit users use this skill to complete conversational onboarding in Telegram. The agent collects setup details, confirms the configuration, updates workspace setup, installs matching skill packs, and schedules a daily morning briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding flow can make persistent workspace changes from chat responses. <br>
Mitigation: Require explicit user confirmation before writing files and document the exact files that may be changed. <br>
Risk: The skill can install unspecified matching skill packs. <br>
Mitigation: List the eligible skill packs before installation and require owner or administrator approval. <br>
Risk: The skill can schedule a recurring daily briefing. <br>
Mitigation: Show the proposed schedule, obtain consent, and document how to disable or roll back the briefing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rithythul/nimmit-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram chat responses plus workspace configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update workspace files, install skill packs, and schedule a recurring daily briefing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
