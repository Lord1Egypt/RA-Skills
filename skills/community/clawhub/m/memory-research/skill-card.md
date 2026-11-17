## Description:

Researches an external company, person, technology, or topic using web search and synthesizes findings into a structured Basic Memory entity proposal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phernandez](https://clawhub.ai/user/phernandez)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research organizations, people, technologies, or topics and turn cited findings into proposed Basic Memory notes. It is suited for building or updating a personal knowledge graph with user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad bare-name and URL triggers may cause unintended web research.

Mitigation: Confirm intent before researching when a prompt is ambiguous or only contains a name or URL.

Risk: Research findings can be outdated, incomplete, or uncertain before they are saved into memory.

Mitigation: Use cited sources, hedged language, research dates, and user review before creating or updating a note.

Risk: User-provided context can be captured in a Basic Memory entity.

Mitigation: Review proposed note content before approval and omit sensitive or unnecessary context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phernandez/skills/memory-research)
- [Publisher Profile](https://clawhub.ai/user/phernandez)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown research summaries with structured Basic Memory note templates and Python-style note operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before creating or updating Basic Memory notes; includes source URLs and hedged statements.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
