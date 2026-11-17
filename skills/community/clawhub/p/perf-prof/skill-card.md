## Description:

Perf Profiler helps agents guide Linux performance troubleshooting with perf-prof workflows for CPU, scheduling, memory, I/O, virtualization, event aggregation, tracing, and custom script analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanery](https://clawhub.ai/user/duanery)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to choose perf-prof profilers, construct safe command lines, and interpret Linux system performance signals during troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-privilege tracing can expose sensitive system state or affect production hosts.

Mitigation: Require explicit user approval for root or CAP_* tracing and constrain scope, duration, output storage, and cleanup before running commands.

Risk: Mutable source installation paths can make builds hard to verify.

Mitigation: Use a pinned, verified perf-prof commit or release and build it in an unprivileged isolated environment.

Risk: Dynamic probes, /proc/kcore access, and expression-driven command behavior can create elevated operational risk.

Mitigation: Require exact approval for dynamic probes, /proc/kcore use, network push or pull actions, and expression command execution.

Risk: Running tracing workflows on production or multi-user systems without controls can disrupt workloads or collect unintended data.

Mitigation: Avoid production or multi-user execution unless scope, duration, storage, and cleanup are explicitly controlled.

## Reference(s):

- [Perf Profiler Skill](SKILL.md)
- [Event Filtering Reference](references/Event_filtering.md)
- [perf-prof Expression Reference](references/expr.md)
- [Kprobe Dynamic Probe Reference](references/kprobe_events.md)
- [Uprobe Dynamic Probe Reference](references/uprobe_events.md)
- [blktrace Profiler Reference](references/profilers/blktrace.md)
- [breakpoint Profiler Reference](references/profilers/breakpoint.md)
- [hrcount/stat Profiler Reference](references/profilers/hrcount.md)
- [kmemleak Profiler Reference](references/profilers/kmemleak.md)
- [kmemprof Profiler Reference](references/profilers/kmemprof.md)
- [kvm-exit Profiler Reference](references/profilers/kvm-exit.md)
- [multi-trace Profiler Reference](references/profilers/multi-trace.md)
- [oncpu Profiler Reference](references/profilers/oncpu.md)
- [profile Profiler Reference](references/profilers/profile.md)
- [python Profiler Reference](references/profilers/python.md)
- [rundelay Profiler Reference](references/profilers/rundelay.md)
- [sql Profiler Reference](references/profilers/sql.md)
- [syscalls Profiler Reference](references/profilers/syscalls.md)
- [task-state Profiler Reference](references/profilers/task-state.md)
- [top Profiler Reference](references/profilers/top.md)
- [trace Profiler Reference](references/profilers/trace.md)
- [Linux Kernel Kprobe Tracing Documentation](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/trace/kprobetrace.rst)
- [Linux Kernel Uprobe Tracing Documentation](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/trace/uprobetracer.rst)
- [FlameGraph](https://github.com/brendangregg/FlameGraph)
- [KVM Documentation](https://www.linux-kvm.org/page/Documents)
- [Intel Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and perf-prof command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require root or CAP_PERFMON approval.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter metadata.version is 0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
