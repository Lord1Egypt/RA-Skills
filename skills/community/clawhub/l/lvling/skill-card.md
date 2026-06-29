## Description: <br>
Blooming Elf（绿灵） helps an agent manage plant-care records, watering reminders, plant diagnostics, fertilizing, repotting, and recurring review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shirley1011](https://clawhub.ai/user/shirley1011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Plant owners and household users use this skill to create plant profiles, keep watering and care logs, receive scheduled care reminders, and get concise plant-care guidance through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interrupt unrelated chats during setup when no plant-care configuration is found. <br>
Mitigation: Install and invoke it only when a plant-care setup flow is desired; review its onboarding behavior before enabling it in a shared agent environment. <br>
Risk: The skill may create persistent plant records in IMA or local markdown files. <br>
Mitigation: Use it only with plant-care data you are comfortable storing persistently, and review the selected IMA notes or local file paths before ongoing use. <br>
Risk: The skill creates scheduled reminders after reminder-time configuration. <br>
Mitigation: Confirm reminder schedules during setup and disable or edit generated reminders if they are not wanted. <br>
Risk: Requested share links or local paths can expose plant archive locations. <br>
Mitigation: Request archive links only when sharing is intended, and avoid posting generated links or local paths into untrusted channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shirley1011/skills/lvling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, plant-profile and care-log markdown templates, scheduled-reminder configuration, and concise procedural guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent plant records in IMA or local markdown files and may create scheduled reminders when configured.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
