## Description:

Provides OpenClaw agents with local, scene-aware, persistent structured memory for task deduplication and long-term workflow recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openmemoai](https://clawhub.ai/user/openmemoai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local persistent memory to OpenClaw agents so repeated coding, research, DevOps, and other multi-step workflows can recall past work and avoid duplicate execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive operational history in local memory.

Mitigation: Do not store credentials, regulated data, customer data, or other secrets in memory; keep memory inspection and deletion available to users.

Risk: The intended localhost-only boundary can be weakened by remote endpoint configuration.

Mitigation: Use only a trusted local OpenMemo adapter and avoid remote endpoints unless they have been explicitly reviewed and approved.

Risk: Task deduplication can encourage an agent to reuse stale or incorrect prior work.

Mitigation: Review recalled memories and task-match recommendations before skipping work or reusing a previous workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openmemoai/skills/openmemo-clawhub-skill)
- [OpenMemo Project](https://github.com/openmemoai/openmemo)
- [OpenMemo OpenClaw Adapter](https://github.com/openmemoai/openmemo-openclaw-adapter)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance with shell commands and structured JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory tool responses depend on a reachable local OpenMemo adapter and the contents of the local memory store.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
