## Description:

Hybrid Memory provides a decision framework for using OpenClaw's built-in vector memory together with Graphiti temporal knowledge graph recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbrunner](https://clawhub.ai/user/clawdbrunner)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to decide when an agent should search markdown memory files, query Graphiti for temporal facts, or combine both sources when recalling past context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory logging may retain personal context without explicit privacy guardrails or retention controls.

Mitigation: Define clear rules for what may be logged, avoid secrets and sensitive personal data, and confirm how Graphiti data can be reviewed and deleted before use.

## Reference(s):

- [Hybrid Memory skill page](https://clawhub.ai/clawdbrunner/skills/hybrid-memory)
- [OpenClaw Graphiti memory setup guide](https://github.com/clawdbrunner/openclaw-graphiti-memory)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision framework for choosing memory_search, memory_get, and Graphiti recall or logging commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
