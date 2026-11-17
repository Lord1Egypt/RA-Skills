## Description:

Maintain persistent cross-session agent memory in the Mneme plain-text format (.mneme files) for decisions, facts, preferences, gotchas, and goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an agent durable, project-local memory across sessions. It guides the agent to read a Mneme spine, recall relevant cells by cue, write or supersede memory cells, and lint local memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to store durable plaintext memory in local .mneme files, which may retain sensitive or unnecessary personal information.

Mitigation: Use it only for intended project memory, do not store secrets, tokens, passwords, regulated data, or unnecessary personal information, and periodically review, delete, or supersede retained entries.

Risk: Long-lived memories can become stale and later mislead the agent.

Mitigation: Use the Mneme state, confidence, and seen fields, and run the bundled lint tool to identify live cells that need verification or state updates.

## Reference(s):

- [Mneme specification](https://github.com/casperkwok/mneme)
- [ClawHub skill page](https://clawhub.ai/casperkwok/skills/mneme)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and plain-text Mneme cells]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local .mneme memory files and suggest linting with the bundled zero-dependency Python tool.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
