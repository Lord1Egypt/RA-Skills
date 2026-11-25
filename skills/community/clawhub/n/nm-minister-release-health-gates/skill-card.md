## Description:

Standardizes release approvals with GitHub-aware checklists and deployment gates. Use before releasing to production to verify all gates pass

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use the skill before production deployments to evaluate scope, quality, communications, and operational readiness, then document gates and approvals in a deployment PR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The “release” trigger may overlap with a built-in command in some setups.

Mitigation: Before installing, check whether the trigger overlaps with a built-in command in your setup.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-minister-release-health-gates)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/minister)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis]

**Output Format:** [Markdown release checklists, GitHub comment snippets, QA summaries, and rollout scorecards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepared for deployment PRs or issues and post-release retrospectives.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
