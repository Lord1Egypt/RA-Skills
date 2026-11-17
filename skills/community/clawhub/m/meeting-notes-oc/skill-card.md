## Description:

智能会议记录和待办事项跟踪助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07)

### License/Terms of Use:


## Use Case:

Employees and external users use this skill to record meeting highlights, decisions, participants, and follow-up action items, then search or review prior meeting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes and action items may be written to persistent local JSON files.

Mitigation: Confirm where meetings.json and action-items.json are stored, who can access them, and how records can be deleted or redacted.

Risk: Highly confidential meeting content may be retained longer than intended.

Mitigation: Avoid using the skill for highly confidential meetings unless local storage access and retention controls have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/skills/meeting-notes-oc)
- [Publisher profile](https://clawhub.ai/user/huangjingzhi07)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or JSON records containing meeting notes and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist meeting notes to local meetings.json and action-items.json files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
