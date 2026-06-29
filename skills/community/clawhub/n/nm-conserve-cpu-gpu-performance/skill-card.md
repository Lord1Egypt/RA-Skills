## Description: <br>
Establishes CPU/GPU baselines before resource-intensive operations, especially builds, training runs, or work that can pin cores or GPUs for over a minute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to measure current CPU/GPU load, narrow validation scope, instrument expensive work, throttle heavy jobs, and record resource-cost decisions before running long builds, tests, or training. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process listings and profiler outputs can expose command-line details in shared or sensitive systems. <br>
Mitigation: Run monitoring commands only in environments where that visibility is acceptable, keep collection scoped to the task, and avoid sharing captured command details unnecessarily. <br>
Risk: Resource-heavy builds, tests, or training runs can starve shared CPU or GPU capacity if launched without a baseline and budget. <br>
Mitigation: Capture current utilization first, set per-task CPU/GPU budgets, prefer targeted or smoke-scale runs, and use throttling or scheduler quotas when appropriate. <br>


## Reference(s): <br>
- [clawhub.ai skill page](https://clawhub.ai/athola/skills/nm-conserve-cpu-gpu-performance) <br>
- [claude-night-market conserve plugin](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and brief run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should cover baseline metrics, chosen scope, instrumentation, throttling tactics, and follow-up items.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
