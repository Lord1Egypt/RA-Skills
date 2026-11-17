## Description:

Builds and queries a cross-meeting knowledge base from Tencent Meeting notes or local meeting-note files, organizing decisions, conclusions, action items, and risks into traceable Markdown or JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golgys0621](https://clawhub.ai/user/golgys0621)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn multiple meeting summaries or transcripts into a searchable knowledge base for follow-up, weekly reporting, retrospectives, onboarding, training, and checking prior decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can aggregate sensitive meeting history into a persistent searchable knowledge-base file.

Mitigation: Use it only on explicitly selected meetings or directories, store generated files in access-controlled locations, and delete or redact outputs that should not remain searchable.

Risk: Search results may surface conflicting decisions from multiple meetings.

Mitigation: Treat cross-meeting conflict notices as review prompts and have a human confirm the current decision before acting on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golgys0621/skills/meeting-kb-skill)
- [跨会议知识库模板](references/kb_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown knowledge-base files, JSON query results, and concise text responses with source meeting references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI supports keyword OR/AND search, category filters, statistics, diagnostics, and structured action-item owner/deadline fields.]

## Skill Version(s):

3.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
