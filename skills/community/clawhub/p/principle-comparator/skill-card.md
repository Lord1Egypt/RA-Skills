## Description:

Compare two sources to find shared and divergent principles — discover what survives independent observation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and knowledge workers use this skill to compare two extractions or raw text sources and identify shared principles, source-specific ideas, and divergences. It supports pattern validation while leaving correctness judgments to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compared content is processed by the configured agent model, which may be cloud-hosted.

Mitigation: Use the skill only for deliberate two-source comparison tasks and avoid submitting sensitive content unless the configured agent environment is approved for that data.

Risk: The skill compares structure and semantic alignment, not factual correctness.

Mitigation: Treat shared principles as pattern evidence and review conclusions before relying on them.

Risk: The artifact contains stray wording about requires_review.md even though security evidence says the skill does not write files.

Mitigation: Do not create review files unless the user explicitly requests a file output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/principle-comparator)
- [Publisher profile](https://clawhub.ai/user/leegitw)
- [Skill homepage](https://github.com/live-neon/skills/tree/main/pbd/principle-comparator)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown narrative with optional JSON comparison results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shared principles, source-specific principles, divergence analysis, confidence levels, N-counts, next steps, and an optional share_text when high-confidence N=2 alignment is found.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
