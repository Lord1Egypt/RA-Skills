## Description: <br>
Java Performance Analyzer helps agents diagnose remote JVM performance issues with Arthas and MCP by collecting targeted JVM, thread, memory, method tracing, class loading, profiling, and heap dump evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyl340321](https://clawhub.ai/user/lyl340321) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate Java application issues such as high CPU, memory pressure or leaks, slow requests, blocked threads, deadlocks, and class loading problems on controlled servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent powerful remote access to live servers and JVM memory. <br>
Mitigation: Install only for trusted publishers and controlled target servers; use SSH keys or a secret manager instead of stored passwords. <br>
Risk: Heap dumps, watch or trace commands, profiling, decompilation, and arbitrary Arthas commands can expose sensitive data or disrupt production workloads. <br>
Mitigation: Require explicit approval before these actions, prefer limited result counts and short sampling windows, and avoid long-running tracing during peak traffic. <br>
Risk: An exposed Arthas HTTP endpoint can broaden access to JVM diagnostics. <br>
Mitigation: Bind Arthas to localhost behind an SSH tunnel and restrict network access with host firewall or equivalent controls. <br>
Risk: The installer downloads a remote Arthas binary before attaching to the target JVM. <br>
Mitigation: Verify downloaded binaries and use approved package or artifact sources before running the installer. <br>


## Reference(s): <br>
- [Arthas command reference](references/arthas-commands.md) <br>
- [ClawHub release page](https://clawhub.ai/lyl340321/java-perf-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool calls, configuration snippets, and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that inspect live JVM state, generate heap dumps, start profilers, or retrieve diagnostic artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
