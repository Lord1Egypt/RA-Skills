## Description:

Standardizes release approvals with GitHub-aware checklists and deployment gates. Use before releasing to production to verify all gates pass

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to prepare production deployments by checking scope, quality signals, documentation, communications, and operational readiness, then recording approvals or waivers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A low-probability trigger conflict may cause this skill to activate alongside another skill with overlapping release-related triggers.

Mitigation: Review installed skills with overlapping release, GitHub, readiness, quality, or governance triggers and adjust activation settings if unexpected overlaps occur.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/minister)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-minister-release-health-gates)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis]

**Output Format:** [Markdown release checklists, gate snippets, QA summaries, and rollout scorecards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses project-specific release, GitHub Checks, and tracker information supplied by the user.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
