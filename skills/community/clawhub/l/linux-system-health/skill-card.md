## Description:

Diagnose Linux OS-level issues including slow servers, OOM kills, disk pressure, high CPU or load, DNS failures, connection timeouts, file descriptor exhaustion, zombie processes, browser automation failures, locale problems, and kernel misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjxylc](https://clawhub.ai/user/zjxylc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to diagnose Linux server health issues and produce severity-sorted findings with observed values and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security assessment says the root-run diagnostics script has unsafe privileged execution paths.

Mitigation: Review before installing, avoid running the full script as root on multi-user or sensitive hosts until the Chromium discovery/launch logic and DNS bash-c construction are fixed, and prefer least-privilege execution of only the relevant read-only sections.

Risk: The skill collects OS-level diagnostic data such as process and socket tables, kernel messages, selected system configuration, and Chromium cache locations in user home directories.

Mitigation: Review the disclosed data access scope before use in sensitive environments and run only the diagnostic sections needed for the reported issue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjxylc/skills/linux-system-health)
- [Project homepage](https://github.com/ecsgo-helper/openclaw-system-health)
- [Linux System Health Reference](reference.md)
- [Diagnostic script](scripts/diagnostics.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with severity-sorted diagnostic findings, observed values, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are organized by severity from FATAL through INFO.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter and changelog mention 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
