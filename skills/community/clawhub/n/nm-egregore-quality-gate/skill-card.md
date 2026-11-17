## Description:

Orchestrates the QUALITY pipeline stage for egregore work items, running code review, unbloat, and test updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using the egregore workflow use this skill to run convention checks, code review, refinement, test updates, and documentation updates for work items or pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can commit fixes or submit a GitHub review, and the security guidance notes a possible command-name conflict.

Mitigation: Review the commands, changes, review target, and publication effects before allowing the workflow to proceed.

Risk: Security analysis was partial because two local references could not be resolved.

Mitigation: Resolve and review the referenced material before relying on the analysis.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/egregore)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-egregore-quality-gate)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Review findings and a pipeline verdict, with shell commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed fixes and a recorded review verdict.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
