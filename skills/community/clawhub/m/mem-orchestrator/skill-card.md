## Description:

Memory Orchestrator helps agents implement a layered, white-box memory system for classifying user input, capturing durable preferences and decisions, recalling relevant topic and object summaries, and reflecting on stored memory over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jl1914](https://clawhub.ai/user/jl1914)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local, inspectable memory workflows to OpenClaw-style conversations. It supports gated memory capture, summary-first recall, durable topic and object records, and periodic reflection without loading all history on every turn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad conversation text into local memory files.

Mitigation: Use a clearly scoped memory directory, avoid capturing sensitive data, and require operator review for memory-worthy events before durable storage.

Risk: CLI path traversal bugs can write YAML files outside the intended memory folders.

Mitigation: Validate and normalize slugs and object types before writing files, and reject paths that resolve outside the configured memory root.

Risk: Memory records may accumulate stale, duplicate, or incorrect preferences and decisions.

Mitigation: Add review, correction, deletion, and reflection workflows so stored memory can be inspected and maintained over time.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jl1914/skills/mem-orchestrator)
- [File Layout](references/file-layout.md)
- [Retrieval Strategy](references/retrieval-strategy.md)
- [Reflection](references/reflection.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Object Models](references/object-models.md)
- [Architecture](ARCHITECTURE.md)
- [Examples](EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files and compact JSON recall payloads when its helper scripts are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
