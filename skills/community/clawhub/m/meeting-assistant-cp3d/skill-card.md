## Description:

Meeting Assistant helps an agent generate meeting minutes, extract action items, manage meeting templates, and summarize local meeting records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and team leads use this skill to turn meeting text into concise minutes, action items, schedules, templates, and meeting summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting records may include sensitive participant names, notes, and action items stored locally in plain JSON.

Mitigation: Use only where local plain-text storage is acceptable, and add deletion, access-control, backup, or encryption practices for confidential meetings.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/meeting-assistant-cp3d)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text responses with local JSON meeting records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores meeting and task data locally as JSON when used through the bundled Python helper.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
