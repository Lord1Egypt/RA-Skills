## Description:

A foundational persistent memory skill that helps an agent store, index, and retrieve local Markdown notes across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent users, and teams use this skill to give an LLM agent a local, structured memory directory for project notes, decisions, people, and knowledge that can be retrieved in later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can retain secrets, credentials, private personal data, or regulated business information on disk and expose it in future searches.

Mitigation: Avoid saving sensitive or regulated information unless persistent local storage and later retrieval are acceptable.

Risk: The skill relies on agent-executed filesystem and shell operations to create, update, and search memory files.

Mitigation: Review proposed file paths and commands before execution, and keep writes scoped to the intended ~/memory directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/persistent-memory-engine-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and retrieves persistent notes under ~/memory/ when the agent follows the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
