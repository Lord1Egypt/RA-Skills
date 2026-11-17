## Description:

基于腾讯会议（tmeet）智能纪要与转写，把多场会议聚合为结构化周报与复盘报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golgys0621](https://clawhub.ai/user/golgys0621)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, project managers, and team leads use this skill to aggregate Tencent Meeting summaries, transcripts, or local meeting notes into weekly reports, retrospectives, and deduplicated action-item lists. It is most useful after a set of meetings when decisions, risks, owners, and next steps need to be turned into shareable Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Meeting records and local meeting notes can contain sensitive business information.

Mitigation: Use explicitly selected meetings or note directories, keep access limited to the intended audience, and review generated reports before sharing.

Risk: Generated reports can misstate people, decisions, deadlines, or source support.

Mitigation: Verify names, conclusions, and action items against the original notes, and keep unsupported items marked as pending confirmation until reviewed.

Risk: Authorized tmeet backfill or push actions could distribute a report more broadly than intended.

Mitigation: Only authorize backfill or push actions when the destination and recipient set are intentional.

## Reference(s):

- [周报模板（weekly）](references/weekly_template.md)
- [复盘模板（retrospective）](references/retrospective_template.md)
- [ClawHub skill page](https://clawhub.ai/golgys0621/skills/meeting-digest-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with optional inline shell commands for the local helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include weekly reports, retrospective reports, action-item lists, and source-confirmation notes.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
