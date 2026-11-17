## Description:

会议纪要助手帮助 agents 将中文会议记录整理为结构化会议纪要，并提取关键讨论点、决议和待办事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to turn existing Chinese meeting notes into structured minutes with discussion points, decisions, and action items. The included local script supports basic Markdown minutes extraction from a text file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises todo extraction and enterprise chat push commands, but the inspected artifact only includes scripts/extract_minutes.py.

Mitigation: Use the included extractor only for local minutes generation unless the missing scripts are supplied and reviewed separately.

Risk: Meeting notes can contain sensitive business or personal information.

Mitigation: Keep input and output files in intended workspace paths and review generated minutes before sharing them.

Risk: The extractor uses simple text heuristics and may omit or misclassify discussions, decisions, or action items.

Mitigation: Review the generated Markdown against the original notes before treating it as the official meeting record.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/skills/meeting-minutes-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local UTF-8 file input and Markdown output; generated minutes should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
