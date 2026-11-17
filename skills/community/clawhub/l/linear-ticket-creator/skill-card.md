## Description:

Generate well-structured Linear tickets from bugs, features, and improvements, with optional codebase exploration to populate technical notes, acceptance criteria, and scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduvigo](https://clawhub.ai/user/luduvigo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to turn bug reports, feature requests, and improvement ideas into Linear-ready ticket drafts with acceptance criteria, technical notes, scope boundaries, and follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticket drafts may include repository file names, components, or technical assumptions when the request references code behavior.

Mitigation: Review the generated ticket before sharing or creating a Linear issue, and remove sensitive or incorrect implementation details.

Risk: Generated acceptance criteria, scope boundaries, or technical notes may be incomplete when the original request lacks detail.

Mitigation: Resolve any [CONFIRM] markers and answer follow-up questions before using the final ticket.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown ticket draft with follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include [CONFIRM] markers for assumptions and codebase-derived technical notes when relevant.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
