## Description:

Agent performance scoring system for OpenClaw agents with seven evidence-based dimensions, crab-themed tiers, and trajectory tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeycacciatore3](https://clawhub.ai/user/joeycacciatore3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to have OpenClaw agents produce structured end-of-session self-evaluations, score trends, and optional peer-review comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic performance questions may trigger a ClawRank report when the user expected a brief informal assessment.

Mitigation: Use the skill when structured self-scoring is desired, and treat mid-session score checks as estimates rather than final ClawRank results.

Risk: Self-scored performance reports can be inflated or unsupported if evidence is missing.

Mitigation: Require one-line evidence for each dimension and default unsupported dimensions to 5/10 as specified by the artifact.

## Reference(s):

- [Clawrank on ClawHub](https://clawhub.ai/joeycacciatore3/skills/nate-clawrank)

## Skill Output:

**Output Type(s):** [Markdown, guidance]

**Output Format:** [Markdown score report with evidence table and optional weekly trend table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a normalized 100-point score from seven 0-10 dimensions; peer review averages self and reviewer scores when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
