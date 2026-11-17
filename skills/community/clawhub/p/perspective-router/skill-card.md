## Description:

Nova Perspective Router matches a task description to relevant expert-perspective skills using local keyword scoring and returns the strongest recommended perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catplus-eric](https://clawhub.ai/user/catplus-eric)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when a task benefits from multiple expert perspectives. It routes the task to one to three companion perspective skills and provides guidance for how Nova should incorporate those perspectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword routing can select an irrelevant or weakly matched perspective for complex tasks.

Mitigation: Review the routing output before applying it and tune keywords or thresholds for the deployment environment.

Risk: Broad triggers can cause ordinary questions to be unnecessarily reframed through named expert-perspective skills.

Mitigation: Review which companion perspective skills are installed and tighten triggers so routine questions remain in the base assistant flow.

Risk: Persona-based perspective guidance can introduce biased or misleading advice if treated as authoritative.

Mitigation: Use routed perspectives as advisory inputs and keep final judgment with the main agent or human reviewer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catplus-eric/skills/perspective-router)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plain text routing report with ranked perspective recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with keyword scoring and reports whether referenced companion perspective skills are installed.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog, released 2026-04-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
