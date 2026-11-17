## Description:

A Chinese-language agent skill for local persistent associative memory, using spreading activation over a neural graph to store, recall, and inject conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to initialize and operate a local neural-memory store for decisions, facts, preferences, todos, and errors, then recall relevant context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local persistent memory can retain and reuse prior conversation context across sessions.

Mitigation: Avoid storing secrets, personal data, customer data, or unrelated project context, and maintain a process to inspect and delete the ~/.neuralmemory database.

Risk: Setup depends on exec-backed commands and the neural-memory package.

Mitigation: Review the neural-memory package and generated commands before enabling the service endpoint.

Risk: Broad memory activation may surface stale or irrelevant context.

Mitigation: Review recalled memories before relying on them and remove or refresh outdated entries when they affect decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/neural-memory-enhanced-free)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local ~/.neuralmemory storage and may reuse cross-session conversation context.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
