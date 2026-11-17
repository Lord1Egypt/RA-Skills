## Description:

ProcessGuard monitors critical local processes, restarts them on failure, tracks CPU and memory usage, sends alerts, writes a heartbeat file, and exposes an optional status dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use ProcessGuard to supervise local services, run health checks, restart failed processes, and route alerts for manual intervention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured restart and command health checks can execute local commands.

Mitigation: Use commandAllowlist, keep configuration files trusted and static, run ProcessGuard under a low-privilege service account, and avoid allowAnyCommand in production.

Risk: The optional HTTP dashboard can expose operational status if reachable outside the intended host.

Mitigation: Bind or expose the dashboard only on loopback, or place it behind authentication and firewall controls.

Risk: Optional CPU and memory monitoring depends on pidusage.

Mitigation: Pin and review pidusage before installing it in environments that enable resource monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/process-guard)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with JavaScript and shell code blocks, plus a JavaScript module artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local process status, JSON dashboard responses, log files, alert JSON lines, and heartbeat files when used in an agent environment.]

## Skill Version(s):

2.1.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
