## Description:

Produces a concise macOS host resource snapshot focused on CPU, memory, GPU, swap, power, fan, temperature, and host summary signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomcatzh](https://clawhub.ai/user/tomcatzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect current macOS resource usage and local-model readiness with a truthful one-shot report instead of continuous monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can report hostnames, process names, hardware identifiers, temperatures, fan speeds, and power readings.

Mitigation: Review generated host output before sharing it outside the local environment.

Risk: Swift-backed hardware helpers self-build on first use and require Apple Command Line Tools or swiftc.

Mitigation: Install only when local helper compilation is acceptable, or prebuild and review the helpers before use.

## Reference(s):

- [mac-system-stat references](references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Swift-backed helpers may compile local binaries on first use and fail explicitly when Command Line Tools or swiftc are unavailable.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
