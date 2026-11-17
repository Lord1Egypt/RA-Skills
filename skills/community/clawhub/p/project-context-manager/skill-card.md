## Description:

Project-based agent context management system for maintaining long-term memory and project state across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changer-changer](https://clawhub.ai/user/changer-changer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to maintain project context, session traces, and structured documentation across software development sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-memory notes can retain secrets, credentials, private customer data, or sensitive code excerpts if the agent records them.

Mitigation: Install only in projects where durable AI_DOC notes are wanted, avoid logging sensitive material, and periodically review or delete retained notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/changer-changer/skills/project-context-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local AI_DOC project notes and AI_memory session trace files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
