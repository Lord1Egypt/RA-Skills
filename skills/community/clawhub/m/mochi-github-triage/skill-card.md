## Description:

Triage a single repository’s exported issues or PRs for unassigned, stale and similar-title items without remote changes. Use for GitHub Issue Triage Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers can review exported issues or pull requests for unassigned work, stale items, and possible title similarities, then use the generated reports to guide triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain private issue information.

Mitigation: Use exports from repositories you authorize, keep reports private, and retain the host sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-github-triage)
- [Publisher homepage](https://mochilab.bz)
- [Input and action contract](references/input.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, HTML, CSV, Files]

**Output Format:** [JSON, HTML, and CSV triage reports saved in the active workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes triage hints and possible title-similarity candidates; similarity is not proof of duplication.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
