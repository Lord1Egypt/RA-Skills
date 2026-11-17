## Description:

Synthesize invariant principles from 3+ sources - find the core that survives across all expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge-management teams use this skill to synthesize three or more related sources into candidate invariant principles and Golden Master candidates for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text supplied for synthesis may be processed by the configured LLM service.

Mitigation: Use the skill only in an agent environment approved for the sensitivity of the source text.

Risk: The evidence notes a documentation inconsistency about possible review-file persistence.

Mitigation: Clarify whether drifted items are written to requires_review.md before using highly sensitive inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/principle-synthesizer)
- [Project homepage](https://github.com/live-neon/skills/tree/main/pbd/principle-synthesizer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces candidate principles, evidence summaries, synthesis metrics, next steps, and optional share text when Golden Master candidates are found.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
