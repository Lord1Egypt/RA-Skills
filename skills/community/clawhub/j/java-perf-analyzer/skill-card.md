## Description:

Java Performance Analyzer helps agents diagnose Java application performance issues by using Arthas and MCP to inspect remote JVMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyl340321](https://clawhub.ai/user/lyl340321)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operations engineers use this skill to investigate Java CPU spikes, memory pressure, slow requests, blocked threads, class loading issues, heap dumps, and flame graphs on remote JVMs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH passwords and host credentials can be exposed or retained during setup.

Mitigation: Use SSH keys or a secret manager, avoid storing SSH passwords in agent memory, and limit access to trusted target environments.

Risk: Remote installation and live JVM control can affect production availability or integrity.

Mitigation: Run the skill only in approved environments, review commands before execution, verify downloaded Arthas binaries, and stop or clean up Arthas after each session.

Risk: An exposed Arthas management API or unrestricted command execution can permit high-impact JVM operations.

Mitigation: Bind Arthas to localhost behind an SSH tunnel and remove or restrict arbitrary Arthas commands where possible.

## Reference(s):

- [Arthas Commands Reference](references/arthas-commands.md)
- [ClawHub Skill Page](https://clawhub.ai/lyl340321/skills/java-perf-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JVM diagnostic summaries, optimization guidance, Arthas command plans, and MCP configuration snippets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
