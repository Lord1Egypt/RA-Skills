## Description: <br>
Manage sales workflows, including deal tracking, call scheduling, and client communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams use this persona to prepare for client calls, log deal updates, convert follow-up emails into tasks, share proposals, and summarize pipeline activity in Google Workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persona can guide an agent toward Google Workspace actions that write spreadsheet updates, upload files, or share client-facing documents. <br>
Mitigation: Use an appropriate work account and provide explicit spreadsheet, Drive folder, sharing, and approval instructions before allowing writes or uploads. <br>
Risk: The persona depends on the gws binary and separate Google Workspace helper skills. <br>
Mitigation: Review and install the referenced helper skills separately before relying on the workflow guidance. <br>


## Reference(s): <br>
- [Persona Sales Ops on ClawHub](https://clawhub.ai/googleworkspace-bot/persona-sales-ops) <br>
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline gws commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-gmail, gws-calendar, gws-sheets, and gws-drive helper skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
