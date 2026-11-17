## Description:

Nova Memory provides local workspace memory storage, semantic retrieval, entity management, tag search, graph summaries, automatic reflection, and local analysis without external API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catplus-eric](https://clawhub.ai/user/catplus-eric)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Nova Memory to add persistent local workspace memory, search saved facts by semantic query or tag, manage entities, and produce reflection or statistics summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores arbitrary user, entity, and workspace data with weak scoping and privacy controls.

Mitigation: Use a confined storage path, avoid storing credentials or sensitive facts, apply owner-only file permissions, and define retention and deletion controls before relying on it.

Risk: Memory recall, graph, reflection, and statistics outputs may reveal sensitive stored facts in terminal or markdown output.

Mitigation: Review outputs before sharing them, sanitize terminal logs and exports, and avoid using shared storage for personal, customer, or secret data.

## Reference(s):

- [Nova Memory on ClawHub](https://clawhub.ai/catplus-eric/skills/nova-memory)
- [CatPluZ Publisher Profile](https://clawhub.ai/user/catplus-eric)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime operations return text, JSON-compatible records, graph structures, and local analysis summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memory records, entity data, tags, and local analysis state under the configured storage path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
