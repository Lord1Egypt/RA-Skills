## Description:

Analyzes code change impact with risk scoring and affected-node mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill before merging to see which code areas a change may affect, identify uncovered functions, and prioritize review actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial, and its guidance recommends checking whether the plugin-directory search fits the intended environment.

Mitigation: Review that search against the local environment and consider the supplied security guidance before deployment.

Risk: Impact results may be incomplete when the required code graph is unavailable or stale.

Mitigation: Confirm the gauntlet graph is available and current; use the documented manual analysis fallback when it is unavailable.

## Reference(s):

- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-pensive-blast-radius)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Risk-ranked Markdown results table with affected nodes, file locations, citation anchors, and review suggestions; findings can also be written as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include untested functions and an overall risk level.]

## Skill Version(s):

1.10.4 (source: server-resolved release; artifact frontmatter states 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
