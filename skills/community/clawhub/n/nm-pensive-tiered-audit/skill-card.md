## Description:

Runs a three-tier codebase audit (git history, targeted scans, full review) with gating

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to assess codebase quality, review branch changes before merging, and investigate unstable areas before a release or after an incident.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's “review” trigger may conflict with an existing command or skill, and some references were not resolved.

Mitigation: Check for naming conflicts before enabling the skill, and verify its referenced dependencies and guidance in the intended environment.

## Reference(s):

- [Pensive plugin project](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-pensive-tiered-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Evidence-backed audit findings in Markdown, with optional JSON output for Tier 1]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings use evidence tags and recommendations; deeper audits require explicit escalation criteria, and a full codebase audit requires user approval.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
