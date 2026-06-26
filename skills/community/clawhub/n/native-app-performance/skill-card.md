## Description: <br>
Native macOS/iOS app performance profiling via xctrace/Time Profiler and CLI-only analysis of Instruments traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to record Time Profiler sessions, export and symbolicate samples, and rank native macOS/iOS app hotspots without opening Instruments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profiling the wrong PID, binary, duration, or trace path can collect irrelevant or sensitive local performance data. <br>
Mitigation: Confirm the target PID or binary path, capture duration, and output trace path before running profiling commands. <br>
Risk: Generated trace, XML, and symbol output can reveal internal function names and app behavior. <br>
Mitigation: Treat generated profiling artifacts as sensitive local files and review them before sharing or publishing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and script-oriented analysis output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can produce time-sample XML exports and CSV-like hotspot tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
