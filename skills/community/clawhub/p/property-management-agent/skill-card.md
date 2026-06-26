## Description: <br>
Autonomous tenant maintenance and ticketing agent that triages tenant requests, distinguishes emergencies from routine maintenance, and syncs tickets with Buildium or AppFolio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property managers and landlords use this skill to handle tenant maintenance requests, classify emergencies, validate tenant and unit details, and route tickets into property management or spreadsheet systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates sensitive tenant workflows and external ticket creation. <br>
Mitigation: Grant only narrow, auditable access to tenant databases, CRMs, and spreadsheet integrations. <br>
Risk: Emergency categorization or repair authorization could create operational or financial harm. <br>
Mitigation: Require human approval for emergencies and repair spending, and configure an explicit currency spending cap before use. <br>
Risk: The setup uses an external ThumbGate package command. <br>
Mitigation: Verify the correct skill identifier and pin or inspect the ThumbGate package before running the npx command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/property-management-agent) <br>
- [Make.com](https://make.com) <br>
- [ElevenLabs](https://elevenlabs.io/affiliates) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and rule descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tenant-triage behavior, setup steps, and ThumbGate guardrails for emergency classification, spending limits, duplicate ticket prevention, and privacy protection.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
