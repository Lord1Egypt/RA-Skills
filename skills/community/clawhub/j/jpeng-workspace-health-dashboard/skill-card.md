## Description:

Unified health monitoring dashboard that consolidates skill quality, dependency security, cleanup needs, and protected skills status into a single health check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to generate a consolidated workspace health report covering skill completeness, dependency inventory, cleanup needs, and protected skill status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can overstate dependency security because the dependency check is lightweight and does not perform a full vulnerability audit.

Mitigation: Run a real dependency vulnerability audit before relying on the dashboard for approval or deployment decisions.

Risk: The dashboard can report the workspace as healthy even when important warnings exist.

Mitigation: Review individual check results, especially protected skills and warning states, before treating the workspace as ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-workspace-health-dashboard)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [JavaScript object and plain-text dashboard report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a health score, overall status, check summaries, cleanup recommendations, and warnings.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
