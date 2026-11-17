## Description:

Manages context overflow by handing off to a fresh subagent at 80% usage

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when a long-running task approaches context limits to checkpoint progress and hand continuation to a fresh agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff guidance can carry forward settings that suppress permission checks and confirmations.

Mitigation: Review inherited execution settings and require normal permission and confirmation checks before a continuation agent acts.

Risk: Security analysis is incomplete because some local references could not be resolved.

Mitigation: Resolve and review the referenced modules, then rerun a complete security scan before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conserve-clear-context)
- [Plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown session-state checkpoint and continuation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May hand off task continuation to a fresh agent.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
