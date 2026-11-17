## Description:

Coordinates foreground responses with background sub-agents for longer tasks, including task routing, interruption handling, status markers, optional two-stage review, and task monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philonis](https://clawhub.ai/user/philonis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route longer or independent work to background sub-agents while keeping the main agent responsive. It provides bilingual guidance for status handling, task interruption, monitoring, and optional two-stage review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill globally or from an untrusted source can broaden supply-chain exposure.

Mitigation: Install from a trusted, versioned source and prefer project-local installation unless global behavior is required.

Risk: Adding the documented AGENTS.md rules persistently changes how the agent dispatches longer tasks.

Mitigation: Review the AGENTS.md changes before deployment and keep the dispatch rules scoped to the intended workspace.

Risk: The documented memory/multi-thread-tasks.json file stores task metadata and may be cleared after the timeout window.

Mitigation: Avoid storing sensitive task details in task metadata and do not rely on the local task-state file as durable storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philonis/skills/multi-thread-dialogue)
- [ClawHub publisher profile](https://clawhub.ai/user/philonis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill primarily guides AGENTS.md behavior and local task-state setup; it does not include executable hooks.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
