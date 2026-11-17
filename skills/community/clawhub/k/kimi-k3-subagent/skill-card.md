## Description:

Provides a Python subagent orchestration framework with two-stage batch scheduling, lifecycle management, event tracking, and rate-limit handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to understand or adapt a Python implementation of subagent spawning, resume and retry flows, batch execution, lifecycle events, and rate-limit-aware scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad child-agent tool access can weaken expected tool boundaries if deployed without explicit permission controls.

Mitigation: Review and patch tool-permission enforcement before runtime use, especially for profiles with write, edit, bash, web_search, or web_fetch access.

Risk: Batch execution may run indefinitely or exceed intended resource limits if concurrency, retry, and timeout controls are not bounded.

Mitigation: Enforce bounded concurrency, per-task timeouts, retry caps, and sandboxed execution before installing or using the code.

Risk: Resume and retry behavior may lose child-agent state if state preservation is not implemented in the host environment.

Mitigation: Verify child-agent state persistence across resume and retry paths before relying on the lifecycle workflow.

## Reference(s):

- [Kimi K3 Subagent Architecture Notes](artifact/references/kimi-k3-subagent-architecture.md)
- [ClawHub Skill Page](https://clawhub.ai/chen6896qqwee/skills/kimi-k3-subagent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include subagent profile, lifecycle, batching, timeout, and rate-limit configuration guidance.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
