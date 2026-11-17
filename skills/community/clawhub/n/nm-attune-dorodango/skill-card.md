## Description:

Polishes working code through successive quality passes in fresh subagents. Use after tests pass when code needs multi-dimension refinement before release

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after implementation and tests are complete to refine working code across correctness, clarity, consistency, and polish before review or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two referenced paths were missing from the scan evidence, leaving scan coverage incomplete.

Mitigation: Review the missing paths and decide whether the coverage is sufficient before installing.

## Reference(s):

- [Attune project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown instructions, code edits, shell commands, and a JSON workflow state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks pass results and convergence in a state file; limits each run to 10 passes.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
