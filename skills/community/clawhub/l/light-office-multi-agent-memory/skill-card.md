## Description:

A general multi-agent memory system for automatic capture, RRF retrieval, knowledge graph construction, contradiction detection, and token tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liucunguang](https://clawhub.ai/user/liucunguang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure and run a prototype multi-agent memory workspace that captures agent events, retrieves memory with RRF, builds a knowledge graph, tracks token use, and manages agent registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user prompts, tool summaries, errors, task results, token logs, and graph data in local workspace files.

Mitigation: Use a dedicated MEMORY_WORKSPACE, avoid capturing secrets or regulated data, and review stored files before sharing or deploying.

Risk: The setup wizard can store an API key in config.yaml.

Mitigation: Leave the API key blank in the wizard and provide credentials through environment variables or a secret manager.

Risk: Dashboard and search behavior include demo-quality or simulated operational values.

Mitigation: Treat dashboard and retrieval results as non-operational until they are replaced with measured production data and validation.

Risk: The release evidence recommends review before installing and pinning dependencies before sensitive use.

Mitigation: Review the skill before execution and pin dependency versions before use in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liucunguang/skills/light-office-multi-agent-memory)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated workspace JSON or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists memory, graph, token, configuration, and agent registry files under MEMORY_WORKSPACE.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
