## Description:

Task orchestration framework for Tencent Coding Plan that routes decomposed work to provider models and can spawn cloud sub-agents with selected workspace context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drifting-snow](https://clawhub.ai/user/drifting-snow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when to delegate parallel or decomposed tasks through Tencent Coding Plan sub-agents, route work to appropriate models, and aggregate results while managing token and file-transfer limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task prompts, user messages, and selected workspace file contents may be sent to the Tencent Coding Plan endpoint during sub-agent work.

Mitigation: Install only when that external routing is intended; confirm which files and prompts will be shared before delegating sensitive tasks.

Risk: Broad orchestration triggers can lead to cloud sub-agent execution for requests such as delegate or parallel.

Mitigation: Review the generated task plan and confirmation thresholds before spawning multiple sub-agents or transferring files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drifting-snow/skills/orchestrator-tencent-codingplan)
- [Tencent Coding Plan API endpoint](https://api.lkeap.cloud.tencent.com/coding/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task decomposition, model-routing rationale, sub-agent results, and cost or file-transfer notices.]

## Skill Version(s):

1.0.6 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
