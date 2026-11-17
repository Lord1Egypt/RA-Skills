## Description:

Runs a three-tier codebase audit (git history, targeted scans, full review) with gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review codebase quality, changes, or instability before release or after incidents. It starts with Git history and escalates to targeted review or a full audit when documented criteria warrant it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a medium-severity conflict involving the “review” trigger; confidence is medium and some reference checks were incomplete.

Mitigation: Check that the trigger matches the intended invocation, and verify referenced local paths before use.

Risk: A full codebase audit can consume substantial time and compute.

Mitigation: Keep Tier 3 gated on documented justification and explicit user approval, as described in the skill.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-pensive-tiered-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Markdown audit findings with evidence and escalation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tiered findings; a full codebase audit requires explicit approval.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
