## Description:

Process unstructured external input (meeting transcripts, conversation logs, pasted documents) into structured Basic Memory entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phernandez](https://clawhub.ai/user/phernandez)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn pasted transcripts, conversation logs, documents, articles, and email threads into structured Basic Memory notes, entities, observations, relations, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain pasted transcripts, emails, and documents verbatim in Basic Memory.

Mitigation: Use it only for material intended to be saved, and redact secrets, regulated data, confidential email, or sensitive transcripts before ingestion.

Risk: Optional web research on extracted entities can send entity details outside the local memory workflow.

Mitigation: Require explicit user opt-in before web research and skip research when the source material already provides sufficient context.

Risk: Extracted entities and observations may introduce incorrect structured knowledge if created without review.

Mitigation: Review proposed entities and approve, skip, or edit them before any new Basic Memory notes are created.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with Basic Memory note templates and Python-style tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve source material verbatim and may propose entity creation before writing memory notes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
