## Description:

Converts meeting notes, chat logs, voice transcripts, and bullet notes into structured action items with owners, deadlines, decisions, risks, and milestones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seulkilu](https://clawhub.ai/user/seulkilu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, project managers, and developers use this skill to turn unstructured meeting or chat content into a project-management style status update with clear follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes, chat logs, and transcripts can contain sensitive internal or personal information.

Mitigation: Only provide meeting or chat content that is appropriate for parsing into structured action items.

Risk: The skill may preserve English section headers for Chinese notes, which can surprise users expecting a fully localized output.

Mitigation: Review the generated action-item summary before sharing it or importing it into project-management tools.

## Reference(s):

- [Entity Recognition & Output Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text or JSON containing a meeting summary, action items, decisions, risks, and next milestones.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action items include owner, task, deadline, and priority; unresolved deadlines are marked for confirmation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
