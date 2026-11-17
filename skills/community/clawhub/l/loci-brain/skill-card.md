## Description:

Memory Palace for AI — persistent structured memory, identity, and task management across every conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codesstar](https://clawhub.ai/user/codesstar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an AI assistant a persistent local memory structure for identity, goals, tasks, decisions, and daily planning across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent local memory profile containing personal facts, tasks, goals, and decisions across conversations.

Mitigation: Use it only when persistent memory is intended; confirm the storage location and establish how to inspect, edit, and delete saved memory files.

Risk: The bootstrap flow auto-downloads mutable external instructions before initializing the local memory system.

Mitigation: Review the downloaded repository contents before relying on the memory system or allowing it to make ongoing updates.

Risk: The skill is designed to save some factual information silently in the background.

Mitigation: Define what may be saved before use and ask for confirmation before saving subjective values, strategy, or sensitive personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codesstar/skills/loci-brain)
- [Project homepage](https://github.com/codesstar/loci)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured file-update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, read, and update local memory files when the user intentionally enables the memory system.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
