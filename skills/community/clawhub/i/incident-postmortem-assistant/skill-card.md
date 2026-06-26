## Description: <br>
Organizes incident materials into a reviewable postmortem draft that separates root cause, contributing factors, amplifiers, impact, and remediation actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident response teams use this skill to turn timelines, alerts, handling notes, and impact details into structured postmortem drafts. It is intended for blameless review, missing-information tracking, and follow-up improvement planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident inputs may contain sensitive operational details or personal data. <br>
Mitigation: Scope inputs to the incident materials needed for the draft, redact sensitive details where possible, and review generated Markdown before sharing. <br>
Risk: Generated postmortem text may misstate chronology, causality, or responsibility if the supplied incident record is incomplete. <br>
Mitigation: Use the skill's待确认项 and review workflow to confirm missing facts before treating the postmortem as final. <br>
Risk: The bundled helper can write an output file and has dormant audit modes controlled by resources/spec.json. <br>
Mitigation: Run the helper only on chosen local files, inspect output paths, and do not alter resources/spec.json to broaden inspection unless that behavior is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/incident-postmortem-assistant) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable drafts, confirmation questions, next-step checklists, and optional local file output when run with python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
