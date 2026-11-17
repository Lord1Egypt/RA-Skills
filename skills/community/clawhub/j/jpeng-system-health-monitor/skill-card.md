## Description:

Monitor system health including disk space, memory usage, process status, and evolution metrics to detect potential issues early.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local health checks for disk space, memory usage, process status, evolution-cycle freshness, and installed skill counts during diagnostics, heartbeat checks, and alerting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local system metrics and local workspace logs or skills directories for health reporting.

Mitigation: Install and run it only in environments where local health-reporting access to those paths is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JavaScript API results and human-readable formatted health reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status levels include healthy, warning, and critical; checks may include local disk, memory, process, logs, and skills directory information.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
