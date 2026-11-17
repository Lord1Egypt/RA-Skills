## Description:

Plans local knowledge-base directories, sharding granularity, naming, update cadence, and access boundaries for reviewable RAG and knowledge workflow design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge managers, and agent users use this skill to turn local knowledge-base requirements into structured Markdown plans covering scope, source tiers, chunking, metadata, updates, and access boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may include private or sensitive local knowledge-base content.

Mitigation: Limit inputs to approved material and redact sensitive data before generating plans or reports.

Risk: A generated indexing plan could blur access boundaries if requirements are incomplete.

Mitigation: Review the Markdown brief for permissions, ownership, update cadence, and rollback assumptions before implementing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/local-rag-index-planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown structured brief, or JSON containing the generated report when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write to an output file when run with the local Python helper; otherwise produces reviewable guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
