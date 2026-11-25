## Description:

Orchestrates multi-domain review (code, arch, tests, security) in a single pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before merging substantial changes or when a review spans several areas. It selects applicable review lenses and combines findings into prioritized recommendations and an action plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the skill suspicious because Makefile examples include package installation and file changes beyond its review purpose; scan coverage is incomplete.

Mitigation: Review the Makefile execution and package-installation examples before installing or using the skill, and treat the scan as incomplete rather than as assurance that all risks were found.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-pensive-unified-review)
- [Homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Structured Markdown review report with findings, recommendations, and an action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review scope and selected domains vary with the repository. May require the configured Night Market proof-of-work, review-core, and structured-output dependencies.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
