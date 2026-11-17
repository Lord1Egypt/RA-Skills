## Description:

Performs workspace health checks across disk usage, file counts, skill health, large files, and empty directories, then returns actionable maintenance recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to diagnose repository or skill-folder health, identify oversized files and empty directories, and generate a Markdown maintenance report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health report may expose local file or directory names from the scanned workspace.

Mitigation: Run it only in workspaces whose path names can be shared with the intended audience, or keep generated reports private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-workspace-health-monitor)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [JavaScript object with a Markdown health report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local workspace metrics, selected relative paths, health score, status, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
