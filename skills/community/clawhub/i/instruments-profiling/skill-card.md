## Description: <br>
Use when profiling native macOS or iOS apps with Instruments/xctrace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to profile native macOS and iOS applications with Instruments/xctrace, choose the correct app binary or process, record Time Profiler traces, export stack data, and avoid common profiling mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profiling the wrong application or process can produce misleading traces or capture unrelated activity. <br>
Mitigation: Confirm the app binary path or PID before recording and verify that the trace process path matches the intended target. <br>
Risk: Generated trace and XML export files can contain sensitive performance data. <br>
Mitigation: Treat trace outputs as sensitive local artifacts and avoid profiling unrelated or sensitive processes. <br>
Risk: Developer Tools permission grants xctrace additional local profiling access. <br>
Mitigation: Grant Developer Tools permission only when needed for the profiling task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/steipete/instruments-profiling) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for local Apple Instruments/xctrace profiling workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
