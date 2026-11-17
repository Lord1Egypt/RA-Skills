## Description:

将口语化办公任务描述转换为结构化文本工单，并以时间戳文件保存到本地导出目录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linyao58](https://clawhub.ai/user/linyao58)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations staff use this skill to capture informal office notes, meeting summaries, and to-do descriptions as structured follow-up tickets. It is suited for routine office task tracking where local file retention is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Office notes and task descriptions are written to timestamped files under ./data/exports, which can retain sensitive workplace content.

Mitigation: Avoid confidential meeting notes, personal data, credentials, or regulated business information unless the runtime environment's retention and access controls are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linyao58/skills/office-auto)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text status message and timestamped .txt work ticket]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes user-provided office notes to ./data/exports using timestamped filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
