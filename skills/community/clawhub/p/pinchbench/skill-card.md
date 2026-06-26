## Description: <br>
PinchBench runs benchmarks to evaluate OpenClaw agent performance across real-world tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olearycrew](https://clawhub.ai/user/olearycrew) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use PinchBench to run real-world OpenClaw agent benchmarks, compare model performance, save JSON results, and optionally submit benchmark results to the PinchBench leaderboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark tasks and automated checks can cause an OpenClaw agent to execute code, change local state, or interact with connected tools. <br>
Mitigation: Run PinchBench only in an isolated OpenClaw profile with disposable workspaces and test accounts. <br>
Risk: Leaderboard submission can publish detailed benchmark results. <br>
Mitigation: Use --no-upload unless publishing results is intended. <br>
Risk: Custom or modified task files may contain untrusted automated checks. <br>
Mitigation: Review task markdown and avoid custom tasks unless their checks are trusted. <br>
Risk: Running against real email, calendar, credential, or file access can expose or alter sensitive data. <br>
Mitigation: Do not run PinchBench where OpenClaw has access to real accounts, credentials, calendars, email, or sensitive files. <br>


## Reference(s): <br>
- [PinchBench homepage](https://pinchbench.com) <br>
- [PinchBench repository](https://github.com/pinchbench/skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [uv package manager](https://docs.astral.sh/uv/) <br>
- [ClawHub skill page](https://clawhub.ai/olearycrew/pinchbench) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and benchmark result JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Benchmark runs can save local JSON results and optionally upload detailed results to a public leaderboard.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
