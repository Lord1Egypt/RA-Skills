## Description: <br>
Generates exec-support outputs (plan, prioritized tasks, comms drafts, meeting prep/follow-ups). USE WHEN you want a personal assistant to triage requests and produce ready-to-send drafts and schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and operators use this skill to turn messages, task lists, calendar availability, and meeting notes into drafting-only administrative support: triage, prioritized plans, schedule proposals, communications drafts, meeting briefs, agendas, and follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans, schedule options, or communications may be unsuitable if the user omits timezone, working-hours exceptions, calendar constraints, or required decision facts. <br>
Mitigation: Provide only the task-relevant messages, calendar details, and notes, and explicitly state timezone, working hours, exceptions, and missing facts before relying on the drafts. <br>
Risk: The skill produces proposals and ready-to-send drafts but does not send messages or book meetings. <br>
Mitigation: Review, edit, and approve all drafts and schedule proposals before taking any external action. <br>


## Reference(s): <br>
- [PA Output JSON Schema](references/pa-output-json-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown pack with a matching structured JSON block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafting-only output; scheduling proposals must respect weekday business hours, avoid weekend meetings, and stop to ask when required information is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
