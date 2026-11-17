## Description:

Heleni Meetings helps an agent coordinate meetings, create calendar invites, summarize meeting notes or transcripts, and extract action items with owners and deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and assistants use this skill to schedule meetings by finding availability, coordinating with another PA, and creating calendar invites. They can also turn pasted meeting notes or transcripts into summaries, decisions, action items, saved notes, and optional todo.md updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts, notes, and action items can include confidential, legal, HR, financial, or personal information.

Mitigation: Review the skill before installing for sensitive meetings, omit raw transcripts by default, and require explicit consent before saving notes.

Risk: Calendar and task operations can modify calendar entries or todo.md without strong upfront consent.

Mitigation: Preview calendar invites and todo.md changes, then require explicit confirmation before applying them.

Risk: Previous-meeting searches could expose unrelated workspace content if run broadly.

Mitigation: Limit searches to the meeting-notes folder unless the user explicitly chooses a broader search.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and structured meeting-note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create meeting-notes/YYYY-MM-DD_topic.md and update todo.md when the user chooses items to add.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
