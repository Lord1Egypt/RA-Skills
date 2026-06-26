## Description: <br>
Produces concise one-shot macOS host resource snapshots covering CPU, memory, GPU, power, fan, temperature, and aggregate host status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomcatzh](https://clawhub.ai/user/tomcatzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Mac users use this skill to capture a truthful one-shot system health and resource-pressure report on macOS, especially when assessing local-model readiness or current machine pressure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local telemetry reports can include hostname, top process names, and GPU or driver details. <br>
Mitigation: Install and run the skill only where sharing local Mac system telemetry is acceptable, and review outputs before forwarding them outside the local context. <br>
Risk: Swift-backed helpers compile locally on first use when Command Line Tools are available. <br>
Mitigation: Treat the release as source-only, keep transient build artifacts out of packaging, and ensure Command Line Tools or prebuilt helpers are available where needed. <br>
Risk: Some hardware counters depend on macOS, Apple Silicon, IOKit, IOReport, AppleSMC, and helper build availability. <br>
Mitigation: Use the helper scripts' structured failure output to distinguish unavailable telemetry from normal readings; CPU and memory helpers remain available without Swift. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tomcatzh/mac-system-stat) <br>
- [mac-system-stat references](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON telemetry from helper scripts, with optional plain-text aggregate summaries and concise Markdown guidance from the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; Swift-backed helpers may auto-build locally on first use and report structured failures if Command Line Tools are unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
