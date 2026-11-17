## Description:

Organizes meeting notes, extracts action items, and turns raw transcripts or bullet notes into structured summaries with owners and deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, and project coordinators use this skill after meetings to convert transcripts, voice memo text, or rough notes into shareable meeting summaries, decisions, action-item tables, and open-question lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated summaries or action items may assign incorrect owners, deadlines, priorities, or decisions.

Mitigation: Review generated notes with meeting participants before sharing or using them as project records.

Risk: Meeting transcripts can contain confidential, personal, or consent-sensitive information, especially when routed through third-party AI or note-taking tools.

Mitigation: Use approved vendors, confirm participant consent, and avoid uploading sensitive transcripts unless the organization permits it.

Risk: Integration examples can send messages or create Jira, Linear, Notion, or Lark records in external systems.

Mitigation: Require scoped credentials and explicit confirmation for each external write or synchronization action.

## Reference(s):

- [Action Item Extraction Guide](references/action-item-extraction.md)
- [Meeting Notes Integration & Tools Guide](references/integration-tools.md)
- [会议纪要模板集合（中文）](references/templates-cn.md)
- [ClawHub skill page](https://clawhub.ai/goldath/skills/meeting-notes-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown meeting summaries, action-item tables, checklists, short message summaries, and integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inferred owners, deadlines, priorities, and open questions that should be reviewed before distribution or external synchronization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
