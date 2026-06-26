## Description: <br>
Organizes sales lead information into qualification judgments, key questions, risk items, and recommended next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and CRM users use this skill to turn lead background, pain points, budget, and timing into reviewable qualification notes, follow-up questions, risks, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python helper includes broader local audit and pattern-scanning behavior than the advertised sales-note workflow requires. <br>
Mitigation: Review the helper before installation and run it only against intended lead-note inputs, not broad private directories. <br>
Risk: Lead notes may include private or sensitive sales information. <br>
Mitigation: Desensitize inputs when needed and review generated notes before sharing or copying them into a CRM. <br>
Risk: Generated qualification notes could be mistaken for authoritative CRM master data. <br>
Mitigation: Use the output as a draft and checklist, and confirm facts against official CRM records before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/lead-qualification-notes) <br>
- [README](artifact/README.md) <br>
- [Output Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Structured Markdown notes, with optional JSON or file output from the local Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only sales-assist output that highlights missing or uncertain information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
