## Description:

Audit GitHub merge queue workflow health with failure-rate, queue-latency, and stale-success risk scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to evaluate GitHub Actions merge queue health from exported run JSON, identify high-risk workflows, and optionally fail CI when critical health thresholds are reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads local GitHub Actions run exports selected by RUN_GLOB, so an overly broad glob can scan unintended local JSON files.

Mitigation: Review RUN_GLOB before execution and point it only at the intended exported GitHub Actions run files.

Risk: The documented collection command exports repository workflow metadata to local files.

Mitigation: Store exported run JSON in an appropriate local artifact directory and handle it according to repository data policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/github-actions-merge-queue-health-audit)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash examples; executed script emits text or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports environment-variable configuration for input glob, grouping, filters, thresholds, output format, timestamp override, and critical-status fail gate.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
