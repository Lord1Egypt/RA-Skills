## Description:

Analyzes Tencent Meeting reports and meeting minutes to quantify meeting health through speaking balance, topic coverage, decision output rate, silent participant identification, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golgys0621](https://clawhub.ai/user/golgys0621)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, meeting facilitators, and team leads use this skill to turn Tencent Meeting reports or local roster and minutes files into a concise meeting health report. It helps identify participation imbalance, low-speaking participants, decision density, topic closure, and practical facilitation improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting reports and minutes can contain participant activity and sensitive discussion details.

Mitigation: Use the skill only when participants and the organization permit this type of meeting analysis, and confirm the meeting ID or local files before analysis.

Risk: Heuristic metrics such as speaking time and silent participant detection can be mistaken for contribution quality.

Mitigation: Treat the report as an improvement aid, review participant roles and meeting context, and avoid using the metrics as a standalone performance assessment.

## Reference(s):

- [Meeting health report template](artifact/references/health_template.md)
- [ClawHub skill page](https://clawhub.ai/golgys0621/skills/meeting-health-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown meeting health report with metrics and recommendations; may include command examples for local analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate a Markdown report file in local mode from a meeting roster CSV and optional minutes file.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
