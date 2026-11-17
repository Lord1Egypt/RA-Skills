## Description:

Obsidian Brain helps an agent maintain cross-session memory by searching layered Obsidian agent-memory fragments before work and writing deduplicated markdown fragments after useful decisions, findings, or lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpda](https://clawhub.ai/user/realpda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they want an agent to retrieve prior Obsidian-based memory fragments at the start of a task and save durable task outcomes back as structured markdown notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent cross-session memory reads and writes, which can store sensitive or incorrect task context.

Mitigation: Limit activation to explicit memory-related requests, review fragments before saving, and avoid storing secrets or confidential content.

Risk: Automatic retrieval of prior memory can over-influence later tasks with stale or unverified context.

Mitigation: Treat retrieved memory as advisory context and confirm important facts against current task evidence before acting.

Risk: The artifact workflow includes publishing when the skill is edited.

Mitigation: Require explicit approval and review before any publish action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realpda/skills/obsidian-brain)
- [Publisher Profile](https://clawhub.ai/user/realpda)
- [System Memory vs Agent Memory Fragments](references/storage-distinction.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file naming, frontmatter, search, and write conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory memory retrieval and persistence instructions for agent workflows; stored fragments should be reviewed before relying on or publishing them.]

## Skill Version(s):

1.7.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
