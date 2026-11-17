## Description:

分布式AI节点系统，实现跨局域网节点的任务分发、并行处理和结果聚合

This skill is ready for commercial/non-commercial use.

## Publisher:

[fqch1981](https://clawhub.ai/user/fqch1981)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate OpenClaw nodes on a trusted LAN for distributed question answering, parallel analysis, result aggregation, and shared task memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can share prompts and results with unauthenticated LAN peers, creating privacy and answer-integrity risk.

Mitigation: Install only on a trusted, controlled LAN; avoid sending secrets, credentials, private business data, or regulated personal data through the skill.

Risk: Peer answers and exported task memory may include untrusted or sensitive full prompts and results.

Mitigation: Authenticate and allowlist peers where possible, review peer answers before relying on them, and inspect memory exports before sharing or storing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fqch1981/skills/neuron)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and text responses with Python API examples, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May export or import task memory as JSON when those utility methods are invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
