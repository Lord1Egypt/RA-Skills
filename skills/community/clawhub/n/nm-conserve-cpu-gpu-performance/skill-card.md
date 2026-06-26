## Description: <br>
Establishes CPU/GPU baselines before resource-intensive operations, including builds, training runs, and tasks that pin cores or GPUs for more than a minute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before builds, tests, training runs, or other resource-intensive work to capture CPU/GPU baselines, choose a narrower execution scope, instrument performance, throttle work, and record follow-up decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local utilization checks can expose sensitive command lines, project names, or workload details in captured output. <br>
Mitigation: Review and redact baseline or process output before sharing it outside the local work context. <br>
Risk: Resource-intensive commands can consume shared CPU or GPU capacity and disrupt other work on the same host. <br>
Mitigation: Set per-task budgets, prefer selective tests or smoke inputs first, and use throttling or scheduler quotas when available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-cpu-gpu-performance) <br>
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes baseline metrics, selected scope, instrumentation captured, throttling tactics, and follow-up items.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
