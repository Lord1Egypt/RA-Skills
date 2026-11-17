## Description:

Monitors hosts, phones, and daemon processes with ICMP health checks and returns structured health status results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to check network reachability and basic health for hosts, phones, or daemon processes during monitoring and operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shell execution guidance could enable unsafe or unintended commands beyond ICMP checks.

Mitigation: Limit use to explicit reachability commands, validate targets before execution, and review proposed commands before running them.

Risk: Overbroad activation guidance may lead agents to use the skill for monitoring tasks outside its stated scope.

Mitigation: Use it only for ICMP reachability and basic health-check workflows; choose a more specialized operations skill for logs, deployment, or remediation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ping-monitor-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON-style status summaries and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitoring targets, configuration notes, success or error status, and recommended follow-up checks.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
