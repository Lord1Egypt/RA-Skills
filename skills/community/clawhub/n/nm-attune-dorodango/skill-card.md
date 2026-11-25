## Description:

Polishes working code through successive quality passes in fresh subagents. Use after tests pass when code needs multi-dimension refinement before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Dorodango after tests pass to refine working code across correctness, clarity, consistency, and polish before review or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence because two file references could not be matched to bundled content.

Mitigation: Review the unresolved references and decide whether they matter before installing; check proposed code changes and test outcomes before accepting them.

## Reference(s):

- [Pass type definitions](modules/pass-definitions.md)
- [Attune project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, JSON]

**Output Format:** [Code changes, pass summaries, and a JSON workflow state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run tests, linters, and formatters while refining the target; up to 10 passes.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
