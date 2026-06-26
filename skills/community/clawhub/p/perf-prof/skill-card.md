## Description: <br>
Perf Profiler guides agents through Linux system performance troubleshooting with perf-prof, including CPU, scheduling, memory, I/O, virtualization, syscall, and custom trace analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duanery](https://clawhub.ai/user/duanery) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and systems engineers use this skill to choose perf-prof analyzers, construct commands, and interpret Linux host performance issues such as high CPU, slow I/O, scheduling delay, memory growth, and VM-exit latency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide agents to run root-level Linux tracing and host-modifying setup commands. <br>
Mitigation: Use only on authorized systems, prefer a test host or maintenance window, and require explicit approval before installing dependencies, building tools, or running privileged commands. <br>
Risk: Tracing can capture sensitive stacks, paths, syscall data, and memory-derived values. <br>
Mitigation: Scope captures to specific PIDs, CPUs, devices, and short durations; handle collected traces as sensitive operational data. <br>
Risk: Expression and tracing features can include shell-command execution hooks or broad kernel/user memory inspection. <br>
Mitigation: Avoid documented system-expression execution unless the expression is fully trusted, and review memory-inspection commands before use. <br>
Risk: Network trace sharing can expose live diagnostic data. <br>
Mitigation: Do not expose trace listeners on public interfaces; bind to trusted networks and restrict access to approved operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duanery/perf-prof) <br>
- [profile analyzer reference](references/profilers/profile.md) <br>
- [task-state analyzer reference](references/profilers/task-state.md) <br>
- [multi-trace analyzer reference](references/profilers/multi-trace.md) <br>
- [syscalls analyzer reference](references/profilers/syscalls.md) <br>
- [blktrace analyzer reference](references/profilers/blktrace.md) <br>
- [kvm-exit analyzer reference](references/profilers/kvm-exit.md) <br>
- [event filtering reference](references/Event_filtering.md) <br>
- [kprobe events reference](references/kprobe_events.md) <br>
- [uprobe events reference](references/uprobe_events.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged Linux tracing commands and analyzer-specific options.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
