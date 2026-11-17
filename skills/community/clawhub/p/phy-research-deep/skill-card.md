## Description:

Deep research skill that decomposes questions into parallel sub-queries, executes searches concurrently, selectively fetches high-value sources, and synthesizes structured answers with confidence ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to conduct multi-source web research, including market research, technology comparisons, fact checking, and current-state investigations. It guides agents to decompose questions, search in parallel, fetch a small set of high-value sources, and synthesize evidence-backed findings with confidence ratings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases such as research and investigate may trigger external web research when a user intended a local-only or simple lookup task.

Mitigation: Use this skill only for multi-source research tasks and choose local search or a single lookup path when external searches are not wanted.

Risk: Research synthesis can still include incomplete, stale, or misleading source material.

Mitigation: Require source review, confidence ratings, gaps, and unknowns in the final answer before relying on the results.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-research-deep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown research report with findings, evidence, confidence assessment, gaps, and sources.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files or code are produced by the skill itself.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
