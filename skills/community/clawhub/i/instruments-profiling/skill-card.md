## Description:

Use when profiling native macOS or iOS apps with Instruments/xctrace. Covers correct binary selection, CLI arguments, exports, and common gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to profile native macOS and iOS apps with Instruments and xctrace, select the intended binary or process, record traces, export stack data, and avoid common profiling mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profiling may target the wrong installed app if LaunchServices resolves a different bundle than intended.

Mitigation: Review the target app path before profiling, prefer a direct binary path or attach to a verified PID, and confirm the process path before trusting the trace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/instruments-profiling)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include xctrace command examples, binary-selection checks, trace export steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
