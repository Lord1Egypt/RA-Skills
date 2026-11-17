## Description:

Native macOS/iOS app performance profiling via xctrace Time Profiler and CLI-only analysis of Instruments traces for recording, extracting samples, symbolication, hotspot finding, and performance optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to profile native macOS and iOS apps with xctrace Time Profiler, extract sample data, symbolicate stacks, and identify performance hotspots from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profiling traces and symbolication output may expose app internals, file paths, and performance details.

Mitigation: Use the skill only on apps, binaries, and processes the operator is authorized to inspect, and avoid sharing trace or symbolication output outside approved contexts.

Risk: Using the wrong binary, symbols, process, or runtime load address can produce misleading hotspot analysis.

Mitigation: Confirm the profiled process and binary path, collect the runtime __TEXT load address with vmmap, and ensure symbols match the traced build before relying on hotspot rankings.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands, script references, and performance hotspot analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local profiling commands and hotspot rankings from Instruments Time Profiler traces.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
