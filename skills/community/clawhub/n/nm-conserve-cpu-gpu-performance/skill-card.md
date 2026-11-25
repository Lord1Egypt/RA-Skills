## Description:

Establishes CPU/GPU baselines before resource-intensive operations. Use before builds, training runs, or any task that pins cores or GPUs for over a minute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before builds, training runs, tests, or retries that may consume substantial CPU or GPU resources. It guides them to capture a baseline, narrow the work, monitor resource use, throttle heavy tasks, and summarize costs and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because one local path-like reference could not be resolved to a bundled artifact.

Mitigation: Review the unresolved reference against the original source before relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conserve-cpu-gpu-performance)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A concise resource-use summary based on the commands and metrics available in the user's environment.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
