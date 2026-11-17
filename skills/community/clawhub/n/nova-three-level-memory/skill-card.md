## Description:

NOVA Memory helps agents design and operate a three-layer long-term memory system with episodic records, semantic knowledge, persistent rules, identity files, and maintenance routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaunleecn](https://clawhub.ai/user/shaunleecn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add durable memory practices to AI assistants, including session recall, identity context, rule storage, memory consolidation, and periodic maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist and reload memory about users, identity, conversations, and operating context.

Mitigation: Make memory writes opt-in, review memory changes before saving them, and avoid committing private memory files.

Risk: The skill includes automatic maintenance, AGENTS.md integration, and Git commit behavior that can change agent behavior over time.

Mitigation: Require explicit approval before adding scheduled maintenance, changing AGENTS.md, or committing generated memory updates.

## Reference(s):

- [ClawHub skill page: NOVA Memory](https://clawhub.ai/shaunleecn/skills/nova-three-level-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file-tree examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose durable memory files, AGENTS.md changes, cron scheduling, and Git commits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
