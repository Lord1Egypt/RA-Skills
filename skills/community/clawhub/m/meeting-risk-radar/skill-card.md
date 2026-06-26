## Description: <br>
Meeting Risk Radar helps users identify high-risk topics, unclear responsibilities, missing materials, and discussions that may go off track before a meeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams, facilitators, and meeting owners use this skill before meetings to turn the topic, participants, and expected decisions into a reviewable risk checklist. It highlights pre-meeting risks, missing materials, unclear ownership, agenda changes, questions to confirm, and contingency plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting inputs may contain personal, confidential, or sensitive business information. <br>
Mitigation: Use redacted inputs for sensitive meetings and avoid including private recordings or unnecessary personal data. <br>
Risk: Generated risk checklists can be incomplete or misleading when the meeting context is incomplete. <br>
Mitigation: Treat outputs as review drafts, confirm missing information explicitly, and do not use the skill as a replacement for formal risk or compliance review. <br>
Risk: The local script can write a report to a user-selected output path. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/meeting-risk-radar) <br>
- [README](artifact/README.md) <br>
- [Skill specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>
- [Example output](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown by default, with an optional JSON wrapper from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local user-provided meeting material and can write the generated report to a user-selected output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
