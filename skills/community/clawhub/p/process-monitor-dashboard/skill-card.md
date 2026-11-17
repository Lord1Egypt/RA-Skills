## Description:

Monitor system processes, resource usage, and performance metrics with real-time terminal dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to inspect local CPU, memory, disk, network, and process activity from a terminal, either as a live dashboard or as one-shot text or JSON snapshots for scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process names and usernames displayed in the terminal can expose sensitive local activity on shared systems.

Mitigation: Run the skill only on machines where displaying local process and user information is acceptable.

Risk: Installing dependencies from an untrusted source can introduce supply-chain risk.

Mitigation: Install psutil from a trusted package source, preferably in a virtual environment or through the operating system package manager.

Risk: Very short refresh intervals can add avoidable CPU overhead.

Mitigation: Use the documented 1-10 second refresh interval range and increase the interval when monitoring overhead matters.

## Reference(s):

- [Process Monitor Dashboard on ClawHub](https://clawhub.ai/derick001/skills/process-monitor-dashboard)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text tables and JSON objects, with shell command examples in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports live dashboard output, one-shot snapshots, top-process listings, process monitoring, system statistics, and threshold alerts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
